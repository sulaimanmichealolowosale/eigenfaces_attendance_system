from kivy.lang import Builder
from kivymd.uix.widget import MDWidget
from kivymd.uix.boxlayout import MDBoxLayout
from train_PCA_LDA import TrainPCAandLDA
from recog_PCA_LDA import RecogPCAandLDA
from kivy.properties import StringProperty, BooleanProperty
import threading


Builder.load_string('''

<LeftScreen>:
    orientation: 'vertical'
    padding: ('20dp', '20dp', '20dp', '20dp')
    spacing: '30dp'
    md_bg_color:[0,0,0,.8]
    # size_hint_y: None
    # height:self.minimum_height
    
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: [1,1,1,.5]
        size_hint: 1, None
        padding: ('20dp', '35dp', '20dp', '20dp')
        height:self.minimum_height
        radius:[10]
        spacing: '30dp'
        MDLabel:
            text: "Capturing"
            halign:"center"
            font_style:"H4"
            theme_text_color:"Custom"
            text_color:"black"

        MDBoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height:self.minimum_height
            spacing: '20dp'
            padding: ('20dp', '20dp', '20dp', '20dp')
            MDTextField:
                hint_text: "User ID"
                id:user_id
                required: True
                mode: "round"
                helper_text_mode: "persistent"
                helper_text_color_normal:"black"
                helper_text: "Enter the user ID"
            MDRectangleFlatIconButton:
                icon: "camera-account"
                text: "C A P T U R E"
                theme_text_color: "Custom"
                text_color: "black"
                line_color: "black"
                theme_icon_color: "Custom"
                icon_color: "black"
                on_release:root.capture()
                    
    MDRectangleFlatIconButton:
        icon:"mixed-martial-arts"
        text:"T R A I N   M O D E L "
        theme_text_color: "Custom"
        text_color: "white"
        line_color: "white"
        theme_icon_color: "Custom"
        icon_color: "white"
        font_size: dp(20)
        # size_hint_x: 1
        on_release:root.train()

    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: [1,1,1,.5]
        size_hint: 1, None
        padding: ('20dp', '35dp', '20dp', '20dp')
        height:self.minimum_height
        radius:[10]
        spacing: '30dp'
        MDLabel:
            text: "Recognition"
            halign:"center"
            font_style:"H4"
            theme_text_color:"Custom"
            text_color:"black"

        MDBoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height:self.minimum_height
            spacing: '20dp'
            padding: ('20dp', '20dp', '20dp', '20dp')
            MDTextField:
                id:department
                hint_text: "Department"
                required: True
                mode: "round"
                helper_text_mode: "persistent"
                helper_text_color_normal:"black"
                helper_text: "Enter the department"
            MDRectangleFlatIconButton:
                icon: "face-recognition"
                text: "R E C O G N I S E"
                theme_text_color: "Custom"
                text_color: "black"
                line_color: "black"
                theme_icon_color: "Custom"
                icon_color: "black"
                on_release:root.recog()
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: [1,1,1,.5]
        padding: ('10dp', '10dp', '10dp', '10dp')
        radius:[10]
        size_hint_y: None
        height: dp(200)
        # spacing: '20dp'
        MDLabel:
            text: "Message"
            font_style:"H4"
            halign:"center"
            theme_text_color:"Custom"
            text_color:"black"

        MDLabel:
            id:message
            text: root.message
            font_style:"Body1"
            halign:"center"
            theme_text_color:"Custom"
            text_color:"black"

        MDSpinner:
            active:root.spinner_state
            size_hint:None, None
            color: [0,0,0,0]
            height: dp(50)
            width: dp(50)
            pos_hint:{'center_x': .5, 'center_y': .5}

''')


class LeftScreen(MDBoxLayout):
    message = StringProperty()
    spinner_state = BooleanProperty(False)

    def capture(self):
        user_id = self.ids.user_id
        try:
            if user_id.text == "":
                self.message = "User ID field cannot be empty"
            else:
                capture = TrainPCAandLDA(user_id.text)
                reg = capture.capture_images()
                if reg == None:
                    self.message = f"User with ID {user_id.text} has been added"
        except BaseException as e:
            self.message = f"{e}"

    def train(self):
        t = threading.Thread(target=self._train)
        t.start()

    def _train(self):
        self.spinner_state = True
        self.message = ""
        try:
            user_id = self.ids.user_id
            train = TrainPCAandLDA(user_id.text)
            tr = train.PCA_train_data()
            if tr == None:
                self.spinner_state = False
                self.message = "Model Trained Successfully"
        except Exception as e:
            self.message = f"{e}"

    def recog(self):
        department = self.ids.department
        try:
            if department.text == "":
                self.message = "Department field cannpot be empty"
            else:
                rec = self.recognise()
            if rec == None:
                self.message = f"Attendance verified"
        except Exception as e:
            print(e)

    def recognise(self):
        department = self.ids.department
        try:
            recognise = RecogPCAandLDA(department.text)
            recognise.load_trained_PCA_LDA()
            recognise.show_video()
            return
        except Exception as e:
            pass
