from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.button import MDFillRoundFlatButton
import datetime
import requests
#from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
import json
import random
from twilio.rest import Client
from kivy.properties import ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout
from pyrebase import pyrebase

Window.size = (350, 600)


class FirstWindow(Screen):
    pass


class SecondWindow(Screen):
    pass


class ThirdWindow(Screen):
    pass


class ForthWindow(Screen):
    pass


class FifthWindow(Screen):
    pass

class SixthWindow(Screen):
    pass

class SeventhWindow(Screen):
    pass

class EighthWindow(Screen):
    pass

class NinthWindow(Screen):
    pass

class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class WindowManager(ScreenManager):
    pass

otp=1980
delivery_time = 'Morning'
source = 'Cow'
freq = 'One Time'
date_type=0
quantity=0
x=0
class MainApp(MDApp):
    check = []
    auth = 'CRdL2RczrkFO2gxMzWMAPO15Nepn4MaTYDVw0dxR'
    def build(self):
        sm=WindowManager()
        self.url = "https://truefresh-889a7-default-rtdb.firebaseio.com/.json"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Cyan"
        self.theme_cls.primary_hue = "700"
        # naming the screen
        root = Builder.load_file('trial101.kv')
        root.get_screen('third').ids.meow.text = f"On{datetime.datetime.now().day}-{datetime.datetime.now().month}-{datetime.datetime.now().year}"
        return root

    def logger(self):
        self.root.ids.welcome_label.text = f'Sup {self.root.ids.user.text}'

    def show_date_picker(self):
        global date_type
        tyear = int(datetime.datetime.now().year)
        tmonth = int(datetime.datetime.now().month)
        tday = int(datetime.datetime.now().day)
        print(tyear,tmonth,tday)
        if date_type==0:
            date_dialog = MDDatePicker(mode='range',year=tyear,month=tmonth,day=tday)
            date_dialog.bind(on_save=self.on_save)
            date_dialog.open()
        else:
            date_dialog = MDDatePicker(year=tyear,month=tmonth,day=tday)
            date_dialog.bind(on_save=self.on_save_two)
            date_dialog.open()

    def on_save(self, instance, value, date_range):
        start_day=str(date_range[0])
        end_day=str(date_range[-1])
        global range_date
        print(f'{str(date_range[0])} - {str(date_range[-1])}')
        self.root.get_screen('third').ids.meow.text = f'{str(date_range[0])} to {str(date_range[-1])}'
    def on_save_two(self, instance, value, date):
        start_day=str(date)
        self.root.get_screen('third').ids.meow.text = f'{str(date)}'

    def generate_otp(self):
        global otp
        otp = random.randint(1000, 9999)
        account_sid = "AC606e0118693a5d2b9464cd461474b509"
        auth_token = 'b2e8fd713ce882f51f6a1c025b7f52c8'
        client = Client(account_sid, auth_token)
        msg = client.messages.create(
            body=f"Your TrueFresh OTP is {otp}",
            from_="+19404274872",
            to=f"+91{self.root.get_screen('second').ids.phone.text}"
        )
    def generate_otp_login(self):
        global otp
        otp = random.randint(1000, 9999)
        account_sid = "AC606e0118693a5d2b9464cd461474b509"
        auth_token = 'b2e8fd713ce882f51f6a1c025b7f52c8'
        client = Client(account_sid, auth_token)
        msg = client.messages.create(
            body=f"Your TrueFresh OTP is {otp}",
            from_="+19404274872",
            to=f"+91{self.root.get_screen('first').ids.phn_login.text}"
        )

    def signup(self):
        signupUsername = self.root.get_screen('second').ids.username.text
        signupPhoneno = self.root.get_screen('second').ids.phone.text
        signupOtp = self.root.get_screen('second').ids.otp.text
        if signupPhoneno.split() == [] or signupOtp.split() == [] or signupUsername.split() == []:
            self.dialog = MDDialog(title='Invalid Input', text='Please Enter a valid Input', size_hint=(0.7, 0.2))
            self.dialog.open()
        if len(signupUsername.split()) > 1:
            self.dialog = MDDialog(title='Invalid Username', text='Please enter username without space')
            self.dialog.open()
        if signupOtp != str(otp):
            self.dialog = MDDialog(title='Incorrect OTP', text='Please recheck and enter the otp again')
            self.dialog.open()
            print("Otp didn't match")

        else:
            print(signupUsername, signupOtp)
            signup_info = str(
                {f'\"{signupPhoneno}\":{{"Username":\"{signupUsername.rstrip()}\"}}'})
            signup_info = signup_info.replace(".", "-")
            signup_info = signup_info.replace("\'", "")
            to_database = json.loads(signup_info)
            print((to_database))
            requests.patch(url=self.url, json=to_database)
            self.dialog = MDDialog(title='Signup Successful', text='Please go back and login.')
            self.dialog.open()
            #self.strng.get_screen('loginscreen').manager.current = 'loginscreen'

    def login(self):
        loginEmail = self.strng.get_screen('loginscreen').ids.login_email.text
        loginPassword = self.strng.get_screen('loginscreen').ids.login_password.text

        self.login_check = False
        supported_loginEmail = loginEmail.replace('.', '-')
        supported_loginPassword = loginPassword.replace('.', '-')
        request = requests.get(self.url + '?auth=' + self.auth)
        data = request.json()
        emails = set()
        for key, value in data.items():
            emails.add(key)
        if supported_loginEmail in emails and supported_loginPassword == data[supported_loginEmail]['Password']:
            self.username = data[supported_loginEmail]['Username']
            self.login_check = True
            self.strng.get_screen('mainscreen').manager.current = 'mainscreen'
        else:
            print("user no longer exists")

    def close_username_dialog(self, obj):
        self.dialog.dismiss()
    def confirm_order(self):
        self.dialog = MDDialog(title='Order Confirmation', text=f"{delivery_time}-{source}-{freq}", size_hint=(0.7, 0.2),
                               buttons=[MDFillRoundFlatButton(text='CONFIRM')])
        self.dialog.open()

    class user_selection():
        def morning(self):
            global delivery_time
            delivery_time= 'Morning'
        def evening(self):
            global delivery_time
            deliver_time='Evening'
        def both(self):
            global delivery_time
            delivery_time='Both'
        def cow(self):
            global source
            source='Cow'
        def buffalo(self):
            global source
            source='Buffalo'
        def mix(self):
            global source
            source='Mix'
        def frequency_eve(self):
            global freq
            global date_type
            freq='Everyday'
            date_type=0
        def frequency_one(self):
            global freq
            global date_type
            freq='One Time'
            date_type=1
        def print_details(self):
            print(delivery_time, '-', source, '-', freq)
    def today_date(self):
        range_date = f"{datetime.datetime.now().day}"

    def swiped(self):
        global x
        #print("Swiped")
        if x==1:
            #print('changed')
            self.root.get_screen('seventh').ids.ima.source = 'a.png'# Default Images
            x=0
        elif x==2:
            self.root.get_screen('seventh').ids.ima2.source = 'aaa.png'# Default Images
            x=0
        elif x==3:
            self.root.get_screen('seventh').ids.ima3.source = '123.png' # Default Images
            x=0
        else:
            pass
            #print('passed')
    def pressed(self,y):
        global x
        print("Pressed")
        #print(y)
        x=y
        if x==1:
            self.root.get_screen('seventh').ids.ima.source = 'cow.jpg' # If Pressed
        elif x==2:
            self.root.get_screen('seventh').ids.ima2.source = 'cow.jpg' # If Pressed
        elif x==3:
            self.root.get_screen('seventh').ids.ima3.source = 'cow.jpg' # If Pressed
    def checkbox_click(self,instance,value,category):
        if (value == True):
            MainApp.check.append(category)
        else:
            MainApp.check.remove(category)
        print(MainApp.check)


    def fetchcosts(self):
        firebaseConfig = {
            'apiKey': "AIzaSyAE5tQUO166gqJ0n_-kEX0k3tNXUjs4cco",
            'authDomain': "cost-bc0fd.firebaseapp.com",
            'databaseURL': "https://cost-bc0fd-default-rtdb.firebaseio.com",
            'projectId': "cost-bc0fd",
            'storageBucket': "cost-bc0fd.appspot.com",
            'messagingSenderId': "371306847156",
            'appId': "1:371306847156:web:e01463a22cd838d4b0f0e1",
            'measurementId': "G-1TQCFPJRBE"
        }
        firebase=pyrebase.initialize_app(firebaseConfig)

        db=firebase.database()
        cowcost =db.child("cow").get()
        self.root.get_screen('sixth').ids.label.text = f'RS {str(cowcost.val())}/L'


MainApp().run()
