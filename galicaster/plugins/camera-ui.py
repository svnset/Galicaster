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
    global recorder_ui


    conf = context.get_conf().get_section(CONFIG_SECTION) or {}
    recorder_ui = context.get_mainwindow().nbox.get_nth_page(0).gui
    notebook = recorder_ui.get_object("data_panel")


    #implement glade file
    builder = Gtk.Builder()
    builder.add_from_file(get_ui_path("camera-ui.glade"))

    #add new settings tab to the notebook
    label = Gtk.Label.new("Settings")
    tabbox = builder.get_object("box")
    tabbox.show_all()
    notebook.append_page(tabbox, label)

    #buttons
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

    button = builder.get_object("zoomin")
    button.connect("pressed", zoom_in)
    button.connect("released", stop_zoom)

    button = builder.get_object("zoomout")
    button.connect("pressed", zoom_out)
    button.connect("released", stop_zoom)

    button = builder.get_object("1")
    button.connect("clicked", preset1)

    button = builder.get_object("2")
    button.connect("clicked", preset2)

    button = builder.get_object("3")
    button.connect("clicked", preset3)

    button = builder.get_object("4")
    button.connect("clicked", preset4)

    button = builder.get_object("5")
    button.connect("clicked", preset5)

    button = builder.get_object("6")
    button.connect("clicked", preset6)

    #scales

    scale = builder.get_object("scale1")
    scale.connect("value-changed", set_bright)




#camera functions

#move
def move_left(button):
    print ("I move left")
    pysca.pan_tilt(DEFAULT_DEVICE, pan=-7)


def move_leftup(button):
    print ("I move leftup")
    pysca.pan_tilt(DEFAULT_DEVICE, pan=-7, tilt=7)


def move_leftdown(button):
    print ("I move leftdown")
    pysca.pan_tilt(DEFAULT_DEVICE, pan=-7, tilt=-7)


def move_right(button):
    print ("I move right")
    pysca.pan_tilt(DEFAULT_DEVICE, pan=7)


def move_rightup(button):
    print ("I move rightup")
    pysca.pan_tilt(DEFAULT_DEVICE, pan=7, tilt=7)


def move_rightdown(button):
    print ("I move rightdown")
    pysca.pan_tilt(DEFAULT_DEVICE, pan=7, tilt=-7)


def move_up(button):
    print ("I move up")
    pysca.pan_tilt(DEFAULT_DEVICE, tilt=7)


def move_down(button):
    print ("I move down")
    pysca.pan_tilt(DEFAULT_DEVICE, tilt=-7)


def stop_move(button):
    print ("I make a break")
    pysca.pan_tilt(DEFAULT_DEVICE, pan=0, tilt=0)


def move_home(button):
    print ("I move home")
    pysca.pan_tilt_home(DEFAULT_DEVICE)

#zoom buttons
def zoom_in(button):
    print ("zoom in")
    pysca.zoom(DEFAULT_DEVICE, pysca.ZOOM_ACTION_TELE, speed=5)

def zoom_out(button):
    print ("zoom out")
    pysca.zoom(DEFAULT_DEVICE, pysca.ZOOM_ACTION_WIDE, speed=5)

def stop_zoom(button):
    print ("stop zoom")
    pysca.zoom(DEFAULT_DEVICE, pysca.ZOOM_ACTION_STOP)

#preset buttons

def preset1(button):
    pysca.recall_memory(DEFAULT_DEVICE, 0)

def preset2(button):
    pysca.recall_memory(DEFAULT_DEVICE, 1)

def preset3(button):
    pysca.recall_memory(DEFAULT_DEVICE, 2)

def preset4(button):
    pysca.recall_memory(DEFAULT_DEVICE, 3)

def preset5(button):
    pysca.recall_memory(DEFAULT_DEVICE, 4)

def preset6(button):
    pysca.recall_memory(DEFAULT_DEVICE, 5)

#brightness scale
def set_bright(scale):
    pysca.set_ae_mode(DEFAULT_DEVICE, pysca.AUTO_EXPOSURE_BRIGHT_MODE)
    pysca.set_brightness(DEFAULT_DEVICE, scale.get_value())