"""
Original idea and code created by Reddit user "saulmessedupman" (https://www.reddit.com/user/saulmessedupman/)
Reddit post: https://www.reddit.com/r/learnpython/comments/9weko5/what_useless_projects_are_you_working_on/
Original code pastebin: https://pastebin.com/zSrYLWtf
"""

import time
import pyautogui
import PySimpleGUI as sg
from subprocess import Popen
from PIL import Image
from keyboard import is_pressed
from math import sqrt

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


def ProcessImage(imagePath: str, compression: str, backgroundColor: tuple, maxSize: tuple[int]) -> dict:
    image = RemoveAlpha(Image.open(imagePath), backgroundColor)
    width, height = image.size
    if width > maxSize[0] or height > maxSize[1]:
        image.thumbnail(maxSize)

    pixelDictionary = {}
    for y in range(image.height):
        for x in range(image.width):
            rgb = image.getpixel((x, y))
            rgb = CompressValue(rgb, compression)
            rgb = NormalizeValues(rgb)
            if rgb == backgroundColor:
                continue

            rgbList = [str(value) for value in rgb]
            rgbKey = ':'.join(rgbList)
            if pixelDictionary.get(rgbKey) is None:
                pixelDictionary[rgbKey] = []

            pixelDictionary[rgbKey].append((x, y))

    return pixelDictionary


def RemoveAlpha(image: Image.Image, backgroundColor: tuple) -> Image.Image:
    image = image.convert('RGBA')
    background = Image.new('RGBA', image.size, backgroundColor)
    return Image.alpha_composite(background, image).convert('RGB')


def NormalizeValues(values: list) -> list:
    for index in range(len(values)):
        if values[index] > 255:
            values[index] = 255

        elif values[index] < 0:
            values[index] = 0

    return values


def ClosestColor(rgb: tuple, colors: list) -> tuple:
    r, g, b = rgb
    colorDiffs = []
    for color in colors:
        cr, cg, cb = color
        colorDiff = sqrt(abs(r - cr)**2 + abs(g - cg)**2 + abs(b - cb)**2)
        colorDiffs.append((colorDiff, color))

    return min(colorDiffs)[1]


def CompressValue(rgb: tuple, compression: str) -> tuple:
    compressionValues = {
        'none': 1,
        'low': 2,
        'medium': 10,
        'high': 20,
        'extreme': 50,
        'retro 4': 0,
        'retro 8': 0
    }
    compressionNumber = compressionValues.get(compression, 2)
    if compression == 'retro 4':
        rgb = ClosestColor(rgb, RETRO_4)

    elif compression == 'retro 8':
        rgb = ClosestColor(rgb, RETRO_8)

    elif compression != 'none':
        rgb = tuple((value // compressionNumber * compressionNumber) for value in rgb)

    return rgb


def ColorComponent(colorValue: int, component: str):
    pyautogui.hotkey('altleft', component)
    pyautogui.typewrite(str(colorValue))


def SetColor(colorValues):
    for value in colorValues:
        assert 0 <= value <= 255, f"RGB values out of range: {value}"

    pyautogui.typewrite(['altleft', 'h', 'e', 'c', ], interval=0.1)
    ColorComponent(colorValues[0], 'r')
    ColorComponent(colorValues[1], 'g')
    ColorComponent(colorValues[2], 'u')
    pyautogui.press('enter')


def Paint(imagePath: str, compression: str, speed: float, brush: str, backgroundColor: str, startX: int, startY: int, endX: int, endY: int, pause: bool, pausePixels: int, pauseTime: float, progressPixels: int):
    global startTime
    window['color_progress_text'].update("Processing image...", text_color='white')
    window.refresh()
    backgroundColor = tuple(int(value) for value in backgroundColor.split(','))
    pixelDictionary = ProcessImage(imagePath, compression, backgroundColor, (endX, endY))
    Popen(['mspaint.exe'])
    time.sleep(2)
    pyautogui.keyDown('alt')
    pyautogui.press(' ')
    pyautogui.press('x')
    pyautogui.keyUp('alt')
    pyautogui.moveTo(startX, startY)
    time.sleep(2)
    startTime = time.time()
    SetColor(backgroundColor)
    pyautogui.typewrite(['alt', 'h', 'k'])
    pyautogui.click(startX, startY)
    if brush == 'brush':
        pyautogui.typewrite(['altleft', 'h', 'b', 'enter'], interval=0.1)

    else:
        pyautogui.typewrite(['altleft', 'h', 'p', '1'], interval=0.1)

    cancelled = False
    paintedColors = 0
    paintedPixels = 0
    totalColors = len(pixelDictionary)
    totalPixels = sum(len(value) for value in pixelDictionary.values())
    for rgb in sorted(pixelDictionary.keys(), key=lambda z: len(pixelDictionary[z]), reverse=True):
        if cancelled:
            break

        colorList = [int(value) for value in rgb.split(':')]
        colorPixels = len(pixelDictionary.get(rgb))
        paintedColorPixels = 0
        ProgressUpdate(paintedColors, totalColors, 'color', 'colors')
        ProgressUpdate(paintedPixels, totalPixels, 'pixel', 'pixels')
        ProgressUpdate(paintedColorPixels, colorPixels, 'color_pixel', 'pixels in current color')
        pyautogui.PAUSE = speed + 0.1
        time.sleep(0.1)
        SetColor(colorList)
        pyautogui.PAUSE = speed
        for pixelX, pixelY in pixelDictionary.get(rgb):
            if pause and paintedPixels % pausePixels == 0:
                time.sleep(float(pauseTime) - float(1))
                pyautogui.typewrite(['alt', 'h', 'e', 'c', 'esc'])
                time.sleep(1)

            pyautogui.click(startX + pixelX, startY + pixelY)
            pyautogui.mouseUp()
            paintedPixels += 1
            paintedColorPixels += 1
            if paintedPixels % progressPixels == 0:
                ProgressUpdate(paintedPixels, totalPixels, 'pixel', 'pixels')
                ProgressUpdate(paintedColorPixels, colorPixels, 'color_pixel', 'pixels in current color')
                UpdatePosition('position_text')
                elapsedTime = round(time.time() - startTime)
                percent = ((paintedPixels / totalPixels) * 100) + 1
                percentLeft = 100 - percent
                timeLeft = round(((elapsedTime / percent) * percentLeft) + (float((totalColors - paintedColors)) * 1.4))
                window['elapsed_time_text'].update(f"Elapsed time: {elapsedTime // (60 * 60)}h {(elapsedTime % (60 * 60)) // 60}m {elapsedTime % 60}s", text_color='white')
                window['time_remaining_text'].update(f"Estimated time remaining: {timeLeft // (60 * 60)}h {(timeLeft % (60 * 60)) // 60}m {timeLeft % 60}s", text_color='white')

            if is_pressed('space') or is_pressed('esc'):
                cancelled = True
                raise pyautogui.FailSafeException

        paintedColors += 1

    ProgressUpdate(totalColors, totalColors, 'color', 'pixels')


def ProgressUpdate(current: int, total: int, bar: str, text: str):
    percent = round(current / total * 100)
    window[f'{bar}_progress_text'].update(f"{current} out of {total} {text} painted. {percent}%", text_color='white')
    window[f'{bar}_progress_bar'].update(current, total)
    window.refresh()


def UpdatePosition(key: str):
    currentPosition = pyautogui.position()
    window[key].update(f"Current mouse position: ({currentPosition.x}, {currentPosition.y})")


pyautogui.PAUSE = 0
originalSpeed = pyautogui.PAUSE
startTime = time.time()
window = sg.Window("Picture Painter", layout)
while True:
    event, values = window.read(50)
    UpdatePosition('position_text')
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
            Paint(
                values['image_path'],
                values['compression_combo'].lower(),
                originalSpeed,
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
