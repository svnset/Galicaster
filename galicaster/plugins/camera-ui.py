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

#camera-ui settings window
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

    button = builder.get_object("zoomin")
    button.connect("clicked", zoom_in)

    button = builder.get_object("zoomout")
    button.connect("clicked", zoom_out)

    #testing scales
    scale = builder.get_object("scale1")
    scale.connect("value-changed", set_bright)

    win.connect("delete-event", win.close)
    win.show_all()



#testing camera functions

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

#zoom
def zoom_in(button):
    print ("zoom in")
    pysca.zoom(DEFAULT_DEVICE, pysca.ZOOM_ACTION_STOP)
    pysca.zoom(DEFAULT_DEVICE, pysca.ZOOM_ACTION_TELE, speed=3)

def zoom_out(button):
    print ("zoom out")
    pysca.zoom(DEFAULT_DEVICE, pysca.ZOOM_ACTION_STOP)
    pysca.zoom(DEFAULT_DEVICE, pysca.ZOOM_ACTION_WIDE, speed=3)

#scale
def set_bright(scale):
    old_value = 0
    new_value = scale.get_value()
    #stash = new_value
    #stash2 = old_value

    #print (old_value)
    #print("here")


    if new_value > old_value :
        print ("It gets lighter")
        #old_value = new_value
        pysca.set_exp_comp(DEFAULT_DEVICE, pysca.AUTO_EXPOSURE_BRIGHT_MODE)
        pysca.set_brightness(DEFAULT_DEVICE, pysca.BRIGHT_ACTION_UP)

    elif new_value < old_value :
        print ("It gets darker")
        pysca.set_exp_comp(DEFAULT_DEVICE, pysca.AUTO_EXPOSURE_BRIGHT_MODE)
        pysca.set_brightness(DEFAULT_DEVICE, pysca.BRIGHT_ACTION_DOWN)

#def get_old_value(scale):
#   old_value = float(scale.get_value())
