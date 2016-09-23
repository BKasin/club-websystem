import os
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
	help = "Turn on or off a maintenance mode file (defaults to 'maint.html' in your STATIC_ROOT). Configure your webserver to serve this file first if it exists."

	def add_arguments(self, parser):
		parser.add_argument(
			'--on',
			action='store_true',
			dest='on',
			default=False,
			help='Turn on maintenance mode by removing the .disabled suffix of the maintenance mode file'
		)
		parser.add_argument(
			'--off',
			action='store_true',
			dest='off',
			default=False,
			help='Turn off maintenance mode by adding a .disabled suffix to the maintenance mode file'
		)

	def handle(self, *args, **options):
		# Find the maintenance mode file
		try:
			maint_mode_file = settings.MAINT_MODE_FILE
		except:
			# If not found, choose a default
			maint_mode_file = os.path.join(settings.STATIC_ROOT, 'maint.html')

		maint_mode_file_disabled = maint_mode_file + '.disabled'

		# Check current state
		maint_mode_status = os.path.isfile(maint_mode_file)

		# Set new state
		changed = False
		if options.get('on'):
			if not maint_mode_status:
				os.rename(maint_mode_file_disabled, maint_mode_file)
				maint_mode_status = True
				changed = True
		elif options.get('off'):
			if maint_mode_status:
				os.rename(maint_mode_file, maint_mode_file_disabled)
				maint_mode_status = False
				changed = True
		self.stdout.write("Maintenance mode {} {}".format(["is currently","has been changed to"][changed], ["OFF","ON"][maint_mode_status]))
