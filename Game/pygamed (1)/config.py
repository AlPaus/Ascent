
WIDTH = 480
HEIGHT = 270
FPS = 30
ANIM_SPEED = 120
PLAYER_HP = 100
PLAYER_SCALE = 0.08
MEASURE = int(WIDTH*PLAYER_SCALE)
PLAYER_SPEED = int(0.1316*MEASURE)
ROOM_SIZE = MEASURE * 12
IMMORTALITY_TIME = 500
JUMP_TIME = 800
JUMP_SPEED = 1.5
JUMP_CD = 4000



bean_shooter_cfg = {'ratio':0.042, 'max_ammo':15, 'damage':4, 'bullet_speed': 8, 'bullet_ratio':0.02, 'bullet_path':'resources/weapons/bean_shooter/bullet','rapidity' : 300,'bullet_ttl':3000,'reload':1500, 'path':'resources/weapons/bean_shooter','shift':[2,2]}
rocket_launcher_cfg = {'ratio':0.082, 'max_ammo':5, 'damage':30, 'bullet_speed': 5.5, 'bullet_ratio':0.032, 'bullet_path':'resources/weapons/rocket_launcher/bullet','rapidity' : 1500,'bullet_ttl':4000,'reload':2500, 'path':'resources/weapons/rocket_launcher', 'shift':[2,2],'effect':'explode1'}
enemy1_cfg = {'hp':100,'weapon':'bean_shooter','speed':2.5,'path':'resources/enemies/enemy1','ratio':0.1,'enemy_dist':MEASURE * 3.5,'reaction_time':500}
explode1_cfg = {'ratio':0.1,'path':'resources/effect/explode_1','anim_speed':85}

WEAPONS_CONF = {'bean_shooter':bean_shooter_cfg,"rocket_launcher":rocket_launcher_cfg}
ENEMIES_CONF = {'enemy1':enemy1_cfg}
EFFECTS_CONF = {'explode1':explode1_cfg}