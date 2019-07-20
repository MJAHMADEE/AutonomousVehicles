#IN THE NAME OF ALLAH
#digitalLab
#mydriver.py 
#ver_3
#97/04/04


##### import packages #####
import serial
import sys		#for terminating the program immediately
import time
import tty, termios, sys #for getChar function


##### global variables ####
#rSpeed = 0
#lSpeed = 0
#left = right = 0
JOYSTICK_DELAY = 0.1
MOTOR_SPEED_MAX = 150
MOTOR_SPEED_STEP = 17
MOTOR_SPEED_TURN = 70
MOTOR_SPEED_minISTEP = 10

kbHitFlag = False


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
		self.kbHitFlag = False
		self.ch = ''
		self.count = 0

		##### try to connect to serial port #####
		try:
			ser = serial.Serial("/dev/ttyUSB0",38400)   # try to connect to serial port
			self.portfd = ser
			print("Successfully connected to serial! (USB0)")
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

	# def joystickMode(self):    
	# 	#left = right = 0    
	# 	ch = self.getChar()
	# 	if(ch == 27):             
	# 		left = right = 0 
	# 		self.setMotorSpeeds(right, left)
	# 		time.sleep(JOYSTICK_DELAY)                
	# 	elif(ch == 'w' or ch == 'W'):
	# 		if(left < MOTOR_SPEED_MAX or right < MOTOR_SPEED_MAX):
	# 			left = min(MOTOR_SPEED_MAX, left + MOTOR_SPEED_STEP)
	# 			right = min(MOTOR_SPEED_MAX, right + MOTOR_SPEED_STEP)
	# 			self.setMotorSpeeds(right, left)
	# 	elif(ch == 's' or ch == 'S'):                    
	# 		if(left > -1*MOTOR_SPEED_MAX or right > -1*MOTOR_SPEED_MAX):
	# 			left = max(-1*MOTOR_SPEED_MAX, left - MOTOR_SPEED_STEP)
	# 			right = max(-1*MOTOR_SPEED_MAX, right - MOTOR_SPEED_STEP)
	# 			self.setMotorSpeeds(right, left)                           
	# 	elif(ch == 'a' or ch == 'A'):                    
	# 		if(left > -1*MOTOR_SPEED_MAX or right < MOTOR_SPEED_MAX):
	# 			left = max(-1*MOTOR_SPEED_MAX, left - MOTOR_SPEED_STEP)
	# 			right = min(MOTOR_SPEED_MAX, right + MOTOR_SPEED_STEP)
	# 			self.setMotorSpeeds(right, left)            
	# 	elif(ch == 'd' or ch == 'D'):                    
	# 		if (left < MOTOR_SPEED_MAX or right > -1*MOTOR_SPEED_MAX):						
	# 			left = min(MOTOR_SPEED_MAX, left + MOTOR_SPEED_STEP)
	# 			right = max(-1*MOTOR_SPEED_MAX, right - MOTOR_SPEED_STEP)
	# 			self.setMotorSpeeds(right, left)                          
	# 	elif(ch == 'q' or ch == 'Q'):                    
	# 		if(left != MOTOR_SPEED_TURN or right < MOTOR_SPEED_MAX):
	# 			if(left < MOTOR_SPEED_TURN):
	# 				left = min(MOTOR_SPEED_TURN, left + MOTOR_SPEED_minISTEP)
	# 			elif (left > MOTOR_SPEED_TURN):
	# 				left = max(MOTOR_SPEED_TURN, left - MOTOR_SPEED_minISTEP)
	# 			right = min(MOTOR_SPEED_MAX, right + MOTOR_SPEED_STEP)
	# 			self.setMotorSpeeds(right, left)            
	# 	elif(ch == 'e' or ch == 'E'):                               
	# 		if(left < MOTOR_SPEED_MAX or right != MOTOR_SPEED_TURN):
	# 			left = min(MOTOR_SPEED_MAX, left + MOTOR_SPEED_STEP)
	# 			if(right < MOTOR_SPEED_TURN):
	# 				right = min(MOTOR_SPEED_TURN, right + MOTOR_SPEED_minISTEP)
	# 			elif(right > MOTOR_SPEED_TURN):
	# 				right = max(MOTOR_SPEED_TURN, right - MOTOR_SPEED_minISTEP)
	# 			self.setMotorSpeeds(right, left)                 
	# 	else:               
	# 		left = right = 0;
	# 		self.setMotorSpeeds(right, left)                                       
	# 	time.sleep(JOYSTICK_DELAY)


	def joystickMode(self):
		#print("In joystickMode function!")
		#print ("Char = %s"%(self.ch))
		if (self.kbHitFlag == True):
			#print ("in if")
			if(self.ch == 'o' or self.ch == 'O'):
				sys.exit() #terminates the program immediately
			elif(self.ch == 'j' or self.ch == 'J'):          
				self.rSpeed = self.lSpeed = 0
				self.setMotorSpeeds(self.rSpeed, self.lSpeed)     
			elif(self.ch == 'w' or self.ch == 'W'):
				if(self.lSpeed < MOTOR_SPEED_MAX or self.rSpeed < MOTOR_SPEED_MAX):
					self.lSpeed = min(MOTOR_SPEED_MAX, self.lSpeed + MOTOR_SPEED_STEP)
					self.rSpeed = min(MOTOR_SPEED_MAX, self.rSpeed + MOTOR_SPEED_STEP)
					self.setMotorSpeeds(self.rSpeed, self.lSpeed)
			elif(self.ch == 's' or self.ch == 'S'):                    
				if(self.lSpeed > -1*MOTOR_SPEED_MAX or self.rSpeed > -1*MOTOR_SPEED_MAX):
					self.lSpeed = max(-1*MOTOR_SPEED_MAX, self.lSpeed - MOTOR_SPEED_STEP)
					self.rSpeed = max(-1*MOTOR_SPEED_MAX, self.rSpeed - MOTOR_SPEED_STEP)
					self.setMotorSpeeds(self.rSpeed, self.lSpeed)                           
			elif(self.ch == 'a' or self.ch == 'A'):                    
				if(self.lSpeed > -1*MOTOR_SPEED_MAX or self.rSpeed < MOTOR_SPEED_MAX):
					self.lSpeed = max(-1*MOTOR_SPEED_MAX, self.lSpeed - MOTOR_SPEED_STEP)
					self.rSpeed = min(MOTOR_SPEED_MAX, self.rSpeed + MOTOR_SPEED_STEP)
					self.setMotorSpeeds(self.rSpeed, self.lSpeed)            
			elif(self.ch == 'd' or self.ch == 'D'):                    
				if (self.lSpeed < MOTOR_SPEED_MAX or self.rSpeed > -1*MOTOR_SPEED_MAX):						
					self.lSpeed = min(MOTOR_SPEED_MAX, self.lSpeed + MOTOR_SPEED_STEP)
					self.rSpeed = max(-1*MOTOR_SPEED_MAX, self.rSpeed - MOTOR_SPEED_STEP)
					self.setMotorSpeeds(self.rSpeed, self.lSpeed)                     
			elif(self.ch == 'q' or self.ch == 'Q'):                    
				if(self.lSpeed != MOTOR_SPEED_TURN or self.rSpeed < MOTOR_SPEED_MAX):
					if(self.lSpeed < MOTOR_SPEED_TURN):
						self.lSpeed = min(MOTOR_SPEED_TURN, self.lSpeed + MOTOR_SPEED_minISTEP)
					elif (self.lSpeed > MOTOR_SPEED_TURN):
						self.lSpeed = max(MOTOR_SPEED_TURN, self.lSpeed - MOTOR_SPEED_minISTEP)
					self.rSpeed = min(MOTOR_SPEED_MAX, self.rSpeed + MOTOR_SPEED_STEP)
					self.setMotorSpeeds(self.rSpeed, self.lSpeed)        
			elif(self.ch == 'e' or self.ch == 'E'):                               
				if(self.lSpeed < MOTOR_SPEED_MAX or self.rSpeed != MOTOR_SPEED_TURN):
					self.lSpeed = min(MOTOR_SPEED_MAX, self.lSpeed + MOTOR_SPEED_STEP)
					if(self.rSpeed < MOTOR_SPEED_TURN):
						self.rSpeed = min(MOTOR_SPEED_TURN, self.rSpeed + MOTOR_SPEED_minISTEP)
					elif(self.rSpeed > MOTOR_SPEED_TURN):
						self.rSpeed = max(MOTOR_SPEED_TURN, self.rSpeed - MOTOR_SPEED_minISTEP)
					self.setMotorSpeeds(self.rSpeed, self.lSpeed) 
			
			self.count += 1
			if (self.count < 12):
				time.sleep(JOYSTICK_DELAY)
				print (self.count)
			else:
				self.kbHitFlag = False
				self.count = 0

		else:
			#print ("in else")
			time.sleep(1)
			self.rSpeed = self.lSpeed = 0
			#self.setMotorSpeeds(self.rSpeed, self.lSpeed)
			tmpCh = self.ch
			self.ch = self.getChar()
			if (tmpCh != self.ch):
				self.setMotorSpeeds(self.rSpeed, self.lSpeed)
			print ("Char = %s"%(self.ch)) 
		
		
		




########### End of class ###########



##### create robot object #####
robot = autRobot()
#ch = 'j'

while True:
	# if(robot.kbHitFlag):
	# 	robot.joystickMode(ch)
	# 	print(robot.kbHitFlag)
	# else:
	# 	#robot.joystickMode('j')
	# 	ch = robot.getChar()
	# 	print(robot.kbHitFlag)

	robot.joystickMode()
