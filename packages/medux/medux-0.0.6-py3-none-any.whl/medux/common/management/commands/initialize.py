import logging

from django.core.management import BaseCommand, call_command
from gdaps.pluginmanager import PluginManager

from medux.common import tools
from medux.core.models import User

logger = logging.getLogger(__file__)


class Command(BaseCommand):
    """Loads vendor preferences.toml in each app into the database"""

    help = "DEV COMMAND: Initializes the application for the first time. Sets up admin account, etc."

    def handle(self, *args, **options):

        admin = User.objects.filter(username="admin").first()
        assert admin
        # if admin is None:
        #     msg = "Creating Admin account: user: 'admin', password: 'admin'... "
        #     admin = User.objects.create_user(username="admin", password="admin")
        #     admin.is_staff = True
        #     admin.is_superuser = True
        #     admin.save()
        #     msg += self.style.SUCCESS("OK")
        #     self.stdout.write(msg)

        # Initialize plugins...
        for app in PluginManager.plugins():
            logger.info(f"Initializing {app.label}...")
            # noinspection PyUnresolvedReferences
            if hasattr(app, "initialize") and callable(app.initialize):
                app.initialize()
            logger.info(f"Creating {app.label} groups/permissions...")
            if hasattr(app, "groups_permissions"):
                # noinspection PyUnresolvedReferences
                tools.create_groups_permissions(app.groups_permissions)
