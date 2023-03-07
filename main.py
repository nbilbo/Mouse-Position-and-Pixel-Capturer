import queue
import threading
import tkinter as tk
import tkinter as ttk
import pyautogui
from pynput.mouse import Listener


def get_cord_and_pixel(x, y, button, pressed):
    """
    Check if mouse as pressed, if True will put the values in the queue.
    """
    if pressed:
        pixel = pyautogui.pixel(x, y)
        position = (x, y)
        the_queue.put((position, pixel))
        return False


def thread_target():
    """
    Start listening mouse click. Just stop if mouse has been clicked.
    """
    with Listener(on_click=get_cord_and_pixel) as listener:
        listener.join()


def callback():
    """
    This function will be called until queue.get() return some value.
    """
    # trying get queue value.
    try:
        position, pixel = the_queue.get(block=False)
        header.config(text='Get current mouse corder and pixel with this application')
        corder_label.config(text=f'Click Position:(X={position[0]}, Y={position[1]})')
        pixel_label.config(text=f'Pixel: {pixel}')
        start_button.config(state=tk.NORMAL)
    
    # queue is empty, lets just call the function again.
    except queue.Empty:
        root.after(100, callback)


def start_button_click():
    """
    Start thread and tkinter callback.
    """
    start_button.config(state=tk.DISABLED)
    header.config(text='Press mouse button to capture informations.')
    threading.Thread(target=thread_target).start()
    root.after(100, callback)

# we need queue to move stuff from threads to tkinter
the_queue = queue.Queue()

# root
root = tk.Tk()
root.title('Tkinter ft PyAutoGui')
root.geometry('700x500+0+0')
root.attributes("-topmost", True)


# widgets
header = tk.Label(root)
header.config(text='Get current mouse corder and pixel with this application')
header.config(font=('Arial', 14, 'bold'))
header.config(anchor=tk.CENTER)
header.pack(side=tk.TOP, fill=tk.X)

corder_label = ttk.Label(root)
corder_label.config(font=('Arial', 14, 'bold'))
corder_label.config(text='Corder')
corder_label.pack(side=tk.TOP, fill=tk.BOTH, expand=ttk.YES)

pixel_label = ttk.Label(root)
pixel_label.config(font=('Arial', 14, 'bold'))
pixel_label.config(text='Pixel')
pixel_label.pack(side=tk.TOP, fill=tk.BOTH, expand=ttk.YES)

start_button = ttk.Button(root)
start_button.config(font=('Arial', 14, 'bold'))
start_button.config(relief='raised', border=4)
start_button.config(text='Start')
start_button.config(command=start_button_click)
start_button.pack(side=tk.TOP, fill=tk.BOTH, expand=ttk.YES)

root.mainloop()

