from kivy.lang import Builder
from kivymd.uix.widget import MDWidget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.datatables import MDDataTable
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.metrics import dp
from kivymd.toast import toast
import pandas as pd
import datetime
import csv


Builder.load_string('''

<RightScreen>:
    MDBoxLayout:
        md_bg_color:[.5,.5,.5,1]
        size_hint: None,1
        width: dp(2)
    MDBoxLayout:
        orientation: 'vertical'
        padding: ('20dp', '20dp', '20dp', '20dp')
        spacing: '50dp'

        MDRectangleFlatIconButton:
            icon:"attachment"
            text:" L O A D   A T T E N D A N C E "
            theme_text_color: "Custom"
            text_color: "black"
            line_color: "black"
            theme_icon_color: "Custom"
            icon_color: "black"
            on_release: root.show_table()
        MDBoxLayout:
            id:table_box

''')


class RightScreen(MDBoxLayout):
    csv_filename = datetime.datetime.now().strftime("%Y-%m-%d") + ".csv"
    data = []
    data_table = ObjectProperty()
    row_data = []

    def read_csv(self):
        try:
            self.data = []

            with open(self.csv_filename, 'r') as csvfile:
                csvreader = csv.DictReader(csvfile)
                for row in csvreader:
                    self.data.append(row)
            
            toast("Attendance Loaded")

        except Exception as e:
            toast(f"{e}")

    def show_table(self):
        self.read_csv()
        table_box = self.ids.table_box
        table_box.clear_widgets()
        self.row_data = []
        for item in self.data[::-1]:
            row = (
                item['Person'],
                item['Department'],
                item['Time']
            )
            self.row_data.append(row)

        layout = AnchorLayout()
        self.data_table = MDDataTable(
            size_hint=(1, 1),
            use_pagination=True,
            column_data=[
                ("User ID", dp(30)),
                ("Department", dp(30)),
                ("Time", dp(30)),

            ],
            row_data=self.row_data

        )
        layout.add_widget(self.data_table)
        table_box.add_widget(layout)
