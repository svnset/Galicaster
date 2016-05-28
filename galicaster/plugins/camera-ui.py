# Galicaster-Plugin


import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from galicaster.core import context
from galicaster.classui import get_ui_path
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
    global win

    builder = Gtk.Builder()
    builder.add_from_file(get_ui_path("camera-ui.glade"))

    win = builder.get_object("window")

    #testing buttons
    button = builder.get_object("left")
    button.connect("clicked", move_left)

    button = builder.get_object("leftup")
    button.connect("clicked", move_leftup)

    button = builder.get_object("leftdown")
    button.connect("clicked", move_leftdown)

    button = builder.get_object("right")
    button.connect("clicked", move_right)

    button = builder.get_object("rightup")
    button.connect("clicked", move_rightup)

    button = builder.get_object("rightdown")
    button.connect("clicked", move_rightdown)


    button = builder.get_object("up")
    button.connect("clicked", move_up)


    button = builder.get_object("down")
    button.connect("clicked", move_down)


    button = builder.get_object("stop")
    button.connect("clicked", stop_move)


    button = builder.get_object("home")
    button.connect("clicked", move_home)


    win.connect("delete-event", win.close)
    win.show_all()



#testing camera functions
def move_left(button):
    pysca.pan_tilt(DEFAULT_DEVICE, pan=-7)
    print ("I move left")

def move_leftup(button):
    pysca.pan_tilt(DEFAULT_DEVICE, pan=-7, tilt=7)
    print ("I move left")

def move_leftdown(button):
    pysca.pan_tilt(DEFAULT_DEVICE, pan=-7, tilt=-7)
    print ("I move left")

def move_right(button):
    pysca.pan_tilt(DEFAULT_DEVICE, pan=7)
    print ("I move right")

def move_rightup(button):
    pysca.pan_tilt(DEFAULT_DEVICE, pan=7, tilt=7)
    print ("I move right")

def move_rightdown(button):
    pysca.pan_tilt(DEFAULT_DEVICE, pan=7, tilt=-7)
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
