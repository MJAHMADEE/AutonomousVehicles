#IN THE NAME OF ALLAH
#digitalLab
#mydriver.py 
#ver_8 with abbas (flask added!)
#97/04/20


##### import packages #####
import serial
import sys		#for terminating the program immediately
import time
import tty, termios, sys #for getChar function

import threading

from flask import Flask , render_template,request



##### global variables ####
#rSpeed = 0
#lSpeed = 0
left = right = 0
JOYSTICK_DELAY = 0.05
MOTOR_SPEED_MAX = 200
MOTOR_SPEED_STEP = 17
MOTOR_SPEED_TURN = 70
MOTOR_SPEED_minISTEP = 10


##### robot class #####
class autRobot:
	def __init__(self):
		#self.portfd = 0;        # File descriptor of robot which data in written to and has to be read from
		self.motorSpeedLeft = 0        # The number has to be set on the left motor input
		self.motorSpeedRight = 0   # The number has to be set on the right motor input
		self.motorShaftLeft = 0        # Left shaft encoder data
		self.motorShaftRight = 0   # Right shaft encoder data
		self.omegaL = 0.0      # Left angular velocity
		self.omegaR = 0.0      # Right angular velocity
		self.sonarRear = 0         # data of sonar number 0
		self.sonarRearL = 0            # data of sonar number 1
		self.sonarFrontL = 0           # data of sonar number 2
		self.sonarFront = 0            # data of sonar number 3
		self.sonarFrontR = 0           # data of sonar number 4
		self.sonarRearR = 0            # data of sonar number 5
		self.battery = 0.0     # battery life percentage
		self.reset = 0         # does robot need reseting?
		self.rSpeed = 0
		self.lSpeed = 0

		#### try to connect to serial port #####
		try:
			ser = serial.Serial("/dev/ttyUSB0",38400)   # try to connect to serial port
			self.portfd = ser
			print("Successfully connected to seial! (USB0)")
		except:
			try:
				ser = serial.Serial("/dev/ttyUSB1",38400)
				self.portfd = ser
				print("Successfully connected to serial! (USB1)")
			except:
				print("Sorry! Can NOT connect to the robot!")
				sys.exit() #terminates the program immediately


	##### write motor speed in serial port #####
	def writeData(self, rSpeed, lSpeed):
		robot.portfd.write(bytes("S %d %d\n"%(rSpeed, lSpeed), 'UTF-8'))


	##### read date from serial port & assign  them to robot  #####
	def readData(self):
		data = []
		for count in range(0,9):
			tmp = self.portfd.readline().decode('UTF-8')         
			if(count < 8):
				data.append(int(tmp))
				#print ("The %d's data is %s"%(count+1, data[count]))
			else:
				self.battery = float(tmp)
				#print(robot.battery)

		self.motorShaftLeft = data[0]
		self.motorShaftRight = data[1]
		self.sonarRear = data[2]
		self.sonarRearL = data[3]
		self.sonarFrontL = data[4]
		self.sonarFront = data[5]
		self.sonarFrontR = data[6]
		self.sonarRearR = data[7]  

	##### print robot data in terminal #####
	def printData(self):
		#pfd = "Port File Descriptor: %s"% (robot.portfd)
		mspl = "Left Motor Speed: %d"% (self.motorSpeedLeft)
		mspr = "Right Motor Speed: %d"% (self.motorSpeedRight)
		mshl = "Left Shaft Encoder Data: %d"% (self.motorShaftLeft)
		mshr = "Right Shaft Encoder Data: %d"% (self.motorShaftRight)
		sr = "Rear Sonar Data: %d"% (self.sonarRear)
		srl = "Rear-Left Sonar Data: %d"% (self.sonarRearL)
		sfl = "Front-Left Sonar Data: %d"% (self.sonarFrontL)
		sf = "Front Sonar Data: %d"% (self.sonarFront)
		sfr = "Front-Right Sonar Data: %d"% (self.sonarFrontR);
		srr = "Rear-Right Sonar Data: %d"% (self.sonarRearR);
		bt = "Battery Voltage: %f"% (self.battery);

		print("\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n"%(mspl, mspr, mshl, mshr, sr, srl, sfl, sf, sfr, srr, bt))


	##### detect key from keyboard #####
	def getChar(self):
	   #Returns a single character from standard input
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch

	def setMotorSpeeds(self, right, left):
		robot.motorSpeedRight = right
		robot.motorSpeedLeft = left    
		#print("rSpeed = %d, lSpeed = %d \n"%(right, left))
		self.updateRobot()

	def updateRobot(self):
		self.writeData(self.motorSpeedRight, self.motorSpeedLeft)
		self.readData()
		self.printData()


	def joystickMode(self):
		ch = self.getChar()
		print ("char = %s"%(ch))
		#if (ch == 'o' or ch == 'O' or ch == 'j' or ch == 'J' or ch == 'w' or ch == 'W' or ch == 's' or ch == 'S' or ch == 'd' or ch == 'D' or ch == 'a' or ch == 'A'):
		#if (self.getChar()):
		if(ch == 'o' or ch == 'O'):
			sys.exit() #terminates the program immediately
		elif(ch == 'j' or ch == 'J'):          
			self.rSpeed = self.lSpeed = 0
			self.setMotorSpeeds(self.rSpeed, self.lSpeed)     
		elif(ch == 'w' or ch == 'W'):
			if(self.lSpeed < MOTOR_SPEED_MAX or self.rSpeed < MOTOR_SPEED_MAX):
				self.lSpeed = min(MOTOR_SPEED_MAX, self.lSpeed + MOTOR_SPEED_STEP)
				self.rSpeed = min(MOTOR_SPEED_MAX, self.rSpeed + MOTOR_SPEED_STEP)
				self.setMotorSpeeds(self.rSpeed, self.lSpeed)
		elif(ch == 's' or ch == 'S'):                    
			if(self.lSpeed > -1*MOTOR_SPEED_MAX or self.rSpeed > -1*MOTOR_SPEED_MAX):
				self.lSpeed = max(-1*MOTOR_SPEED_MAX, self.lSpeed - MOTOR_SPEED_STEP)
				self.rSpeed = max(-1*MOTOR_SPEED_MAX, self.rSpeed - MOTOR_SPEED_STEP)
				self.setMotorSpeeds(self.rSpeed, self.lSpeed)                           
		elif(ch == 'a' or ch == 'A'):                    
			if(self.lSpeed > -1*MOTOR_SPEED_MAX or self.rSpeed < MOTOR_SPEED_MAX):
				self.lSpeed = max(-1*MOTOR_SPEED_MAX, self.lSpeed - MOTOR_SPEED_STEP)
				self.rSpeed = min(MOTOR_SPEED_MAX, self.rSpeed + MOTOR_SPEED_STEP)
				self.setMotorSpeeds(self.rSpeed, self.lSpeed)            
		elif(ch == 'd' or ch == 'D'):                    
			if (self.lSpeed < MOTOR_SPEED_MAX or self.rSpeed > -1*MOTOR_SPEED_MAX):						
				self.lSpeed = min(MOTOR_SPEED_MAX, self.lSpeed + MOTOR_SPEED_STEP)
				self.rSpeed = max(-1*MOTOR_SPEED_MAX, self.rSpeed - MOTOR_SPEED_STEP)
				self.setMotorSpeeds(self.rSpeed, self.lSpeed)                         
		time.sleep(JOYSTICK_DELAY)
########### End of class ###########

##### create robot object #####
robot = autRobot()


########### ABBAS ###############
def go_up():
	print("going up")
	for Speed in range(20,200,20):
		robot.setMotorSpeeds(Speed,Speed)
		time.sleep(JOYSTICK_DELAY)
	time.sleep(2.5)
	robot.setMotorSpeeds(0,0) 
	print("break going up")

def go_down():
	print("going down")
	for Speed in range(20,200,20):
		robot.setMotorSpeeds(-Speed,-Speed)
		time.sleep(JOYSTICK_DELAY)
	time.sleep(2.5)
	robot.setMotorSpeeds(0,0) 
	print("break going down") 

def go_right():
	print("going down")
	for Speed in range(20,200,20):
		robot.setMotorSpeeds(Speed,-Speed)
		time.sleep(JOYSTICK_DELAY)
	time.sleep(2.5)
	robot.setMotorSpeeds(0,0) 
	print("break going right")

def go_left():
	print("going left")
	for Speed in range(20,200,20):
		robot.setMotorSpeeds(-Speed,Speed)
		time.sleep(JOYSTICK_DELAY)
	time.sleep(2.5)
	robot.setMotorSpeeds(0,0) 
	print("break going left")      


app=Flask (__name__)


@app.route('/login/<myname>',methods=['GET', 'POST'])
def myfunc4(myname):
	if request.method=='POST':
		my_command=request.form['command']
		
		if my_command=="UP":
			t1=threading.Thread(target=go_up)
			t1.start()
		elif my_command=="DOWN":
			t2=threading.Thread(target=go_down)
			t2.start()
		elif my_command=="LEFT":
			t3=threading.Thread(target=go_left)
			t3.start()
		elif my_command=="RIGHT":
			t4=threading.Thread(target=go_right)
			t4.start()
			
		return render_template('myHTML.html',myname=myname,command=my_command)
	return render_template('myHTML.html',myname=myname,command=None)

if __name__ == '__main__':
	app.run(threaded=True,debug=True, host='0.0.0.0',port=2000)
