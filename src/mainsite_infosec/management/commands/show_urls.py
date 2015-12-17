from django.core.management.base import BaseCommand
from django.conf import settings
from importlib import import_module

class Command(BaseCommand):
  help = "Lists all registered URLs"

  def handle(self, *args, **options):
    urlconf = import_module(settings.ROOT_URLCONF)
    self.show_urls(urlconf.urlpatterns)

  def show_urls(self, urllist, depth=0):
    for entry in urllist:
      self.stdout.write(' '.join(("  " * depth, entry.regex.pattern,
        entry.callback and entry.callback.__module__ or '',
        entry.callback and entry.callback.func_name or ''))
      )
      if hasattr(entry, 'url_patterns'):
        self.show_urls(entry.url_patterns, depth + 1)
