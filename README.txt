django-taggit (+ django-taggit-autocomplete)
============================================

This is a combination of alex/django-taggit & fcurella/django-taggit-autocomplete.

Install:

> Install taggit according to its instructions.
> Add the content of the static folder to your folder specified by STATIC_URL in settings.py


All credit goes to the developers of alex/django-taggit & fcurella/django-taggit-autocomplete.

In template (jinja2):

{% block extra_head %}
	<script src="{{ STATIC_URL }}js/jquery.autoSuggest.js" type="text/javascript" ></script>
    <link rel="stylesheet" type="text/css" href="/static/css/autoSuggest.css" media="screen">
{% endblock %}
<!-- ... snip ... -->
{% for tag in myobj.tags.all() %}
    {{ tag }},
{% endfor %}
<form action="{{ "my_tag_list_url"|url(myobj.pk) }}" method="POST">
    {{ form|safe }}
    <input type="submit" />
</form>
<!-- ... snip ... -->

Basic submit form.py:

from django import forms
from taggit.forms import TagField
from taggit.widgets import TagAutocomplete
class TagForm(forms.Form):
    tags = TagField(widget=TagAutocomplete)

 
In view.py:
@login_required
def post_tags(request, obj_id):
    data = {'success': False}
    obj = getmyobj(obj_id)
    if request.POST:
        form = TagForm(request.POST)
        if form.is_valid():
            tags = form.cleaned_data['tags']
            all_tags = obj.tags.all()
            for tag in tags:
                if len(tag) > 2:
                    if not tag in all_tags:
                        obj.tags.add(tag)
            data['success'] = True
    return HttpResponse(simplejson.dumps(data))