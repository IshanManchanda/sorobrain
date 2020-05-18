from string import Template

from django.forms.widgets import ClearableFileInput
from django.utils.safestring import mark_safe
import boto3
from botocore.client import Config

from sorobrain.settings import MEDIA_URL, AWS_PRIVATE_MEDIA_LOCATION


class PictureWidget(ClearableFileInput):
	def render(self, name, value, attrs=None, renderer=None):
		super_html = super().render(name, value, attrs, renderer)

		s3 = boto3.client('s3', config=Config(signature_version='s3v4',
		                                      region_name='ap-south-1'))
		url = s3.generate_presigned_url(
				ClientMethod='get_object',
				Params={
					'Bucket': 'sorobrain-assets',
					'Key'   : f'{AWS_PRIVATE_MEDIA_LOCATION}/{value}',
				}
		)

		html = f"""<img class="img-thumbnail" src="{url}" style="max-width:70px; max-height:70px; height:auto; width: auto; "/>"""
		return mark_safe(f'{html} <br/> {super_html}')
