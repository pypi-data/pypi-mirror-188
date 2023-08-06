import logging
import os
from pathlib import Path

import requests
from django.apps import apps
from django.core.management import BaseCommand

logger = logging.getLogger(__file__)


class Command(BaseCommand):
    """Download libraries and save them into the static folder.

    The `libradies` dict has the name of the library as key, and a list of
    3-tuples, each containing:
      - the local file path of the downloaded file
      - the URL to download the file
      - a mode how to write the file: "w" for text files, "wb" for binary files like icon fonts

    """

    libraries: dict[list[tuple[str, str, str]]] = {
        "htmx": [
            ("js/htmx/htmx.js", "https://unpkg.com/htmx.org@latest/dist/htmx.js", "w"),
            (
                "js/htmx/htmx.min.js",
                "https://unpkg.com/htmx.org@latest/dist/htmx.min.js",
                "w",
            ),
            (
                "js/htmx/ext/ws.js",
                "https://unpkg.com/htmx.org@latest/dist/ext/ws.js",
                "w",
            ),
            (
                "js/htmx/ext/debug.js",
                "https://unpkg.com/htmx.org@latest/dist/ext/debug.js",
                "w",
            ),
        ],
        # "bootstrap": [
        #     (
        #         "js/bootstrap.bundle.min.js",
        #         "https://unpkg.com/bootstrap@latest/dist/js/bootstrap.bundle.min.js",
        #         "w",
        #     ),
        #     (
        #         "js/bootstrap.bundle.min.js.map",
        #         "https://unpkg.com/bootstrap@latest/dist/js/bootstrap.bundle.min.js.map",
        #         "w",
        #     ),
        #     (
        #         "css/bootstrap.min.css",
        #         "https://unpkg.com/bootstrap@latest/dist/css/bootstrap.min.css",
        #         "w",
        #     ),
        #     (
        #         "css/bootstrap.min.css.map",
        #         "https://unpkg.com/bootstrap@latest/dist/css/bootstrap.min.css.map",
        #         "w",
        #     ),
        # ],
        "bootstrap-icons": [
            (
                "css/bootstrap-icons.css",
                "https://unpkg.com/bootstrap-icons@latest/font/bootstrap-icons.css",
                "w",
            ),
            (
                "css/fonts/bootstrap-icons.woff",
                "https://unpkg.com/bootstrap-icons@latest/font/fonts/bootstrap-icons.woff",
                "wb",
            ),
            (
                "css/fonts/bootstrap-icons.woff2",
                "https://unpkg.com/bootstrap-icons@latest/font/fonts/bootstrap-icons.woff2",
                "wb",
            ),
        ],
        "sortable": [
            (
                "js/Sortable.min.js",
                "https://cdn.jsdelivr.net/npm/sortablejs@latest/Sortable.min.js",
                "w",
            )
        ],
        "tabler": [
            (
                "css/tabler.css",
                "https://raw.githubusercontent.com/nerdoc/tabler/medux/dist/css/tabler.css",
                "w",
            ),
            (
                "js/tabler.js",
                "https://raw.githubusercontent.com/nerdoc/tabler/medux/dist/js/tabler.js",
                "w",
            ),
        ],
    }
    help = "DEV COMMAND: downloads needed MedUX Javascript/CSS libraries and fonts."

    def add_arguments(self, parser):
        parser.add_argument(
            "library",
            help=f"Specify the library do download. Available are: {[l for l in self.libraries]}",
        )

    def handle(self, *args, **options):
        target_path_root = (
            Path(apps.get_app_config("common").path) / "static" / "common"
        )
        if not options["library"] in self.libraries:
            return f"No library named '{options['library']}' found. Available are: {[l for l in self.libraries]}"

        library = self.libraries[options["library"]]
        for file_name, url, mode in library:
            data = requests.get(url)
            os.makedirs(os.path.dirname(target_path_root / file_name), exist_ok=True)
            self.stdout.write(file_name)
            with open(target_path_root / file_name, mode) as f:
                if mode == "w":
                    f.write(data.text)
                elif mode == "wb":
                    f.write(data.content)
