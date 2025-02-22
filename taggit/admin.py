from django.contrib import admin

from taggit.models import Tag, TaggedItem


def tagged_items_count(obj):
    tagged_items_count = TaggedItem.objects.filter(tag=obj).count()
    return tagged_items_count
tagged_items_count.short_description = 'Tagged Items Count'


class TaggedItemInline(admin.StackedInline):
    model = TaggedItem


class TagAdmin(admin.ModelAdmin):
    list_display = ["name", tagged_items_count, ]
    list_filter = ["namespace", ]
    inlines = [
        TaggedItemInline
    ]
    search_fields = ["name", ]
    list_per_page = 50


admin.site.register(Tag, TagAdmin)
