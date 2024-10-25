#import threading # run functions in parallel 
app.level = 1 
counter_label = Label(0,20,20, size=30)
app.finish_label = Label("You Won", 200,200, size=50, visible=False)
counter_label.toBack()
app.start = False

how_label = Label("Use the keys w,a,s,d to navigate the obstacle course. Avoid touching the red", 200,200,size=11.5)
how_label2 = Label("and get to each check point. Press the mouse to continue.", 200,230, size=12)
label3 = Label("Inspired by The Worlds Hardest Game", 200,250,size=10)

class walls():
    def __init__(self, *rects):
        self.rects = rects
        for rect in self.rects:
            rect.fill = "red"
    
    def hits_rects(self, object):
        for rect in self.rects:
            if rect.hitsShape(object) and rect.visible == True:
                return True
                
    def visible(self, vis):
        for rect in self.rects:
            rect.visible = vis
            
class check_points():
    def __init__(self, *rects):
        self.rects = list(rects)
        for rect in self.rects:
            rect.fill = "green"
            rect.toBack()
            rect.checked = False
        
    def hits_check_point(self, player):
        for rect in self.rects:
            if rect.visible:
                if rect.hitsShape(player):
                    rect.fill = "limeGreen"
                    rect.checked = True
                    return True, rect.centerX, rect.centerY
                else:
                    rect.fill = "Green"
        return "_"
        
    def is_Complete(self):
        check = 0 
        for rect in self.rects:
            if rect.checked == True:
             check += 1 
        if check == len(self.rects):
            return True
            
    def visible(self, vis):
        for rect in self.rects:
            rect.visible = vis
    
class player():
    def __init__(self, start_pos): # [x,y]
        self.start_pos = start_pos
        self.player = Rect(self.start_pos[0], self.start_pos[1], 20,20,fill="blue")
    
    def return_player(self):
        return self.player
    
    def player_reset(self):
        self.player.centerX = self.start_pos[0]
        self.player.centerY = self.start_pos[1]
    
    def new_start_pos(self, x,y):
        self.start_pos[0] = x
        self.start_pos[1] = y
        
    def update(self, keys):
        for key in keys:
            key = key.lower()
            if key == "w":
                self.player.centerY -= 2
            elif key == "s":
                self.player.centerY += 2 
            elif key == "a":
                self.player.centerX -= 2 
            elif key == "d":
                self.player.centerX += 2 
                
class circles():
    def __init__(self, *circles_pos): # (X,Y,X,Y, direction) The direction arg can either be True or False and it must be in a list or tuple
        self.circles_pos = list(circles_pos)
        self.circles = [Circle(circle_pos[0], circle_pos[1],5,fill="red") if circle_pos[4] == True
        else Circle(circle_pos[2], circle_pos[3],5,fill="red") for circle_pos in self.circles_pos]
        
        self.directionsX = [False for i in range(len(self.circles_pos))]
        self.directionsY = [False for i in range(len(self.circles_pos))]
        
    def visible(self, vis):
        for circle in self.circles:
            circle.visible = vis
            
    def is_visible(self):
        return self.circles[0].visible
    
    def hits_circle(self, object):
        for circle in self.circles:
            if circle.hitsShape(object) and circle.visible == True:
                return True
    
    def all(self):
        return self.circles_pos, sefl.circles
    
    def update(self):
        directionsX = self.directionsX
        directionsY = self.directionsY
        circles = self.circles
        circles_pos = self.circles_pos
        for i in range(len(circles)):
            # X
            if not circles_pos[i][2] == circles_pos[i][0]:
                if circles_pos[i][2] < circles[i].centerX:
                    directionsX[i] = False
                elif circles_pos[i][0] > circles[i].centerX:
                    directionsX[i] = True
                if directionsX[i] == False:
                    circles[i].centerX -= 1 
                if directionsX[i] == True:
                    circles[i].centerX += 1 
            # Y
            if not circles_pos[i][1] == circles_pos[i][3]:
                if circles_pos[i][1] > circles[i].centerY:
                    directionsY[i] = False
                if circles_pos[i][3] < circles[i].centerY:
                    directionsY[i] = True
                if directionsY[i] == True:
                    circles[i].centerY -= 1
                if directionsY[i] == False:
                    circles[i].centerY += 1 
                
app.player = player([20,360])
class level_1():
    def __init__(self):   # Initialize obsticale course
        app.c_level = circles((160,340,430,340,False), (160,375,430,375, False), 
        (160,350,430,360,True), (80,80,360,80,True),
        (0,160,400,160,True), (40, 200, 360, 200, True), (40, 160, 360, 160, False))
        app.w_level = walls(Rect(0,0,400,3), Rect(0,0,3,400), Rect(0, 397, 400,400), Rect(397,0,400,400),
        Rect(0,320,370,10), Rect(30,240,400,10))
        app.check_point = check_points(Rect(350,270,30,30), Rect(345,25,30,30))
        
    def remove(self):
        app.c_level.visible(False)
        app.w_level.visible(False)
        app.check_point.visible(False)
        app.c_level = None
        app.check_point = None
        app.level += 1 
        
class level_2():
    def __init__(self):
        ...
    
    def remove(self):
        ...

class level_3():
    def __init__(self):
        ...
    
    def remove(self):
        ...

if app.level == 1 and app.start == True:
    app.level1 = level_1()

def level1_function():
    app.c_level.update()
    
    checkP = app.check_point.hits_check_point(app.player.return_player())
    if checkP[0] == True:
        app.player.new_start_pos(checkP[1], checkP[2])
        
    if (app.w_level.hits_rects(app.player.return_player()) == True or 
    app.c_level.hits_circle(app.player.return_player()) == True):
        app.player.player_reset()
        counter_label.value += 1 
    if app.check_point.is_Complete() == True:
        print("level 2 ")
        app.level1.remove()
        app.finish_label.visible = True
        
def onStep():
    if app.start == True:
        if app.level == 1:
            level1_function()
        
def onKeyHold(keys):
    app.player.update(keys)

def onMousePress(mx,my):
    if app.start == False and app.level == 1:
        app.level1 = level_1()
        how_label.visible = False
        how_label2.visible = False
        label3.visible = False
        app.player.player_reset()
        app.start = True
        
        
