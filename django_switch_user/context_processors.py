class switch_user(object):
	"""
	This is a class based context processor. This provides a
	form for super users to switch to another user.
	"""

	def __new__(cls, request,*args, **kwargs):
		obj = super(switch_user,cls).__new__(cls)
		return obj(request, *args, **kwargs)

	def __call__(self,request,*args,**kwargs):
		if self.is_allowed_to_switch(request):
			form = self.get_form()

			return {self.get_context_var_name(): form(prefix=self.get_form_prefix()) }
		return {}

	def is_allowed_to_switch(self,request):
		if request.user.is_superuser or \
			request.user.has_perm('Switch User') or \
			(request.session and request.session.has_key('superuser-switch')):
			return True
		return False

	def get_user_queryset(self):
		from django.contrib.auth.models import User
		return User.objects.filter(is_active=True).order_by('username')

	def get_form(self):
		from django import forms
		class SelectUser(forms.Form):
			user = forms.ModelChoiceField(queryset=self.get_user_queryset())
		return SelectUser

	def get_context_var_name(self):
		return "switch_user_form"

	def get_form_prefix(self):
		return "django-switch"
