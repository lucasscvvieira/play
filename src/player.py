# player.py
#
# Copyright 2022 Lucas Campos Vieira
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from enum import Enum

from gi.repository import Gtk, GObject
from mpv import MPV

from .widgets.mpv_glarea import MPVGlArea


class PlayerState(Enum):
    PLAYING = 0
    PAUSED = 1
    STOPPED = 2


class Player(GObject.Object):
    _state = PlayerState.STOPPED

    def __init__(self):
        self.mpv = MPV()
        self._widget = MPVGlArea(self.mpv)

    def load(self, uri: str, sub_uri: str = None):
        self.mpv.loadfile(uri, sub_file=sub_uri)
        self.mpv.wait_until_playing()
        self._state = PlayerState.PLAYING

    @property
    def widget(self) -> Gtk.Widget:
        return self._widget
