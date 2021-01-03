import boto3
from botocore.client import Config
from django.core.mail import send_mail

from main.models.ledger import Ledger
from sorobrain.settings import AWS_PRIVATE_MEDIA_LOCATION


def get_presigned_url(relative_path_from_private_media_root: str) -> str:
	"""Returns a presigned url from the private media root to access
	   private media programmatically.
	"""

	s3 = boto3.client('s3', config=Config(signature_version='s3v4',
	                                      region_name='ap-south-1'))
	url = s3.generate_presigned_url(
			ClientMethod='get_object',
			Params={
				'Bucket': 'sorobrain-assets',
				'Key'   : f'{AWS_PRIVATE_MEDIA_LOCATION}/{relative_path_from_private_media_root}',
			}
	)
	return url


def send_product_bought_mail(subject: str, msg: str, msg_html: str, to: list):
	send_mail(subject,
	          msg,
	          'sorobrain.devs@gmail.com',
	          to,
	          html_message=msg_html)


def _add_ledger_record(user, credit, debit, description='') -> None:
	Ledger.objects.create(user=user, credit=credit, debit=debit, description=description)


def add_ledger_credit(user, credit, description):
	_add_ledger_record(user, credit, None, description)


def add_ledger_debit(user, debit, description):
	_add_ledger_record(user, None, debit, description)
