# importing necessary libraries
# import numpy as np
# import cv2
# import sys
# import os
# import csv
# import datetime

# RESIZE_FACTOR = 4


# class RecogPCAandLDA:
#     def __init__(self):
#         haarcascadePath = "haarcascade_frontalface_default.xml"
#         self.haarcascade = cv2.CascadeClassifier(haarcascadePath)
#         self.face_dir = 'face_data'
#         self.department = sys.argv[1]
#         self.modelLDA = cv2.face.FisherFaceRecognizer_create()
#         self.modelPCA = cv2.face.EigenFaceRecognizer_create()
#         self.face_names = []
#         self.conf_list = []
#         self.video_capture = cv2.VideoCapture(0)

#     # loading the trained algorithms
#     def load_trained_PCA_LDA(self):
#         names = {}
#         key = 0

#         # Reading the trained LDA and PDA data in the current directories
#         for (subdirs, dirs, files) in os.walk(self.face_dir):
#             for subdir in dirs:
#                 names[key] = subdir
#                 key += 1
#         self.names = names
#         self.modelLDA.read('LDA_data.xml')
#         self.modelPCA.read('PCA_data.xml')

#     # initialising the camera
#     def show_video(self):
#         # self.video_capture = cv2.VideoCapture(0)
#         while True:
#             ret, frame = self.video_capture.read()
#             inImg = np.array(frame)
#             outImg, self.face_names = self.process_images(inImg)
#             cv2.imshow('Video', outImg)

#             # When everything is finished, press 'q' to close computing the video
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 self.video_capture.release()
#                 cv2.destroyAllWindows()
#                 return

#     # function updating the database
#     def update_database(self, person):
#         print("known")
#         current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         data = [self.department, person, current_time]

#         with open('attendance.csv', 'a+') as attendance:
#             writer = csv.writer(attendance)
#             writer.writerow(data)
#         self.video_capture.release()
#         cv2.destroyAllWindows()

#     # function extracing the facial features and resizing the derived image

#     def process_images(self, inImg):
#         frame = cv2.flip(inImg, 1)
#         # Fixing the resolution of the face images
#         resized_width, resized_height = (92, 112)
#         # Changing the colours of the images into the grey scale
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         gray_resized = cv2.resize(gray, (int(
#             round(gray.shape[1]/RESIZE_FACTOR)), int(round(gray.shape[0]/RESIZE_FACTOR))))
#         faces = self.haarcascade.detectMultiScale(
#             gray_resized,
#             scaleFactor=1.1,
#             minNeighbors=5,
#             minSize=(30, 30),
#             flags=cv2.CASCADE_SCALE_IMAGE
#         )
#         people = []
#         for i in range(len(faces)):
#             face_i = faces[i]
#             x = face_i[0] * RESIZE_FACTOR
#             y = face_i[1] * RESIZE_FACTOR
#             w = face_i[2] * RESIZE_FACTOR
#             h = face_i[3] * RESIZE_FACTOR
#             face = gray[y:y+h, x:x+w]
#             face_resized = cv2.resize(face, (resized_width, resized_height))

#             # Assigning the similarity level (the lower the level is, the more similar the face picture is)
#             confidenceLDA = self.modelLDA.predict(face_resized)
#             confidencePCA = self.modelPCA.predict(face_resized)

#             # If the similarity level of LDA and PCA meet the treshold, show the appropriate recognition rate with the recognised person's ID
#             if confidenceLDA[1] < 300 and confidencePCA[1] < 3500:
#                 self.conf_list.append(confidencePCA[1])
#                 personLDA = self.names[confidenceLDA[0]]
#                 personPCA = self.names[confidencePCA[0]]
#                 cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
#                 cv2.putText(frame, 'LDA: ' + personLDA + ' - ' + str(
#                     round(confidenceLDA[1])), (x-10, y-25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
#                 cv2.putText(frame, 'PCA: ' + personPCA + ' - ' + str(
#                     round(confidencePCA[1])), (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
#             elif confidenceLDA[1] < 300:
#                 personLDA = self.names[confidenceLDA[0]]
#                 personPCA = 'Unknown'
#                 cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 3)
#                 cv2.putText(frame, 'LDA: ' + personLDA + ' - ' + str(
#                     round(confidenceLDA[1])), (x-10, y-25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
#                 cv2.putText(frame, 'PCA: ' + personPCA, (x-10, y-10),
#                             cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))
#                 self.conf_list.clear()
#             elif confidencePCA[1] < 3500:
#                 personLDA = 'Unknown'
#                 personPCA = self.names[confidencePCA[0]]
#                 cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 3)
#                 cv2.putText(frame, 'LDA: ' + personLDA, (x-10, y-25),
#                             cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))
#                 cv2.putText(frame, 'PCA: ' + personPCA + ' - ' + str(
#                     round(confidencePCA[1])), (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
#                 self.conf_list.clear()
#             else:
#                 personLDA = 'Unknown'
#                 personPCA = 'Unknown'
#                 cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 3)
#                 cv2.putText(frame, 'LDA: ' + personLDA, (x-10, y-25),
#                             cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))
#                 cv2.putText(frame, 'PCA: ' + personPCA, (x-10, y-10),
#                             cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))
#                 self.conf_list.clear()
#             people.append(personLDA)
#             people.append(personPCA)

#             if str(personLDA) != 'Unknown' and str(personPCA) != 'Unknown' and personLDA == personPCA:
#                 if len(self.conf_list) == 100:
#                     self.update_database(personPCA)
#                     self.conf_list.clear()
#             else:
#                 self.conf_list.clear()
#                 print('unknown')
#         return (frame, people)


# # callig the main function
# if __name__ == '__main__':
#     recogniserImage = RecogPCAandLDA()
#     recogniserImage.load_trained_PCA_LDA()
#     print("Press 'q' to quit")
#     recogniserImage.show_video()


# importing necessary libraries
import numpy as np
import cv2
import sys
import os
import csv
import datetime
import time
# import mysql.connector

RESIZE_FACTOR = 4


class RecogPCAandLDA:
    def __init__(self, department):
        haarcascadePath = "haarcascade_frontalface_default.xml"
        self.haarcascade = cv2.CascadeClassifier(haarcascadePath)
        self.face_dir = 'face_data'
        self.department = department
        self.modelLDA = cv2.face.FisherFaceRecognizer_create()
        self.modelPCA = cv2.face.EigenFaceRecognizer_create()
        self.face_names = []
        self.conf_list = []
        self.percent_count = 0
        self.video_capture = cv2.VideoCapture(0)
        self.message = ""
        self.count = 100
        self.person_id = ""

    # loading the trained algorithms
    def load_trained_PCA_LDA(self):
        names = {}
        key = 0

        # Reading the trained LDA and PDA data in the current directories
        for (subdirs, dirs, files) in os.walk(self.face_dir):
            for subdir in dirs:
                names[key] = subdir
                key += 1
        self.names = names
        self.modelLDA.read('LDA_data.xml')
        self.modelPCA.read('PCA_data.xml')

    # initialising the camera
    def show_video(self):
        # self.video_capture = cv2.VideoCapture(0)
        while True:
            ret, frame = self.video_capture.read()
            inImg = np.array(frame)
            outImg, self.face_names = self.process_images(inImg)
            cv2.imshow('Video', outImg)

            # When everything is finished, press 'q' to close computing the video
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.video_capture.release()
                cv2.destroyAllWindows()
                return

    # function updating the database
    def update_database(self, person):
        current_time = datetime.datetime.now().strftime("%H:%M")
        data = [self.department, person, current_time]

        csv_filename = datetime.datetime.now().strftime("%Y-%m-%d") + ".csv"

        if not os.path.isfile(csv_filename):
            with open(csv_filename, 'w') as attendance:
                writer = csv.writer(attendance)
                # Write the header row
                writer.writerow(["Department", "Person", "Time"])

        with open(csv_filename, 'a+') as attendance:
            writer = csv.writer(attendance)
            writer.writerow(data)

        self.video_capture.release()
        cv2.destroyAllWindows()
        self.message = f"Attendance verified for {person}"
        return

    # function extracing the facial features and resizing the derived image

    def process_images(self, inImg):
        frame = cv2.flip(inImg, 1)
        # Fixing the resolution of the face images
        resized_width, resized_height = (92, 112)
        # Changing the colours of the images into the grey scale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_resized = cv2.resize(gray, (int(
            round(gray.shape[1]/RESIZE_FACTOR)), int(round(gray.shape[0]/RESIZE_FACTOR))))
        faces = self.haarcascade.detectMultiScale(
            gray_resized,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        people = []

        for i in range(len(faces)):
            face_i = faces[i]
            x = face_i[0] * RESIZE_FACTOR
            y = face_i[1] * RESIZE_FACTOR
            w = face_i[2] * RESIZE_FACTOR
            h = face_i[3] * RESIZE_FACTOR
            face = gray[y:y+h, x:x+w]
            face_resized = cv2.resize(face, (resized_width, resized_height))

            # Assigning the similarity level (the lower the level is, the more similar the face picture is)
            confidencePCA = self.modelPCA.predict(face_resized)

            if confidencePCA[1] < 3500:
                self.conf_list.append(confidencePCA[1])
                personPCA = self.names[confidencePCA[0]]
                self.percent_count += 1
                self.percent_count = (self.percent_count/self.count)*100
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
                cv2.putText(frame, 'PCA: ' + personPCA + ' - ' + str(
                    round(self.percent_count)) + '%', (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
                # cv2.putText(frame, 'PCA: ' + personPCA + ' - ' + str(
                #     round(confidencePCA[1])), (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
            else:
                personPCA = 'Unknown'
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 3)
                cv2.putText(frame, 'PCA: ' + personPCA, (x-10, y-10),
                            cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))
                self.conf_list.clear()
                self.percent_count = 0
            # people.append(personLDA)
            people.append(personPCA)
            if str(personPCA) != 'Unknown':
                if len(self.conf_list) == self.count:
                    self.update_database(personPCA)
                    self.conf_list.clear()
                    return

            else:
                self.message = "Could not verify attendance"
                print('unknown')
        return (frame, people)


# # callig the main function
# if __name__ == '__main__':
#     recogniserImage = RecogPCAandLDA()
#     recogniserImage.load_trained_PCA_LDA()
#     print("Press 'q' to quit")
#     recogniserImage.show_video()
