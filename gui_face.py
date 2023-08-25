from tkinter import *
import os
from tkinter import ttk
import csv
from train_PCA_LDA import TrainPCAandLDA
from recog_PCA_LDA import RecogPCAandLDA
import pandas as pd
import datetime
import threading
import time

root = Tk(className='Facial Recognition attendance using Eigenfaces')
root.geometry('800x500')

idnumberstring = StringVar()  # Defining a string variable for the name
classroomstring = StringVar()  # Defining a string variable for the classroom

# Create the Treeview widget
tree = ttk.Treeview(root)
tree.pack(expand=True)
message = ""


# Function to load PCA and LDA recognition
# def recog_PCA_LDA_btn_load():
#     classroom = classroomstring.get()
#     os.system('python3 recog_PCA_LDA.py %s' % classroom)


# Function to capture individual's ID No.
def capture():
    try:
        id = idnumberstring.get()
        train = TrainPCAandLDA(id)
        train.capture_images()
        message_label.config(text=f"User with ID {id} has been added")
    except Exception as e:
        message_label.config(text=f"{e}")


# Function to train the PCA model

def train():
    t = threading.Thread(target=_train)
    t.start()


def _train():
    try:
        id = idnumberstring.get()
        train = TrainPCAandLDA(id)
        train.PCA_train_data()
        message_label.config(text=f"{train.message}")
        print(id)
    except Exception as e:
        message_label.config(text=f"{e}")



def recognise():
    try:
        department = classroomstring.get()
        if department == "":
            message_label.config(text="Department field is empty")
        else:
            recog = RecogPCAandLDA(department)
            recog.load_trained_PCA_LDA()
            recog.show_video()
            message_label.config(text="Attendance verified")
    except Exception as e:
        pass
        # message_label.config(text=f"{e}")
# Function to open the CSV file and read its contents


def open_csv_file():
    try:
        csv_filename = datetime.datetime.now().strftime("%Y-%m-%d") + ".csv"
        tree.delete(*tree.get_children())
        data = pd.read_csv(csv_filename)
        columns = data.columns.tolist()

        # Set the columns of the Treeview
        tree["columns"] = columns

        # Insert the header row as column headings
        for column in columns:
            tree.heading(column, text=column)
        style = ttk.Style()
        # Set background color for the entire Treeview
        style.configure(
            "Treeview",
            # bordercolor='orange',
            borderwidth=1,
            cellwidth=100,
            cellheight=30,
            # background="orange",
            foreground="black",
            font=("Helvetica", 12),
            fieldbackground="#E1E1E1"
            # padding=10,
        )

        style.map("Treeview",
                  bordercolor=[("selected", "#A9A9A9"),
                               ("!selected", "#E1E1E1"),
                               ("active", "#A9A9A9")])
        # Customize column headings font
        style.configure(
            "Treeview.Heading",
            background="#C0C0C0",
            foreground="black",
            font=("Arial", 12, "bold"),
            padding=5,
            borderwidth=1,
            relief="solid")

        # Insert the data rows into the Treeview
        for index, row in data.iterrows():
            tree.insert("", "end", values=row.tolist(), tags=('centered',))
        message_label.config(text="Attendance loaded")
    except Exception as e:
        message_label.config(text=f"{str(e)[10::]}")


# open_csv_file()

root_frame = Frame(root)
root_frame.pack()


text_frame = Frame(root_frame)
text_frame.pack(side=LEFT, anchor=NW, pady=10)

label_frame = Frame(root)
label_frame.pack(pady=30)


# Entry for individual's ID No.
id_label = Label(text_frame, text="ID Number:", font=('Helvetica', 14))
id_label.grid(row=0, column=0, padx=10, pady=5, sticky=E)
id_entry = Entry(text_frame, textvariable=idnumberstring,
                 width=25, font=('Helvetica', 14))
id_entry.grid(row=0, column=1, padx=10, pady=5)

# Entry for classroom

text_frame.grid_rowconfigure(1, minsize=45)

classroom_label = Label(text_frame, text="Department:", font=('Helvetica', 14))
classroom_label.grid(row=2, column=0, padx=10, pady=5, sticky=E)
classroom_entry = Entry(
    text_frame, textvariable=classroomstring, width=25, font=('Helvetica', 14))
classroom_entry.grid(row=2, column=1, padx=10, pady=5)

# Frame for buttons
button_frame = Frame(root_frame)
button_frame.pack(side=RIGHT, pady=5)

# Button to capture images
capture_btn = Button(button_frame, text="Add new user",
                     command=capture, bg="#4CAF50", fg="white", width=15, font=('Helvetica', 12), pady=5)
capture_btn.grid(row=0, column=0, padx=5, pady=5)

# Button to train the PCA model
train_btn = Button(button_frame, text="Train",
                   command=train, bg="#008CBA", fg="white", width=15, font=('Helvetica', 12), pady=5)
train_btn.grid(row=1, column=0, padx=5, pady=5)

# Button to verify attendance
recog_btn = Button(button_frame, text="Verify Attendance",
                   command=recognise, bg="#AA0F50", fg="white", width=15, font=('Helvetica', 12), pady=5)
recog_btn.grid(row=2, column=0, padx=5, pady=5)

load_attendance = Button(button_frame, text="Load Attendance",
                         command=open_csv_file, width=15, font=('Helvetica', 12), pady=5)
load_attendance.grid(row=3, column=0, padx=5, pady=5)

message_label = Label(
    label_frame, text=f"{message}", bg="#000000", fg="white", padx=10, pady=10, width=50, font=('Helvetica', 14, 'italic'))
message_label.grid(row=0, column=0, padx=10, pady=5, sticky=E)

root.mainloop()
