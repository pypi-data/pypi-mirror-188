#  MedUX - Open Source Electronical Medical Record
#  Copyright (c) 2022  Christian González
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
from django.views.generic import FormView
from medux.common.htmx.mixins import HtmxMixin

from medux.core.api import ICommand


class CommandLineView(HtmxMixin, FormView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._command = None

    def execute(self):
        for plugin in ICommand:
            pass

    def parse(self):
        for plugin in ICommand:
            if self.command_text.startswith(plugin.shortcut):
                self._command = plugin
