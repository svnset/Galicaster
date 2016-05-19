#Galicaster-Plugin


import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from galicaster.core import context
import galicaster.utils.pysca as pysca





def init():
    global recorder, dispatcher
    dispatcher = context.get_dispatcher()
    recorder = context.get_recorder()
    dispatcher.connect("init", post_init)


def post_init(source=None):

    global recorder_ui, buttonbox

    conf = context.get_conf()
    recorder_ui = context.get_mainwindow().nbox.get_nth_page(0)
    buttonbox =  recorder_ui.gui.get_object("buttonbox")

    new_button = Gtk.Button("config")
    new_button.connect('clicked', new_window)
    buttonbox.add(new_button)



def new_window(button):
    global recorder, recorder_ui
    win = Gtk.Window()
    button1 = Gtk.Button("1")
    button2 = Gtk.Button("2")
    win.add(button1)
    win.add(button2)
    Gtk.main()
