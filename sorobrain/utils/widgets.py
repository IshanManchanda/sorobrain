from string import Template

from django.forms.widgets import ClearableFileInput
from django.utils.safestring import mark_safe


class PictureWidget(ClearableFileInput):
	def render(self, name, value, attrs=None, renderer=None):
		super_html = super().render(name, value, attrs, renderer)
		html = Template(
				"""<img src="$link" style="max-width:70px; max-height:70px; height:auto; width: auto; "/>""")
		return mark_safe(f'{html.substitute(link=value)} <br/> {super_html}')
