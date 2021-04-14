"""
Original code created by Reddit user saulmessedupman (https://www.reddit.com/user/saulmessedupman/)
https://www.reddit.com/r/learnpython/comments/9weko5/what_useless_projects_are_you_working_on/
https://pastebin.com/zSrYLWtf
"""

import time, pyautogui
from subprocess import Popen
from math import hypot
from keyboard import is_pressed
from PIL import Image
import PySimpleGUI as sg

sg.theme('Black')

layout = [
    [sg.Text("Image file")],
    [sg.Input(key='image_path'), sg.FileBrowse(file_types=(("Image Files", "*.jpg"), ("Image Files", "*.jpeg"), ("Image Files", "*.png"), ("Image Files", "*.bmp"), ))],
    [sg.Text('', size=(40, 1), key='image_path_text')],
    [sg.Column([
        [sg.Text("Compression")],
        [sg.Combo(["None", "Low", "Medium", "High", "Extreme"], default_value="Medium", key='compression_combo', readonly=True)]
    ]),
    sg.Column([
        [sg.Text("Brush type")],
        [sg.Combo(["Pixel", "Brush"], default_value="Pixel", key='brush_combo', readonly=True)]
    ]),
    sg.Column([
        [sg.Text("Background color")],
        [sg.Input("255, 255, 255", key='bg_color_input', size=(12, 1))]
    ])],
    [sg.Column([
        [sg.Checkbox("Linear motion", default=True, key='linear_checkbox')]
    ])],
    [sg.Button("Draw", key='draw_button')],
    [sg.Text('', size=(45, 1), key='color_progress_text')],
    [sg.ProgressBar(max_value=500, size=(45, 20), key='color_progress_bar')],
    [sg.Text('', size=(45, 1), key='pixel_progress_text')],
    [sg.ProgressBar(max_value=500, size=(45, 20), key='pixel_progress_bar')],
    [sg.Text('', size=(45, 1), key='color_pixel_progress_text')],
    [sg.ProgressBar(max_value=500, size=(45, 20), key='color_pixel_progress_bar')]
]

def ProcessImage(imagePath, compression = 'medium', linear = False, backgroundColor = (255, 255, 255)):
    image = RemoveAlpha(Image.open(imagePath), backgroundColor)
    pixelDictionary = {}
    for y in range(image.height):
        for x in range(image.width):
            rgb = image.getpixel((x, y))
            if rgb == backgroundColor:
                continue

            rgbRounded = CompressValue(rgb, compression)
            rgbRounded = NormalizeValues(rgbRounded)
            rgbList = list(map(str, rgbRounded))
            rgbKey = ':'.join(rgbList)
            if pixelDictionary.get(rgbKey) is None:
                pixelDictionary[rgbKey] = []

            pixelDictionary[rgbKey].append((x, y))

    if not linear:
        for key, value in pixelDictionary.items():
            pixelDictionary[key] = GroupPoints(value)

    return pixelDictionary

def ProcessImageLinear(imagePath, compression = 'medium'):
    image = Image.open(imagePath)
    pixelDictionary = {}
    for y in range(image.height):
        for x in range(image.width):
            rgb = image.getpixel((x, y))
            rgbRounded = CompressValue(rgb, compression)
            rgbRounded = NormalizeValues(rgbRounded)
            rgbList = list(map(str, rgbRounded))
            xyKey = f'{x}:{y}'
            rgbKey = ':'.join(rgbList)
            if pixelDictionary.get(xyKey) is None:
                pixelDictionary[xyKey] = rgbKey

    return pixelDictionary

def RemoveAlpha(image, backgroundColor = (255, 255, 255)):
    image = image.convert('RGBA')
    background = Image.new('RGBA', image.size, backgroundColor)
    return Image.alpha_composite(background, image).convert('RGB')

def NormalizeValues(numList):
    for index in range(len(numList)):
        if numList[index] > 255:
            numList[index] = 255

        elif numList[index] < 0:
            numList[index] = 0

    return numList

def CompressValue(rgb, compression):
    compressionValues = {
        'none': 1,
        'low': 2,
        'medium': 10,
        'high': 20,
        'extreme': 50
    }
    compressionNumber = compressionValues.get(compression, 2)
    if compression != 'none':
        rgb = list(map(lambda value: (value // compressionNumber * compressionNumber), rgb))

    return rgb

def GroupPoints(points):
    groups = []
    while points:
        farPoints = []
        ref = points.pop()
        groups.append([ref])
        for point in points:
            d = GetDisatance(ref, point)
            if d < 30:
                groups[-1].append(point)

            else:
                farPoints.append(point)

        points = farPoints

    return [item for sublist in groups for item in sublist]

def GetDisatance(ref, point):
    x1, y1 = ref
    x2, y2 = point
    return hypot(x2 - x1, y2 - y1)

def ColorComponent(colorValue, component):
    pyautogui.hotkey('altleft', component)
    pyautogui.typewrite(str(colorValue))

def SetColor(colorValues):
    for num in colorValues:
        assert 0 <= num <= 255, f"RGB values out of range: {num}"

    pyautogui.typewrite(['altleft', 'h', 'e', 'c', ], interval=0.1)
    ColorComponent(colorValues[0], 'r')
    ColorComponent(colorValues[1], 'g')
    ColorComponent(colorValues[2], 'u')
    pyautogui.press('enter')

def Draw(imagePath, compression, speed, brush = 'pixel', linear = False, backgroundColor = (255, 255, 255)):
    window['color_progress_text'].update("Processing image...", text_color='white')
    window.refresh()
    backgroundColor = tuple(map(int, backgroundColor.split(',')))
    pixelDictionary = ProcessImage(imagePath, compression, linear, backgroundColor)# if linear is False else ProcessImageLinear(imagePath, compression)
    Popen(['mspaint.exe'])
    time.sleep(2)
    pyautogui.keyDown('alt')
    pyautogui.press(' ')
    pyautogui.press('x')
    pyautogui.keyUp('alt')
    pyautogui.moveTo(30, 200)
    # manually determined with the menu turned off the start of the canvas is at 25, 83. otherwise use .position()
    #startX, startY = 25, 83
    startX, startY = pyautogui.position()
    time.sleep(2)
    SetColor(backgroundColor)
    pyautogui.typewrite(['alt', 'h', 'k'])
    pyautogui.click(startX, startY)
    if brush == 'brush':
        pyautogui.typewrite(['altleft', 'h', 'b', 'enter'], interval=0.1)

    else:
        pyautogui.typewrite(['altleft', 'h', 'p', '1'], interval=0.1)

    #if linear is False:
    Paint(pixelDictionary, speed, startX, startY)

    #elif linear is True:
    #    PaintLinear(pixelDictionary, speed, startX, startY)

def Paint(pixelDictionary, speed, startX, startY):
    cancelled = False
    paintedColors = 0
    paintedPixels = 0
    totalColors = len(pixelDictionary)
    totalPixels = sum(len(value) for value in pixelDictionary.values())
    for rgb in sorted(pixelDictionary.keys(), key=lambda z: len(pixelDictionary[z]), reverse=True):
        if cancelled:
            break

        colorList = list(map(int, rgb.split(':')))
        colorPixels = len(pixelDictionary.get(rgb))
        paintedColorPixels = 0
        ProgressUpdate(paintedColors, totalColors, 'color', "colors")
        ProgressUpdate(paintedPixels, totalPixels, 'pixel')
        ProgressUpdate(paintedColorPixels, colorPixels, 'color_pixel', "pixels in current color")
        pyautogui.PAUSE = speed + 0.1
        time.sleep(0.1)
        SetColor(colorList)
        pyautogui.PAUSE = speed
        for pixelX, pixelY in pixelDictionary.get(rgb):
            #if paintedPixels % 2000 == 0:
            #    time.sleep(2)
            #    pyautogui.typewrite(['alt', 'h', 'e', 'c', 'esc'])
            #    time.sleep(1)
                
            pyautogui.click(startX + pixelX, startY + pixelY)
            pyautogui.mouseUp()
            paintedPixels += 1
            paintedColorPixels += 1
            if paintedPixels % 1 == 0 or paintedColorPixels < 200:
                ProgressUpdate(paintedPixels, totalPixels, 'pixel')
                ProgressUpdate(paintedColorPixels, colorPixels, 'color_pixel', 'pixels in current color')

            if is_pressed('space') or is_pressed('esc'):
                cancelled = True
                raise pyautogui.FailSafeException

        paintedColors += 1

    ProgressUpdate(totalColors, totalColors)

def PaintLinear(pixelDictionary, speed, startX, startY):
    global prevColorList
    paintedPixels = 0
    totalPixels = len(pixelDictionary)
    cancelled = False
    for xy in pixelDictionary.keys():
        if cancelled:
            break
        
        ProgressUpdate(paintedPixels, totalPixels, 'pixel')
        rgb = pixelDictionary.get(xy)
        pixelX, pixelY = xy.split(':')
        pyautogui.PAUSE = speed + 0.1
        colorMap = map(int, rgb.split(':'))
        colorList = list(colorMap)
        if colorList != prevColorList:
            time.sleep(0.1)
            SetColor(colorList)

        pyautogui.PAUSE = speed
        pyautogui.click(startX + int(pixelX), startY + int(pixelY))
        prevColorList = colorList
        if is_pressed('space') or is_pressed('esc'):
            cancelled = True
            raise pyautogui.FailSafeException

        paintedPixels += 1

def ProgressUpdate(current, total, bar = 'color', text = "pixels"):
    percent = round(current / total * 100)
    window[f'{bar}_progress_text'].update(f"{current} out of {total} {text} painted. {percent}%", text_color='white')
    window[f'{bar}_progress_bar'].update(current, total)
    window.refresh()

pyautogui.PAUSE = 0
originalSpeed = pyautogui.PAUSE
startTime = time.time()
prevColorList = None
window = sg.Window("Picture Painter", layout)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    elif event == 'draw_button':
        try:
            if values['image_path'].split('.')[-1] not in ['jpg', 'jpeg', 'png', 'bmp']:
                window['image_path_text'].update("Invalid image file", text_color='red')

            else:
                Draw(values['image_path'], values['compression_combo'].lower(), originalSpeed, values['brush_combo'].lower(), values['linear_checkbox'], values['bg_color_input'])
                window['color_progress_text'].update(f"Elapsed time: {round(time.time() - startTime, 3)} seconds", text_color='white')
                pyautogui.alert(text="Picture painting completed", title="Finsished")

        except pyautogui.FailSafeException:
            pyautogui.mouseUp()
            window['color_progress_text'].update("Failsafe tripped. Operation stopped", text_color='red')
            pyautogui.alert(text="Failsafe tripped\nOperation stoped", title="E-STOP")

        except Exception as exception:
            window['color_progress_text'].update(f"Error: {exception}", text_color='red')

window.close()