from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class SwitchUserBackend(ModelBackend):

	"""
	Allow a user to be authenticated if they are switching
	from a super user, or from someone to whom a super
	user switched
	"""

	def authenticate(self,original_username=None, new_username=None, superuser_session=False):
		try:
			original_user = User.objects.get(username=original_username)
			if original_user.is_superuser or superuser_session:
				return User.objects.get(username=new_username)
		except User.DoesNotExist:
			return None
