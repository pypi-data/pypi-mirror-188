import logging

from django_unicorn.components import UnicornView

from medux.utils import parse_date_string

logger = logging.getLogger(__name__)


class PatientSearchInputView(UnicornView):
    search_text = ""

    def search(self):
        params = {}
        self.search_text = self.search_text.strip().lower()  # type: str
        if self.search_text.isnumeric():
            # FIXME: birth date search does not work yet
            params["birth_date__date"] = parse_date_string(self.search_text)
        elif self.search_text.count(",") == 1:
            (
                params["names__last_name__startswith"],
                params["names__first_name__startswith"],
            ) = self.search_text.split(",")
        else:
            params["names__last_name__startswith"] = self.search_text

        self.parent.load_table(params)
        logger.debug(params)
