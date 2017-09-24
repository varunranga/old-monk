import kivy
kivy.require('1.10.0') # replace with your current kivy version !

# base class of the app must inherit the App class
from kivy.app import App 

# uix package holds the interface elements
from kivy.uix.label import Label

#importing the grid layout
from kivy.uix.gridlayout import GridLayout

#from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from kivy.uix.button import Button

from kivy.uix.screenmanager import ScreenManager, Screen


#screenMan=ScreenManager()
my_screenmanager=ScreenManager()

def changeToPage(*args):
	my_screenmanager.current='screen2'

class main(GridLayout,Screen):
	

	def __init__(self, **kwargs):
		super(main, self).__init__(**kwargs)
		self.cols = 1
		
		welcome=Label(text='Welcome To Old Monk',font_size=30)
		self.add_widget(welcome)

		btn=Button(text='Continue',font_size=30);
		self.add_widget(btn)

		btn.bind(on_press=changeToPage)

	def changer(self,*args):
		self.manager.screen='screen1'

	

class login(GridLayout,Screen):

	def __init__(self, **kwargs):
		super(login, self).__init__(**kwargs)

		self.cols = 1
		

		welcome=Label(text='Welcome To Old Monk',font_size=30)
		self.add_widget(welcome)

		userNameDisp=Label(text='User Name',font_size=30)
		self.add_widget(userNameDisp)

		self.username = TextInput(multiline=False)
		
		self.add_widget(self.username)
		
		passwordDisp=Label(text='Password',font_size=30)
		self.add_widget(passwordDisp)

		self.password = TextInput(password=True, multiline=False)
		
		self.add_widget(self.password)

		btn=Button(text='Login',font_size=30);
		self.add_widget(btn)
	def changer(self,*args):
		self.manager.screen='screen2'

screen1=main(name='screen1')
screen2=login(name='screen2')
my_screenmanager.add_widget(screen1)
my_screenmanager.add_widget(screen2)

# base class of the app
class MyApp(App,Screen):
	#initialising and returning the root widget
	def build(self):
		my_screenmanager=ScreenManager()
		screen1=main(name='screen1')
		screen2=login(name='screen2')
		my_screenmanager.add_widget(screen1)
		my_screenmanager.add_widget(screen2)
		return login()    	

if __name__ == '__main__':
    MyApp().run()