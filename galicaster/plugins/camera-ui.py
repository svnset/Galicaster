#Galicaster-Plugin


import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from galicaster.core import context
#import galicaster.utils.pysca as pysca


def init():
    global recorder, dispatcher
    dispatcher = context.get_dispatcher()
    recorder = context.get_recorder()
    dispatcher.connect("init", post_init)


def post_init(source=None):

    global recorder_ui, edit_button

    conf = context.get_conf()
    recorder_ui = context.get_mainwindow().nbox.get_nth_page(0)
    edit_button =  recorder_ui.gui.get_object("editbutton")
    edit_button.connect('clicked', on_edit_meta)
    edit_button.handler_block_by_func(recorder_ui.on_edit_meta)


def on_edit_meta(button):
    win = Gtk.Window.new(Gtk.WindowType.TOPLEVEL)
    win.set_border_width(10)
    hbox = Gtk.Box(spacing=6)
    win.add(hbox)

    button = Gtk.Button.new_with_label("Click Me")
    button.connect("clicked", on_click_me_clicked)
    hbox.pack_start(button, True, True, 0)

    button = Gtk.Button.new_with_mnemonic("_Open")
    button.connect("clicked", on_open_clicked)
    hbox.pack_start(button, True, True, 0)

    button = Gtk.Button.new_with_mnemonic("_Close")
    button.connect("clicked", on_close_clicked)
    hbox.pack_start(button, True, True, 0)

    win.connect("delete-event", win.close)
    win.show_all()


def on_click_me_clicked(self, button):
    print("\"Click me\" button was clicked")


def on_open_clicked(self, button):
    print("\"Open\" button was clicked")


def on_close_clicked(self, button):
    print("Closing application")
    Gtk.main_quit()



