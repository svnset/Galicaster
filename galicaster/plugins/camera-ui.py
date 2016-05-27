# Galicaster-Plugin


import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from galicaster.core import context
import galicaster.utils.pysca as pysca

# DEFAULTS
CONFIG_SECTION = "camera-ui"
PORT_KEY = "/dev/ttyS0"


def init():
    global recorder, dispatcher

    dispatcher = context.get_dispatcher()
    recorder = context.get_recorder()
    dispatcher.connect("init", post_init)
    pysca.connect(context.get_conf().get(CONFIG_SECTION, PORT_KEY))


def post_init(source=None):
    global recorder_ui, edit_button

    conf = context.get_conf()  # get_section(CONFIG_SECTION) or {}

    recorder_ui = context.get_mainwindow().nbox.get_nth_page(0).gui
    buttonbox = recorder_ui.get_object("buttonbox")
    image = recorder_ui.get_object("moreimage")
    new_button = Gtk.Button.new()
    new_button.set_image(image)
    new_button.connect('clicked', open_config)
    new_button.show_all()
    buttonbox.add(new_button)


def open_config(button):
    win = Gtk.Window.new(Gtk.WindowType.TOPLEVEL)
    win.set_border_width(50)
    hbox = Gtk.Box(spacing=6)
    win.add(hbox)

    # testing optional buttons
    button = Gtk.Button.new_with_label("left")
    button.connect("clicked", move_left)
    hbox.pack_start(button, True, True, 0)

    button = Gtk.Button.new_with_label("right")
    button.connect("clicked", move_right)
    hbox.pack_start(button, True, True, 0)

    button = Gtk.Button.new_with_label("up")
    button.connect("clicked", move_up)
    hbox.pack_start(button, True, True, 0)

    button = Gtk.Button.new_with_label("down")
    button.connect("clicked", move_down)
    hbox.pack_start(button, True, True, 0)

    win.connect("delete-event", win.close)
    win.show_all()


def move_left(button):
    print ("I move left")


def move_right(button):
    print ("I move right")


def move_up(button):
    print ("I move up")


def move_down(button):
    print ("I move down")
