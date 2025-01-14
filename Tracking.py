import os
from tkinter import filedialog
from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
import argparse
import imutils
import dlib
import cv2
from pynput.keyboard import Key, Controller
import time
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import shutil
keyboard = Controller()
def load_config(file_path):
    config = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.split('#', 1)[0].strip()
                config[key] = float(value)
        return config
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
    except ValueError as e:
        print(f"Error processing file: {e}")
        return {}
config_file = 'Config.txt'
config = load_config(config_file)
def mouth_aspect_ratio(mouth):
	A = dist.euclidean(mouth[2], mouth[10])
	B = dist.euclidean(mouth[4], mouth[8])
	C = dist.euclidean(mouth[0], mouth[6])
	mar = (A + B) / (2.0 * C)
	return mar
def eye_aspect_ratio(eye):
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])
	C = dist.euclidean(eye[0], eye[3])
	ear = (A + B) / (2.0 * C)
	return ear
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
	help="path to facial landmark predictor")
ap.add_argument("-v", "--video", type=str, default="",
	help="path to input video file")
args = vars(ap.parse_args())
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(mStart, mEnd) = (49, 68)
vs = VideoStream(src=0).start()
fileStream = False
time.sleep(1.0)
def button1_action():
	current_directory = os.getcwd()
	folder_name = 'Images'
	folder_path = os.path.join(current_directory, folder_name)
	if not os.path.exists(folder_path):
		response = messagebox.askyesno("Error", "Image directory does not exist, You may either continue without any model. Or go back and add some png's. Do you with to continue?")
		if response:
			RunProgram()
		else:
			pass
	else:
		RunProgram()
		DisplayWindow()
def submit2(entry, root1):
	global user_input
	user_input = entry.get()
	root1.destroy()
	submit()
def DisplayWindow():
	global user_input
	root1 = tk.Toplevel(root)
	root1.title("Png Size")
	label = tk.Label(root1, text="Enter Png Window size. EG: 100x300")
	label.pack(pady=10)
	entry = tk.Entry(root1, width=30)
	entry.pack(pady=5)
	submit_button = tk.Button(root1, text="Submit", command=lambda: submit2(entry, root1))
	submit_button.pack(pady=10)
	global ImageToLoad
	ImageToLoad = "Null"
def submit():
	global user_input
	pngwindow = tk.Toplevel(root)
	pngwindow.title("")
	pngwindow.overrideredirect(True)
	pngwindow.attributes("-topmost", True)
	transparent_color = "white"
	pngwindow.configure(bg=transparent_color)
	pngwindow.wm_attributes("-transparentcolor", transparent_color)
	window_width, window_height = map(int, user_input.split("x"))
	screen_width = pngwindow.winfo_screenwidth()
	screen_height = pngwindow.winfo_screenheight()
	x = screen_width - window_width
	y = screen_height - window_height
	pngwindow.geometry(f"{window_width}x{window_height}+{x}+{y}")
	try:
		pngwindow.geometry(user_input)
	except Exception as e:
		pngwindow.geometry("200x400")

	global Surprised 
	Surprised = False
	global Smiling
	Smiling = False
	global Open
	Open = False
	global Slightly_Open
	Slightly_Open = False
	global Default
	Default = False
	global Very_Open
	Very_Open = False
	global Very_Open_eyes
	Very_Open_eyes = False
	def check_for_changes():
		global Slightly_Open
		global ImageToLoad
		global Very_Open
		global Default
		global Open
		global Smiling
		global Surprised
		global image_copy
		global photo
		global label
		global Very_Open_eyes
		Surprised = False
		Slightly_Open = False
		Default = False
		Very_Open = False
		Smiling = False
		Open = False
		if Mouthstate == "Surprised":
			if Surprised == False:
				if os.path.exists(os.curdir  + "/Images/Surprised.png"):
					ImageToLoad = Image.open(os.curdir + "/Images/Surprised.png")
					Surprised = True
					Smiling = False
					Open = False
					Slightly_Open = False
					Default = False
					Very_Open = False
				else:
					pass
		elif Mouthstate == "Smiling":
			if Smiling == False:
				if os.path.exists(os.curdir + "/Images/Smiling.png"):
					ImageToLoad = Image.open(os.curdir + "/Images/Smiling.png")
					Smiling = True
					Surprised = False
					Open = False
					Slightly_Open = False
					Default = False
					Very_Open = False
				else:
					pass
		elif Mouthstate == "Open":
			if Open == False:
				if os.path.exists(os.curdir + "/Images/Open.png"):
					ImageToLoad = Image.open(os.curdir + "/Images/Open.png")
					Open = True
					Surprised = False
					Smiling = False
					Slightly_Open = False
					Default = False
					Very_Open = False
				else:
					pass
		elif Mouthstate == "Slightly-Open":
			if Slightly_Open == False:
				if os.path.exists(os.curdir + "/Images/Slightly-Open.png"):
					ImageToLoad = Image.open(os.curdir + "/Images/Slightly-Open.png")
					Slightly_Open = True
					Surprised = False
					Smiling = False
					Open = False
					Default = False
					Very_Open = False
				else:
					pass
		elif Mouthstate == "Very-Open":
			if Very_Open == False:
				if Eyestate == "Very-Open":
					if os.path.exists(os.curdir + "/Images/Surprised.png"):
						ImageToLoad = Image.open(os.curdir + "/Images/Surprised.png")
						Very_Open = True
						Surprised = False
						Smiling = False
						Open = False
						Slightly_Open = False
						Default = False
					else:
						pass
				elif os.path.exists(os.curdir + "/Images/Very-Open.png"):
					ImageToLoad = Image.open(os.curdir + "/Images/Very-Open.png")
					Very_Open = True
					Surprised = False
					Smiling = False
					Open = False
					Slightly_Open = False
					Default = False
				else:
					pass
		elif Eyestate == "Very-Open":
			if Very_Open_eyes == False:
				if os.path.exists(os.curdir + "/Images/Wide-Eyes.png"):
					ImageToLoad = Image.open(os.curdir + "/Images/Wide-Eyes.png")
					Very_Open_eyes = True
					Surprised = False
					Very_Open = False
					Smiling = False
					Open = False
					Slightly_Open = False
					Default = False
				else:
					pass
		else:
			if Default == False:
				if os.path.exists(os.curdir + "/Images/Default.png"):
					ImageToLoad = Image.open(os.curdir + "/Images/Default.png")
					Default = True
					Surprised = False
					Smiling = False
					Open = False
					Slightly_Open = False
					Very_Open = False
				else:
					pass

		image_copy = ImageToLoad.copy()
		photo = ImageTk.PhotoImage(image_copy)
		label.config(image=photo)
		label.image = photo  # Prevent garbage collection
		root.after(20, check_for_changes)
	global label
	ImageToLoad = Image.open(os.curdir + "/Images/Default.png") if os.path.exists(os.curdir + "/Images/Default.png") else None
	image_copy = ImageToLoad.copy() if ImageToLoad else None
	photo = ImageTk.PhotoImage(image_copy) if ImageToLoad else None
	label = tk.Label(pngwindow, image=photo)
	label.pack(fill=tk.BOTH, expand=True)
	def resize_image(event):
		global label
		new_width = event.width
		new_height = event.height
		resized_image = image_copy.resize((new_width, new_height), Image.Resampling.LANCZOS)
		new_photo = ImageTk.PhotoImage(resized_image)
		label.config(image=new_photo)
		label.image = new_photo
	pngwindow.bind("<Configure>", resize_image)

	check_for_changes()
def RunProgram():
	global neutral_mouth
	EYE_AR_THRESH = config.get('EYE_AR_THRESH', 0.25)
	EYE_AR_THRESH2 = config.get('EYE_AR_THRESH2', 0.35)
	MOUTH_AR_THRESH = config.get('MOUTH_AR_THRESH', 0.87)
	MOUTH_AR_THRESH2 = config.get('MOUTH_AR_THRESH2', 0.77)
	MOUTH_AR_THRESH3 = config.get('MOUTH_AR_THRESH3', 0.68)
	CheckMouthState = config.get('CheckMouthState', 0.1)
	CheckEyeState = config.get('CheckEyeState', 0.02)
	CheckEyeState2 = config.get('CheckEyeState2', 1)
	SMILE_THRESHOLD = config.get('SMILE_THRESHOLD', 1.11)
	EYE_AR_CONSEC_FRAMES = 4
	global Mouthstate
	Mouthstate = "Null"
	global Eyestate
	Eyestate = "Null"
	global COUNTER
	COUNTER = 0
	global TOTAL
	TOTAL = 0
	global last_mouth_check_time
	last_mouth_check_time = 0
	global last_eye_check_time
	last_eye_check_time = 0
	last_eye_check_time2 = 0
	global last_very_open_time
	last_very_open_time = 0
	global delay
	delay = 0.3
	global i
	i = 0
	def check_for_changes2():
		global Mouthstate
		global neutral_mouth
		global TOTAL
		global Eyestate
		global i
		global last_mouth_check_time
		global last_eye_check_time
		global COUNTER
		global delay
		global last_very_open_time
		frame = vs.read()
		frame = imutils.resize(frame, width=450)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		rects = detector(gray, 0)
		current_time = time.time()
		current_time2 = time.time()
		for rect in rects:
			shape = predictor(gray, rect)
			shape = face_utils.shape_to_np(shape)
			mouth = shape[mStart:mEnd]
			current_width = dist.euclidean(mouth[0], mouth[6])
			if i == 0:
				neutral_mouth = current_width
				i+=1
			for (x, y) in mouth:
				cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
			mouthMAR = mouth_aspect_ratio(mouth)
			mar = mouthMAR
			width_ratio = current_width / neutral_mouth
			mouthHull = cv2.convexHull(mouth)
			cv2.drawContours(frame, [mouthHull], -1, (0, 255, 0), 1)
			if current_time - last_mouth_check_time >CheckMouthState:
				if mar > MOUTH_AR_THRESH:
					Mouthstate = "Very-Open"
				elif mar > MOUTH_AR_THRESH2:
					Mouthstate = "Open"
				elif mar > MOUTH_AR_THRESH3:
					Mouthstate = "Slightly-Open"
				elif width_ratio > SMILE_THRESHOLD:
					Mouthstate = "Smiling"
				elif mar < MOUTH_AR_THRESH3:
					Mouthstate = "Closed"
				last_mouth_check_time = current_time
			if current_time - last_eye_check_time >CheckEyeState:
				leftEye = shape[lStart:lEnd]
				rightEye = shape[rStart:rEnd]
				leftEAR = eye_aspect_ratio(leftEye)
				rightEAR = eye_aspect_ratio(rightEye)
				ear = (leftEAR + rightEAR) / 2.0
				leftEyeHull = cv2.convexHull(leftEye)
				rightEyeHull = cv2.convexHull(rightEye)
				if ear < EYE_AR_THRESH:
					COUNTER += 1
				else:
					if COUNTER >= EYE_AR_CONSEC_FRAMES:
						TOTAL += 1
					COUNTER = 0
				last_eye_check_time = current_time
			if current_time - last_eye_check_time2 >CheckEyeState2:
				if ear > EYE_AR_THRESH2:
					cv2.putText(frame, "Eye's Very Open", (100,160),
						cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255),2)
					Eyestate = "Very-Open"
					last_very_open_time = current_time2
				else:
					if current_time2 - last_very_open_time >= delay:
						Eyestate = "Null"
			cv2.putText(frame, Mouthstate, (30,60),
				cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255),2)
			cv2.putText(frame, "Blinks: {}".format(TOTAL), (10, 30),
				cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
			cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
				cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
			cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
			cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			TOTAL=0
			cv2.destroyAllWindows()
			vs.stop()
		root.after(20, check_for_changes2)
	check_for_changes2()
def button2_action():
	current_directory = os.getcwd()
	folder_name = 'Images'
	folder_path = os.path.join(current_directory, folder_name)
	if not os.path.exists(folder_path):
		os.mkdir(folder_path)
		OpenEditWindow()
	else:
		OpenEditWindow()
class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
    def show_tooltip(self, event=None):
        if self.tooltip_window is not None:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, background="yellow", relief="solid", borderwidth=1, font=("Arial", 10))
        label.pack()
    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None
global Filename
Filename = "Null"
def open_and_rename_image():
    file_path = filedialog.askopenfilename(
        title="Select an Image File",
        filetypes=[("Image Files", "*.png")]
    )
    if not file_path:
        return
    current_directory = os.getcwd()
    images_directory = os.path.join(current_directory, "Images")
    os.makedirs(images_directory, exist_ok=True)
    new_file_name = Filename + os.path.splitext(file_path)[1]
    new_file_path = os.path.join(images_directory, new_file_name)
    try:
        shutil.copy(file_path, new_file_path)
    except Exception as e:pass
def btn1_action():
	global Filename
	Filename = "Default"
	open_and_rename_image()
def btn2_action():
	global Filename
	Filename = "Slightly-Open"
	open_and_rename_image()
def btn3_action():
	global Filename
	Filename = "Open"
	open_and_rename_image()
def btn4_action():
	global Filename
	Filename = "Very-Open"
	open_and_rename_image()
def btn5_action():
	global Filename
	Filename = "Wide-Eyes"
	open_and_rename_image()
def btn6_action():
	global Filename
	Filename = "Surprised"
	open_and_rename_image()
def btn7_action():
	global Filename
	Filename = "Smiling"
	open_and_rename_image()
def OpenEditWindow():
	pngeditwindow = tk.Toplevel(root)
	pngeditwindow.title("choose files")
	pngeditwindow.geometry("300x200")
	canvas = tk.Canvas(pngeditwindow)
	scrollbar = ttk.Scrollbar(pngeditwindow, orient="vertical", command=canvas.yview)
	scrollable_frame = ttk.Frame(canvas)
	canvas.configure(yscrollcommand=scrollbar.set)
	scrollbar.pack(side="right", fill="y")
	canvas.pack(side="left", fill="both", expand=True)
	scrollable_frame_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
	def update_scrollregion(event):
		canvas.configure(scrollregion=canvas.bbox("all"))
	scrollable_frame.bind("<Configure>", update_scrollregion)
	button1 = tk.Button(scrollable_frame, text="Default Png", command=btn1_action)
	button1.pack(pady=5)
	Tooltip(button1, "If your mouth is closed, Eye's are normal, And nothing is odd. This is the png that will be shown. You may skip this if you don't have a default png")
	button2 = tk.Button(scrollable_frame, text="Mouth Slightly open Png", command=btn2_action)
	button2.pack(pady=5)
	Tooltip(button2, "If your mouth is slightly open, This is the png that will be shown. You may skip this if you don't have a mouth slightly open png (if you have it to put a normal talking/mouth open one here if you don't have 1 for each)")
	button3 = tk.Button(scrollable_frame, text="Mouth open Png", command=btn3_action)
	button3.pack(pady=5)
	Tooltip(button3, "If your mouth is normally open, This is the png that will be shown. You may skip this if you don't have a seperate mouth open to put here")
	button4 = tk.Button(scrollable_frame, text="Mouth Very open Png", command=btn4_action)
	button4.pack(pady=5)
	Tooltip(button4, "If your mouth is very open, This is the png that will be shown. You may skip this if you don't have a mouth very open png(if you have one a yawning png might fit good here)")
	button5 = tk.Button(scrollable_frame, text="Wide Eye's Png", command=btn5_action)
	button5.pack(pady=5)
	Tooltip(button5, "If your eye's are wide, And mouth is anything but very open, This is the png that will be shown. You may skip this if you don't have a Eye's wide png")
	button6 = tk.Button(scrollable_frame, text="Surprised Png", command=btn6_action)
	button6.pack(pady=5)
	Tooltip(button6, "If your mouth is very open, And eye's are very wide, This is the png that will be shown. You may skip this if you don't have a Surprised png")
	button7 = tk.Button(scrollable_frame, text="Smiling Png", command=btn7_action)
	button7.pack(pady=5)
	Tooltip(button7, "If you're is Smiling, This is the png that will be shown. You may skip this if you don't have a smiling png")
def button3_action():
	root.destroy()
	exit()
	cv2.destroyAllWindows()
	vs.stop()
root = tk.Tk()
root.title("Select one")
root.geometry("300x200") 
button1 = tk.Button(root, text="Load Tracker Program", command=button1_action)
button1.pack(pady=10)
button2 = tk.Button(root, text="Add New Png's", command=button2_action)
button2.pack(pady=10)
button3 = tk.Button(root, text="Exit", command=button3_action)
button3.pack(pady=10)
root.mainloop()