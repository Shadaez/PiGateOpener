import web
import RPi.GPIO as GPIO
"""
This is one part of a gate opening software I'm writing. 
It's the only currently functioning part, I'm working on the rest at the moment.
I have an Android script (which will later be compiled into an APK with SL4A/Py4A)
that connects to the web.py server and opens the gate! No more need for remote gate openers.
I use basic threading to open the gate and sleep, then close it without stopping the rest of the program!
"""

OPENGATE_PIN = 4

urls = ('/open', 'open')
render = web.template.render('templates/')

class GPIO_Controller(object):
	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(OPENGATE_PIN, GPIO.OUT)

	def GPIO_out(self, pin, time): #turns on the GPIO pin for the amount of time determined by the time arg
		t = threading.Thread(target=self.GPIO_output_threading, args=(pin, time))
		t.start()
	
	def GPIO_output_threading(self, pin, time):
		GPIO.output(pin, True)
		sleep(time)
		GPIO.output(pin, False)

GPIO_controller = GPIO_Controller()

class index:
	def GET(self, name):
		return render.index(name)


class open:
	def GET(self):
		passwords = ["1111"] #just an example password, don't try and open my gate with it :)
		#TODO add more passwords and possibly lock the gate to certain passwords at night,
		#and will log the times and etc to a sqlite DB
		i = web.input(password=None) #makes it so that everything after password= here: 
		#the_gate_ip:8080/open?password=THIS <- becomes variable "i.password"
 		opened = i.password in passwords
		if opened:
			GPIO_controller.GPIO_out(OPENGATE_PIN, 10)
		return render.open(opened) #this tells the html file what to display. It simply displays "Gate Opened" or 
		#"Wrong Password" currently, which I read from in my Android script and toast to the screen.

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()

