import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk, GObject
from galicaster.core import context
from galicaster.classui import get_ui_path
import galicaster.utils.camera_profiles as camera
#  from galicaster.mediapackage import repository


def init():
    global cam, recorder, dispatcher, logger

# connect to the camera
    ip = '134.95.128.120'
    username = "root"
    password = "opencast"

    cam = camera.AXIS_V5915()
    cam.connect(ip, username, password)
    dispatcher = context.get_dispatcher()
    dispatcher.connect("init", init_ui)
    logger = context.get_logger()
    logger.info("Cam connected")
    #  init_ui()


def init_ui(element):
    global recorder_ui, brightscale, movescale, zoomscale, presetlist, presetdelbutton, flybutton, builder, onoffbutton, prefbutton


    #  conf = contex.get_conf().get_section(CONFIG_SECTION) or {}
    recorder_ui = context.get_mainwindow().nbox.get_nth_page(0).gui

# load css file
    css = Gtk.CssProvider()
    css.load_from_path(get_ui_path("camera-ui.css"))

    Gtk.StyleContext.reset_widgets(Gdk.Screen.get_default())
    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(),
        css,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )

    # load glade file
    builder = Gtk.Builder()
    builder.add_from_file(get_ui_path("ipui.glade"))
    
    # add new settings tab to the notebook
    notebook = recorder_ui.get_object("data_panel")
    mainbox = builder.get_object("mainbox")
    label = builder.get_object("notebooklabel")
    mainbox.show_all()
    notebook.append_page(mainbox, label)
    notebook.show_all()


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
    button.connect("released", stop_move)

    button = builder.get_object("zoomout")
    button.connect("pressed", zoom_out)
    button.connect("released", stop_move)

# presets
    
    presetlist = builder.get_object("preset_list")
    # fill the list with current presets
    for preset in cam.getPresets():
        presetlist.append_text(preset.Name)
    presetlist.connect("changed", change_preset)

# to set a new preset
    newpreset = builder.get_object("newpreset")
    newpreset.connect("activate", save_preset)
    newpreset.connect("icon-press", save_preset_icon)


# to delete a preset
    presetdelbutton = builder.get_object("presetdel")
    presetdelbutton.connect("pressed", empty_entry)

# fly-mode for camera-movement
    flybutton = builder.get_object("fly")
    flybutton.connect("clicked", fly_mode)

#  # on-off button
    #  onoffbutton = builder.get_object("on-off")
    #  onoffbutton.connect("state-set", turn_on_off)

# reset all settings
    button = builder.get_object("reset")
    button.connect("clicked", reset)

# show/hide preferences
    prefbutton = builder.get_object("pref")
    prefbutton.connect("clicked", show_pref)

# scales
    #  brightscale = builder.get_object("brightscale")
    #  brightscale.connect("value-changed", set_bright)
    movescale = builder.get_object("movescale")
    zoomscale = builder.get_object("zoomscale")
    

# camera functions

# movement functions
def move_left(button):
    print ("I move left")
    cam.goLeft(movescale.get_value())


def move_leftup(button):
    print ("I move leftup")
    cam.goLeftUp(movescale.get_value())

def move_leftdown(button):
    print ("I move leftdown")
    cam.goLeftDown(movescale.get_value())


def move_right(button):
    print ("I move right")
    cam.goRight(movescale.get_value())


def move_rightup(button):
    print ("I move rightup")
    cam.goRightUp(movescale.get_value())

def move_rightdown(button):
    print ("I move rightdown")
    cam.goRightDown(movescale.get_value())


def move_up(button):
    print ("I move up")
    cam.goUp(movescale.get_value())


def move_down(button):
    print ("I move down")
    cam.goDown(movescale.get_value())


def stop_move(button):
    print ("I make a break")
    cam.stop()


def move_home(button):
    print ("I move home")
    cam.goHome()


# zoom functions
def zoom_in(button):
    print ("zoom in")
    cam.zoom_in(zoomscale.get_value())


def zoom_out(button):
    print ("zoom out")
    cam.zoom_out(zoomscale.get_value())


# preset functions
def change_preset(presetlist):
    if presetdelbutton.get_active():
        cam.removePreset(cam.identifyPreset(presetlist.get_active_text()))
        presetdelbutton.set_active(False)
        presetlist.remove(presetlist.get_active())
        
    else:
        if not presetlist.get_active_text() is None:
            print("Going to: " + presetlist.get_active_text())
            cam.goToPreset(cam.identifyPreset(presetlist.get_active_text()))
            #presetlist.set_active(-1)

def empty_entry(presetdelbutton):
    presetlist.set_active(-1)

def save_preset_icon(newpreset, pos, event):
    cam.setPreset(newpreset.get_text())
    presetlist.append_text(newpreset.get_text())
    newpreset.set_text("")


def save_preset(newpreset):
    cam.setPreset(newpreset.get_text())
    presetlist.append_text(newpreset.get_text())
    newpreset.set_text("")


# brightness scale
def set_bright(brightscale):
    return None

# reset all settings
def reset(button):
    movescale.set_value(0.5)
    zoomscale.set_value(0.5)
    # reset location
    cam.goHome()

#  # turns the camera on/off
#  def turn_on_off(onoffbutton, self):
    #  if onoffbutton.get_active():
        #  pysca.set_power_on(DEFAULT_DEVICE, True)
    #  else:
        #  pysca.set_power_on(DEFAULT_DEVICE, False)


# hides/shows the advanced preferences
def show_pref(prefbutton):
    scalebox1 = builder.get_object("scales1")
    scalebox2 = builder.get_object("scales2")
    # settings button activated
    if scalebox1.get_property("visible"):
        print ("hide advanced settings")
        scalebox1.hide()
        scalebox2.hide()
    # settings button deactivated
    else:
        print ("show advanced settings")
        scalebox1.show()
        scalebox2.show()



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

# start
#  init()
