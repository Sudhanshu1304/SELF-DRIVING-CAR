import numpy as np
import matplotlib.pyplot as plt
import time
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color,Line
from kivy.config import Config
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.image import Image
from AI11 import Dqn

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

last_x = 0
last_y = 0
n_points = 0
length = 0


brain = Dqn(6,3,0.9)
action2rotation = [0,20,-20]
last_reward = 0
scores = []


first_update = True
Explore=10
T=4
time_keeper=0
container=[]
def init():
    #global Explore
    global sand
    global goal_x
    global goal_y
    global del_t
    global t0
    global TR,flag
    global action

    action=0
    flag=0
    sand = np.zeros((longueur,largeur))
    goal_x = 20
    goal_y = largeur - 20
    t0=time.time()
    del_t=0
    TR=0
    first_update = False

last_distance = 0


class Car(Widget):

    angle = NumericProperty(0)
    rotation = NumericProperty(0)
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y) # velocity vector
    sensor1_x = NumericProperty(0)
    sensor1_y = NumericProperty(0)
    sensor1 = ReferenceListProperty(sensor1_x, sensor1_y)
    sensor2_x = NumericProperty(0)
    sensor2_y = NumericProperty(0)
    sensor2 = ReferenceListProperty(sensor2_x, sensor2_y)
    sensor3_x = NumericProperty(0)
    sensor3_y = NumericProperty(0)
    sensor3 = ReferenceListProperty(sensor3_x, sensor3_y)
    signal1 = NumericProperty(0)
    signal2 = NumericProperty(0)
    signal3 = NumericProperty(0)

    def move(self, rotation):
        val=20
        self.pos = Vector(*self.velocity) + self.pos
        self.rotation = rotation
        self.angle = self.angle + self.rotation
        self.sensor1 = Vector(35, 0).rotate(self.angle) + self.pos # updating the position of sensor 1
        self.sensor2 = Vector(35, 0).rotate((self.angle+90)%360) + self.pos # updating the position of sensor 2
        self.sensor3 = Vector(35, 0).rotate((self.angle-90)%360) + self.pos # updating the position of sensor 3
        self.signal1 = int(np.sum(sand[int(self.sensor1_x)-val:int(self.sensor1_x)+val, int(self.sensor1_y)-val:int(self.sensor1_y)+val]))/400. # getting the signal received by sensor 1 (density of sand around sensor 1)
        self.signal2 = int(np.sum(sand[int(self.sensor2_x)-val:int(self.sensor2_x)+val, int(self.sensor2_y)-val:int(self.sensor2_y)+val]))/400. # getting the signal received by sensor 2 (density of sand around sensor 2)
        self.signal3 = int(np.sum(sand[int(self.sensor3_x)-val:int(self.sensor3_x)+val, int(self.sensor3_y)-val:int(self.sensor3_y)+val]))/400. # getting the signal received by sensor 3 (density of sand around sensor 3)
        ###print("Values of signals  ",self.signal1,self.signal2,self.signal3)
        if self.sensor1_x > longueur-10 or self.sensor1_x<10 or self.sensor1_y>largeur-10 or self.sensor1_y<10: # if sensor 1 is out of the map (the car is facing one edge of the map)
            self.signal1 = 1.
        if self.sensor2_x > longueur-10 or self.sensor2_x<10 or self.sensor2_y>largeur-10 or self.sensor2_y<10: # if sensor 2 is out of the map (the car is facing one edge of the map)
            self.signal2 = 1.
        if self.sensor3_x > longueur-10 or self.sensor3_x<10 or self.sensor3_y>largeur-10 or self.sensor3_y<10: # if sensor 3 is out of the map (the car is facing one edge of the map)
            self.signal3 = 1.



class Sensor3(Widget):
    angle=NumericProperty(0)
    def move3(self, rotation):
        self.center = self.pos
        self.rotation = rotation
        self.angle = self.angle + self.rotation


class Sensor2(Widget):
    angle=NumericProperty(0)
    def move2(self,rotation):
        self.center=self.pos
        self.rotation=rotation
        self.angle = self.angle + self.rotation


class Sensor1(Widget):
    angle=NumericProperty(0)
    def move1(self,rotation):
        self.center=self.pos
        self.rotation=rotation
        self.angle = self.angle + self.rotation

class Game(Widget):
    car = ObjectProperty(None)
    sensor_1 = ObjectProperty(None)
    sensor_2 = ObjectProperty(None)
    sensor_3 = ObjectProperty(None)

    def serve_car(self):
        self.car.center = self.center
        self.car.velocity = Vector(6, 0)

    def update(self, dt):

        global t0
        global Explore
        global brain
        global last_reward
        global scores
        global last_distance
        global goal_x
        global goal_y
        global longueur
        global largeur
        global first_update
        global del_t
        global TR,flag
        global action
        global T,time_keeper
        global container

        GR=0
        #TR=0
        PR=0
        DR=0
        WR=0
        LE=0
        RE=0
        BE=0
        UE=0

        longueur = self.width
        largeur = self.height
        if first_update==True:
            init()
            first_update=False

        t2=time.time()

        if((int(t2)-int(t0))%2==0):
            del_t=del_t+1

        xx = goal_x - self.car.x
        yy = goal_y - self.car.y
        orientation = Vector(*self.car.velocity).angle((xx,yy))/180.

        self.sensor_1.color=(1,0,0,1)

        last_signal = [self.car.signal1, self.car.signal2, self.car.signal3, orientation, -orientation,last_reward]
        action = brain.update(last_reward, last_signal)
        scores.append(brain.score())
        l_x=self.car.x
        l_y=self.car.y
        rotation = action2rotation[action]
        self.car.move(rotation)

        self.sensor_1.move1(rotation)
        self.sensor_2.move2(rotation)
        self.sensor_3.move3(rotation)

        distance = np.sqrt((self.car.x - goal_x)**2 + (self.car.y - goal_y)**2)
        self.sensor_1.pos = self.car.sensor1
        self.sensor_2.pos = self.car.sensor2
        self.sensor_3.pos = self.car.sensor3



        if sand[int(self.car.x),int(self.car.y)] > 0:
            self.car.velocity = Vector(1, 0).rotate(self.car.angle)
            last_reward = -2
            WR=-3
        else:
            self.car.velocity = Vector(6, 0).rotate(self.car.angle)
            if (flag==0):
                if distance < last_distance:

                    DR=0.1
                    last_reward = DR
                else:
                    PR=-0.2
                    last_reward=PR

            if (del_t > 3):
                last_reward = -0.01
                del_t=0
                TR=TR-0.02
                time_keeper = time_keeper + 0.02

        if self.car.x < 10:
            self.car.x = 10
            last_reward = -1
            LE=-1
        if self.car.x > self.width-10:
            self.car.x = self.width-10
            last_reward = -1
            RE=-1
        if self.car.y < 10:
            self.car.y = 10
            last_reward = -1
            BE=-1
        if self.car.y > self.height-10:
            self.car.y = self.height-10
            last_reward = -1
            UE=-1



        print('\nTR is : ',TR,"   ",Explore,"    ",T)

        # This Part Tries That The Car Is Not At the Same Position For A Long Time

        if (TR <= 0 and TR >-2.0):
            brain.T = Explore
        elif(TR<=-2.0 and TR>-3.0):
            brain.T = Explore
            PR=0.1
            DR=-0.2
            flag=1
        elif(TR<-3.0 and TR>-4.0):
            PR=0.1
        elif(TR<=-5.0):
            brain.T=Explore
            TR=0
        else:
            brain.T = 100
            flag=0

        container.append([last_reward,last_signal])

        if distance < 100:
            if(T>time_keeper):

                T=time_keeper
                if (len(container)>50):
                    del container[0]
                for i in range(len(container)):


                    brain.update(container[i][0],container[i][1])
            else:
                container=[]
            TR=0
            time_keeper = 0
            del_t=0

            goal_x = self.width - goal_x
            goal_y = self.height - goal_y
        last_distance = distance


class MyPaintWidget(Widget):

    def on_touch_down(self, touch): # putting some sand when we do a left click
        global length,n_points,last_x,last_y

        with self.canvas:
            Color(0.18,0.8,0.44)
            d=10.
            touch.ud['line'] = Line(source="car_img3.png",points = (touch.x, touch.y), width = 10)# It is a Dictionary To store the the Dta of Line and can be use in other modules
            #touch.ud['Rect'] = Rectangle(pos=(touch.x, touch.y), size=(30,30))
            last_x = int(touch.x)#+10
            last_y = int(touch.y)#+10
            n_points = 0
            length = 0
            cx=int(touch.x)
            cy=int(touch.y)

            sand[int(touch.x), int(touch.y)] = 1


    def on_touch_move(self, touch): # putting some sand when we move the mouse while pressing left
        global length,n_points,last_x,last_y
        if touch.button=='left':

            touch.ud['line'].points += [touch.x, touch.y]
            x = int(touch.x)
            y = int(touch.y)

            length += np.sqrt(max((x - last_x)**2 + (y - last_y)**2, 2))
            n_points += 1.
            density = n_points/(length)
            touch.ud['line'].width = int(20*density + 1)
            sand[int(touch.x) - 10 : int(touch.x) + 10, int(touch.y) - 10 : int(touch.y) + 10] = 1
            last_x = x
            last_y = y


class CarroApp(App):

    img = Image(source="house1.png")
    school=Image(source="school1.png")

    def build(self): # building the app

        parent = Game()
        parent.serve_car()
        Clock.schedule_interval(parent.update, 1.0 / 60.0)
        self.painter = MyPaintWidget()

        size=(80,80)
        clearbtn = Button(text='clear',size=size)
        savebtn = Button(text='save',pos=(parent.width,0),size=size)
        loadbtn = Button(text='load',pos=(2*parent.width,0),size=size)

        exp_down=Button(text="Explore Less",pos=(Window.size[0]-100,Window.size[1]-60),size=(100,60))
        exp_more = Button(text="Explore More", pos=(Window.size[0] - 200, Window.size[1] - 60), size=(100, 60))
        th_reset=Button(text="TH Reset",pos=(Window.size[0] - 300, Window.size[1] - 60), size=(100, 60))

        self.img.pos = (Window.size[0] - self.img.width,10)
        self.school.pos=(10,Window.size[1]-self.school.height)

        clearbtn.bind(on_release=self.clear_canvas)
        savebtn.bind(on_release=self.save)
        loadbtn.bind(on_release=self.load)
        exp_down.bind(on_release=self.Explor_Down)
        exp_more.bind(on_release=self.Explor_Up)
        th_reset.bind(on_release=self.Timer_Reset)

        parent.add_widget(self.painter)
        parent.add_widget(exp_down)
        parent.add_widget(exp_more)
        parent.add_widget(clearbtn)
        parent.add_widget(savebtn)
        parent.add_widget(loadbtn)
        parent.add_widget(th_reset)
        parent.add_widget(self.img)
        parent.add_widget(self.school)

        return parent


    def Timer_Reset(self,obj):

        global T,time_keeper,container
        #container=[] # Helps in Selecting Best Actions
        time_keeper=0
        T=4
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^          ", T)

    # To Increase The Accuracy In Selection
    def Explor_Up(self,obj):

        global Explore
        if(Explore>10):
            Explore=Explore-10
        else:
            Explore=10

    # To Increase The EXPLORATION

    def  Explor_Down(self,obj):
        global Explore
        if(Explore<100):
            Explore=Explore+10
        else:
            Explore=100


    def clear_canvas(self, obj): # clear button
        global sand
        self.painter.canvas.clear()
        sand = np.zeros((longueur,largeur))

    def save(self, obj): # save button
        print("saving brain...")
        brain.save()
        plt.plot(scores)
        plt.show()

    def load(self, obj): # load button
        print("loading last saved brain...")
        brain.load()

# Running the app
if __name__ == '__main__':
    '''
    a = multiprocessing.Process(target=CarroApp)
    b = multiprocessing.Process(target=CarroApp)
    #obj2=CarroApp()
    ##obj.run()
    #print('###########################################################################################################')
    #obj2.run()
    a.start()
    print("@############")
    b.start()
    '''
    CarroApp().run()
