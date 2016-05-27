# Galicaster-Plugin


import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from galicaster.core import context
import galicaster.utils.pysca as pysca

#DEFAULTS
DEFAULT_DEVICE = 1
CONFIG_SECTION = "camera-ui"
PORT_KEY = "/dev/ttyS0"


def init():
    global recorder, dispatcher

    dispatcher = context.get_dispatcher()
    recorder = context.get_recorder()
    dispatcher.connect("init", post_init)
    pysca.connect(PORT_KEY)


def post_init(source=None):
    global recorder_ui, edit_button

    conf = context.get_conf().get_section(CONFIG_SECTION) or {}

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
    hbox = Gtk.Box(spacing=10)
    win.add(hbox)

    #testing buttons
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

    button = Gtk.Button.new_with_label("stop")
    button.connect("clicked", stop_move)
    hbox.pack_start(button, True, True, 0)

    button = Gtk.Button.new_with_label("home")
    button.connect("clicked", move_home)
    hbox.pack_start(button, True, True, 0)

    win.connect("delete-event", win.close)
    win.show_all()


#testing camera functions
def move_left(button):
    pysca.pan_tilt(DEFAULT_DEVICE, pan=-7)
    print ("I move left")

def move_right(button):
    pysca.pan_tilt(DEFAULT_DEVICE, pan=7)
    print ("I move right")

def move_up(button):
    pysca.pan_tilt(DEFAULT_DEVICE, tilt=7)
    print ("I move up")

def move_down(button):
    pysca.pan_tilt(DEFAULT_DEVICE, tilt=-7)
    print ("I move down")

def stop_move(button):
    pysca.pan_tilt(DEFAULT_DEVICE, pan=0, tilt=0)
    print ("I make a break")

def move_home(button):
    pysca.pan_tilt_home(DEFAULT_DEVICE)
    print ("I move home")
