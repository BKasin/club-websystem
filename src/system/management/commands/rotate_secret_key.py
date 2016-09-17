from django.core.management.base import BaseCommand

class Command(BaseCommand):
	help = "If you store Django's SECRET_KEY in a dedicated file outside of source control, this command can easily regenerate a random 50-char key and write it to your file (defaults to 'secretkey.txt' in CONF_DIR)."

	def add_arguments(self, parser):
		parser.add_argument(
			'--force',
			action='store_true',
			dest='force',
			default=False,
			help='Replace the existing key without prompting'
		)

	def handle(self, *args, **options):
		import os
		import string
		from django.utils.six.moves import input
		from django.conf import settings

		# Find the key file
		try:
			key_file = settings.SECRET_KEY_FILE
		except:
			# If not found, choose a default
			key_file = os.path.join(settings.CONF_DIR, 'secretkey.txt')

		# If the file exists and already has contents, then only replace if --force argument was given
		existing_key = ''
		try:
			existing_key = open(key_file).read().strip()
		except:
			pass # No key file found, so we're safe to create a new one without prompting
		else:
			if existing_key:
				self.stdout.write("EXISTING SECRET KEY: {}".format(existing_key))
				if not options.get('force'):
					if input("Replace this with a new key? [Y/N] ").lower() != 'y': return

		self.stdout.write('')

		# Generate new key
		import random
		char_list = string.ascii_letters + string.digits + string.punctuation
		generated_key = ''.join([random.SystemRandom().choice(char_list) for _ in range(50)])
		self.stdout.write("NEW SECRET KEY:      {}".format(generated_key))

		# Write new key to file
		with open(key_file, 'w') as f:
			f.write(generated_key)
		self.stdout.write("Written to {}".format(key_file))
