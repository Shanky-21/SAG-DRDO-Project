
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
import random
from datetime import datetime
import Priority_Queue
import os
import threading
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pandas as pd
import multiprocessing


global pq
pq = Priority_Queue.PriorityQueue()
global queue
queue = []

class Entity:
    def __init__(self):
        self.type_ = random.choice(["old-adult","adult","teen","child"])
        self.gender = random.choice(["male", "female"])
        self.step = self.step_time()
    def step_time(self):
        if self.type_ == "old-adult":
            return random.randint(3,6)
        elif self.type_ == "adult":
            return random.randint(1,5)
        elif self.type_ == "teen":
            return random.randint(1,2)
        else:
            return random.randint(1,3)
    def description(self):
        return [self.type_,self.gender,self.step]

class coordinates(Entity):
    def __init__(self):
        self.x = random.choice([-1, random.choice([-0.39, -0.35, -0.30, -0.28]),
                                 random.choice([0.07, 0.15, 0.20, 0.25, 0.30, 0.35, 0.45])])
        self.y = float("{:.2}".format(random.uniform(-0.24, 0.24)))
        Entity.__init__(self)
    def coor(self):
        return( (self.x, self.y, self.z))
    
    def data(self):
        return( [self.step, self.step, self.type_, self.gender, [self.x, self.y]])

# function to refresh priority ( Step Time )
def refresh():
    global pq
    global queue
    ind = []
    for i,ent in enumerate(pq.queue):
        if ent[0] >= .2:
            ent[0]-= .2
        else:
            ent[0] = 0
            queue.append(ent)
            pq.delete()
    
# To generate Entity ( Person on Road ) 
def entity_Generation():
    nums = random.randint(500,1000)
    print(nums)
    starttime = float("{:.2}".format(time.perf_counter()))
    for _ in range(nums):

        # Creating entity
        entity = coordinates()
        
        data =  entity.data()
        
        # Adding entity to priority queue
        pq.insert(data)
        if ((float("{:.2}".format(time.perf_counter())) -starttime)) % .2:       #Refreshing Priority Queue every 200 ms
            refresh()
        
        time.sleep(.2)
    
        
# Clear Screen 
def clearScreen():

    glClearColor(1.0, 1.0, 1.0, 1.0)

    gluOrtho2D(-1.0, 1.0,-1.0,1.0)

def keyPressed(*args):
    if args[0] == '\x1b':
        os.exit(1)
# Calculating The Pressure on Road
def pressure(q):
    c1, c2, c3, c4, c5, c6 = 0, 0, 0, 0, 0, 0
    for pt in q:
        if pt[-1][0] >= -0.95 and pt[-1][0] < -0.6:
            c1 += 1
        elif pt[-1][0] >= -0.6 and pt[-1][0] < -0.4:
            c2 += 1
        elif pt[-1][0]>-0.4 and pt[-1][0] < 0:
            c3 += 1
        elif pt[-1][0]>0 and pt[-1][0] < 0.07:
            c4 += 1
        elif pt[-1][0]> 0.07 and pt[-1][0] < 0.52:
            c5 += 1
        elif pt[-1][0]> 0.52 and pt[-1][0] < 0.80:
            c6 += 1
    return c1, c2, c3, c4, c5, c6

# Checking Whether Stampede Occurred or not      
def stampede(q):
    a, b, c, d, e, f = pressure(q)
    if a > 50:
        return [True, "section A"]
    elif b > 50:
        return [True, "Section B"]
    elif c > 50:
        return [True, "Section C"]
    elif d > 50:
        return [True, "Section D"]
    elif e > 50:
        return [True, "Section E"] 
    elif f > 50:
        return [True, "Section F"]
    else: return False, "NONE"

# Finding Clusters in Section - > Just for fun
def Clustering(data,b):
    sec = b
    X = []
    for i in data:
        X.append(i[-1])
    df = pd.DataFrame(X, columns = ['X', "Y"])
    Kmeans = KMeans(5)
    identified_clusters = Kmeans.fit_predict(df)
    data_with_clusters = df.copy()
    data_with_clusters['Clusters'] = identified_clusters
    plt.scatter(data_with_clusters["X"], data_with_clusters["Y"], c = data_with_clusters['Clusters'],cmap = 'rainbow')
    plt.xlim(-1.3, 1.3)
    plt.ylim(-0.5, 0.5)
    plt.annotate("Stampede = {}".format(b), xy=(-0.5,-0.5), xytext=(.96,.94), 
            xycoords="data", textcoords="axes fraction",
            bbox={'facecolor':'w','pad':5}, ha="right", va="top")
    plt.show()


# Main Function for Simulation
def main(pq_queue = None):
    
    global queue
    n = 10
    count = 0
    begin = time.time()
    while len(queue) > 0:

        glClear(GL_COLOR_BUFFER_BIT)

        glColor3f(0.0,0.0,0.0)

        glBegin(GL_LINES)        # GL_POINTS -> GL_LINES

        # Top line
        glVertex2f(-1.0, 0.25)
        glVertex2f(0.07, 0.25)
        
        glVertex2f(0.52, 0.25)
        glVertex2f(1.0, 0.25)
        
        glVertex2f(-0.37, 0.5)
        glVertex2f(0.07,0.25)
        
        glVertex2f(0.08, 0.5)
        glVertex2f(0.52, 0.25)        # Added another Vertex specifying end coordinates of line

        # Bottom Line

        glVertex2f(-1.0, -0.25)
        glVertex2f(-0.4,-0.25)

        glVertex2f(0,-0.25)
        glVertex2f(1,-0.25)

        glVertex2f(-0.4,-0.25)
        glVertex2f(-0.6, -0.45)

        glVertex2f(0, -0.25)
        glVertex2f(-0.21, -0.45)
        
        glEnd()
    

        #glColor3f(1.0, 0.0, 0.0)

        glPointSize(10.0)

        glBegin(GL_POINTS)
        glColor3f(1,0,0)

        for pt in queue:
            x,y = pt[-1]
            if pt[3] == "female":
                glColor3f(1,0,0)         # Female > Red Color
            else:
                glColor3f(0,0,1)         # Male > Blue Color

            glVertex2f(*pt[-1])
            if pt[0] <= 0:       
                pt[0] = pt[1]
                x += 0.06                # Movement
                if (x > 1):
                    queue.remove(pt)     # poping out of simulating Queue
                else:
                    pt[-1] = (x,y)
            else:
                pt[0] -= 1
        if (time.time() - begin) % 3:
            a,b = stampede(queue)        # Checking Stampede
            if a:
                print("Stampede Detected", b)
                glutLeaveMainLoop()
                #Clustering(queue,b)
                break

        glEnd()

        glFlush()

        time.sleep(1)
    else:
        print("out of loop")
        glutLeaveMainLoop()

# Creating Simulating Window
def window():
    print("In window")
    time.sleep(3)
    glutInit()
    glutInitDisplayMode(GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(100,100)
    glutCreateWindow("Real Time Stampede Detection")
    glutDisplayFunc(main)
    glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_GLUTMAINLOOP_RETURNS)
    glutKeyboardFunc(keyPressed)
    clearScreen()
    print("before glut mainloop")
    glutMainLoop()
    print("Back in glut Main Loop ")
    

# Main Python function
if __name__ == '__main__':
    begin = datetime.now()

    p1 = threading.Thread(target = entity_Generation)
    p2 = threading.Thread(target = window)
    

    p1.start()
    print("p1 started")

    p2.start()
    print("p2 started")

    p1.join()
    print("P1 over")
    p2.join()

    
    print("Done")
    
   
    end = datetime.now()
    print(end-begin)
