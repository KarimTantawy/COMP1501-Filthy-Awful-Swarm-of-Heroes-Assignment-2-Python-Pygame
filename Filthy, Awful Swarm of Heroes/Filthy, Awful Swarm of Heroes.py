import pygame
import random
import sys
import math
import time
import os
import csv

# import the pygame constants (specifically the key codes and event types)
from pygame.locals import *

#load next level check
LOAD_LEVEL = False

#GAME STATES
CURRENT_STATE = 0
STATE_MAIN = 0
STATE_PLAY = 1
STATE_WAIT = 2 # setup the current level
STATE_LOAD = 3
STATE_CREDITS = 4

# constants for accessing the attributes of the mouse
MOUSE_LMB = 0
MOUSE_RMB = 1
MOUSE_X   = 2
MOUSE_Y   = 3

window_wid = 1280
window_hgt = 768
# the frame rate is the number of frames per second that will be displayed and although
# we could (and should) measure the amount of time elapsed, for the sake of simplicity
# we will make the (not unreasonable) assumption that this "delta time" is always 1/fps
frame_rate = 30
delta_time = 1 / frame_rate

# these are the colours through which the game objects can be "cycled"
included_colours = []
included_colours.append(Color(0, 0, 255))
included_colours.append(Color(0, 255, 0))
included_colours.append(Color(0, 255, 255))

# these are the unique identifiers for the game objects
object_unique_id = 1000

# this is the only game object included in the "toy" - rename it when5 you decide what
# these objects will represent within the "magic circle" of your final game submission
# and feel free to modify it as required, as long as you preserve the core mechanics 
class Swarm_Individual:

	def __init__(self):

		# get the next unique identifier and increment
		global object_unique_id
		self.id = object_unique_id
		object_unique_id += 1
	
		# the radius of the game object is fixed
		self.radius = 30
		
		# the initial colour is randomly selected and the "focus" flag is false
		self.colour = random.randint(0, len(included_colours) - 1)
		self.flag = False
		
		# (x, y) / (dx, dy) / (ddx, ddy) is the position / velocity / acceleration
		#self.x = random.randint(self.radius, window_wid - 1 - self.radius)
		#self.y = random.randint(self.radius, window_hgt - 1 - self.radius)
		self.x = 2000
		self.y = 2000
		angle = random.randint(0, 359)
		self.dx = math.cos(math.radians(angle)) * 0.1
		self.dy = math.sin(math.radians(angle))	* 0.1	
		self.ddx = 0
		self.ddy = 0

#### ====================================================================================================================== ####
#############										 INITIALIZE												   #############
#### ====================================================================================================================== ####
def initialize():
	screen = initialize_pygame()
	return initialize_data(screen)
	
def initialize_data(screen):
	level_size = 20*12
	
	game_data = {"screen": screen,
				"cur_color": random.randint(0, len(included_colours) - 1),
				"start_time": time.time(),
				"font": pygame.font.Font("assets/Minecraft.ttf", 30),
				"rats_left": 15,
				"skull": pygame.image.load("assets/skull.png"),
				"main_menu": [],
				"credits": pygame.image.load("assets/Credits.png"),
				"death_locations": [],
				"level_assets": [],
				"swarm": [],
				"level_settings": [],
				"current_level": 1, #remember to change to 0
				'is_open': True}
	
	game_data["main_menu"].append(pygame.image.load("assets/Main_Menu.png"))
	game_data["main_menu"].append(pygame.image.load("assets/Story.png"))
	game_data["main_menu"].append(pygame.image.load("assets/Controls.png"))
	game_data["main_menu"].append(pygame.image.load("assets/Tutorial.png"))
	
				
	for _ in range(level_size):
		game_data["level_assets"].append({"type": "wall",
									"location": [2000, 2000],
									 "size": (64, 64),
									 "sprite": pygame.image.load("assets/Wall-Main.png"),
									 "active": False})
									 
		game_data["level_assets"].append({"type": "side",
									"location": [2000, 2000],
									 "size": (64, 64),
									 "sprite": pygame.image.load("assets/Wall-Side.png"),
									 "active": False})
									 
		game_data["level_assets"].append({"type": "floor",
									 "location": [2000, 2000],
									 "size": (64, 64),
									 "sprite": pygame.image.load("assets/Floor-Main.png"),
									 "active": False})
									 
		game_data["level_assets"].append({"type": "background",
									 "location": [2000, 2000],
									 "size": (64, 64),
									 "sprite": pygame.image.load("assets/Background.png"),
									 "active": False})
		
	for _ in range(30):
		game_data["level_assets"].append({"type": "trap",
									"location": [2000, 2000],
									 "size": (64, 64),
									 "time": 0,
									 "delay": 100,
									 "delay_reset": 100,
									 "sprite": pygame.image.load("assets/SpikeTrap.png"),
									 "sprite_idle": pygame.image.load("assets/SpikeTrap.png"),
									 "sprite_active": pygame.image.load("assets/SpikeTrap-Active.png"),
									 "active": False})
									 
	game_data["level_assets"].append({"type": "wizard",
									 "location": [2000, 2000],
									 "velocity": [0, 0],
									 "size": (48, 48),
									 "attack": False,
									 "sprite": pygame.image.load("assets/wizard.png"),
									 "active": False})
	
	for _ in range(2):
		game_data["level_assets"].append({"type": "grug",
									 "location": [2000, 2000],
									 "velocity": [0, 0],
									 "size": (48, 48),
									 "attack": False,
									 "sprite": pygame.image.load("assets/Enemy1-Grug.png"),
									 "active": False})
		
		game_data["level_assets"].append({"type": "spider",
									 "location": [2000, 2000],
									 "velocity": [0, 0],
									 "size": (48, 48),
									 "attack": False,
									 "sprite": pygame.image.load("assets/Spider.png"),
									 "rotated_image": pygame.image.load("assets/Spider.png"),
									 "use_rotated": False,
									 "active": False})
									 
	game_data["level_assets"].append({"type": "exit",
									"location": [2000, 2000],
									 "size": (64, 64),
									 "sprite": pygame.image.load("assets/Door-Locked.png"),
									 "sprite_idle": pygame.image.load("assets/Door-Locked.png"),
									 "sprite_active": pygame.image.load("assets/Door-Unlocked.png"),
									 "can_pass": False,
									 "active": False})
	
	game_data["level_assets"].append({"type": "key",
									 "location": [2000, 2000],
									 "size": (32, 32),
									 "sprite": pygame.image.load("assets/Key.png"),
									 "active": False})
	
	for _ in range(15):
		game_data["swarm"].append({"type": "rat",
									 "game_object": Swarm_Individual(),
									 "location": [0, 0],
									 "size": (16, 16),
									 "sprite": pygame.image.load("assets/Swarm-Rat.png"),
									 "active": False})
	level_names = []
	level_names.append("Follow Me, Comrades")
	level_names.append("For The Greater Good, Comrade")
	level_names.append("Comrades!!!")
	level_names.append("Oh No, It's Grug!")
	level_names.append("Sneak Past Or Distract, Your Call!")
	level_names.append("I Thought He Was On Our Side?")
	level_names.append("There Are Two Of Him Now?")
	level_names.append("RUNNNNNNN!!!")
	level_names.append("Keep Going!")
	level_names.append("Almost There!")
	level_names.append("Almost There!")
	level_names.append("Finally, Comrades. We Have Him!")

	rats_required = []
	rats_required.append(15)
	rats_required.append(13)
	rats_required.append(10)
	rats_required.append(12)
	rats_required.append(8)
	rats_required.append(12)
	rats_required.append(11)
	rats_required.append(7)
	rats_required.append(6)
	rats_required.append(15)
	rats_required.append(15)
	rats_required.append(15)
	
	for i in range(12):
		game_data["level_settings"].append({"level": i+1,
									 "level_name": level_names[i],
									 "map": "assets/level_"+str(i+1)+".csv",
									 "items": "assets/level_"+str(i+1)+"_items.csv",
									 "rats_required": rats_required[i],
									 "time": 0.0,
									 "level_completed": False,
									 "cur_level": False})
				
	return game_data
	
def initialize_pygame():
	pygame.init()
	pygame.font.init()
	pygame.display.set_caption('Filthy, Awful Swarm of Heroes')
	pygame.key.set_repeat(1, 1)
	return pygame.display.set_mode((1280, 764))


#### ====================================================================================================================== ####
#############										   HELPER METHODS												#############
#### ====================================================================================================================== ####
def rotate_sprite(initial_image, position, angle):
	
	rotated_image = pygame.transform.rotate(initial_image, angle)
	
	rotated_rect = rotated_image.get_rect(center = position)
	
	return rotated_image, rotated_rect	
	
#### ====================================================================================================================== ####
#############										   INPUT												#############
#### ====================================================================================================================== ####

def get_all_inputs():

	# get the state of the mouse (i.e., button states and pointer position)
	mouse_dict = {}
	(mouse_dict[MOUSE_LMB], _, mouse_dict[MOUSE_RMB]) = pygame.mouse.get_pressed()
	(mouse_dict[MOUSE_X], mouse_dict[MOUSE_Y]) = pygame.mouse.get_pos()

	# get the state of the keyboard
	keybd_tupl = pygame.key.get_pressed()
		
	# look in the event queue for the quit event
	quit_ocrd = False
	for evnt in pygame.event.get():
		if evnt.type == QUIT:
			quit_ocrd = True

	# return all possible inputs
	return mouse_dict, keybd_tupl, quit_ocrd

def input(game_data, mouse_dict, keybd_tupl):
	if keybd_tupl[K_r]:
		#game_data["current_level"] += 1
		global CURRENT_STATE
		CURRENT_STATE = STATE_LOAD
		
	change_swarm_breakup(game_data, keybd_tupl)
	
	return
	
#############										  INPUT HANDLERS												   #############
#### ---------------------------------------------------------------------------------------------------------------------- ####
def change_swarm_breakup(game_data, keybd_tupl):
	cur_colour = 0
	next_colour = 0
	split = 0
	amount = 0
	flock = False
	
	if(keybd_tupl[K_a]):
		split = game_data["rats_left"]
	elif(keybd_tupl[K_s]):
		split = game_data["rats_left"] - 2
	elif(keybd_tupl[K_d]):
		split = game_data["rats_left"] // 2
	elif(keybd_tupl[K_f]):
		split = game_data["rats_left"] // 3
		amount = split
		flock = True
	
	if(split != 0):	
		for rat in game_data["swarm"]:
			if(rat["active"] == True):
				cur_colour = next_colour
				
				if(split <= 0):
					next_colour += 1
					if(flock):
						split = amount
					else:
						split = 50
				else:
					split -= 1
					
				rat["game_object"].colour = cur_colour
	
	return

#### ====================================================================================================================== ####
#############											UPDATE													#############
#### ====================================================================================================================== ####
	
def update(game_objects, game_data, mouse_dict):
	for ent in game_data["level_assets"]:
		if(ent["type"] == "trap" and ent["active"] == True):
			update_trap(game_data, ent)
		elif(ent["type"] == "key" and ent["active"] == True):
			update_key(game_data, ent)
		elif(ent["type"] == "exit" and ent["active"] == True and ent["can_pass"] == True):
			update_exit(game_data, ent)
		elif(ent["type"] == 'grug' and ent["active"] == True):
			update_enemy(game_data, ent, 3, 135, 13)
		elif(ent["type"] == 'spider' and ent["active"] == True):
			rot_enemy(ent, update_enemy(game_data, ent, 1, 192, 17))
		elif(ent["type"] == 'wizard' and ent["active"] == True):
			update_wizard(game_data, ent, 3, 160, 8)
			
	#REEEEEEEEEEEEEEEEEEEEEEEEMMMMMMMMMMMMMMMMMMMMMMMMMMMMMEEEEEEEEEEEEEEEEMMMMMMMMBERRRR THIS
	if(game_data["rats_left"] == 0):
		load_level(game_data)
	
	return update_swarm(game_objects, game_data, mouse_dict)

#############										  UPDATE HELPERS													#############
#### ---------------------------------------------------------------------------------------------------------------------- ####
def update_game_UI(game_data):
	
	timer = 0;
	
	for ent in game_data["level_settings"]:
		if(ent["level"] == game_data["current_level"]):
			ent["time"] = int(time.time() - game_data["start_time"])
			#timer, current level, level name, how many rats are left, rats required
			render_game_UI(game_data, ent["time"], ent["level"], ent["level_name"], game_data["rats_left"], ent["rats_required"])
	return

def rot_enemy(enemy, rat):
	if(rat != -1):
		angle = -(math.atan2(enemy["location"][1] - rat["location"][1], enemy["location"][0] - rat["location"][0])) * 180/math.pi + 270
		
		enemy["rotated_image"] = pygame.transform.rotate(enemy["sprite"], angle)
		enemy["use_rotated"] = True
	else:
		enemy["use_rotated"] = False

def update_enemy(game_data, enemy, required_rats, dist, speed):
	rats_in_range = 0
	close_rat = -1
	initial_rat = 0
	attack = False

	for rat in game_data["swarm"]:
		if(distance(rat, enemy) < dist*1.2):
			close_rat = rat
		if(distance(rat, enemy) < dist):
			if(rats_in_range == 0):
				initial_rat = rat
				rats_in_range += 1
			else:
				rats_in_range += 1
			
		if(has_collided(enemy, rat)):
				kill_rat(rat, game_data)
	
	if(rats_in_range >= required_rats):
		attack = True
		
	if(attack == True):
		delta_x = initial_rat["location"][0] - enemy["location"][0]
		delta_y = initial_rat["location"][1] - enemy["location"][1]
		magnitude = math.sqrt(delta_x ** 2 + delta_y ** 2)
								
		enemy["velocity"][0] = (enemy["velocity"][0] + (delta_x / magnitude) / 2) * speed
		enemy["velocity"][1] = (enemy["velocity"][1] + (delta_y / magnitude) / 2) * speed
			
		move_x = True
		move_y = True
		#check if any of the swarm is collding with a wall
		for m in game_data["level_assets"]:
			if((m["active"] == True) and (m["type"] == "wall" or m["type"] == "side")):
				if(will_clip(m, enemy, (delta_x, 0))):
					move_x = False
				elif(will_clip(m, enemy, (0, delta_y))):
					move_y = False

		# update the positions
		if(move_x == True):
			enemy["location"][0] += enemy["velocity"][0]
			
		enemy["velocity"][0] = 0
					
		if(move_y == True):
			enemy["location"][1] += enemy["velocity"][1]

		enemy["velocity"][1] = 0
		
	return close_rat

def update_wizard(game_data, enemy, required_rats, dist, speed):
	rats_in_range = 0
	close_rat = -1
	initial_rat = 0
	attack = False

	for rat in game_data["swarm"]:
		if(distance(rat, enemy) < dist*1.2):
			close_rat = rat
		if(distance(rat, enemy) < dist):
			if(rats_in_range == 0):
				initial_rat = rat
				rats_in_range += 1
			else:
				rats_in_range += 1
			
		if(has_collided(enemy, rat)):
			enemy["active"] = False
			game_data["death_locations"].append(enemy["location"])
			enemy["location"] = [2000, 2000]
			return
	
	if(rats_in_range >= required_rats):
		attack = True
		
	if(attack == True):
		delta_x = initial_rat["location"][0] - enemy["location"][0]
		delta_y = initial_rat["location"][1] - enemy["location"][1]
		magnitude = math.sqrt(delta_x ** 2 + delta_y ** 2)
								
		enemy["velocity"][0] = (enemy["velocity"][0] + (delta_x / magnitude) / 2) * speed
		enemy["velocity"][1] = (enemy["velocity"][1] + (delta_y / magnitude) / 2) * speed
			
		move_x = True
		move_y = True
		#check if any of the swarm is collding with a wall
		for m in game_data["level_assets"]:
			if((m["active"] == True) and (m["type"] == "wall" or m["type"] == "side")):
				if(will_clip(m, enemy, (-delta_x, 0))):
					move_x = False
				elif(will_clip(m, enemy, (0, -delta_y))):
					move_y = False

		# update the positions
		if(move_x == True):
			enemy["location"][0] -= enemy["velocity"][0]
			
		enemy["velocity"][0] = 0
					
		if(move_y == True):
			enemy["location"][1] -= enemy["velocity"][1]

		enemy["velocity"][1] = 0
		
	return close_rat

def distance(cur, tar):
	return math.sqrt((cur["location"][0] - tar["location"][0])**2 + 
	(cur["location"][1] - tar["location"][1])**2)

def kill_rat(rat, game_data):
	rat["active"] = False
	game_data["death_locations"].append(rat["location"])
	game_data["rats_left"] -= 1
	rat["location"] = [2000, 2000]
	rat["game_object"].x = 2000
	rat["game_object"].y = 2000
				
def update_exit(game_data, exit):
	global LOAD_LEVEL
	for rat in game_data["swarm"]:
		if(has_collided(exit, rat)):
			for cur_lev in game_data["level_settings"]:
				if(cur_lev["level"] == game_data["current_level"] and 
				game_data["rats_left"] >= cur_lev["rats_required"] and LOAD_LEVEL == False):
					print("loading")
					LOAD_LEVEL = True
					level_complete(game_data, cur_lev)
					break

def level_complete(game_data, cur_lev):
	global CURRENT_STATE
	print(cur_lev["time"])
	game_data["current_level"] += 1
	CURRENT_STATE = STATE_LOAD
			
def update_key(game_data, key):
	for rat in game_data["swarm"]:
		if(has_collided(key, rat)):
				key["active"] = False
				key["location"] = [2000, 2000]
				for ent in game_data["level_assets"]:
					if(ent["type"] == "exit"):
						ent["sprite"] = ent["sprite_active"]
						ent["can_pass"] = True
						
	
def update_trap(game_data, trap):
	if(time.time() - trap["time"] < trap["delay"]):
		trap["delay"] -= time.time() - trap["time"]
		trap["sprite"] = trap["sprite_idle"]
	else:
		for rat in game_data["swarm"]:
			if(has_collided(trap, rat)):
				trap["sprite"] = trap["sprite_active"]
				kill_rat(rat, game_data)
				trap["time"] = time.time()
				trap["delay"] = trap["delay_reset"]
			
	
def update_swarm(game_objects, game_data, mouse_dict):
	# visit all the game objects...
	if mouse_dict[MOUSE_LMB]:
		game_data["cur_color"] = (game_data["cur_color"] + 1) % len(included_colours)		
	elif(mouse_dict[MOUSE_RMB]):
		for sw in game_data["swarm"]:
			if(sw["active"] == True):
				swarm_additive_x = 0
				swarm_additive_y = 0
				
				object = sw["game_object"]

				sw["location"][0] = object.x-32
				sw["location"][1] = object.y
						
				if object.colour == game_data["cur_color"]:
							
					delta_x = pygame.mouse.get_pos()[0] - object.x
					delta_y = pygame.mouse.get_pos()[1] - object.y
					magnitude = math.sqrt(delta_x ** 2 + delta_y ** 2)
								
					object.dx = object.dx + (delta_x / magnitude) / 2
					object.dy = object.dy + (delta_y / magnitude) / 2
			
				
					#make it look more like a swarm
					swarm_additive_x = random.randint(-3, 3)
					swarm_additive_y = random.randint(-3, 3)
				
				dx = object.dx*15+swarm_additive_x
				dy = object.dy*15+swarm_additive_y
				move_x = True
				move_y = True
				#check if any of the swarm is collding with a wall
				for m in game_data["level_assets"]:
					if((m["active"] == True) and (m["type"] == "wall" or m["type"] == "side")):
						if(will_clip(m, sw, (dx, 0))):
							move_x = False
						elif(will_clip(m, sw, (0, dy))):
							move_y = False
							
				# update the positions
				if(move_x == True):
					object.x += dx
					object.dx = 0
				else:
					object.dx = 0
					
				if(move_y == True):
					object.y += dy
					object.dy = 0
				else:
					object.dy = 0
			
	return game_objects
	
def has_collided(cur, tar):
	c_x1 = cur["location"][0]
	c_y1 = cur["location"][1]
	c_x2 = cur["location"][0]+cur["size"][0]
	c_y2 = cur["location"][1]+cur["size"][1]
	
	t_x1 = tar["location"][0]
	t_y1 = tar["location"][1]
	t_x2 = tar["location"][0]+(cur["size"][0]*0.6)
	t_y2 = tar["location"][1]+(cur["size"][1]*0.6)
	
	if t_x1 > c_x2 or t_x2 < c_x1 or t_y1 > c_y2 or t_y2 < c_y1:
		return False
		
	return True

def will_clip(cur, tar, tar_vel):
	c_x1 = cur["location"][0]
	c_y1 = cur["location"][1]
	c_x2 = cur["location"][0]+cur["size"][0]
	c_y2 = cur["location"][1]+cur["size"][1]
	
	t_x1 = tar["location"][0]+tar_vel[0]
	t_y1 = tar["location"][1]+tar_vel[1]
	t_x2 = tar["location"][0]+tar_vel[0]+(cur["size"][0]*0.6)
	t_y2 = tar["location"][1]+tar_vel[1]+(cur["size"][1]*0.6)
	
	if t_x1 > c_x2 or t_x2 < c_x1 or t_y1 > c_y2 or t_y2 < c_y1:
		return False
		
	return True
	
#### ====================================================================================================================== ####
#############											RENDER													#############
#### ====================================================================================================================== ####

def render(game_data, game_objects):
	global CURRENT_STATE
	''' Central Render function. Calls helper functions to render various views.
	Input: game_data Dictionary
	Output: None
	'''
	if(game_data["current_level"] > len(game_data["level_settings"])):
		CURRENT_STATE = STATE_CREDITS
		return
		
	render_level(game_data)
	render_swarm(game_data, game_objects)
	render_skulls(game_data)
	
	if(CURRENT_STATE == STATE_PLAY):
		update_game_UI(game_data)

#############										  RENDER HELPERS													#############
#### ---------------------------------------------------------------------------------------------------------------------- ####

def render_main_menu(game_data, entity):
	''' Replace this and the return statement with your code '''
	return

	
def render_skulls(game_data):
	for loc in game_data["death_locations"]:
		game_data["screen"].blit(game_data["skull"], (loc[0], loc[1]))
		
def render_game_UI(game_data, timer, cur_level, level_name, rats_left, rats_required):
	padding = 18
	
	font = game_data["font"]
	
	surface = font.render(str(cur_level)+". "+level_name, False, (255, 255, 255))
	center = window_wid//2-(surface.get_rect().width//2)-padding*3
	game_data["screen"].blit(surface, (center, padding))
	
	surface = font.render("Time: " + str(timer), False, (255, 255, 255))
	game_data["screen"].blit(surface, (padding*5, padding))

	colour = (255, 255, 255)
	
	for cur_lev in game_data["level_settings"]:
		if(cur_lev["level"] == game_data["current_level"]):
			if(cur_lev["rats_required"] > game_data["rats_left"]):
				colour = (255, 0, 0)
	
	surface = font.render(str(rats_left) + " / " + str(rats_required) + " Rats Needed", False, colour)
	center = window_wid-(surface.get_rect().width)-padding*5
	game_data["screen"].blit(surface, (center, padding))
	
def render_swarm(game_data, game_objects):
	render_current_color_on_cursor(game_data, game_objects)
	# draw each of the game objects and encircle the one that is flagged
	for s in game_data["swarm"]:
		
		pygame.draw.circle(game_data["screen"], included_colours[s["game_object"].colour], (int(s["game_object"].x), 
		int(s["game_object"].y+12)), 7)
			
		if s["game_object"].flag:
			pygame.draw.circle(game_data["screen"], Color(0, 0, 0), (int(s["game_object"].x), 
			int(s["game_object"].y+20)), s["game_object"].radius, 2)
		
		game_data["screen"].blit(s["sprite"], (s["game_object"].x-32, s["game_object"].y))
		
def render_current_color_on_cursor(game_data, game_objects):
		pygame.draw.circle(game_data["screen"], included_colours[game_data["cur_color"]], (pygame.mouse.get_pos()[0], 
		pygame.mouse.get_pos()[1]-10), 7)
		
def render_level(game_data):
	for asset in game_data["level_assets"]:
		if(asset["active"] == True and asset["type"] == "spider"):
			if(asset["use_rotated"] == True):
				game_data["screen"].blit(asset["rotated_image"], (asset["location"][0], asset["location"][1]))
			else:
				game_data["screen"].blit(asset["sprite"], (asset["location"][0], asset["location"][1]))
		elif(asset["active"] == True and asset["type"] != "spider"):
			game_data["screen"].blit(asset["sprite"], (asset["location"][0], asset["location"][1]))
	
#############										  LOAD ASSETS AND LEVEL													#############
#### ---------------------------------------------------------------------------------------------------------------------- ####
def load_level(game_data):
	global LOAD_LEVEL
	
	game_data["start_time"] = time.time()
	game_data["death_locations"] = []
	game_data["rats_left"] = 15
	
	for asset in game_data["level_assets"]:
		asset["location"] = [2000, 2000]
		asset["active"] = False
		
		if(asset["type"] == "exit"):
			asset["sprite"] = asset["sprite_idle"]
			asset["can_pass"] = False
		elif(asset["type"] == "grug" or asset["type"] == "spider"):
			asset["attack"] = False
	#should be 20x12
	
	level = ""
	items = ""
	
	for lev_set in game_data["level_settings"]:
		if(lev_set["level"] == game_data["current_level"]):
			level = read_csv(lev_set["map"])
			items = read_csv(lev_set["items"])
	
	x = 0
	y = 0
	
	min_x = 32
	max_x = 96
	min_y = -70
	max_y = 16
	
	for row in items:
		x = 0
		for pos in row:
			if(pos == 'r'):
				for obj in game_data["swarm"]:
					obj["game_object"].x = random.randint(x+min_x, x+max_x)
					obj["game_object"].y = random.randint(y+min_y, y+max_y)
					obj["active"] = True
			elif(pos == 't'):
				for asset in game_data["level_assets"]:
					if(asset["type"] == "trap" and asset["active"] == False):
							asset["location"] = [x, y]
							asset["active"] = True
							break
			elif(pos == 'k'):
				for asset in game_data["level_assets"]:
					if(asset["type"] == "key" and asset["active"] == False):
							asset["location"] = [x, y]
							asset["active"] = True
							break
			elif(pos == 'e'):
				for asset in game_data["level_assets"]:
					if(asset["type"] == "exit" and asset["active"] == False):
							asset["location"] = [x, y]
							asset["active"] = True
							break
			elif(pos == 'g'):
				for asset in game_data["level_assets"]:
					if(asset["type"] == "grug" and asset["active"] == False):
							asset["location"] = [x, y]
							asset["active"] = True
							break
			elif(pos == 'p'):
				for asset in game_data["level_assets"]:
					if(asset["type"] == "spider" and asset["active"] == False):
							asset["location"] = [x, y]
							asset["active"] = True
							break
			elif(pos == 'm'):
				for asset in game_data["level_assets"]:
					if(asset["type"] == "wizard" and asset["active"] == False):
							asset["location"] = [x, y]
							asset["active"] = True
							break
			x += 64
		y += 64	
	
	y = 0
	x = 0
	
	for row in level:
		x = 0
		for pos in row:
			if(pos == 'b'):
				for asset in game_data["level_assets"]:
					if(asset["type"] == "background" and asset["active"] == False):
						asset["location"] = [x, y]
						asset["active"] = True
						break
			elif(pos == 'w'):
				for asset in game_data["level_assets"]:
					if(asset["type"] == "wall" and asset["active"] == False):
						asset["location"] = [x, y]
						asset["active"] = True
						break
			elif(pos == 'f'):
				for asset in game_data["level_assets"]:
					if(asset["type"] == "floor" and asset["active"] == False):
						asset["location"] = [x, y]
						asset["active"] = True
						break
			elif(pos == 's'):
				for asset in game_data["level_assets"]:
					if(asset["type"] == "side" and asset["active"] == False):
						asset["location"] = [x, y]
						asset["active"] = True
						break
			x += 64
		y += 64
	
	render_level(game_data)
	LOAD_LEVEL = False
	
	return

def read_csv(file_name):

	result = []

	csvfile = open(file_name)
	delim = ','

	reader = csv.reader(csvfile, delimiter = delim)
	
	for row in reader:
		result.append(row);
	
	return result	
	
#### ====================================================================================================================== ####
#############											 MAIN													 #############
#### ====================================================================================================================== ####
	
def main():
	global CURRENT_STATE
	#Remember to remove
	CURRENT_STATE = STATE_MAIN
	
	cur_main = 0
	ignore_tmr = 0
	
	game_data = initialize();
	# create a clock
	clock = pygame.time.Clock()

	game_objects = []
	for i in game_data["swarm"]:
		game_objects.append(i["game_object"])
	
	game_data["screen"].fill(Color(32, 70, 49))
	
	# the game loop is a postcondition loop controlled using a Boolean flag
	closed_flag = False
	while game_data["is_open"]:

		#HANDLE INPUT
		mouse_dict, keybd_tupl, closed_flag = get_all_inputs()
		
		#CHECK IF PLAYER WANTS TO CLOSE
		if keybd_tupl[pygame.K_ESCAPE]:
			game_data["is_open"] = False

			
		if(CURRENT_STATE == STATE_MAIN):
			if cur_main < len(game_data["main_menu"]):
				game_data["screen"].blit(game_data["main_menu"][cur_main], (0, 0))
				
				if ignore_tmr > 0:
					ignore_tmr = max(ignore_tmr - delta_time, 0)
					keybd_tupl = tuple([0] * 323)
				elif(keybd_tupl[pygame.K_SPACE]):
					ignore_tmr = 1
					cur_main += 1
			else:
				CURRENT_STATE = STATE_LOAD
				
		elif(CURRENT_STATE == STATE_PLAY):
			if(keybd_tupl[K_r]):
				print("Restarting Level")
				CURRENT_STATE = STATE_LOAD
				
			input(game_data, mouse_dict, keybd_tupl)
			game_objects = update(game_objects, game_data, mouse_dict)
			render(game_data, game_objects)
			#print("WAITING")
		elif(CURRENT_STATE == STATE_LOAD):
			load_level(game_data)
			CURRENT_STATE = STATE_PLAY
		elif(CURRENT_STATE == STATE_CREDITS):
			print("credits")
			game_data["screen"].blit(game_data["credits"], (0, 0))
		
		# update the display and enforce the minimum frame rate
		pygame.display.update()
		clock.tick(frame_rate)

		
if __name__ == "__main__":
	main()
