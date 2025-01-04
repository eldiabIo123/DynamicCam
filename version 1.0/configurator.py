import os
import cv2
import json
import pyaudio
import tkinter
import webbrowser
import tkinter.filedialog
from screeninfo import get_monitors
from tkinter import Tk, ttk, Canvas, Entry, PhotoImage, END

if str(os.name) == 'nt':
    config_path = f"{os.path.dirname(os.path.abspath(__file__))}\\config.json"
else:
    config_path = f"{os.path.dirname(os.path.abspath(__file__))}/config.json"

DEFAULT_CONFIG = {
    "window_name": "Dynamic Cam Preview",
    "fullscreen": True,
    "audio": True,
    "idle_file": "",
    "selected_camera": "",
    "selected_screen": "",
    "selected_mic": "",
    "sensitivity": 300,
    "FPS": 144,
    "ratio1": 16,
    "ratio2": 9,
    "cam_w": 1920,
    "cam_h": 1080,
    "audio_rate": 22050,
    "audio_buffer": 256
}

def assets(path: str): 
    if str(os.name) == 'nt':
        return f"{os.path.dirname(os.path.abspath(__file__))}\\assets\\{path}"
    else:
        return f"{os.path.dirname(os.path.abspath(__file__))}/assets/{path}"
    
def get_camera_list():
    cameras = []
    for i in range(10):  
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            cameras.append(f"Camera {i}")
            cap.release()
    return cameras

cameras = get_camera_list()

def get_monitor_list():
    monitors = []
    for monitor in get_monitors():
        monitors.append(f"{monitor.name} - {monitor.width}x{monitor.height} @ {monitor.x},{monitor.y}")
    return monitors

monitors = get_monitor_list()
    
def get_microphone_list():
    mics = []
    for i in range(pyaudio.PyAudio().get_device_count()):
        mic_info = pyaudio.PyAudio().get_device_info_by_index(i)
        if mic_info["maxInputChannels"] > 0:
            mics.append(mic_info["name"])
    pyaudio.PyAudio().terminate()
    return mics
    
microphones = get_microphone_list()

class Config:
    def create_config(file_path=config_path, default_config=DEFAULT_CONFIG):
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                json.dump(default_config, file, indent=4)

    def window_name():
        with open(config_path, 'r') as file:
            data = json.load(file)
        return str(data['window_name'])
    def fullscreen():
        with open(config_path, 'r') as file:
            data = json.load(file)
        return bool(data['fullscreen'])
    def audio():
        with open(config_path, 'r') as file:
            data = json.load(file)
        return bool(data['audio'])
    def idle_file():
        with open(config_path, 'r') as file:
            data = json.load(file)
        return str(data['idle_file'])
    def selected_camera():
        with open(config_path, 'r') as file:
            data = json.load(file)
        return str(data['selected_camera'])
    def selected_screen():
        with open(config_path, 'r') as file:
            data = json.load(file)
        return str(data['selected_screen'])
    def selected_mic():
        with open(config_path, 'r') as file:
            data = json.load(file)
        return str(data['selected_mic'])
    
    def change_window_name(name: str):
        with open(config_path, 'r') as file:
            data = json.load(file)
        data['window_name'] = name
        with open(config_path, 'w') as file:
            json.dump(data, file)
    def change_fullscreen(yes: bool):
        with open(config_path, 'r') as file:
            data = json.load(file)
        data['fullscreen'] = yes
        with open(config_path, 'w') as file:
            json.dump(data, file)
    def change_audio(yes: bool):
        with open(config_path, 'r') as file:
            data = json.load(file)
        data['audio'] = yes
        with open(config_path, 'w') as file:
            json.dump(data, file)
    def change_idle_file(path: str):
        with open(config_path, 'r') as file:
            data = json.load(file)
        data['idle_file'] = path
        with open(config_path, 'w') as file:
            json.dump(data, file)
    def change_selected_camera(cam: str):
        with open(config_path, 'r') as file:
            data = json.load(file)
        data['selected_camera'] = cam
        with open(config_path, 'w') as file:
            json.dump(data, file)
    def change_selected_screen(scr: str):
        with open(config_path, 'r') as file:
            data = json.load(file)
        data['selected_screen'] = scr
        with open(config_path, 'w') as file:
            json.dump(data, file)
    def change_selected_mic(mic: str):
        with open(config_path, 'r') as file:
            data = json.load(file)
        data['selected_mic'] = mic
        with open(config_path, 'w') as file:
            json.dump(data, file)

def start():
    print("Hello World!")
    Config.create_config()
    wind_entry.insert(0, Config.window_name())
    global fullscreen
    if Config.fullscreen():
        fullscreen = True
        canvas.itemconfig(fullscr_btn_off, state='hidden')
        canvas.itemconfig(fullscr_btn_on, state='normal')
    else:
        fullscreen = False
        canvas.itemconfig(fullscr_btn_off, state='normal')
        canvas.itemconfig(fullscr_btn_on, state='hidden')
    global audio
    if Config.audio():
        audio = True
        canvas.itemconfig(audio_btn_off, state='hidden')
        canvas.itemconfig(audio_btn_on, state='normal')
    else:
        audio = False
        canvas.itemconfig(audio_btn_off, state='normal')
        canvas.itemconfig(audio_btn_on, state='hidden')
    if not str(Config.idle_file()).endswith('.png') or not os.path.exists(Config.idle_file()):
        if not os.path.exists(assets("no_signal_elgato.png")):
            Config.change_idle_file("")
        else:
            Config.change_idle_file(assets("no_signal_elgato.png"))
    path_entry.insert(0, Config.idle_file())

fullscreen = True
def fullscreen_off(event):
    global fullscreen
    if fullscreen != True:
        fullscreen = True
        canvas.itemconfig(fullscr_btn_off, state='hidden')
        canvas.itemconfig(fullscr_btn_on, state='normal')
    else:
        fullscreen = False
        canvas.itemconfig(fullscr_btn_off, state='normal')
        canvas.itemconfig(fullscr_btn_on, state='hidden')

def fullscreen_on(event):
    global fullscreen
    if fullscreen == True:
        fullscreen = False
        canvas.itemconfig(fullscr_btn_off, state='normal')
        canvas.itemconfig(fullscr_btn_on, state='hidden')
    else:
        fullscreen = True
        canvas.itemconfig(fullscr_btn_off, state='hidden')
        canvas.itemconfig(fullscr_btn_on, state='normal')

audio = True
def audio_off(event):
    global audio
    if audio != True:
        audio = True
        canvas.itemconfig(audio_btn_off, state='hidden')
        canvas.itemconfig(audio_btn_on, state='normal')
    else:
        audio = False
        canvas.itemconfig(audio_btn_off, state='normal')
        canvas.itemconfig(audio_btn_on, state='hidden')

def audio_on(event):
    global audio
    if audio == True:
        audio = False
        canvas.itemconfig(audio_btn_off, state='normal')
        canvas.itemconfig(audio_btn_on, state='hidden')
    else:
        audio = True
        canvas.itemconfig(audio_btn_off, state='hidden')
        canvas.itemconfig(audio_btn_on, state='normal')

def select_idle(event):
    try:
        output_path = tkinter.filedialog.askopenfile(filetypes=[("PNG Images", "*.png")]).name
        path_entry.delete(0, END)
        path_entry.insert(0, str(output_path))
    except Exception as err:
        if str(err) != "'NoneType' object has no attribute 'name'":
            print(f"Error [in selecting idle file]: {str(err)}")

def apply_clicked(event):
    Config.change_window_name(str(wind_entry.get()))
    Config.change_fullscreen(bool(fullscreen))
    Config.change_audio(bool(audio))
    if not str(path_entry.get()).endswith('.png') or not os.path.exists(str(path_entry.get())):
        if not os.path.exists(assets("no_signal_elgato.png")):
            Config.change_idle_file("")
            path_entry.delete(0, END)
        else:
            Config.change_idle_file(assets("no_signal_elgato.png"))
            path_entry.delete(0, END)
            path_entry.insert(0, assets("no_signal_elgato.png"))
    Config.change_idle_file(str(path_entry.get()))
    Config.change_selected_camera(str(camera_combobox.get()))
    Config.change_selected_screen(str(monitor_combobox.get()))
    Config.change_selected_mic(str(mic_combobox.get()))

window = Tk()

window.title("DynamicCam Configurator")
window.geometry("400x820")
window.configure(bg = "#000000")


canvas = Canvas(
    window,
    bg = "#000000",
    height = 820,
    width = 400,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)

img_title = PhotoImage(file=assets("title.png"))
img_long = PhotoImage(file=assets("long_box.png"))
img_wind = PhotoImage(file=assets("wind_text.png"))
img_fullscr = PhotoImage(file=assets("fullscr_text.png"))
img_btn_off = PhotoImage(file=assets("btn_off.png"))
img_btn_on = PhotoImage(file=assets("btn_on.png"))
img_audio = PhotoImage(file=assets("audio_text.png"))
img_path = PhotoImage(file=assets("path_box.png"))
img_idle = PhotoImage(file=assets("idle_text.png"))
img_select = PhotoImage(file=assets("select_btn.png"))
img_cam = PhotoImage(file=assets("cam_text.png"))
img_screen = PhotoImage(file=assets("screen_text.png"))
img_mic = PhotoImage(file=assets("mic_text.png"))
img_apply = PhotoImage(file=assets("apply_btn.png"))
img_author = PhotoImage(file=assets("author.png"))

title = canvas.create_image(
    208.0,
    52.0,
    image=img_title
)

wind_bg = canvas.create_image(
    200.0,
    180.0,
    image=img_long
)
wind_entry = Entry(
    bd=0,
    bg="#3B3B3B",
    fg="#FFFFFF",
    highlightthickness=0
)
wind_entry.place(
    x=13.0,
    y=159.0,
    width=374.0,
    height=40.0
)

wind_text = canvas.create_image(
    99.0,
    144.0,
    image=img_wind
)

fullscr_text = canvas.create_image(
    135.0,
    246.0,
    image=img_fullscr
)

fullscr_btn_off = canvas.create_image(
    330.0,
    246.0,
    image=img_btn_off
)
canvas.tag_bind(fullscr_btn_off,'<Button-1>', fullscreen_off)

fullscr_btn_on = canvas.create_image(
    330.0,
    246.0,
    image=img_btn_on
)
canvas.tag_bind(fullscr_btn_on,'<Button-1>', fullscreen_on)

audio_text = canvas.create_image(
    99.0,
    296.0,
    image=img_audio
)

audio_btn_off = canvas.create_image(
    330.0,
    296.0,
    image=img_btn_off
)
canvas.tag_bind(audio_btn_off,'<Button-1>', audio_off)

audio_btn_on = canvas.create_image(
    330.0,
    296.0,
    image=img_btn_on
)
canvas.tag_bind(audio_btn_on,'<Button-1>', audio_on)

path_bg = canvas.create_image(
    147.5,
    382.0,
    image=img_path
)
path_entry = Entry(
    bd=0,
    bg="#3B3B3B",
    fg="#FFFFFF",
    highlightthickness=0
)
path_entry.place(
    x=13.0,
    y=361.0,
    width=269.0,
    height=40.0
)

idle_text = canvas.create_image(
    57.0,
    346.0,
    image=img_idle
)

select_btn = canvas.create_image(
    345.0,
    382.0,
    image=img_select
)
canvas.tag_bind(select_btn,'<Button-1>', select_idle)

cam_text = canvas.create_image(
    97.0,
    438.0,
    image=img_cam
)

cam_bg = canvas.create_image(
    200.0,
    474.0,
    image=img_long
)

camera_combobox = ttk.Combobox(window, values=cameras, font=("Arial", 12), state="readonly", width=40)
camera_combobox.place(x=11, y=462)

if Config.selected_camera() in cameras:
    camera_combobox.set(Config.selected_camera())
else:
    if cameras:
        camera_combobox.current(0)
        Config.change_selected_camera(str(camera_combobox.get()))

scr_text = canvas.create_image(
    93.0,
    523.0,
    image=img_screen
)

scr_bg = canvas.create_image(
    200.0,
    559.0,
    image=img_long
)

monitor_combobox = ttk.Combobox(window, values=monitors, font=("Arial", 12), state="readonly", width=40)
monitor_combobox.place(x=11, y=547)

if Config.selected_screen() in monitors:
    monitor_combobox.set(Config.selected_screen())
else:
    if monitors:
        monitor_combobox.current(0)
        Config.change_selected_screen(str(monitor_combobox.get()))

mic_text = canvas.create_image(
    123.0,
    608.0,
    image=img_mic
)

mic_bg = canvas.create_image(
    200.0,
    644.0,
    image=img_long
)

mic_combobox = ttk.Combobox(window, values=microphones, font=("Arial", 12), state="readonly", width=40, background="#3C3C3C")
mic_combobox.place(x=11, y=632)

if Config.selected_mic() in microphones:
    mic_combobox.set(Config.selected_mic())

apply = canvas.create_image(
    200.0,
    736.0,
    image=img_apply
)
canvas.tag_bind(apply,'<Button-1>', apply_clicked)

def author_url(event):
    webbrowser.open_new_tab("https://eldiablo123.pl")
author = canvas.create_image(
    204.0,
    798.0,
    image=img_author
)
canvas.tag_bind(author,'<Button-1>', author_url)

window.resizable(False, False)
window.after(0, start)
window.mainloop()