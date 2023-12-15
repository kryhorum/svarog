import keyboard
from PIL import ImageGrab
import pytesseract
import tkinter as tk
import asyncio
import g4f
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
custom_config = r'--oem 3 --psm 6'

def take_screenshot_and_extract_text():
    try:
        # Capture the screenshot directly into memory
        screenshot = ImageGrab.grab()

        # Convert the screenshot to RGB mode for OCR compatibility
        screenshot = screenshot.convert('RGB')

        # Use pytesseract to perform OCR without saving the image
        text = pytesseract.image_to_string(screenshot)

        return text
    except Exception as e:
        print("Error:", e)


def copy_to_clipboard(text_to_copy):
    root.clipboard_clear()
    root.clipboard_append(text_to_copy)
    root.update()


def close_window():
    root.destroy()

def open_fullscreen_window(text):
    global root  # Make root a global variable
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.configure(bg='gray')

    frame = tk.Frame(root, bg='gray')
    frame.pack(expand=True)

    scrollable_text = tk.Text(frame, width=150, height=40, bg='#333333', fg='white', font=('Arial', 16, 'bold'))
    scrollable_text.pack(side='top', anchor='center')
    scrollable_text.insert('1.0', text)

    copy_button = tk.Button(frame, text='Copy to Clipboard', command=lambda: copy_to_clipboard(text), bg='green',
                            fg='white', font=('Arial', 16, 'bold'))
    copy_button.pack(side='top', anchor='nw')

    close_button = tk.Button(frame, text='Close                     ', command=close_window, bg='red', fg='white', font=('Arial', 16, 'bold'))
    close_button.pack(side='top', anchor='nw')

    root.mainloop()


async def process_with_gpt(salt):
    try:
        print(".")
        text = take_screenshot_and_extract_text()
        response = g4f.ChatCompletion.create(
            model="gpt-4-0613",
            provider=g4f.Provider.You,
            messages=[{"role": "user", "content": salt + text}],
        )
        open_fullscreen_window("\n\n\n"+response)
    except Exception as e:
        open_fullscreen_window("Expection")
        return "Expection"



print("CTRL + ALT + NUMPAD\n---------------------------\n1-EXAM QUESTION\n2-CODE IMPROVEMENT\n3-SUMARISE SCREENSHOT")
keyboard.add_hotkey('ctrl+alt+3', lambda: asyncio.run(process_with_gpt("This is all text from the screenshot. Summarize everything. Don not write anything unnecessary: ")))
keyboard.add_hotkey('ctrl+alt+1', lambda: asyncio.run(process_with_gpt("This is a text from the screenshot of a exam. There is also text from other stuff than the exam, ignore it. Provide only the correct answer, don not write anything unnecessary: ")))
keyboard.add_hotkey('ctrl+alt+2', lambda: asyncio.run(process_with_gpt("This is a text from the screenshot of a code. There is also text from other stuff than the code, ignore it. Reply with the improved version of the code: ")))

# Keep the script running
keyboard.wait('ctrl+alt+0')  # Press the 'esc' key to exit the script
