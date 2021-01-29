!/usr/bin/env python3
import sys
import time
import os
import math
import keyboard
import cv2

try:
	import numpy as np
except ImportError:
	sys.exit("Cannot import numpy: Do ‘pip3 install --user numpy‘ to install") 

try:
	from PIL import Image
except ImportError:
	sys.exit("Cannot import from PIL: Do ‘pip3 install --user Pillow‘ to install")

def cozmo_stream_images(robot: cozmo.robot.Robot):
	drive_dir = 1
	turn_dir = 0
	FORWARD_SPEED = 35
	TURNING_SPEED = 0
	TIME_LENGTH_OF_IMAGE_SEQUENCE = 600
	''' 
	Enable streaming of images and color images
	and obtain the camera configuration for yaml
	file '''
	robot.camera.image_stream_enabled = True
	robot.camera.color_image_enabled = True
	# Get robot camera configurations
	robot_focal_length = robot.camera.config.focal_length
	robot_image_center = robot.camera.config.center

	# Set text file object to write timestamps and
	the images
	file_rgb = open("rgb.txt", "a")
	file_config = open("config.txt", "w+")
	file_ground = open("groundtruth.txt", "a")

	file_config.write("%s %s" % (robot_focal_length, robot_image_center))

	# Set start time and capture image sequence for20s
	end_time = time.time() + TIME_LENGTH_OF_IMAGE_SEQUENCE
	turn_time = 20
	last_time = time.time()
	drive_control = 1
	longLength = 1
	c = ’l’

	while time.time() <= end_time:
		if keyboard.is_pressed(’w’):
			drive_dir = 1
			turn_dir = 0
			# Drive the robot with desired speed
			l_wheel_speed = (drive_dir * FORWARD_SPEED) + (turn_dir * TURNING_SPEED)
			r_wheel_speed = (drive_dir * FORWARD_SPEED)- (turn_dir * TURNING_SPEED)
			robot.drive_wheels(l_wheel_speed,r_wheel_speed)
		
		elif keyboard.is_pressed(’s’):
			drive_dir = -1
			turn_dir = 0
			# Drive the robot with desired speed			
			l_wheel_speed = (drive_dir * FORWARD_SPEED)+ (turn_dir * TURNING_SPEED)
			r_wheel_speed = (drive_dir * FORWARD_SPEED) - (turn_dir * TURNING_SPEED)
			robot.drive_wheels(l_wheel_speed,r_wheel_speed)

		elif keyboard.is_pressed(’a’):
			drive_dir = 0
			turn_dir = 1
			# Drive the robot with desired speed
			l_wheel_speed = (drive_dir * FORWARD_SPEED)+ (turn_dir * TURNING_SPEED)
			r_wheel_speed = (drive_dir * FORWARD_SPEED)+ (turn_dir * 35.0)
			robot.drive_wheels(l_wheel_speed,r_wheel_speed)

		elif keyboard.is_pressed(’d’):
			drive_dir = 0
			turn_dir = 1
			# Drive the robot with desired speed
			l_wheel_speed = (drive_dir * FORWARD_SPEED)+ (turn_dir * 35.0)
			r_wheel_speed = (drive_dir * FORWARD_SPEED)+ (turn_dir * TURNING_SPEED)
			robot.drive_wheels(l_wheel_speed,r_wheel_speed)

		# Get the current image frame from camera
		current_image = robot.world.latest_image

		if current_image is not None:
			# Obtain the received time of the image
			current_image = current_image.raw_image
			received_time = time.time()

			# State of the robot or ground truth
			positionx = robot.pose.position.x
			positiony = robot.pose.position.y
			positionz = robot.pose.position.z
			rotation1 = robot.pose.rotation.q0
			rotation2 = robot.pose.rotation.q1
			rotation3 = robot.pose.rotation.q2
			rotation4 = robot.pose.rotation.q3

			# Set directory and file name to store the image
			image_directory = os.path.join("image01", "%s" % received_time)	

			image_name = image_directory + ".png"
			current_image.save(image_name)
			file_rgb.write("%s %s\n" % (received_time,image_name))
			file_ground.write("%s %.4f %.4f %.4f %.4f%.4f %.4f %.4f\n" % (received_time, positionx, positiony, positionz, rotation2, rotation3,rotation4, rotation1))
			file_config.close()
			file_rgb.close()
			cozmo.robot.Robot.drive_off_charger_on_connect = False # Cozmo can stay on his charger for this example
			cozmo.run_program(cozmo_stream_images)