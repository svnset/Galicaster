# Galicaster-Plugin


import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, GObject
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
    global recorder_ui, scale, presetbutton, flybutton, builder, onoffbutton


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
    #movement
    button = builder.get_object("left")
    button.connect("pressed", move_left)
    button.connect("released", stop_move)

    button = builder.get_object("leftup")
    button.connect("pressed", move_leftup)
    button.connect("released", stop_move)

    button = builder.get_object("leftdown")
    button.connect("pressed", move_leftdown)
    button.connect("released", stop_move)

    button = builder.get_object("right")
    button.connect("pressed", move_right)
    button.connect("released", stop_move)

    button = builder.get_object("rightup")
    button.connect("pressed", move_rightup)
    button.connect("released", stop_move)

    button = builder.get_object("rightdown")
    button.connect("pressed", move_rightdown)
    button.connect("released", stop_move)

    button = builder.get_object("up")
    button.connect("pressed", move_up)
    button.connect("released", stop_move)

    button = builder.get_object("down")
    button.connect("pressed", move_down)
    button.connect("released", stop_move)

    button = builder.get_object("home")
    button.connect("clicked", move_home)

    #zoom
    button = builder.get_object("zoomin")
    button.connect("pressed", zoom_in)
    button.connect("released", stop_zoom)

    button = builder.get_object("zoomout")
    button.connect("pressed", zoom_out)
    button.connect("released", stop_zoom)

    #presets
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

    #to set a new preset
    presetbutton = builder.get_object("preset")

    #fly-mode for camera-movement
    flybutton = builder.get_object("fly")
    flybutton.connect("clicked", fly_mode)

    #on-off button
    onoffbutton = builder.get_object("on-off")
    onoffbutton.connect("state-set", turn_on_off)

    #reset all settings
    button = builder.get_object("reset")
    button.connect("clicked", reset)

    #scales
    scale = builder.get_object("brightscale")
    scale.connect("value-changed", set_bright)



#camera functions

#movement functions
def move_left(button):
    print ("I move left")
    pysca.pan_tilt(DEFAULT_DEVICE, pan=-8)


def move_leftup(button):
    print ("I move leftup")
    pysca.pan_tilt(DEFAULT_DEVICE, pan=-7, tilt=7)


def move_leftdown(button):
    print ("I move leftdown")
    pysca.pan_tilt(DEFAULT_DEVICE, pan=-7, tilt=-7)


def move_right(button):
    print ("I move right")
    pysca.pan_tilt(DEFAULT_DEVICE, pan=8)


def move_rightup(button):
    print ("I move rightup")
    pysca.pan_tilt(DEFAULT_DEVICE, pan=7, tilt=7)


def move_rightdown(button):
    print ("I move rightdown")
    pysca.pan_tilt(DEFAULT_DEVICE, pan=7, tilt=-7)


def move_up(button):
    print ("I move up")
    pysca.pan_tilt(DEFAULT_DEVICE, tilt=8)


def move_down(button):
    print ("I move down")
    pysca.pan_tilt(DEFAULT_DEVICE, tilt=-8)


def stop_move(button):
    print ("I make a break")
    pysca.pan_tilt(DEFAULT_DEVICE, pan=0, tilt=0)


def move_home(button):
    print ("I move home")
    pysca.pan_tilt_home(DEFAULT_DEVICE)

#zoom functions
def zoom_in(button):
    print ("zoom in")
    pysca.zoom(DEFAULT_DEVICE, pysca.ZOOM_ACTION_TELE, speed=5)

def zoom_out(button):
    print ("zoom out")
    pysca.zoom(DEFAULT_DEVICE, pysca.ZOOM_ACTION_WIDE, speed=5)

def stop_zoom(button):
    print ("stop zoom")
    pysca.zoom(DEFAULT_DEVICE, pysca.ZOOM_ACTION_STOP)

#preset functions

def preset1(button):
    if presetbutton.get_active():
        pysca.set_memory(DEFAULT_DEVICE, 0)
        presetbutton.set_active(False)
    else:
        pysca.recall_memory(DEFAULT_DEVICE, 0)

def preset2(button):
    if presetbutton.get_active():
        pysca.set_memory(DEFAULT_DEVICE, 1)
        presetbutton.set_active(False)
    else:
        pysca.recall_memory(DEFAULT_DEVICE, 1)

def preset3(button):
    if presetbutton.get_active():
        pysca.set_memory(DEFAULT_DEVICE, 2)
        presetbutton.set_active(False)
    else:
        pysca.recall_memory(DEFAULT_DEVICE, 2)

def preset4(button):
    if presetbutton.get_active():
        pysca.set_memory(DEFAULT_DEVICE, 3)
        presetbutton.set_active(False)
    else:
        pysca.recall_memory(DEFAULT_DEVICE, 3)

def preset5(button):
    if presetbutton.get_active():
        pysca.set_memory(DEFAULT_DEVICE, 4)
        presetbutton.set_active(False)
    else:
        pysca.recall_memory(DEFAULT_DEVICE, 4)

def preset6(button):
    if presetbutton.get_active():
        pysca.set_memory(DEFAULT_DEVICE, 5)
        presetbutton.set_active(False)
    else:
        pysca.recall_memory(DEFAULT_DEVICE, 5)

#brightness scale
def set_bright(scale):
    pysca.set_ae_mode(DEFAULT_DEVICE, pysca.AUTO_EXPOSURE_BRIGHT_MODE)
    pysca.set_brightness(DEFAULT_DEVICE, scale.get_value()+15)

#reset all settings
def reset(button):
    #reset brightness
    pysca.set_ae_mode(DEFAULT_DEVICE, pysca.AUTO_EXPOSURE_BRIGHT_MODE)
    pysca.set_brightness(DEFAULT_DEVICE, 15)
    scale.set_value(0)
    #reset zoom
    pysca.set_zoom(DEFAULT_DEVICE, 0000)
    #reset location
    pysca.pan_tilt_home(DEFAULT_DEVICE)

#turns the camera on/off
def turn_on_off(onoffbutton, self):
    if onoffbutton.get_active():
        pysca.set_power_on(DEFAULT_DEVICE, True)
    else:
        pysca.set_power_on(DEFAULT_DEVICE, False)

#flymode activation connects clicked signal and disconnects
# pressed/released to keep the movement
def fly_mode(flybutton):
    #fly mode turned on
    if flybutton.get_active():
        print ("fly mode turned on")
        button = builder.get_object("left")
        GObject.signal_handlers_destroy(button)
        button.connect("clicked", move_left)

        button = builder.get_object("leftup")
        GObject.signal_handlers_destroy(button)
        button.connect("clicked", move_leftup)

        button = builder.get_object("leftdown")
        GObject.signal_handlers_destroy(button)
        button.connect("clicked", move_leftdown)

        button = builder.get_object("right")
        GObject.signal_handlers_destroy(button)
        button.connect("clicked", move_right)

        button = builder.get_object("rightup")
        GObject.signal_handlers_destroy(button)
        button.connect("clicked", move_rightup)

        button = builder.get_object("rightdown")
        GObject.signal_handlers_destroy(button)
        button.connect("clicked", move_rightdown)

        button = builder.get_object("up")
        GObject.signal_handlers_destroy(button)
        button.connect("clicked", move_up)

        button = builder.get_object("down")
        GObject.signal_handlers_destroy(button)
        button.connect("clicked", move_down)

        button = builder.get_object("home")
        img = builder.get_object("stopimg")
        GObject.signal_handlers_destroy(button)
        button.set_image(img)
        button.connect("clicked", stop_move)


    #fly mode turned off
    else:
        print("fly mode turned off")

        button = builder.get_object("left")
        GObject.signal_handlers_destroy(button)
        button.connect("pressed", move_left)
        button.connect("released", stop_move)

        button = builder.get_object("leftup")
        GObject.signal_handlers_destroy(button)
        button.connect("pressed", move_leftup)
        button.connect("released", stop_move)

        button = builder.get_object("leftdown")
        GObject.signal_handlers_destroy(button)
        button.connect("pressed", move_leftdown)
        button.connect("released", stop_move)

        button = builder.get_object("right")
        GObject.signal_handlers_destroy(button)
        button.connect("pressed", move_right)
        button.connect("released", stop_move)

        button = builder.get_object("rightup")
        GObject.signal_handlers_destroy(button)
        button.connect("pressed", move_rightup)
        button.connect("released", stop_move)

        button = builder.get_object("rightdown")
        GObject.signal_handlers_destroy(button)
        button.connect("pressed", move_rightdown)
        button.connect("released", stop_move)

        button = builder.get_object("up")
        GObject.signal_handlers_destroy(button)
        button.connect("pressed", move_up)
        button.connect("released", stop_move)

        button = builder.get_object("down")
        GObject.signal_handlers_destroy(button)
        button.connect("pressed", move_down)
        button.connect("released", stop_move)

        button = builder.get_object("home")
        img = builder.get_object("homeimg")
        GObject.signal_handlers_destroy(button)
        button.set_image(img)
        button.connect("clicked", move_home)
