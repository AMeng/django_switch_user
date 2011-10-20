from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class SwitchUserBackend(ModelBackend):

	"""
	Authenticate only if all parameters are passed in
	"""

	def authenticate(self,original_username=None, new_username=None, auth_session=False):
		try:
			original_user = User.objects.get(username=original_username)
			new_user = User.objects.get(username=new_username)

		except User.DoesNotExist:
			pass

		else:
			if auth_session:
				return new_user

		return None
