# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5

# globals for game objects
SHIP_ANGULAR_VELOCITY = 0.1
SHIP_LINEAR_VELOCITY = 0.4
SHIP_DECELERATION = 0.98

# globals for keyboard events


class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2013.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(angle):
    return [math.cos(angle), math.sin(angle)]

def distance(p,q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image

        # cannot import copy so create new object to store info
        self.image_info = ImageInfo(info.get_center(), 
                                    info.get_size(), 
                                    info.get_radius(), 
                                    info.get_lifespan(), 
                                    info.get_animated())
        
    def draw(self,canvas):
        if self.thrust:
            # get the second image from image map.
            image_center = list(self.image_info.get_center())
            image_center[0] += self.image_info.get_size()[0]
            canvas.draw_image(ship_image, 
                              image_center, 
                              self.image_info.get_size(), 
                              my_ship.pos, 
                              self.image_info.get_size(), 
                              self.angle)
        else:
            canvas.draw_image(ship_image, 
                              self.image_info.get_center(), 
                              self.image_info.get_size(), 
                              my_ship.pos, 
                              self.image_info.get_size(), 
                              self.angle)

    def update(self):
        
        # update angle based on angular velocity
        self.angle += self.angle_vel
        
        # update velocity based on angle
        if self.thrust:
            vector = angle_to_vector(self.angle)
            self.vel[0] += SHIP_LINEAR_VELOCITY * vector[0]
            self.vel[1] += SHIP_LINEAR_VELOCITY * vector[1]
        
        # update velocity based on friction
        self.vel[0] *= SHIP_DECELERATION
        self.vel[1] *= SHIP_DECELERATION
        
        # update position based on velocity
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        # wrap around the edges
        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT
    
    def set_thrust(self,thrust):
        self.thrust = thrust
        if thrust:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()
            
    def fire_missle(self):
        global a_missile
        vector = angle_to_vector(self.angle)
        pos_gun = list(self.pos)
        pos_gun[0] += vector[0] * self.image_info.get_radius()
        pos_gun[1] += vector[1] * self.image_info.get_radius()
        vel_gun = list(self.vel)
        vel_gun[0] += vector[0] * 10
        vel_gun[1] += vector[1] * 10
        a_missile = Sprite(pos_gun, vel_gun, 0, 0, missile_image, missile_info, missile_sound)

       
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.age = 0
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image

        # cannot import copy so create new object to store info
        self.image_info = ImageInfo(info.get_center(), 
                                    info.get_size(), 
                                    info.get_radius(), 
                                    info.get_lifespan(), 
                                    info.get_animated())
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        #canvas.draw_circle(self.pos, self.image_info.get_radius(), 1, "Red", "Red")
        canvas.draw_image(self.image, 
                          self.image_info.get_center(), 
                          self.image_info.get_size(), 
                          self.pos, 
                          self.image_info.get_size(), 
                          self.angle)
    
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]        

        # wrap around the edges
        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT
           
def draw(canvas):
    global time
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()
    
    # display score
    canvas.draw_text("Lives Remaining: %d" % lives, [10, 30], 20, "White")
    canvas.draw_text("Current Score: %d" % score, [WIDTH - 160, 30], 20, "White")

    
# timer handler that spawns a rock    
def rock_spawner():
    global a_rock
    position = [random.random() * WIDTH, random.random() * HEIGHT]
    velocity = [random.randrange(-3,1) + random.randrange(1,3), random.randrange(-3,1) + random.randrange(1,3)]
    angle = random.random() * 2 * math.pi
    angle_velocity = random.randrange(-10,10) / float(100)
    a_rock = Sprite(position, velocity, angle, angle_velocity, asteroid_image, asteroid_info)

# keydown handler
def keydown_handler(key):
    
    # todo: problem when both left and right arrows are pressed
    if key == simplegui.KEY_MAP['left']:
        my_ship.angle_vel = -SHIP_ANGULAR_VELOCITY
    elif key == simplegui.KEY_MAP['right']:
        my_ship.angle_vel = SHIP_ANGULAR_VELOCITY
    elif key ==  simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.fire_missle()

def keyup_handler(key):

    # todo: problem when both left and right arrows are pressed
    if key == simplegui.KEY_MAP['left'] or key == simplegui.KEY_MAP['right']:
        my_ship.angle_vel = 0
    elif key ==  simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
a_missile = Sprite([WIDTH / 3, HEIGHT / 3], [0,0], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keyup_handler(keyup_handler)
frame.set_keydown_handler(keydown_handler)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
