import pygame
import numpy as np
import random
import random as rd
pygame.init()
width,height=500,500
screen=pygame.display.set_mode((width,height))
game_over=False
clock=pygame.time.Clock()
fps=70
posx=0
posy=0
grid=2
maxpop=1000
x=[]
y=[]
for p in range(0,width,grid):
    x.append(p)
for p in range(0, height, grid):
    y.append(p)



class Snake:
    def __init__(self,weights1,weights2):
        self.weights1=weights1
        self.weights2=weights2
        self.lost=False
        self.score=0
        self.livetime=0
        self.dist=0
        self.posx=x[random.randint(0,len(x)-1)]#must be grid divisible
        self.posy=y[random.randint(0,len(y)-1)]#must be grid divisible
        self.body = [[self.posx, self.posy]]
        self.fx=random.randint(1, (width // grid )- 1) * grid#must be grid divisible
        self.fy=random.randint(1, (width // grid )- 1) * grid#must be grid divisible
        self.died=False
        self.energy=(height+width)//grid#must be grid divisible
    def draw(self,input_data,input_data2):
        hiden_layer_output = input_data.dot(self.weights1)
        final_output = hiden_layer_output.dot(self.weights2)
        big=max(final_output)
        self.livetime+=1
        if self.livetime>self.energy:
            self.died=True
            self.lost=True
        self.firstone=True
        click=0
        for i in range(4):
            if big==final_output[i]:
                click=i
        if big==0:
            self.firstone=False

        if self.firstone:
            if click==0:
                self.xdirection=0
                self.ydirection=-1
                self.posy += grid * self.ydirection

            if click==1:
                self.xdirection = 0
                self.ydirection = +1
                self.posy += grid * self.ydirection


            if click==2:
                self.xdirection = -1
                self.ydirection = 0
                self.posx += grid * self.xdirection

            if click==3:
                self.xdirection = 1
                self.ydirection = 0
                self.posx += grid * self.xdirection


        else:
            hiden_layer_output = input_data2.dot(self.weights1)
            final_output = hiden_layer_output.dot(self.weights2)
            big = max(final_output)

            self.firstone = True
            click = 0
            for i in range(4):
                if big == final_output[i]:
                    click = i

            if click==0:#left corner up
                self.xdirection=-1
                self.ydirection=-1
                self.posy += grid * self.ydirection
                # self.posx += grid * self.xdirection

            if click==1:#right corner up
                self.xdirection = 1
                self.ydirection = -1
                self.posy += grid * self.ydirection
                # self.posx += grid * self.xdirection


            if click==2:# left corner down
                self.xdirection = -1
                self.ydirection = 1
                self.posx += grid * self.xdirection
                # self.posy += grid * self.ydirection

            if click==3:
                self.xdirection = 1
                self.ydirection = 1
                self.posx += grid * self.xdirection
                # self.posy += grid * self.ydirection
            #
        # self.posx+=grid*self.xdirection
        # self.posy+=grid*self.ydirection
        def draw_snake(body):
            for pos in body:
                # pygame.draw.rect(screen,(0,0,0),(pos[0],pos[1],grid,grid))
                pygame.draw.rect(screen, (0, 0, 0), (pos[0], pos[1], grid, grid))  # snake
        draw_snake(self.body)
                # screen.blit(snimg, (pos[0], pos[1]))
        pygame.draw.rect(screen, (255, 0, 0), (self.fx, self.fy, grid, grid))#food



def weight_generator():
    weight1 = np.array(
        [[random.random(), random.random(), random.random(), random.random()],
         [random.random(), random.random(), random.random(), random.random()],
         [random.random(), random.random(), random.random(), random.random()],
         [random.random(), random.random(), random.random(), random.random()],
         # [random.random(), random.random(), random.random(), random.random(), random.random(), random.random(), random.random(), random.random()],
         # [random.random(), random.random(), random.random(), random.random(), random.random(), random.random(), random.random(), random.random()],
         # [random.random(), random.random(), random.random(), random.random(), random.random(), random.random(), random.random(), random.random()],
         # [random.random(), random.random(), random.random(), random.random(), random.random(), random.random(), random.random(), random.random()]
         ]).T
    weight2 = np.array(
        [[random.random(), random.random(), random.random(), random.random()],
         [random.random(), random.random(), random.random(), random.random()],
         [random.random(), random.random(), random.random(), random.random()],
         [random.random(), random.random(), random.random(), random.random()]
         ]).T
    return weight1,weight2

def populate(maxpop):
    generationlist=[]
    for i in range(maxpop):
        weights1,weights2=weight_generator()
        tempsnake=Snake(weights1,weights2)
        generationlist.append(tempsnake)
    return generationlist
snakes=populate(maxpop)

def reproduction(pre_gen):
    #fitness
    fitnesslist = []
    for i in range(len(pre_gen)):
        fitnesslist.append(pre_gen[i].score)
    # top3 selection
    top3 = []
    for i in range(3):
        top3.append(pre_gen[fitnesslist.index(max(fitnesslist))])
        fitnesslist[fitnesslist.index(max(fitnesslist))] = -1
    generationlist=[]
    champions = 0
    for i in range(len(pre_gen) - champions):
        while True:
            rd1 = rd.randint(0, len(top3) - 1)
            rd2 = rd.randint(0, len(top3) - 1)
            if rd1 != rd2:
                break
            else:
                break

        mutationprob = 2
        md = rd.randint(0, 10)
        # learning_rate = 0.01
        mutaion_will_happen = False
        if md < mutationprob:
            mutaion_will_happen = True

        parent1 = top3[rd1]
        parent2 = top3[rd2]
        w1 = []
        for j in parent1.weights1.T:
            w1.append(list(j))
        w2 = []
        for j in parent2.weights1.T:
            w2.append(list(j))
        wlength = len(w1)
        part1 = wlength // 2
        result_weight1list = w1[0:part1] + w2[part1:wlength]
        # mutation 1

        if mutaion_will_happen:
            ft=1

            for m in range(random.randint(4,15)):
                result_weight1list[rd.randint(0, len(result_weight1list) - 1)][
                rd.randint(0, len(result_weight1list[0]) - 1)] += rd.random()*ft
                if m%2==0:
                    ft=-1
                else:
                    ft=1



            # result_weight1list[rd.randint(0, len(result_weight1list) - 1)][
            #     rd.randint(0, len(result_weight1list[0]) - 1)] = rd.random()
            # result_weight1list[rd.randint(0, len(result_weight1list) - 1)][rd.randint(0,len(result_weight1list[0])-1)] =rd.random()
            # result_weight1list[rd.randint(0, len(result_weight1list) - 1)][rd.randint(0,len(result_weight1list[0])-1)] =rd.random()

        result_weight1array = np.array(result_weight1list).T

        hw1 = []
        for j in parent1.weights2.T:
            hw1.append(list(j))
        hw2 = []
        for j in parent2.weights2.T:
            hw2.append(list(j))
        hwlength = len(w1)
        hpart1 = hwlength // 2
        hresult_weight1list = hw1[0:hpart1] + hw2[hpart1:hwlength]
        # mutaion 2
        if mutaion_will_happen:
            hresult_weight1list[rd.randint(0, len(hresult_weight1list) - 1)][
                rd.randint(0, len(hresult_weight1list[0]) - 1)] = rd.random()
            hresult_weight1list[rd.randint(0, len(hresult_weight1list) - 1)][
                rd.randint(0, len(hresult_weight1list[0]) - 1)] = rd.random()
            hresult_weight1list[rd.randint(0, len(hresult_weight1list) - 1)][rd.randint(0,len(hresult_weight1list[0])-1)] = rd.random()
            # hresult_weight1list[rd.randint(0, len(hresult_weight1list) - 1)][rd.randint(0,len(hresult_weight1list[0])-1)] += 0.01
        hresult_weight1array = np.array(hresult_weight1list).T

        # child creation
        child = Snake(result_weight1array, hresult_weight1array)
        generationlist.append(child)
    # for i in top3:
    #     generationlist.append(i)
    top3[0].score=0

    # generationlist.append(top3[0])
    # generationlist.append(top3[1])

    return generationlist





def show_text(gen_no,score):
    font = pygame.font.Font('freesansbold.ttf', 15)
    text = font.render(f' Generation: {gen_no} , best score: {score} ', True, (0, 180, 0))
    textRect = text.get_rect()
    textRect.center = (235,30)
    screen.blit(text, textRect)





fx, fy = random.randint(1, (width // grid )- 1) * grid, random.randint(1, (height // grid)-1) * grid

scoreincrease=0
timer=0
seconds=3
checkpoint=0
delay=3
death=0
genno=1
scoreboard=[0]
update=False
highestscore=0
# print("gen: 1")
while not game_over:
    screen.fill((255,255,255))
    for events in pygame.event.get():
        if events.type==pygame.QUIT:
            game_over=True

    def draw_food():
        pygame.draw.rect(screen,(255,0,0),(fx,fy,grid,grid))


    def draw_snake():
        global scoreincrease,death
        for i in range(len(snakes)):
            inputlist=[0,0,0,0]
            if snakes[i].posy==snakes[i].fy:#horizontal
                if snakes[i].posx<snakes[i].fx:
                    #food is in left
                    inputlist[2]=((snakes[i].posx-snakes[i].fx)**2 + (snakes[i].posy-snakes[i].fy)**2)**(1/2)
                else:
                    #food is in right
                    inputlist[3] = ((snakes[i].posx - snakes[i].fx) ** 2 + (snakes[i].posy - snakes[i].fy) ** 2) ** (1 / 2)
            if snakes[i].posx==snakes[i].fx:#vertical
                if snakes[i].posy<snakes[i].fy:
                    #food is in up
                    inputlist[0] = ((snakes[i].posx - snakes[i].fx) ** 2 + (snakes[i].posy - snakes[i].fy) ** 2) ** (1 / 2)
                else:
                    #food is in down
                    inputlist[1] = ((snakes[i].posx - snakes[i].fx) ** 2 + (snakes[i].posy - snakes[i].fy) ** 2) ** (1 / 2)

            # distance from walls/sides
            # inputlist[4]=snakes[i].posy#up
            # inputlist[5]=height-snakes[i].posy
            # inputlist[6]=snakes[i].posx
            # inputlist[7]=width-snakes[i].posx
            inputlist2=[0,0,0,0]
            if snakes[i].posx>snakes[i].fx:
                #the food is in in left side
                inputlist2[0]=((snakes[i].posx-snakes[i].fx)**2 + (snakes[i].posy-snakes[i].fy)**2)**(1/2)
            if snakes[i].posx<snakes[i].fx:
                #the food is in in right side
                inputlist2[1]=((snakes[i].posx-snakes[i].fx)**2 + (snakes[i].posy-snakes[i].fy)**2)**(1/2)
            if snakes[i].posy>snakes[i].fy:
                #the food is in in up side
                inputlist2[2]=((snakes[i].posx-snakes[i].fx)**2 + (snakes[i].posy-snakes[i].fy)**2)**(1/2)
            if snakes[i].posy<snakes[i].fy:
                #the food is in in up side
                inputlist2[3]=((snakes[i].posx-snakes[i].fx)**2 + (snakes[i].posy-snakes[i].fy)**2)**(1/2)


            #lost checking
            if snakes[i].posx>=width or snakes[i].posy<0 and not snakes[i].lost:
                snakes[i].lost=True
                snakes[i].dist=((snakes[i].posx-snakes[i].fx)**2 + (snakes[i].posy-snakes[i].fy)**2)**(1/2)
                scoreboard.append(snakes[i].score)

            if snakes[i].posy>=height or snakes[i].posx<0 and not snakes[i].lost:
                snakes[i].lost=True
                snakes[i].dist = ((snakes[i].posx - snakes[i].fx) ** 2 + (snakes[i].posy - snakes[i].fy) ** 2) ** (1 / 2)
                scoreboard.append(snakes[i].score)


            ##eatchecking
            if snakes[i].posy==snakes[i].fy and snakes[i].posx==snakes[i].fx and not snakes[i].lost:
                scoreincrease+=1
                snakes[i].score+=1
                snakes[i].fx, snakes[i].fy = random.randint(1, (width // grid) - 1) * grid, random.randint(1, (height // grid) - 1) * grid
                snakes[i].energy+=(height+width)//grid
                snakes[i].body.reverse()
                snakes[i].body.append([snakes[i].posx, snakes[i].posy])
                snakes[i].body.reverse()



            # #death cheaking by energy-lost/starving
            # if snakes[i].died:
            #     snakes



            #drawing on the screen if not lost
            if not snakes[i].lost and not snakes[i].died:
                snakes[i].draw(np.array(inputlist),np.array(inputlist2))
                snakes[i].livetime+=1
                snakes[i].body.insert(0, [snakes[i].posx, snakes[i].posy])
                snakes[i].body.pop()
                # death cheaking by energy-lost/starving
            # if snakes[i].died:





    # draw_food()
    draw_snake()

    def isalldied(snakes):
        count=0
        sboard = []
        global highestscore
        highestscore=0
        for i in snakes:
            if i.lost:
                count+=1
            sboard.append(i.score)
        # print(len(sboard))
        try:
             highestscore=max(sboard)
        except:
            highestscore=0
        if count==len(snakes):
            return True
        return False
    overlap=False
    if isalldied(snakes):
        tempsnake=snakes
        del snakes
        highestscore = 0
        snakes=reproduction(tempsnake)
        del tempsnake
        timer=0
        death=0
        genno+=1
        # print('all died')
        # print("gen: ", genno,"max score: ",max(scoreboard))
        scoreboard=[]
        overlap=True
        checkpoint=0



    show_text(genno,highestscore)
    pygame.display.update()
    timer+=1
    clock.tick(fps)
pygame.quit()
print("highest score: ",highestscore)