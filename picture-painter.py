import time
import pyautogui
import PySimpleGUI as sg
from subprocess import Popen
from math import sqrt
from PIL import Image
from keyboard import is_pressed

RETRO_4 = [
    (0, 0, 0),
    (0, 0, 170),
    (0, 170, 0),
    (0, 170, 170),
    (170, 0, 0),
    (170, 0, 170),
    (170, 85, 0),
    (170, 170, 170),
    (85, 85, 85),
    (85, 85, 255),
    (85, 255, 85),
    (85, 255, 255),
    (255, 85, 85),
    (255, 85, 255),
    (255, 255, 85),
    (255, 255, 255)
]

RETRO_8 = [
    (0, 0, 0),
    (0, 0, 170),
    (0, 170, 0),
    (0, 170, 170),
    (170, 0, 0),
    (170, 0, 170),
    (170, 85, 0),
    (170, 170, 170),
    (85, 85, 85),
    (85, 85, 255),
    (85, 255, 85),
    (85, 255, 255),
    (255, 85, 85),
    (255, 85, 255),
    (255, 255, 85),
    (255, 255, 255),
    (0, 0, 0),
    (16, 16, 16),
    (32, 32, 32),
    (53, 53, 53),
    (69, 69, 69),
    (85, 85, 85),
    (101, 101, 101),
    (117, 117, 117),
    (138, 138, 138),
    (154, 154, 154),
    (170, 170, 170),
    (186, 186, 186),
    (202, 202, 202),
    (223, 223, 223),
    (239, 239, 239),
    (255, 255, 255),
    (0, 0, 255),
    (65, 0, 255),
    (130, 0, 255),
    (190, 0, 255),
    (255, 0, 255),
    (255, 0, 190),
    (255, 0, 130),
    (255, 0, 65),
    (255, 0, 0),
    (255, 65, 0),
    (255, 130, 0),
    (255, 190, 0),
    (255, 255, 0),
    (190, 255, 0),
    (130, 255, 0),
    (65, 255, 0),
    (0, 255, 0),
    (0, 255, 65),
    (0, 255, 130),
    (0, 255, 190),
    (0, 255, 255),
    (0, 190, 255),
    (0, 130, 255),
    (0, 65, 255),
    (130, 130, 255),
    (158, 130, 255),
    (190, 130, 255),
    (223, 130, 255),
    (255, 130, 255),
    (255, 130, 223),
    (255, 130, 190),
    (255, 130, 158),
    (255, 130, 130),
    (255, 158, 130),
    (255, 190, 130),
    (255, 223, 130),
    (255, 255, 130),
    (223, 255, 130),
    (190, 255, 130),
    (158, 255, 130),
    (130, 255, 130),
    (130, 255, 158),
    (130, 255, 190),
    (130, 255, 223),
    (130, 255, 255),
    (130, 223, 255),
    (130, 190, 255),
    (130, 158, 255),
    (186, 186, 255),
    (202, 186, 255),
    (223, 186, 255),
    (239, 186, 255),
    (255, 186, 255),
    (255, 186, 239),
    (255, 186, 223),
    (255, 186, 202),
    (255, 186, 186),
    (255, 202, 186),
    (255, 223, 186),
    (255, 239, 186),
    (255, 255, 186),
    (239, 255, 186),
    (223, 255, 186),
    (202, 255, 186),
    (186, 255, 186),
    (186, 255, 202),
    (186, 255, 223),
    (186, 255, 239),
    (186, 255, 255),
    (186, 239, 255),
    (186, 223, 255),
    (186, 202, 255),
    (0, 0, 113),
    (28, 0, 113),
    (57, 0, 113),
    (85, 0, 113),
    (113, 0, 113),
    (113, 0, 85),
    (113, 0, 57),
    (113, 0, 28),
    (113, 0, 0),
    (113, 28, 0),
    (155, 57, 0),
    (155, 85, 0),
    (155, 113, 0),
    (85, 113, 0),
    (57, 113, 0),
    (28, 113, 0),
    (0, 113, 0),
    (0, 113, 28),
    (0, 113, 57),
    (0, 113, 85),
    (0, 113, 113),
    (0, 85, 113),
    (0, 57, 113),
    (0, 28, 113),
    (57, 57, 113),
    (69, 57, 113),
    (85, 57, 113),
    (97, 57, 113),
    (113, 57, 113),
    (113, 57, 97),
    (113, 57, 85),
    (113, 57, 69),
    (113, 57, 57),
    (113, 69, 57),
    (113, 85, 57),
    (113, 97, 57),
    (113, 113, 57),
    (97, 113, 57),
    (85, 113, 57),
    (69, 113, 57),
    (57, 113, 57),
    (57, 113, 69),
    (57, 113, 85),
    (57, 113, 97),
    (57, 113, 113),
    (57, 97, 113),
    (57, 85, 113),
    (57, 69, 113),
    (81, 81, 113),
    (89, 81, 113),
    (97, 81, 113),
    (97, 81, 113),
    (105, 81, 113),
    (113, 81, 113),
    (113, 81, 105),
    (113, 81, 97),
    (113, 81, 89),
    (113, 81, 81),
    (113, 89, 81),
    (113, 97, 81),
    (113, 105, 81),
    (113, 113, 81),
    (105, 113, 81),
    (97, 113, 81),
    (89, 113, 81),
    (81, 113, 81),
    (81, 113, 89),
    (81, 113, 97),
    (81, 113, 105),
    (81, 113, 113),
    (81, 105, 113),
    (81, 97, 113),
    (81, 89, 113),
    (0, 0, 65),
    (16, 0, 65),
    (32, 0, 65),
    (49, 0, 65),
    (65, 0, 65),
    (65, 0, 49),
    (65, 0, 32),
    (65, 0, 16),
    (65, 0, 0),
    (65, 16, 0),
    (65, 32, 0),
    (65, 49, 0),
    (65, 65, 0),
    (49, 65, 0),
    (32, 65, 0),
    (16, 65, 0),
    (0, 65, 0),
    (0, 65, 16),
    (0, 65, 32),
    (0, 65, 49),
    (0, 65, 65),
    (0, 49, 65),
    (0, 32, 65),
    (0, 16, 65),
    (32, 32, 65),
    (40, 32, 65),
    (49, 32, 65),
    (57, 32, 65),
    (65, 32, 65),
    (65, 32, 57),
    (65, 32, 49),
    (65, 32, 40),
    (65, 32, 32),
    (65, 40, 32),
    (65, 49, 32),
    (65, 57, 32),
    (65, 65, 32),
    (57, 65, 32),
    (49, 65, 32),
    (40, 65, 32),
    (32, 65, 32),
    (32, 65, 40),
    (32, 65, 49),
    (32, 65, 57),
    (32, 65, 65),
    (32, 57, 65),
    (32, 49, 65),
    (32, 40, 65),
    (45, 45, 65),
    (49, 45, 65),
    (53, 45, 65),
    (61, 45, 65),
    (65, 45, 65),
    (65, 45, 61),
    (65, 45, 53),
    (65, 45, 49),
    (65, 45, 45),
    (65, 49, 45),
    (65, 53, 45),
    (65, 61, 45),
    (65, 65, 45),
    (61, 65, 45),
    (53, 65, 45),
    (49, 65, 45),
    (45, 65, 45),
    (45, 65, 49),
    (45, 65, 53),
    (45, 65, 61),
    (45, 65, 65),
    (45, 61, 65),
    (45, 53, 65),
    (45, 49, 65),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0)
]


sg.theme('Black')

layout = [
    [sg.Text("Image file")],
    [
        sg.Input(key='image_path', size=(60, 1)),
        sg.FileBrowse(file_types=(("Image Files", "*.jpg"), ("Image Files", "*.jpeg"), ("Image Files", "*.png"), ("Image Files", "*.bmp"), ("Image Files", "*.jfif")))
    ],
    [sg.Text('', size=(40, 1), key='image_path_text')],
    [
        sg.Column([
            [sg.Text("Compression")],
            [sg.Combo(["None", "Low", "Medium", "High", "Extreme", "Retro 4", "Retro 8"], default_value="Medium", key='compression_combo', readonly=True)]
        ]),
        sg.Column([
            [sg.Text("Brush type")],
            [sg.Combo(["Pixel", "Brush"], default_value="Pixel", key='brush_combo', readonly=True)]
        ]),
        sg.Column([
            [sg.Text("Background color")],
            [sg.Input('255, 255, 255', key='bg_color_input', size=(12, 1))]
        ])
    ],
    [sg.Text("Current mouse position: ", key='position_text', size=(40, 1))],
    [
        sg.Text("Starting position:\tX"),
        sg.Input('30', key='start_x', size=(10, 1), enable_events=True),
        sg.Text("Y"),
        sg.Input('200', key='start_y', size=(10, 1), enable_events=True)
    ],
    [
        sg.Text("Boundary limit:\tX"),
        sg.Input('1800', key='end_x', size=(10, 1), enable_events=True),
        sg.Text("Y"),
        sg.Input('900', key='end_y', size=(10, 1), enable_events=True)
    ],
    [
        sg.Checkbox("Pause every", key='pause_checkbox', enable_events=True),
        sg.Input('2000', key='pause_pixels', size=(10, 1), enable_events=True, disabled=True, disabled_readonly_background_color='black'),
        sg.Text("pixels for"),
        sg.Input('3', key='pause_time', size=(5, 1), enable_events=True, disabled=True, disabled_readonly_background_color='black'),
        sg.Text("seconds")
    ],
    [sg.Text("Progress update every"), sg.Input('1', key='progress_pixels', size=(10, 1), enable_events=True), sg.Text("pixels")],
    [sg.Button("Draw", key='draw_button')],
    [sg.Text('', size=(60, 1), key='elapsed_time_text')],
    [sg.Text('', size=(60, 1), key='time_remaining_text')],
    [sg.Text('', size=(60, 1), key='color_progress_text')],
    [sg.ProgressBar(max_value=500, size=(45, 20), key='color_progress_bar')],
    [sg.Text('', size=(60, 1), key='pixel_progress_text')],
    [sg.ProgressBar(max_value=500, size=(45, 20), key='pixel_progress_bar')],
    [sg.Text('', size=(60, 1), key='color_pixel_progress_text')],
    [sg.ProgressBar(max_value=500, size=(45, 20), key='color_pixel_progress_bar')]
]


def process_image(image_path: str, compression: str, background_color: tuple[int, int, int], max_size: tuple[int, int]) -> dict:
    image = remove_alpha(Image.open(image_path), background_color)
    width, height = image.size
    if width > max_size[0] or height > max_size[1]:
        image.thumbnail(max_size)
    pixel_dictionary = {}
    for y in range(image.height):
        for x in range(image.width):
            rgb = image.getpixel((x, y))
            rgb = compress_value(rgb, compression, background_color)
            rgb = normalize_values(rgb)
            if rgb == background_color:
                continue
            rgb_list = [str(value) for value in rgb]
            rgb_key = ':'.join(rgb_list)
            if pixel_dictionary.get(rgb_key) is None:
                pixel_dictionary[rgb_key] = []
            pixel_dictionary[rgb_key].append((x, y))
    return pixel_dictionary


def remove_alpha(image: Image.Image, background_color: tuple[int, int, int]) -> Image.Image:
    image = image.convert('RGBA')
    background = Image.new('RGBA', image.size, background_color)
    return Image.alpha_composite(background, image).convert('RGB')


def normalize_values(values: tuple[int, int, int]) -> tuple[int, int, int]:
    for index in range(len(values)):
        if values[index] > 255:
            values[index] = 255
        elif values[index] < 0:
            values[index] = 0
    return values


def closest_color(rgb: tuple[int, int, int], colors: list) -> tuple[int, int, int]:
    r, g, b = rgb
    color_diffs = []
    for color in colors:
        cr, cg, cb = color
        color_diff = sqrt(abs(r - cr)**2 + abs(g - cg)**2 + abs(b - cb)**2)
        color_diffs.append((color_diff, color))
    return min(color_diffs)[1]


def compress_value(rgb: tuple[int, int, int], compression: str, background_color: tuple[int, int, int]) -> tuple[int, int, int]:
    if rgb == background_color:
        return rgb
    compression_values = {
        'none': 1,
        'low': 2,
        'medium': 10,
        'high': 20,
        'extreme': 50,
        'retro 4': 0,
        'retro 8': 0
    }
    compression_number = compression_values.get(compression, 2)
    if compression == 'retro 4':
        rgb = closest_color(rgb, RETRO_4)
    elif compression == 'retro 8':
        rgb = closest_color(rgb, RETRO_8)
    elif compression != 'none':
        rgb = tuple((value // compression_number * compression_number) for value in rgb)
    return rgb


def set_color(rgb: tuple[int, int, int]):
    def color_component(value: int, component: str):
        pyautogui.hotkey('altleft', component)
        pyautogui.typewrite(str(value))
    for value in rgb:
        assert 0 <= value <= 255, f"RGB values out of range: {value}"
    pyautogui.typewrite(['altleft', 'h', 'e', 'c', ], interval=0.1)
    color_component(rgb[0], 'r')
    color_component(rgb[1], 'g')
    color_component(rgb[2], 'u')
    pyautogui.press('enter')


def paint(image_path: str, compression: str, speed: float, brush: str, background_color: str, start_x: int, start_y: int, end_x: int, end_y: int, pause: bool, pause_pixels: int, pause_time: float, progress_pixels: int):
    global start_time
    window['color_progress_text'].update("Processing image...", text_color='white')
    window.refresh()
    background_color = tuple(int(value) for value in background_color.split(','))
    pixel_dictionary = process_image(image_path, compression, background_color, (end_x, end_y))
    Popen(['mspaint.exe'])
    time.sleep(2)
    pyautogui.hotkey('win', 'up')
    pyautogui.moveTo(start_x, start_y)
    time.sleep(2)
    start_time = time.time()
    set_color(background_color)
    pyautogui.typewrite(['alt', 'h', 'k'])
    pyautogui.click(start_x, start_y)
    if brush == 'brush':
        pyautogui.typewrite(['altleft', 'h', 'b', 'enter'], interval=0.1)
    else:
        pyautogui.typewrite(['altleft', 'h', 'p', '1'], interval=0.1)
    cancelled = False
    painted_colors = 0
    painted_pixels = 0
    total_colors = len(pixel_dictionary)
    total_pixels = sum(len(value) for value in pixel_dictionary.values())
    for rgb in sorted(pixel_dictionary.keys(), key=lambda key: len(pixel_dictionary[key]), reverse=True):
        if cancelled:
            break
        color_list = [int(value) for value in rgb.split(':')]
        color_pixels = len(pixel_dictionary.get(rgb))
        painted_color_pixels = 0
        progress_update(painted_colors, total_colors, 'color', 'colors')
        progress_update(painted_pixels, total_pixels, 'pixel', 'pixels')
        progress_update(painted_color_pixels, color_pixels, 'color_pixel', 'pixels in current color')
        pyautogui.PAUSE = speed + 0.1
        time.sleep(0.1)
        set_color(color_list)
        pyautogui.PAUSE = speed
        for pixel_x, pixel_y in pixel_dictionary.get(rgb):
            if pause and painted_pixels % pause_pixels == 0:
                time.sleep(float(pause_time) - float(1))
                pyautogui.typewrite(['alt', 'h', 'e', 'c', 'esc'])
                time.sleep(1)
            pyautogui.click(start_x + pixel_x, start_y + pixel_y)
            pyautogui.mouseUp()
            painted_pixels += 1
            painted_color_pixels += 1
            if painted_pixels % progress_pixels == 0:
                progress_update(painted_pixels, total_pixels, 'pixel', 'pixels')
                progress_update(painted_color_pixels, color_pixels, 'color_pixel', 'pixels in current color')
                update_position('position_text')
                elapsed_time = round(time.time() - start_time)
                percent = ((painted_pixels / total_pixels) * 100) + 1
                percent_remaining = 100 - percent
                time_remaining = round(((elapsed_time / percent) * percent_remaining) + (float((total_colors - painted_colors)) * 1.4))
                window['elapsed_time_text'].update(f"Elapsed time: {elapsed_time // (60 * 60)}h {(elapsed_time % (60 * 60)) // 60}m {elapsed_time % 60}s", text_color='white')
                window['time_remaining_text'].update(f"Estimated time remaining: {time_remaining // (60 * 60)}h {(time_remaining % (60 * 60)) // 60}m {time_remaining % 60}s", text_color='white')
            if is_pressed('space') or is_pressed('esc'):
                cancelled = True
                raise pyautogui.FailSafeException
        painted_colors += 1
    progress_update(total_colors, total_colors, 'color', 'pixels')


def progress_update(current: int, total: int, bar: str, text: str):
    percent = round(current / total * 100)
    window[f'{bar}_progress_text'].update(f"{current} out of {total} {text} painted. {percent}%", text_color='white')
    window[f'{bar}_progress_bar'].update(current, total)
    window.refresh()


def update_position(key: str):
    current_position = pyautogui.position()
    window[key].update(f"Current mouse position: ({current_position.x}, {current_position.y})")


pyautogui.PAUSE = 0
original_speed = pyautogui.PAUSE
start_time = time.time()
window = sg.Window("Picture Painter", layout)
while True:
    event, values = window.read(50)
    update_position('position_text')
    if event == sg.WIN_CLOSED:
        break
    elif event in ['start_x', 'start_y', 'end_x', 'end_y', 'pause_pixels', 'progress_pixels'] and values[event] != '' and values[event][-1] not in '0123456789':
        window[event].update(values[event][:-1])
    elif event == 'pause_time' and values[event] != '' and values[event][-1] not in '0123456789.':
        window[event].update(values[event][:-1])
    elif event == 'draw_button':
        try:
            if values['image_path'] == '':
                window['image_path_text'].update("Choose an image", text_color='red')
                continue
            window['image_path_text'].update('', text_color='white')
            paint(
                values['image_path'],
                values['compression_combo'].lower(),
                original_speed,
                values['brush_combo'].lower(),
                values['bg_color_input'],
                int(values['start_x']),
                int(values['start_y']),
                int(values['end_x']),
                int(values['end_y']),
                values['pause_checkbox'],
                int(values['pause_pixels']),
                float(values['pause_time']),
                int(values['progress_pixels'])
            )
            window['time_remaining_text'].update("Estimated time remaining: 0h 0m 0s", text_color='white')
            pyautogui.alert(text="Picture painting completed", title="Finished")
        except pyautogui.FailSafeException:
            pyautogui.mouseUp()
            window['color_progress_text'].update("Failsafe tripped. Operation stopped.", text_color='red')
            pyautogui.alert(text="Failsafe tripped.\nOperation stopped.", title="Emergency Stop")
        except Exception as exception:
            window['color_progress_text'].update(f"Error: {exception}", text_color='red')
    elif event == 'pause_checkbox':
        if values['pause_checkbox']:
            window['pause_pixels'].update(disabled=False)
            window['pause_time'].update(disabled=False)
        else:
            window['pause_pixels'].update(disabled=True)
            window['pause_time'].update(disabled=True)
window.close()
