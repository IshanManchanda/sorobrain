from django.forms.widgets import ClearableFileInput
from django.utils.safestring import mark_safe

from sorobrain.utils import get_presigned_url


class PictureWidget(ClearableFileInput):
	initial_text = 'Current Avatar'

	def render(self, name, value, attrs=None, renderer=None):
		super_html = super().render(name, value, attrs, renderer)
		url = get_presigned_url(value)
		html = f"""<img class="img-thumbnail" src="{url}" style="max-width:
					70px; max-height:70px; height:auto; width: auto; "/>"""
		return mark_safe(f'{html} <br/> {super_html}')
