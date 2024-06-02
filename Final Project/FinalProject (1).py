from tkinter import *
from tkinter import filedialog
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from tkinter import messagebox

# Function to handle Edge Detection with Canny or DoG
def detect_edges(method):
    filename = filedialog.askopenfilename()
    if filename:
        image = cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2RGB)
        if method == "DoG":
            # Apply Difference of Gaussians (DoG)
            blurred = cv2.GaussianBlur(cv2.cvtColor(image, cv2.COLOR_RGB2GRAY), (5, 5), 0)
            edges = cv2.subtract(blurred, cv2.GaussianBlur(blurred, (9, 9), 0))
        
        # Display Edge Detection results
        plt.figure(figsize=(8, 4))
        plt.imshow(edges, cmap='gray')
        plt.axis('off')
        plt.title(f"{method} Edge Detection")
        plt.tight_layout()
        plt.show() 
        
# Function to handle file upload and stitching
def upload_file():
    filenames = filedialog.askopenfilenames()
    if len(filenames) != 2:
        messagebox.showinfo("Error", "Please select exactly two images.")
        return

    images = []
    for filename in filenames:
        image = cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2RGB)
        images.append(image)

    # Stitch images
    stitcher = cv2.Stitcher_create()
    status, stitched_image = stitcher.stitch(images)

    if status == cv2.Stitcher_OK:
        # Display images and stitched image using Matplotlib
        plt.figure(figsize=(15, 5))

        # Plot first original image
        plt.subplot(1, 3, 1)
        plt.imshow(images[0])
        plt.axis('off')
        plt.title("Original Image 1")

        # Plot second original image
        plt.subplot(1, 3, 2)
        plt.imshow(images[1])
        plt.axis('off')
        plt.title("Original Image 2")

        # Plot stitched image
        plt.subplot(1, 3, 3)
        plt.imshow(stitched_image)
        plt.axis('off')
        plt.title("Stitched Image")

        plt.tight_layout()

        plt.show()
    else:
        print("Error during stitching.")


def run_tester_file():
    import subprocess
    subprocess.Popen(["python", "tester.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


# Create the main window
myframe = Tk()
myframe.title("Computer Vision Project")
myframe.config(bg="lightblue")  # set the background color

# Get the screen width and height
screen_width = myframe.winfo_screenwidth()
screen_height = myframe.winfo_screenheight()

# Set the window geometry to cover the whole screen
myframe.geometry(f"{screen_width}x{screen_height}+0+0")

canvas = Canvas(myframe, width=1050, height=50, bg="white")
canvas.pack()

canvas.create_rectangle(0, 0, 1050, 50, fill="SlateGray")

# Create a list of buttons
buttons_frame = Frame(myframe, bg="lightblue")
buttons_frame.pack(pady=40)

button_texts = ["Stitching", "Edge Detection > DoG", "Edge Detection > Canny", "AI-based Human Edge Detection"]
buttons = []


for text in button_texts:
    button = Button(buttons_frame, text=text, width=20, height=2)  # Change the width here
    button.pack(side=TOP, pady=2)  # Pack buttons vertically with padding between them
    buttons.append(button)

buttons[0].config(command=upload_file)
buttons[1].config( command=lambda: detect_edges("DoG"))  # Associate the Edge Detection function with the button
buttons[2].config(command=run_tester_file) 

myframe.mainloop()
