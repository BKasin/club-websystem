from django.core.management.base import BaseCommand

class Command(BaseCommand):
	help = "Generate configuration files dynamically from templates using Django's settings as template context. Add a DYNCONF_DEF_FILE setting that points to a file containing your output_file=template_file list (defaults to 'dynamic_configs.conf' in CONF_DIR)."

	def handle(self, *args, **options):
		import os
		import pwd
		import grp
		from django.conf import settings
		from django.template import Context, Template

		# Context that all templates will receive
		uid = os.getuid()
		gid = os.getgid()
		context = Context({
			'settings': settings,
			'venv': os.environ['VIRTUAL_ENV'],
			'username': pwd.getpwuid(uid).pw_name,
			'uid': uid,
			'groupname': grp.getgrgid(gid).gr_name,
			'gid': gid,
		})

		# Find the definitions file
		try:
			definition_file = settings.DYNCONF_DEF_FILE
		except:
			# If not found, choose a default
			definition_file = os.path.join(settings.CONF_DIR, 'dynamic_configs.conf')

		# Load the definitions
		try:
			with open(definition_file, 'r') as file:
				contents = file.read()
		except Exception as e:
			self.stderr.write("Failed to load definition file: {}".format(definition_file))
			return

		# Process the definitions file with the same context we'll use later for the templates
		output = Template(contents).render(context)

		# Loop through each line
		lines = output.split("\n")
		default_dir = os.path.dirname(os.path.abspath(definition_file))
		for line in lines:
			# Skip any that aren't key=value format
			line = line.strip()
			if line.startswith('#') or len(line)==0: continue
			parts = line.split('=')
			if len(parts)!=2: continue

			# Extract the two filenames and translate them into absolute paths
			output_file = parts[0].strip()
			if not output_file.startswith('/'): output_file = os.path.join(default_dir, output_file)
			template_file = parts[1].strip()
			if not template_file.startswith('/'): template_file = os.path.join(default_dir, template_file)

			# Load the template file
			try:
				with open(template_file, 'r') as file:
					contents = file.read()
				self.stdout.write("Loaded template '{}'".format(template_file))
			except Exception as e:
				self.stderr.write("Failed to load template '{}': {}".format(template_file, repr(e)))
				continue # Go on to the next config file

			# Render the template
			try:
				output = Template(contents).render(context)
			except Exception as e:
				self.stderr.write("    Failed to render template '{}': {}".format(template_file, repr(e)))
				continue # Go on to the next config file

			# Output the rendered results
			try:
				with open(output_file, 'w') as file:
					file.write(output)
				self.stdout.write("    Rendered to '{}'".format(output_file))
			except Exception as e:
				self.stderr.write("    Failed to write new output file '{}': {}".format(output_file, repr(e)))
				continue # Go on to the next config file
