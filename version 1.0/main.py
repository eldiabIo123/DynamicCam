import os
import cv2
import json
import pygame
import pyaudio
import pystray
import PIL.Image
import threading
import numpy as np
from screeninfo import get_monitors

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
    def sensitivity():
        with open(config_path, 'r') as file:
            data = json.load(file)
        return int(data['sensitivity'])
    def FPS():
        with open(config_path, 'r') as file:
            data = json.load(file)
        return int(data['FPS'])
    def ratio1():
        with open(config_path, 'r') as file:
            data = json.load(file)
        return int(data['ratio1'])
    def ratio2():
        with open(config_path, 'r') as file:
            data = json.load(file)
        return int(data['ratio2'])
    def cam_w():
        with open(config_path, 'r') as file:
            data = json.load(file)
        return int(data['cam_w'])
    def cam_h():
        with open(config_path, 'r') as file:
            data = json.load(file)
        return int(data['cam_h'])
    def audio_rate():
        with open(config_path, 'r') as file:
            data = json.load(file)
        return int(data['audio_rate'])
    def audio_buffer():
        with open(config_path, 'r') as file:
            data = json.load(file)
        return int(data['audio_buffer'])
    
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

running = True
preview = False
man_preview = False

def stray_clicked(stray, item):
    global running, man_preview
    if str(item) == "Manual preview":
        if man_preview:
            man_preview = False
            print("Manual preview off")
        else:
            man_preview = True
            print("Manual preview on")
    elif str(item) == "Turn off":
        running = False
        print("Goodbye ;c")

stray = pystray.Icon(name=str(Config.window_name()), icon=PIL.Image.open(assets("icon.png")), menu=pystray.Menu(
    pystray.MenuItem(text="Manual preview", action=stray_clicked),
    pystray.MenuItem(text="Turn off", action=stray_clicked)
))

def get_microphone_index(selected_mic=None):
    if not selected_mic:
        selected_mic = ""

    pa = pyaudio.PyAudio()
    mic_index = None
    for i in range(pa.get_device_count()):
        device_info = pa.get_device_info_by_index(i)
        print(f"Sprawdzam urządzenie: {device_info['name']}")
        if selected_mic == device_info['name']:
            mic_index = i
            break
    pa.terminate()
    return mic_index

camera_index = ""

if Config.selected_camera() and "Camera" in Config.selected_camera():
    try:
        camera_index = int(Config.selected_camera().split()[-1])
    except ValueError:
        print("Niepoprawny format kamery w pliku JSON.")
        camera_index = None
else:
    print("Nie ustawiono kamery w pliku JSON.")
    camera_index = None

idle_image_path = Config.idle_file()
if idle_image_path is None or not os.path.exists(idle_image_path):
    print("Idle image not set or file does not exist. Exiting.")
idle_image = cv2.imread(idle_image_path, cv2.IMREAD_GRAYSCALE)

cap = cv2.VideoCapture(camera_index)
if not cap.isOpened():
    print("Error: Unable to access the camera.")

def stray_loop():
    stray.run()

cap_lock = threading.Lock()

def main_loop():
    global preview
    while running:
        with cap_lock:
            ret, frame = cap.read()
        if not ret:
            print("Error reading frame from camera.")
            continue
        
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        small_frame = cv2.resize(gray_frame, (640, 360))
        resized_idle_image = cv2.resize(idle_image, (small_frame.shape[1], small_frame.shape[0]))
        diff = cv2.absdiff(resized_idle_image, small_frame)
        _, thresh = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)
        non_zero_count = cv2.countNonZero(thresh)
        print(f"Non-zero pixels: {non_zero_count}")
        
        if int(non_zero_count) > int(Config.sensitivity()):
            if not preview:
                preview = True
        else:
            if preview:
                preview = False
    stray.stop()

def preview_loop():
    global preview, man_preview
    is_window = False
    while running:
        if preview or man_preview:
            if not is_window:
                pygame.init()
                is_window = True
                window_size = (1280, 720)
                borderless = Config.fullscreen()
                if borderless:
                    window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    window = pygame.display.set_mode(window_size, pygame.RESIZABLE)
                pygame.display.set_caption(Config.window_name())
                clock = pygame.time.Clock()
                target_aspect_ratio = int(Config.ratio1()) / int(Config.ratio2())
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        borderless = not borderless
                        if borderless:
                            window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        else:
                            window = pygame.display.set_mode(window_size, pygame.RESIZABLE)
                elif event.type == pygame.QUIT:
                    pass

            with cap_lock:
                ret, frame = cap.read()
            if not ret:
                print("Error reading frame from camera.")
                break
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            window_width, window_height = window.get_size()
            window_aspect_ratio = window_width / window_height

            if window_aspect_ratio > target_aspect_ratio:
                scaled_height = window_height
                scaled_width = int(scaled_height * target_aspect_ratio)
            else:
                scaled_width = window_width
                scaled_height = int(scaled_width / target_aspect_ratio)

            frame = cv2.resize(frame, (scaled_width, scaled_height))
            surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

            window.fill((0, 0, 0))
            x_offset = (window_width - scaled_width) // 2
            y_offset = (window_height - scaled_height) // 2
            window.blit(surface, (x_offset, y_offset))

            pygame.display.update()
            clock.tick(Config.FPS())
        else:
            if is_window:
                pygame.quit()
                is_window = False
    pygame.quit()

def audio_loop():
    first = False
    stream = None
    pa = None

    try:
        while running:
            if Config.audio():
                if preview or man_preview:
                    if not first:
                        first = True
                        mic_index = get_microphone_index(Config.selected_mic())
                        if mic_index is None:
                            print(f"Nie znaleziono mikrofonu o nazwie: {Config.selected_mic()}")
                            continue
                        pa = pyaudio.PyAudio()
                        stream = pa.open(format=pyaudio.paInt16,
                                         channels=1,
                                         rate=Config.audio_rate(),
                                         input=True,
                                         output=True,
                                         frames_per_buffer=Config.audio_buffer(),
                                         input_device_index=mic_index)
                    data = stream.read(Config.audio_buffer(), exception_on_overflow=False)
                    stream.write(data, Config.audio_buffer())
                else:
                    if first:
                        first = False
                        if stream:
                            stream.stop_stream()
                            stream.close()
                            stream = None
                        if pa:
                            pa.terminate()
                            pa = None
            else:
                first = False
    except Exception as e:
        print(f"Error in audio_loop: {e}")
    finally:
        if stream:
            stream.stop_stream()
            stream.close()
        if pa:
            pa.terminate()


Config.create_config()
thread_stray = threading.Thread(target=stray_loop)
thread_main = threading.Thread(target=main_loop)
thread_preview = threading.Thread(target=preview_loop)
thread_audio = threading.Thread(target=audio_loop)

thread_stray.start()
stray.stop()
thread_main.start()
thread_preview.start()
thread_audio.start()

thread_stray.join()
thread_main.join()
thread_preview.join()
thread_audio.join()

stray.stop()