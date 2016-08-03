# Galicaster-Plugin


import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, GObject, Gdk
from galicaster.core import context
from galicaster.classui import get_ui_path
import galicaster.utils.pysca as pysca
from galicaster.classui.mainwindow import _

# DEFAULTS
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
    global recorder_ui, brightscale, movescale, zoomscale, presetbutton, flybutton, builder, onoffbutton, prefbutton

    conf = context.get_conf().get_section(CONFIG_SECTION) or {}
    recorder_ui = context.get_mainwindow().nbox.get_nth_page(0).gui

    # load css file
    cssold = Gtk.CssProvider.get_default()
    css = Gtk.CssProvider()
    css.load_from_path(get_ui_path("camera-ui.css"))
    Gtk.StyleContext.remove_provider_for_screen(
        Gdk.Screen.get_default(),
        cssold
    )
    Gtk.StyleContext.reset_widgets(Gdk.Screen.get_default())
    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(),
        css,
        Gtk.STYLE_PROVIDER_PRIORITY_USER
    )

    # load glade file
    builder = Gtk.Builder()
    builder.add_from_file(get_ui_path("camera-ui.glade"))

    # add new settings tab to the notebook
    notebook = recorder_ui.get_object("data_panel")
    label = Gtk.Label.new("Control")
    label.set_name("settingslabel")
    mainbox = builder.get_object("mainbox")
    mainbox.show_all()
    notebook.append_page(mainbox, label)


    # buttons
    # movement
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

    # zoom
    button = builder.get_object("zoomin")
    button.connect("pressed", zoom_in)
    button.connect("released", stop_zoom)

    button = builder.get_object("zoomout")
    button.connect("pressed", zoom_out)
    button.connect("released", stop_zoom)

    # presets
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

    # to set a new preset
    presetbutton = builder.get_object("preset")

    # fly-mode for camera-movement
    flybutton = builder.get_object("fly")
    flybutton.connect("clicked", fly_mode)

    # on-off button
    onoffbutton = builder.get_object("on-off")
    onoffbutton.connect("state-set", turn_on_off)

    # reset all settings
    button = builder.get_object("reset")
    button.connect("clicked", reset)

    # show/hide preferences
    prefbutton = builder.get_object("pref")
    prefbutton.connect("clicked", show_pref)

    # scales
    brightscale = builder.get_object("brightscale")
    brightscale.connect("value-changed", set_bright)
    movescale = builder.get_object("movescale")
    zoomscale = builder.get_object("zoomscale")


# camera functions

# movement functions
def move_left(button):
    print ("I move left")
    pysca.pan_tilt(DEFAULT_DEVICE, pan=-movescale.get_value())


def move_leftup(button):
    print ("I move leftup")
    pysca.pan_tilt(DEFAULT_DEVICE, pan=-movescale.get_value(), tilt=movescale.get_value())


def move_leftdown(button):
    print ("I move leftdown")
    pysca.pan_tilt(DEFAULT_DEVICE, pan=-movescale.get_value(), tilt=-movescale.get_value())


def move_right(button):
    print ("I move right")
    pysca.pan_tilt(DEFAULT_DEVICE, pan=movescale.get_value())


def move_rightup(button):
    print ("I move rightup")
    pysca.pan_tilt(DEFAULT_DEVICE, pan=movescale.get_value(), tilt=movescale.get_value())


def move_rightdown(button):
    print ("I move rightdown")
    pysca.pan_tilt(DEFAULT_DEVICE, pan=movescale.get_value(), tilt=-movescale.get_value())


def move_up(button):
    print ("I move up")
    pysca.pan_tilt(DEFAULT_DEVICE, tilt=movescale.get_value())


def move_down(button):
    print ("I move down")
    pysca.pan_tilt(DEFAULT_DEVICE, tilt=-movescale.get_value())


def stop_move(button):
    print ("I make a break")
    pysca.pan_tilt(DEFAULT_DEVICE, pan=0, tilt=0)


def move_home(button):
    print ("I move home")
    pysca.pan_tilt_home(DEFAULT_DEVICE)


# zoom functions
def zoom_in(button):
    print ("zoom in")
    pysca.zoom(DEFAULT_DEVICE, pysca.ZOOM_ACTION_TELE, speed=zoomscale.get_value())


def zoom_out(button):
    print ("zoom out")
    pysca.zoom(DEFAULT_DEVICE, pysca.ZOOM_ACTION_WIDE, speed=zoomscale.get_value())


def stop_zoom(button):
    print ("stop zoom")
    pysca.zoom(DEFAULT_DEVICE, pysca.ZOOM_ACTION_STOP)


# preset functions
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


# brightness scale
def set_bright(brightscale):
    pysca.set_ae_mode(DEFAULT_DEVICE, pysca.AUTO_EXPOSURE_BRIGHT_MODE)
    pysca.set_brightness(DEFAULT_DEVICE, brightscale.get_value() + 15)


# reset all settings
def reset(button):
    # reset brightness
    pysca.set_ae_mode(DEFAULT_DEVICE, pysca.AUTO_EXPOSURE_BRIGHT_MODE)
    pysca.set_brightness(DEFAULT_DEVICE, 15)
    brightscale.set_value(0)
    movescale.set_value(7)
    zoomscale.set_value(3.5)
    # reset zoom
    pysca.set_zoom(DEFAULT_DEVICE, 0000)
    # reset location
    pysca.pan_tilt_home(DEFAULT_DEVICE)


# turns the camera on/off
def turn_on_off(onoffbutton, self):
    if onoffbutton.get_active():
        pysca.set_power_on(DEFAULT_DEVICE, True)
    else:
        pysca.set_power_on(DEFAULT_DEVICE, False)


# hides/shows the advanced preferences
def show_pref(prefbutton):
    scalebox1 = builder.get_object("scales1")
    scalebox2 = builder.get_object("scales2")
    scalebox3 = builder.get_object("scales3")
    # settings button activated
    if scalebox1.get_property("visible"):
        print ("hide advanced settings")
        scalebox1.hide()
        scalebox2.hide()
        scalebox3.hide()
    # settings button deactivated
    else:
        print ("show advanced settings")
        scalebox1.show()
        scalebox2.show()
        scalebox3.show()



# flymode activation connects clicked signal and disconnects
# pressed/released to keep the movement
def fly_mode(flybutton):
    # fly mode turned on
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


    # fly mode turned off
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
