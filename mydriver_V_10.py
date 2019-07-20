#IN THE NAME OF ALLAH
#digitalLab
#mydriver.py 
#ver_10 (ESP)
#97/04/22


##### import packages #####
import serial
import sys		#for terminating the program immediately
import time
import tty, termios, sys #for getChar function

import sys, termios, atexit #for I/O functions
from select import select


##### global variables ####
#rSpeed = 0
#lSpeed = 0
#left = right = 0
JOYSTICK_DELAY = .2
MOTOR_SPEED_MAX = 200
MOTOR_SPEED_STEP = 17
MOTOR_SPEED_TURN = 70
MOTOR_SPEED_minISTEP = 10

kbHitFlag = False



########### I/O functions ###########
# save the terminal settings
fd = sys.stdin.fileno()
new_term = termios.tcgetattr(fd)
old_term = termios.tcgetattr(fd)

# new terminal setting unbuffered
new_term[3] = (new_term[3] & ~termios.ICANON & ~termios.ECHO)

# switch to normal terminal
def set_normal_term():
    termios.tcsetattr(fd, termios.TCSAFLUSH, old_term)

# switch to unbuffered terminal
def set_curses_term():
    termios.tcsetattr(fd, termios.TCSAFLUSH, new_term)

# def putch(ch):
#     sys.stdout.write(ch)

def getch():
    return sys.stdin.read(1)

# def getche():
#     ch = getch()
#     putch(ch)
#     return ch

def kbhit():
    dr,dw,de = select([sys.stdin], [], [], 0)
    return dr

atexit.register(set_normal_term)
set_curses_term()


##### robot class #####
class autRobot:
	def __init__(self, getch, kbhit, robotSerialp, ESPSerialp):
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
		self.kbHitFlag = False
		self.ch = ''
		self.count = 0
		self.getch = getch #for I/O
		self.kbhit = kbhit
		self.ESPflag = 0
		self.ESPSerial = 0
		self.robotSerialp = robotSerialp
		self.ESPSerialp = ESPSerialp

		##### try to connect to serial port #####
		try:
			ser = serial.Serial("/dev/ttyUSB%s"%(self.robotSerialp),38400)   # try to connect to serial port
			self.portfd = ser
			print("Successfully connected to serial! (USB%s)"%(self.robotSerialp))
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
		self.kbHitFlag = True
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(1)
		#print ("Char in getchar = %s"%(self.ch))
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch

	def setMotorSpeeds(self, right, left):
		robot.motorSpeedRight = right
		robot.motorSpeedLeft = left    
		self.updateRobot()

	def updateRobot(self):
		self.writeData(self.motorSpeedRight, self.motorSpeedLeft)
		self.readData()
		self.printData()


	def joystickMode(self, ch):
		#print("In joystickMode function!")
		#print ("Char = %s"%(self.ch))
		#if (self.kbhit()):
			#print ("kbhit = True")
			#ch = getch()
			#ch = self.getChar()
		print ("This is ch: '%s'"%(ch))
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
		elif(ch == 'q' or ch == 'Q'):                    
			if(self.lSpeed != MOTOR_SPEED_TURN or self.rSpeed < MOTOR_SPEED_MAX):
				if(self.lSpeed < MOTOR_SPEED_TURN):
					self.lSpeed = min(MOTOR_SPEED_TURN, self.lSpeed + MOTOR_SPEED_minISTEP)
				elif (self.lSpeed > MOTOR_SPEED_TURN):
					self.lSpeed = max(MOTOR_SPEED_TURN, self.lSpeed - MOTOR_SPEED_minISTEP)
				self.rSpeed = min(MOTOR_SPEED_MAX, self.rSpeed + MOTOR_SPEED_STEP)
				self.setMotorSpeeds(self.rSpeed, self.lSpeed)        
		elif(ch == 'e' or ch == 'E'):                               
			if(self.lSpeed < MOTOR_SPEED_MAX or self.rSpeed != MOTOR_SPEED_TURN):
				self.lSpeed = min(MOTOR_SPEED_MAX, self.lSpeed + MOTOR_SPEED_STEP)
				if(self.rSpeed < MOTOR_SPEED_TURN):
					self.rSpeed = min(MOTOR_SPEED_TURN, self.rSpeed + MOTOR_SPEED_minISTEP)
				elif(self.rSpeed > MOTOR_SPEED_TURN):
					self.rSpeed = max(MOTOR_SPEED_TURN, self.rSpeed - MOTOR_SPEED_minISTEP)
				self.setMotorSpeeds(self.rSpeed, self.lSpeed) 

	
		time.sleep(JOYSTICK_DELAY) 
		print("R: %d ------- L: %d"%(self.rSpeed, self.lSpeed))

	def serialConnect2(self):
		try:
			ser = serial.Serial("/dev/ttyUSB%s"%(self.ESPSerialp),115200)   # try to connect to serial port
			self.ESPSerial = ser
			print("ESP Successfully connected to serial! (USB%s)"%(self.ESPSerialp))
			self.ESPflag = 0 
		except:
			print("Sorry! Can NOT connect to the robot!")
			sys.exit() #terminates the program immediately
	
	def ESPserialRead(self):
		char = self.ESPserial.readline().decode('UTF-8')
		print("Received character is '%s' \n"%(char[0]))
		return char[0]
########### End of class ###########

robotSerialp = 1
ESPSerialp = 0

##### create robot object #####
robot = autRobot(getch, kbhit, robotSerialp, ESPSerialp)
robot.serialConnect2()
#ch = 'j'


#while True:
	# if(robot.kbHitFlag):
	# 	robot.joystickMode(ch)
	# 	print(robot.kbHitFlag)
	# else:
	# 	#robot.joystickMode('j')
	# 	ch = robot.getChar()
	# 	print(robot.kbHitFlag)



while True:
	char = robot.ESPserialRead()
	robot.joystickMode(char)

