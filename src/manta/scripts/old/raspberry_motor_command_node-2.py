#!/usr/bin/env python

## Talker that publishes CmdMotors messages
## to the 'command_motors' topic

import rospy
import serial
import time
import math
from manta.msg import CmdMotors
from manta.msg import Radio
#from std_msgs  import Float32

startMotors = False;
motorLeft   = 0;
motorRight  = 0;

message   = 0;
vitesse_moteur = 0;
difference_moteur = 85;

def callback(data):
	global message
	global vitesse_moteur
	global difference_moteur
        message = data.message
        vitesse_moteur = data.valeur1
        difference_moteur = data.valeur2

#def callback2(data):
#	global difference_moteur
#	global message
#	if message == 2: 
#		difference_moteur = data

def eval_command():
        global startMotors
        global motorLeft
        global motorRight
	global message
	global difference_moteur
        global vitesse_moteur

	if message == 0:
		startMotors = False
	else: #message > 0
		startMotors = True

	difference_m = int(difference_moteur) - 85
	motorRight = int(vitesse_moteur) + difference_m
	motorLeft  = int(vitesse_moteur) - difference_m
	if motorLeft < 0:
		motorRight = motorRight - motorLeft
		motorLeft = 0
	elif motorLeft > 170:
		motorRight = motorRight - (motorLeft - 170)
		motorLeft = 170
	elif motorRight < 0:
		motorLeft = motorLeft - motorRight
		motorRight = 0
	elif motorRight > 170:
		motorLeft = motorLeft - (motorRight - 170)
		motorRight = 170

def talker():
        global r_timer
        global startMotors
        global motorLeft
        global motorRight
	rospy.init_node('raspberry_motor_command_node', anonymous=True)
	pub = rospy.Publisher('command_motors', CmdMotors, queue_size=10)
	rospy.Subscriber("radio",Radio, callback)
	rate = rospy.Rate(20) # 10hz
	while not rospy.is_shutdown():
		eval_command()                      
		command = CmdMotors()
		command.startMotors = startMotors
		command.motorLeft   = motorLeft
		command.motorRight  = motorRight
        	rospy.loginfo(command)
        	pub.publish(command)
        	rate.sleep()

if __name__ == '__main__':
    try:
        talker()
	
    except rospy.ROSInterruptException:
        pass

