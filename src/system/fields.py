# Subclass of Django's OneToOneField that will add an is_ property to determine if the foreign model exists without causing an error.
# Inpired by https://www.fusionbox.com/blog/detail/django-onetoonefields-are-hard-to-use-lets-make-them-better/551/

# class User(models.Model):
# 	email = models.CharField('Email')
# class UserProfile(models.Model):
# 	user = OneToOneFieldWithFlag(User, related_name='profile', flag_name='has_profile')
# 	phone = models.CharField('Phone number')
# user = user.objects.get(email='test@example.com')
# if user.has_profile:
# 	print("Yes, this user has a profile with a phone number of {}".format(user.profile.phone))

from django.db.models import OneToOneField
class OneToOneFieldWithFlag(OneToOneField):
	def __init__(self, *args, **kwargs):
		self.flag_name = kwargs.pop('flag_name')
		super(OneToOneFieldWithFlag, self).__init__(*args, **kwargs)

	def contribute_to_related_class(self, cls, related):
		super(OneToOneFieldWithFlag, self).contribute_to_related_class(cls, related)
		def flag(model_instance):
			return hasattr(model_instance, related.get_accessor_name())
		setattr(cls, self.flag_name, property(flag))

	def deconstruct(self):
		name, path, args, kwargs = super(OneToOneFieldWithFlag, self).deconstruct()
		kwargs['flag_name'] = self.flag_name
		return name, path, args, kwargs
