import re
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from django.utils import formats, timezone

# get localized date input formats
input_formats = formats.get_format_lazy("DATE_INPUT_FORMATS")


def parse_date_string(date_string: str) -> date | None:
    """Tries to guess which date format the date_string has and returns a correct date object."""
    if not date_string:
        return None
    date_string = date_string.strip()
    if not re.sub("[/.]", "", date_string).isnumeric():
        return None
    # this does not work. Input formats are in an order we cant anticipate, and this could create
    # situations where a DE localizable fast-entered "131279" is not parsed into datetime(1979, 12, 13), but
    # the first format in DE is used (%d.%m.%Y) which tries to interpret the last 4 places as YEAR, so it
    # parses datetime(1279, 3, 1) out of it...
    # for input_format in input_formats:  # type: str
    #     stripped_format = re.sub(",|\.|/| ", "", input_format)
    #     if search_date := datetime.strptime(date_string, stripped_format):
    #         return search_date.date()
    # return None
    if len(date_string) == 6:
        # DDMMYY
        if re.match(r"^[0123]\d[01]\d\d\d$", date_string):
            return datetime.strptime(date_string, "%d%m%y").date()
    elif len(date_string) == 8:
        # DD.MM.YY
        if re.match(r"^[0123]\d\.[01]\d\.\d\d$", date_string):
            return datetime.strptime(date_string, "%d.%m.%y").date()
        # DDMMYYYY
        if re.match(r"^[0123]\d[01]\d[12][90]\d\d$", date_string):
            return datetime.strptime(date_string, "%d%m%Y").date()
    elif len(date_string) == 10:
        # DD.MM.YYYY
        if re.match(r"^[0123]\d\.[01]\d\.[12][90]\d\d$", date_string):
            return datetime.strptime(date_string, "%d.%m.%Y").date()
        elif date_string.isnumeric():  # SVNR + DDMMYY
            dt = datetime.strptime(date_string[4:], "%d%m%y").date()
            if dt > timezone.now().date():
                dt -= relativedelta(years=100)
            return dt
    return None
