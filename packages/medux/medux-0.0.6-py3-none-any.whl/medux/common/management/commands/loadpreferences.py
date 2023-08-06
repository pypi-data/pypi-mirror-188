import logging
from pathlib import Path

from django.apps import apps
from django.core.management import BaseCommand

from medux.preferences.loaders import TomlPreferencesLoader

logger = logging.getLogger(__file__)


class Command(BaseCommand):
    """Loads vendor preferences.toml in each app into the database"""

    help = "DEV COMMAND: Load (VENDOR) preferences from a file into the database."

    def handle(self, *args, **options):
        for app in apps.get_app_configs():
            filename = Path(app.path, "preferences.toml")
            if filename.exists():
                from medux.preferences.definitions import Scope

                loader = TomlPreferencesLoader(filename, scope=Scope.VENDOR)
                loader.load()

                logger.info(f"Loaded preferences from {filename} into database.")
