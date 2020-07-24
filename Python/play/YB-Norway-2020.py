import math
import tkinter as tk 
import time

env = {'course' : [(0,0), (100, 700)], 'left_margin': 10, 'right_margin' : 15, 'max_acc' : 10, 'max_velocity' : 20, 'max_angle': 45}

class Vehicle:
	def __init__ (self, env, name):
		self.name  = name
		self.xpos = env['course'][1][0]/4
		self.ypos = env['course'][0][1]
		self.xVelocity = 0
		self.yVelocity = 0
		self.acc = 0
		self.angle = 0

	def boost(self, val):
		self.acc += val

	def brake(self, val):
		self.acc -= val 

	def stop(self):
		self.acc = 0

	def straight(self):
		self.angle = 0

	def turn(self, turn_dir, turn_val):
		if turn_dir == 'left':
			self.angle -= turn_val
		elif turn_dir == 'right':
			self.angle += turn_val

def deny():
	print ('action denied')

def checker(v, env):
	if v.acc >= env['max_acc'] or abs(v.angle) >= env['max_angle'] : 
		deny()
		v.straight()
		v.stop()
	if v.yVelocity >= env['max_velocity']:
		v.stop()
		v.brake(2)
	if v.xVelocity >= env['max_velocity']:
		v.straight()
		v.xVelocity = 0
	if v.xpos <= env['left_margin'] and (v.angle < 0 or v.xVelocity < 0): 
		v.straight()
		v.xVelocity = 0
	if v.xpos >= env['course'][1][0] - env['right_margin'] and (v.angle > 0 or v.xVelocity > 0): 
		v.straight()
		v.xVelocity = 0

	if v.yVelocity <= 0.1:
		v1.stop()
		v1.boost(2)


v1 = Vehicle(env, 'Proto1')
v1.turn('right', 10)
v1.boost(5)
Time = 0

Tk = tk.Tk()
canvas = tk.Canvas(Tk, width = env['course'][1][0], height = env['course'][1][1])
canvas.grid()

v = canvas.create_oval(v1.xpos, env['course'][1][1], v1.xpos+10, env['course'][1][1]-10, fill = 'light blue')

# Tk.mainloop()
i = 0
while v1.ypos <= env['course'][1][1]:
	i += 1
	# if i%10 == 0:
	# 	v1.turn('left', 20)
	# if i%16 == 0:
	# 	v1.turn('right', 40)
	print(round(v1.xpos,2), round(v1.ypos,2), round(v1.xVelocity,2), round(v1.yVelocity,2), v1.acc, v1.angle )
	Time += 1
	xacc = v1.acc * math.sin(v1.angle*math.pi/180)
	yacc = v1.acc * math.cos(v1.angle*math.pi/180)
	v1.xpos = 0.5*xacc + v1.xVelocity + v1.xpos
	v1.ypos = 0.5*yacc + v1.yVelocity + v1.ypos

	v1.xVelocity += xacc 
	v1.yVelocity += yacc
	# canvas.move(v, v1.xVelocity, -v1.yVelocity)
	v = canvas.create_oval(v1.xpos, env['course'][1][1]-v1.ypos, v1.xpos+10, env['course'][1][1]-v1.ypos-10, fill = 'light blue')

	checker(v1, env)
	Tk.update()
	time.sleep(0.25)
	pass

Tk.mainloop()



