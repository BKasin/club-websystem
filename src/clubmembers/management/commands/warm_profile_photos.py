import sys
from django.core.management.base import BaseCommand
from clubmembers.models import Member
from versatileimagefield.image_warmer import VersatileImageFieldWarmer

class Command(BaseCommand):
  help = "Creates the resized copies of member's profile photos, as described in the VERSATILEIMAGEFIELD_RENDITION_KEY_SETS['memberphoto'] setting."

  def handle(self, *args, **options):
    self.stdout.write("Creating and/or verifying profile photos...")
    num_created, failed_to_create = VersatileImageFieldWarmer(
      instance_or_queryset=Member.objects.all(),
      rendition_key_set='memberphoto',
      image_attr='photo',
      verbose=True
    ).warm()

    if len(failed_to_create):
      image_list = "\n".join("- "+str(n) for n in failed_to_create)
      self.stderr.write("\nFailed to create {} images:\n".format(len(failed_to_create)) + image_list)
      sys.exit(1)
