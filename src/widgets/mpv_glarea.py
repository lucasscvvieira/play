# mpv_glarea.py
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

import ctypes

import gi

gi.require_version('GL', '1.0')

from gi.repository import Gtk, GLib
from OpenGL import GL, GLX

from mpv import MPV, MpvRenderContext, MpvGlGetProcAddressFn


def get_process_address(_, name):
    address = GLX.glXGetProcAddress(name.decode("utf-8"))
    return ctypes.cast(address, ctypes.c_void_p).value


class MPVGlArea(Gtk.GLArea):

    def __init__(self, mpv: MPV, **kwargs):
        super().__init__(**kwargs)

        self._proc_addr_wrapper = MpvGlGetProcAddressFn(get_process_address)

        self.ctx = None
        self.mpv = mpv

        self.connect("realize", self.on_realize)
        self.connect("render", self.on_render)
        self.connect("unrealize", self.on_unrealize)

    def on_realize(self, area):
        self.make_current()
        self.ctx = MpvRenderContext(self.mpv, 'opengl',
                                    opengl_init_params={'get_proc_address': self._proc_addr_wrapper})
        self.ctx.update_cb = self.wrapped_c_render_func

    def on_unrealize(self, arg):
        self.ctx.free()
        self.mpv.terminate()

    def wrapped_c_render_func(self):
        GLib.idle_add(self.call_frame_ready, None, GLib.PRIORITY_HIGH)

    def call_frame_ready(self, *args):
        if self.ctx.update():
            self.queue_render()

    def on_render(self, arg1, arg2):
        if self.ctx:
            factor = self.get_scale_factor()

            width = self.get_allocated_width() * factor
            height = self.get_allocated_height() * factor

            fbo = GL.glGetIntegerv(GL.GL_DRAW_FRAMEBUFFER_BINDING)
            self.ctx.render(flip_y=True, opengl_fbo={'w': width, 'h': height, 'fbo': fbo})
            return True
        return False
