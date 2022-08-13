# file_chooser.py
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

from pathlib import Path

from gi.repository import Gtk, Gio


class FileChooser(Gtk.FileChooserDialog):
    home = Path.home()

    def __init__(self, parent: Gtk.Widget):
        super().__init__(transient_for=parent, use_header_bar=True)

        self.set_action(action=Gtk.FileChooserAction.OPEN)
        self.set_modal(modal=True)

        self.set_current_folder(Gio.File.new_for_path(path=str(self.home)))

        # Criando os botões que ficarão na barra de título (Gtk.HeaderBar()).
        self.add_buttons(
            '_Cancel', Gtk.ResponseType.CANCEL,
            '_Open', Gtk.ResponseType.OK
        )
        btn_select = self.get_widget_for_response(response_id=Gtk.ResponseType.OK)
        btn_cancel = self.get_widget_for_response(response_id=Gtk.ResponseType.CANCEL)
        # Adicionando estilo no botão.
        btn_select.get_style_context().add_class(class_name='suggested-action')
        btn_cancel.get_style_context().add_class(class_name='destructive-action')
