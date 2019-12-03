#!/usr/bin/env python
import numpy as np
import math
from numpy import *
from math import sqrt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# import Person and World objects
from person_geometric import Person
from world import *
from dmp_walking import DMP
def main():
	# l - distance to s
	# h - stair height
	# r - stair run
	# w = stair width
	l = 2280.6
	h = 177.8
	r = 304.8
	w = 609.6
	# using 9in, 7in, 12in, and 24in in mm for base staircase (based on Al-b's staircase)
	
	# using Al-b's biometric data for leg length and foot size
	subject = Person(1000, 279.4)

	dmp_runner = DMP("leg_info.csv")
	dmp_runner.train();

	step_length = subject._leg_lenth * 0.413
	steps = l / step_length ;

	walking_start_end_poses = []
	stair_climb_start_end_poses = []

	print("start position")
	subject.print_pos()
	jangles = subject.inverse_kinematics();
	print(jangles);
	subject.forward_kinematics(jangles);
	print("start position-after-ik-k")
	subject.print_pos()
	jangles = subject.inverse_kinematics();
	print(jangles)

	for i in range(0, int(steps)):
		start_joint_angles = subject.inverse_kinematics();
		foot = subject.getTrailingFoot();
		foot_pos = foot[1];

		subject.set_foot(foot[0], (foot_pos[0]), foot_pos[1], foot_pos[2]+step_length);
		goal_joint_angles = subject.inverse_kinematics(); 

		joint_pairs = []
		for j in range(0, 6):
			joint_pairs.append((start_joint_angles[j], goal_joint_angles[j]))

		walking_start_end_poses.append(joint_pairs);
		print("position update - forward")
		print(str(subject._right_hip_pos[0]) + ' ' + str(subject._right_hip_pos[2]))
		print(str(subject._right_knee_pos[0]) + ' ' + str(subject._right_knee_pos[2]))
		print(str(subject._right_ankle_pos[0]) + ' ' + str(subject._right_ankle_pos[2]))
		print(str(subject._right_toe_pos[0]) + ' ' + str(subject._right_toe_pos[2]))

	stair_count = 2;
	for i in range(0, int(stair_count)):
		start_joint_angles = subject.inverse_kinematics();
		foot = subject.getTrailingFoot();
		foot_pos = foot[1];

		subject.set_foot(foot[0], foot_pos[0]+ h , foot_pos[1], foot_pos[2] + (r * 0.75));	
		goal_joint_angles = subject.inverse_kinematics(); 

		joint_pairs = []
		for j in range(0, 6):
			joint_pairs.append((start_joint_angles[j], goal_joint_angles[j]))

		stair_climb_start_end_poses.append(joint_pairs)
		print("position update - up")
		print(str(subject._right_hip_pos[0]) + ' ' + str(subject._right_hip_pos[2]))
		print(str(subject._right_knee_pos[0]) + ' ' + str(subject._right_knee_pos[2]))
		print(str(subject._right_ankle_pos[0]) + ' ' + str(subject._right_ankle_pos[2]))
		print(str(subject._right_toe_pos[0]) + ' ' + str(subject._right_toe_pos[2]))

	angles = []	
	for i in walking_start_end_poses:
		print("walk ")
		angles.append(dmp_runner.run(i))

	for i in stair_climb_start_end_poses:
		print("step")
		angles.append(dmp_runner.run(i))

	staircase = World(l,h,r,w)
	subject2 = Person(1000, 279.4)
	i = 0;
	for i in angles:	
		print(len(angles))
		for j in i:
			print(len(i))
			subject2.forward_kinematics(j);
			plt.figure(1)
			print(str(subject2._right_hip_pos[0]) + ' ' + str(subject2._right_hip_pos[2]))
			print(str(subject2._right_knee_pos[0]) + ' ' + str(subject2._right_knee_pos[2]))
			print(str(subject2._right_ankle_pos[0]) + ' ' + str(subject2._right_ankle_pos[2]))
			print(str(subject2._right_toe_pos[0]) + ' ' + str(subject2._right_toe_pos[2]))

			plt.plot(subject2._right_hip_pos[0], subject2._right_hip_pos[2], 'ro')
			plt.plot(subject2._right_knee_pos[0], subject2._right_knee_pos[2], 'go')
			plt.plot(subject2._right_ankle_pos[0], subject2._right_ankle_pos[2], 'bo')
			plt.plot(subject2._right_toe_pos[0], subject2._right_toe_pos[2], 'ro')
			
			plt.pause(0.001)
			plt.show()
		break;	

	input("What's your name? ")			
			
		

		

if __name__ == '__main__':
	main()