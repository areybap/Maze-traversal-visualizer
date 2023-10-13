import random as random
import sys
import math
import time
import os

#ANSI escape codes for colors, for maze
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
BLACK = "\033[30m"
BRIGHT_WHITE = "\033[97m"
RESET = "\033[0m"

#ANSI 256 escape codes for player pointers
colors = [

    "\033[32m",         # GREEN
    "\033[38;5;214m",   # ORANGE
    "\033[35m",         # MAGENTA
    "\033[38;5;14m",    # CYAN
    "\033[38;5;52m",    # DARK RED
    "\033[38;5;136m",   # BOLD_ORANGE
    "\033[38;5;148m",   # BOLD_GREEN
    "\033[93m",         # BOLD_YELLOW
    "\033[38;5;17m",    # BOLD_BLUE
    "\033[95m",         # BOLD_MAGENTA
    "\033[38;5;142m",   # GOLD
    "\033[38;5;8m"      # LIGHT_GRAY
]

maze = [

    ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
    ['1','S','0','0','0','0','0','0','0','0','0','0','0','0','1','0','0','0','0','0','0','0','0','0','1','0','0','0','0','0','0','0','0','0','1','0','0','0','0','0','1'],
    ['1','1','1','1','1','1','1','0','1','1','1','1','1','0','1','1','1','1','1','0','1','1','1','0','1','1','1','1','1','1','1','1','1','0','1','0','1','0','1','1','1'],
    ['1','0','0','0','0','0','0','0','1','0','0','0','1','0','0','0','1','0','0','0','1','0','1','0','0','0','0','0','1','0','0','0','0','0','1','0','1','0','0','0','1'],
    ['1','0','1','1','1','1','1','1','1','1','1','0','1','1','1','0','1','0','1','1','1','0','1','1','1','1','1','0','1','0','1','1','1','1','1','0','1','1','1','0','1'],
    ['1','0','0','0','0','0','1','0','0','0','0','0','0','0','1','0','0','0','1','0','0','0','0','0','0','0','0','0','1','0','0','0','0','0','0','0','0','0','1','0','1'],
    ['1','1','1','1','1','0','1','1','1','0','1','1','1','1','1','1','1','1','1','0','1','1','1','1','1','1','1','0','1','1','1','1','1','1','1','1','1','1','1','0','1'],
    ['1','0','0','0','1','0','0','0','1','0','0','0','0','0','0','0','0','0','1','0','1','0','0','0','0','0','1','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
    ['1','0','1','0','1','1','1','0','1','1','1','1','1','1','1','1','1','0','1','0','1','0','1','1','1','0','1','1','1','1','1','1','1','1','1','0','1','1','1','1','1'],
    ['1','0','1','0','0','0','0','0','1','0','0','0','1','0','0','0','1','0','1','0','1','0','1','0','0','0','1','0','0','0','1','0','0','0','0','0','1','0','0','0','1'],
    ['1','0','1','1','1','1','1','1','1','0','1','0','1','0','1','0','1','0','1','0','1','0','1','0','1','0','1','0','1','0','1','0','1','1','1','0','1','0','1','0','1'],
    ['1','0','1','0','0','0','0','0','1','0','1','0','0','0','1','0','1','0','0','0','1','0','1','0','1','0','0','0','1','0','1','0','0','0','1','0','0','0','1','0','1'],
    ['1','0','1','0','1','1','1','0','1','0','1','1','1','1','1','0','1','1','1','1','1','0','1','0','1','1','1','1','1','0','1','1','1','1','1','0','1','1','1','0','1'],
    ['1','0','1','0','0','0','1','0','0','0','1','0','0','0','0','0','0','0','0','0','0','0','1','0','0','0','0','0','1','0','0','0','0','0','0','0','1','E','0','0','1'],
    ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']
]


knownwalls=[(0,0)]                       #did not use this, but will be faster if used, my idea was to pass on known walls for every generation
dead_end_walls=[(0,0)]                   #dead end walls for dead end penalty, coordinate will be added id a player reaches deadend

def checkstartend(maze):
    start = (0,0)
    end = (0,0)

    #to iterate through maze and find S,E
    for x, row in enumerate(maze):
        for y, value in enumerate(row):
            if value == "S":
                start = (x, y)
            elif value == "E":
                end = (x, y)

    #return S,E or error
    if (start == end):
      print("maze error")
      sys.exit()
    else:
      return start, end

def display_maze_final(maze, path):
#to display final path

    m2 = [row[:] for row in maze]      #shallow copy is giving bad results eventhough algoriyhm works fine
    '''m2=m[:]'''

    #mark "green ██" for cell in trail
    for x, y in path:
        m2[x][y] = GREEN + "██" + RESET


    x, y = path[-1]             #set current x,y as last element in path
    m2[x][y] = YELLOW + "██" +  RESET           #set current x,y as in X

    # Apply character replacements and construct the draw string to print maze
    draw = ""
    for row in m2:
        for element in row:

            if element == "1":
                draw += BLACK + "██" + RESET
            elif element == "0":
                draw += BRIGHT_WHITE + "██" + RESET
            elif element == "S":
                draw += BLUE + "██" + RESET
            elif element == "E":
                draw += RED + "██" + RESET
            else:
                draw += str(element)

        draw += "\n"

    print(draw)



def display_maze(maze, path):
#to display player points with above colors

    m2 = [row[:] for row in maze]      #shallow copy is giving bad results eventhough algoriyhm works fine
    '''m2=m[:]'''

    color_index = 0  # Initialize the color index to the first color

    #assign colors to  "██"for cell in trail
    for x, y in path:
        color = colors[color_index]  # Get the current color
        m2[x][y] = color + "██" + RESET

        # Increment the color index and wrap around if needed
        color_index = (color_index + 1) % len(colors)
    

    '''for x, y in path:
        m2[x][y] = GREEN + "██" + RESET'''

    # Apply character replacements and construct the draw string to print maze
    draw = ""
    for row in m2:
        for element in row:

            if element == "1":
                draw += BLACK + "██" + RESET
            elif element == "0":
                draw += BRIGHT_WHITE + "██" + RESET
            elif element == "S":
                draw += BLUE + "██" + RESET
            elif element == "E":
                draw += RED + "██" + RESET
            else:
                draw += str(element)

        draw += "\n"

    print(draw)



#check if the (x,y) is a dead end, if dead end, append to dead end list
def is_dead_end(x, y):
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    wall_count = 0  # Count of neighboring cells with value 1
    if maze[x][y]=='0':
        for dx, dy in dirs:
            new_x, new_y = x + dx, y + dy
            if maze[new_x][new_y] == "1":
                wall_count+=1

    if wall_count == 3:  #if 3 walls then dead end, append in dead end
        dead_end_walls.append((x, y))
        return True
    else:
        return False




class Player:

    def __init__(self, player_id, maze):
        self.victory= False
        self.path = [(1,1)]
        self.id = player_id
        self.fitness=0
        self.spawn=(1,1)
        self.goal=(13,37)


    def movement(self):

        stop=False
        dirs=[(0,1),(0,-1),(1,0),(-1,0)]
        count=0
        while stop == False:

            (x,y) = self.path[-1]
            dir=random.choice(dirs)                      #selects a random direction
            new_x,new_y = x+dir[0], y+dir[1]             #set newx, newy as x+dx, y+dy
 
            #if (newx, newy) goal then set player.victory== true, stop the movement loop
            if (new_x == self.goal[0] and new_y==self.goal[1]):     
                #print('Solution found')
                self.path.append((new_x,new_y))
                self.victory=True
                stop = True
                #exit
                
                
            '''print(self.path, end="->")
                print(self.fitness)
                self.victory == True
                #sys.exit()'''
            
              
            #if (newx,newy) dead end, add dead end penalty 1000 to player.fitness
            if is_dead_end(new_x, new_y):
                if (new_x,new_y) == self.goal:
                    self.victory= True

                else:
                    self.fitness+=1000
                    stop == True
                    
            #if (newx,newy) already in path continue, if wall then stop program, add penalty 200, if 0 continue add to path, continue while
            if (new_x,new_y) in self.path:   #if (new_x,new_y) in self.path and know_walls: for faster exec
                continue
            elif maze[new_x][new_y] == "1":
                stop = True
                self.fitness+=200
                #knownwalls.append((new_x,new_y)) for faster execution but no truely genetic i suppose
            elif (new_x,new_y) not in self.path and maze[new_x][new_y] == "0" and (0 <= new_x < len(maze) and 0 <= new_y < len(maze[0])):
                self.path.append((new_x,new_y))


    #calls movement, after player moves, calculates fitness, i,e. euclidean distance
    def eval_fitness(self,maze):  #remove maze
        self.movement()
        (x, y) = self.path[-1]
        dx = x - self.goal[0]
        dy = y - self.goal[1]
        euclidean_distance = math.sqrt(dx ** 2 + dy ** 2)
        self.fitness += euclidean_distance



    #because iam taking coordinate as path, most of them will either overlap or would  be completely disjoint
    #it would be meaningless to do child = parent_1[:cross_over_point_1] + parent_2[cross_over_point_1:] or something similar
    
    def crossover(self,mate):   #function call parent1.crossovers(parent2) to give child player
                   
        child=Player(self.id, maze)

        #if parent1.path==child1.path, used multiple conditions, for increase diversity
        if self.path == mate.path:
            
            i=random.random()            
            if i<0.4:                           #40% chance for child=80%parent
                if(len(self.path)>3):
                    index=80*len(self.path)//100 #integer division
                    child.path=self.path[:index]

            elif 0.4<i<0.9:                     #50% chance for child=100%parent
                child.path=self.path

            else:                               #10% chance for child=any%parent
                index= random.randint(0,len(self.path)-1)
                child.path=self.path[:index]


        #commonpathcords, stores list of coordinates that are presesnt in parent1,parent2
        commonpathcords = []
        # Iterate through lista and check if each element exists in listb
        for index, element in enumerate(self.path):
            if element in mate.path:
                commonpathcords.append(index)

        #if parent1.fitness<parent2.fitness in sorted population
        #then parent1.path lies in parent2.path
        #therefore child=parent1    

        if mate.fitness < self.fitness:
            #index1=80*len(self.path)//100
            #commonpathcords= list(set(self.path).intersection(set(mate.path)))
            index=commonpathcords[-1]
            #if
            child.path=self.path[:index]


        elif mate.fitness > self.fitness:
            #commonpathcords= list(set(self.path).intersection(set(mate.path)))

            index=commonpathcords[-1]
            child.path=mate.path[:index]

        #to ensure crossover is not empty, add (1,1)
        if(len(child.path))==0:
                child.path=[(1,1)]
        return child


    #mutate changes child.path into child.path[:index]
    def mutate(self):
        #if random.random()<0.2:
            if len(self.path)<2:
                return self.path
            else:
                index = random.randint(0,len(self.path)-1)
                self.path=self.path[:index]

            if(len(self.path)==0):
                self.path=[(1,1)]




class Genetic():

    population=[]
    unique_players=[]
    bestPlayer = 0

    def __init__(self, noofgen, popsize, mutationrate, start, goal, maze, inputs):
        self.noofgen = noofgen
        self.gen = 0
        self.popsize = popsize
        self.mutatonrate = mutationrate
        self.start = start
        self.goal = goal
        self.victory = False
        self.inputs = inputs
        self.maze=maze
        self.initPopulation(maze)

    #is called when genetic class is initialized, initalizes population
    def initPopulation(self,maze):
        pop=[Player(i,maze) for i in range(self.popsize)]
        for player in pop:
            player.eval_fitness(maze)
        self.population=pop
        self.result(maze)

    #for every player assign id
    def idassign(self):                                  
        id=1
        for player in self.population:
            player.id=id
            id+=1

    #for every player call eval fitness
    def movefit(self,maze):                     
        for player in self.population:
            player.eval_fitness(maze)

    #performs cross over
    #breed is selection and crossover
    #here we are using unique players beacause, normal crossover generates same player paths, for increasing diversity
    def breed(self):
        for player in self.population:
        # Check if player.path is not in any of the existing unique player paths    
            if all(player.path != p.path for p in self.unique_players):
            # If it's not a duplicate, add it to the unique_players list
                self.unique_players.append(player)              #add in unique players

        childpop=[]                                             #intialize child population
        self.population.sort(key=lambda x: x.fitness)           #sort population by fitness
        self.unique_players.sort(key=lambda x: x.fitness)       #sort unique_players by fitness

        #first perform this to increase diversity (to not get stuck, as we use euclidean distance)
        for _ in range(1):                                      #fill some child population by crossing over each element in unique_players
            for i in range(len(self.unique_players)):
                for j in range(i, len(self.unique_players)):
                    child=self.unique_players[i].crossover(self.unique_players[j])
                    childpop+=[child]


        childpop.extend(self.unique_players)                   #add unique players in child pop

        indice=(len(self.population)//2)                       #for remaining length of childpop perform elitism
        lenth = self.popsize-len(childpop)

        #then perform this, this is elitism
        cutoff=self.population[:indice]                             
        for i in range(lenth):                                 #randomly select parents from top 50% of population and crossover
            parent1,parent2=random.sample(cutoff,2)
            child=parent1.crossover(parent2)
            childpop+=[child]



        self.population = childpop                            #population= childpopulation
        index=self.popsize
        self.population=self.population[:index]               #preventive measure for removing some last elements

    #for every player call mutate()
    def mutation(self):                                       #if random probability then mutate the child
        for player in self.population:
            if random.random()<self.mutatonrate:
                player.mutate()

    #to display result, print the maze frame, print best player info
    def result(self, maze):                                   #sort for pop by fitness for best player
        self.bestPlayer=min(self.population, key=lambda x: x.fitness)
        best_player_id=self.bestPlayer.id
        best_player = self.bestPlayer.fitness
        best_path = self.bestPlayer.path
        print("playerid", end="->")
        print("fitness")
        print (best_player_id, end='->')
        print (best_player)
        print(f"populationsize->{len(self.population)} ")
        print(len(self.unique_players))
        print(" ")
        #display_maze_final(maze,best_path)

        #as there exists many same type of player paths, we print unique elements
        unique = []
        playerpoints = []
        for player in self.population:
            if all(player.path != p.path for p in unique):
                unique.append(player)

        unique.sort(key=lambda x: x.fitness)

        for i in range(min(12, len(unique))):
            player = unique[i]
            playerpoint = player.path[-1]
            playerpoints.append(playerpoint)
            
        if(self.inputs=='0' and self.gen%25==0):
            display_maze(maze,playerpoints)
            time.sleep(0.1)        


        elif(self.inputs=='1'):
            
            display_maze(maze,playerpoints)
            if best_player==0:
                time.sleep(0.1)
            else:
                if self.gen<260:
                    time.sleep(0.6)
                elif 260<=self.gen<330:
                    time.sleep(1)    
                else:
                    time.sleep(1)    
                                           

    #calls all the above function in order for genesis
    def NextGeneration(self):                               

        self.gen+=1

        
        self.breed()

        self.idassign()

        self.mutation()

        # update fitness values for each path
        self.movefit(maze)
        
        if (self.inputs=='1'):
            os.system('cls' if os.name == 'nt' else 'clear')


            print("Current generation:" ,self.gen)
            self.result(maze)



        self.bestPlayer = min(self.population, key=lambda x: x.fitness)
        if(self.inputs=='0' and self.bestPlayer.fitness==0 and self.bestPlayer.path[-1]==self.goal):
            self.inputs='1'

            print("Current generation:" ,self.gen)
            self.result(maze)

        if(self.inputs=='0' and self.gen%25==0):
            '''for i in range(1025):
                sys.stdout.write("\033[F\033[K")'''
            
            print("Current generation:" ,self.gen)
            self.result(maze)     


        '''if (self.gen>400):          #for debugging
          unique = []
          for player in self.population:
            if all(player.path != p.path for p in unique):
              unique.append(player)
          for player in unique:
            print (player.path, end='->')
            print (player.id, end='->')
            print (player.fitness)'''

        #print path of the best player after reaching the solution
        self.bestPlayer = min(self.population, key=lambda x: x.fitness)           
        if self.bestPlayer.fitness==0 and self.bestPlayer.path[-1]==self.goal:
            self.victory==True
            print('Solution found')
            best_player_id=self.bestPlayer.id
            best_player = self.bestPlayer.fitness
            best_path = self.bestPlayer.path
            print("playerid", end="->")
            print("fitness")
            print (best_player_id, end='->')
            print (best_player)
            display_maze_final(maze,best_path)
            print(self.bestPlayer.path)
            time.sleep(10)
            exit()                       #exit if goal is reached

            

if __name__=='__main__':

    maze = maze

    def checkstartend(maze):
        start = (0,0)
        end = (0,0)

        #to iterate through maze and find S,E
        for x, row in enumerate(maze):
            for y, value in enumerate(row):
                if value == "S":
                    start = (x, y)
                elif value == "E":
                    end = (x, y)

        #return S,E or error
        if (start == end):
            print("maze error")
            sys.exit()
        else:
            return start, end
        
    Popsize=1000
    Maxnumberofgens = 10000
    MutationRate=0.3    
    Start=(1,1)
    Goal=(13,37)

    os.system('cls' if os.name == 'nt' else 'clear') #clear screen

    display_maze_final(maze,[(0,0)])

    print("You can change the parameters if you want, they are inside the main function")
    print("Do you want to check the traversal for each iteration? slower runtime, but enjoy traversal :} 1 or 0")
    inputs=input()

    genetic = Genetic(Maxnumberofgens, Popsize, MutationRate, Start, Goal, maze,inputs)

    if(inputs=="1"):

        while genetic.gen<genetic.noofgen:


            genetic.NextGeneration()
    

            if (genetic.gen>=genetic.noofgen):
                print("no solution found, try increasing max number of gens, deafult parametrs take about 500 gens for solution")

    else:
        while genetic.gen<genetic.noofgen:
            
            
            genetic.NextGeneration()

            if (genetic.gen>=genetic.noofgen):
                print("no solution found, try increasing max number of gens, deafult parametrs take about 500 gens for solution")           



