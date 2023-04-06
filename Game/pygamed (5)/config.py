import pygame
import json

def get_value(str):
  str2 = ""
  i = 0
  while(str[i] != "="):
    i += 1
  i += 1
  while(str [i] == " "):
    i += 1
  while(i < len(str)):
    str2 += str[i]
    i +=1
  return str2
  
def get_name(str):
  str2 = ""
  i = 0
  while(str[i] != " "):
    str2 += str[i]
    i +=1
  return str2

def load_settings():
  with open('settings.json', 'r') as ex:
    d = json.load(ex)
  return d

S_DICT = load_settings()
  

# file = open('config.txt', 'r+')
FULLSCREEN = S_DICT['FULLSCREEN'] #bool(int(  get_value( file.readline() ) ))
WIDTH = S_DICT['WIDTH'] 
HEIGHT = S_DICT['HEIGHT'] 
FPS = S_DICT['FPS'] 
ANIM_SPEED = S_DICT['ANIM_SPEED'] 
PLAYER_HP = S_DICT['PLAYER_HP'] 
PLAYER_SCALE = S_DICT['PLAYER_SCALE'] 
MEASURE = int(WIDTH*PLAYER_SCALE)
PLAYER_SPEED = int(0.1316*MEASURE)
ROOM_SIZE = S_DICT['ROOM_SIZE'] 
IMMORTALITY_TIME = S_DICT['IMMORTALITY_TIME'] 
JUMP_TIME = S_DICT['JUMP_TIME'] 
JUMP_SPEED = S_DICT['JUMP_SPEED'] 
JUMP_CD = S_DICT['JUMP_CD'] 
SHOCKWAVE_CD = S_DICT['SHOCKWAVE_CD'] 
DEAD_BODY_TIME = S_DICT['DEAD_BODY_TIME']

BUTTONS = S_DICT
#BUTTONS = {}

#BUTTONS_NUM = 10
#for i in range(BUTTONS_NUM):
#    str = file.readline()
#    BUTTONS[get_name(str)] = int(get_value(str))
# print('BUTTON', chr(pygame.K_w), ord('w')) # 119
# print('SPACE', pygame.K_SPACE)
#file.close()


# FULLSCREEN = False
# WIDTH = 480
# HEIGHT = 270 
# FPS = 30
# ANIM_SPEED = 120
# PLAYER_HP = 100
# PLAYER_SCALE = 0.08
# MEASURE = int(WIDTH*PLAYER_SCALE)
# PLAYER_SPEED = int(0.1316*MEASURE)
# ROOM_SIZE = MEASURE * 12
# IMMORTALITY_TIME = 500
# JUMP_TIME = 800
# JUMP_SPEED = 1.5
# JUMP_CD = 4000
# SHOCKWAVE_CD = 5000



bean_shooter_cfg = {'ratio':0.042, 'max_ammo':15, 'damage':15, 'bullet_speed': MEASURE * 0.2105, 'bullet_ratio':0.02, 'bullet_path':'resources/weapons/bean_shooter/bullet','rapidity' : 300,'bullet_ttl':3000,'reload':1500, 'path':'resources/weapons/bean_shooter','shift':[2,2], 'sound':None}
bean_shooter_enemy_cfg = {'ratio':0.042, 'max_ammo':15, 'damage':8, 'bullet_speed': MEASURE * 0.2105, 'bullet_ratio':0.02, 'bullet_path':'resources/weapons/bean_shooter/bullet','rapidity' : 1000,'bullet_ttl':3000,'reload':1500, 'path':'resources/weapons/bean_shooter','shift':[2,2], 'sound':None,'lvl':1}
rocket_launcher_cfg = {'ratio':0.082, 'max_ammo':5, 'damage':30, 'bullet_speed': MEASURE * 0.14447, 'bullet_ratio':0.032, 'bullet_path':'resources/weapons/rocket_launcher/bullet','rapidity' : 1500,'bullet_ttl':4000,'reload':2500, 'path':'resources/weapons/rocket_launcher', 'shift':[2,2],'effect':'explode1', 'sound':None,'lvl':2}
shotgun_cfg = {'ratio':0.082, 'max_ammo':8, 'damage':12, 'bullet_speed': MEASURE * 0.2894, 'bullet_ratio':0.052, 'bullet_path':'resources/weapons/shotgun/bullet','rapidity' : 1200,'bullet_ttl':5000,'reload':1800, 'path':'resources/weapons/shotgun', 'shift':[2,2], 'sound':None,'lvl':2}
enemy1_cfg = {'hp':100,'weapon':'bean_shooter_enemy','speed':2.5,'path':'resources/enemies/enemy1','ratio':0.1,'enemy_dist':MEASURE * 3.5,'reaction_time':500,'value':2, 'sound':None}
enemy2_cfg = {'hp':200,'weapon':'shotgun','speed':2.5,'path':'resources/enemies/enemy2','ratio':0.1,'enemy_dist':MEASURE * 3.5,'reaction_time':10,'value':6, 'sound':None}
explode1_cfg = {'ratio':0.1,'path':'resources/effect/explode_1','anim_speed':45,'damage_wearoff':400, 'sound':None}
enemy_spawn_cfg = {'ratio':0.15,'path':'resources/effect/enemy_spawn','anim_speed':20,'damage_wearoff':400, 'sound':None}
WEAPONS_CONF = {'bean_shooter':bean_shooter_cfg,'bean_shooter_enemy':bean_shooter_enemy_cfg,"rocket_launcher":rocket_launcher_cfg,'shotgun':shotgun_cfg}
ENEMIES_CONF = {'enemy1':enemy1_cfg, 'enemy2':enemy2_cfg}
EFFECTS_CONF = {'explode1':explode1_cfg, 'enemy_spawn':enemy_spawn_cfg}

# BUTTONS = {'forward': pygame.K_w, 'left':pygame.K_a, 'back': pygame.K_s, 'right':  pygame.K_d, 'jump': pygame.K_SPACE, 'take_weapon': pygame.K_e, 'shockwave': pygame.K_f,'weapon1':  pygame.K_1, 'weapon2':  pygame.K_2, 'weapon_3': pygame.K_3}


def dump_settings(dict_to_dump: dict):
  with open('settings.json', 'w') as ex:
    json.dump(dict_to_dump, ex, indent=4)

    
# dtd = {
#   'FULLSCREEN': FULLSCREEN,
#   'WIDTH': WIDTH,
#   'HEIGHT': HEIGHT,
#   'FPS': FPS,
#   'ANIM_SPEED': ANIM_SPEED,
#   'PLAYER_HP': PLAYER_HP,
#   'PLAYER_SCALE': PLAYER_SCALE,
#   'MEASURE': MEASURE,
#   'PLAYER_SPEED': PLAYER_SPEED,
#   'ROOM_SIZE': ROOM_SIZE,
#   'IMMORTALITY_TIME': IMMORTALITY_TIME,
#   'JUMP_TIME': JUMP_TIME,
#   'JUMP_SPEED' : JUMP_SPEED,
#   'JUMP_CD' : JUMP_CD,
#   'SHOCKWAVE_CD' : SHOCKWAVE_CD
# }
# dtd.update(BUTTONS)

# dump_settings(dtd)


