import datetime
import django
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.db import models, IntegrityError, transaction
from django.template.defaultfilters import slugify as default_slugify
from django.utils.translation import ugettext_lazy as _, ugettext


class TagBase(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=100)
    slug = models.SlugField(verbose_name=_('Slug'), unique=True, max_length=100)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk and not self.slug:
            self.slug = self.slugify(self.name)
            if django.VERSION >= (1, 2):
                from django.db import router
                using = kwargs.get("using") or router.db_for_write(
                    type(self), instance=self)
                # Make sure we write to the same db for all attempted writes,
                # with a multi-master setup, theoretically we could try to
                # write and rollback on different DBs
                kwargs["using"] = using
                trans_kwargs = {"using": using}
            else:
                trans_kwargs = {}
            i = 0
            while True:
                i += 1
                try:
                    sid = transaction.savepoint(**trans_kwargs)
                    res = super(TagBase, self).save(*args, **kwargs)
                    transaction.savepoint_commit(sid, **trans_kwargs)
                    return res
                except IntegrityError:
                    transaction.savepoint_rollback(sid, **trans_kwargs)
                    self.slug = self.slugify(self.name, i)
        else:
            return super(TagBase, self).save(*args, **kwargs)

    def slugify(self, tag, i=None):
        slug = default_slugify(tag)
        if i is not None:
            slug += "_%d" % i
        return slug


class Tag(TagBase):
    namespace = models.CharField(_('namespace'), max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.namespace = self.name.partition(":")[0] if self.name.partition(":")[1] == ":" else u''
        return super(Tag, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class ItemBase(models.Model):
    def __unicode__(self):
        return ugettext("%(object)s tagged with %(tag)s") % {
            "object": self.content_object,
            "tag": self.tag
        }

    class Meta:
        abstract = True

    @classmethod
    def tag_model(cls):
        return cls._meta.get_field_by_name("tag")[0].rel.to

    @classmethod
    def tag_relname(cls):
        return cls._meta.get_field_by_name('tag')[0].rel.related_name

    @classmethod
    def lookup_kwargs(cls, instance):
        return {
            'content_object': instance
        }

    @classmethod
    def bulk_lookup_kwargs(cls, instances):
        return {
            "content_object__in": instances,
        }

class VotableBase(models.Model):
    up_votes = models.PositiveIntegerField(default=0)
    down_votes = models.PositiveIntegerField(default=0)
    score = models.IntegerField(default=0)
    timestamp = models.DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        self.score = self.up_votes - self.down_votes
        self.timestamp = datetime.datetime.now()
        super(VotableBase, self).save(*args, **kwargs)

    class Meta:
        abstract = True

class TagVote(models.Model):
    tag_id = models.PositiveIntegerField()
    user = models.PositiveIntegerField()
    up = models.BooleanField(default=True)

    class Meta:
        unique_together = (("tag_id", "user"),)

class TaggedItemBase(ItemBase):
    if django.VERSION < (1, 2):
        tag = models.ForeignKey(Tag, related_name="%(class)s_items")
    else:
        tag = models.ForeignKey(Tag, related_name="%(app_label)s_%(class)s_items")

    class Meta:
        abstract = True

    @classmethod
    def tags_for(cls, model, instance=None):
        if instance is not None:
            return cls.tag_model().objects.filter(**{
                '%s__content_object' % cls.tag_relname(): instance
            })
        return cls.tag_model().objects.filter(**{
            '%s__content_object__isnull' % cls.tag_relname(): False
        }).distinct()


class GenericTaggedItemBase(ItemBase):
    object_id = models.BigIntegerField(verbose_name=_('Object id'), db_index=True)
    if django.VERSION < (1, 2):
        content_type = models.ForeignKey(
            ContentType,
            verbose_name=_('Content type'),
            related_name="%(class)s_tagged_items"
        )
    else:
        content_type = models.ForeignKey(
            ContentType,
            verbose_name=_('Content type'),
            related_name="%(app_label)s_%(class)s_tagged_items"
        )
    content_object = GenericForeignKey()

    class Meta:
        abstract = True

    @classmethod
    def lookup_kwargs(cls, instance):
        return {
            'object_id': instance.pk,
            'content_type': ContentType.objects.get_for_model(instance)
        }

    @classmethod
    def bulk_lookup_kwargs(cls, instances):
        # TODO: instances[0], can we assume there are instances.
        return {
            "object_id__in": [instance.pk for instance in instances],
            "content_type": ContentType.objects.get_for_model(instances[0]),
        }

    @classmethod
    def tags_for(cls, model, instance=None):
        ct = ContentType.objects.get_for_model(model)
        kwargs = {
            "%s__content_type" % cls.tag_relname(): ct
        }
        if instance is not None:
            kwargs["%s__object_id" % cls.tag_relname()] = instance.pk
        return cls.tag_model().objects.filter(**kwargs).distinct()


class TaggedItem(GenericTaggedItemBase, TaggedItemBase, VotableBase):
    class Meta:
        verbose_name = _("Tagged Item")
        verbose_name_plural = _("Tagged Items")
