import os
import time
import sys
import copy
from collections import deque
import time
import random


#ANSI escape codes for colors
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
BLACK = "\033[30m"
BRIGHT_WHITE = "\033[97m"
RESET = "\033[0m"



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

#function to check for start S, end E value in the maze, return coordinates
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
      sys.exit
    else:
      return start, end

#function to display maze path frame for DFS
def display_maze(maze, path, Time):
    Time = Time

    os.system('cls' if os.name == 'nt' else 'clear')        #to clear previous output, terminal gets cluttered as every frame is displayed

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
    
    time.sleep(Time)            #add a delay between steps to visualize traversal

#to apply dfs traversal to find path to end
def dfs(maze, start, end, Time):
    Time = Time

    stack = [start]           #initialize stack list with pushing start's (x,y)
    visited = []              #initialize visited list


    #while stack is not empty do
    while stack:                
        path = stack.pop()  #path= popped path list from stack
        cur = path[-1]      #set cur x,y to last element of path i,e current cell

        '''stack_copy = copy.deepcopy(stack)            #for visualizing elements while traversing paths in stack
            
        print("Elements in the stack after pop:")
        for item in stack_copy:
            print(item)

        print("Elements in the path:")
        print(path)

        print("Elements in the visited:")
        print(visited)'''

        display_maze(maze, path, Time)

       # check if the current position is the goal
        if cur == end:
            finalpath = path        #final path = path 
            print("Solution found! Press Enter to finish")
            return finalpath

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(directions)  # Shuffle the order of directions randomly

        # explore neighboring cells in up,down,left,right
        for dx, dy in directions:
            new_x, new_y = cur[0] + dx, cur[1] + dy     #to traverse in matrix x,y+1; x,y-1; x+1,y; x-1,y
               

            # check f the new cell is within bounds and not a wall/"1"
            if ( 0 <= new_x < len(maze) and 0 <= new_y < len(maze[0]) and maze[new_x][new_y] != "1"  and (new_x, new_y) not in visited ):
                new_path = path + [(new_x, new_y)]     #add new (x,y) to cuurent path list, assign to newpath list 
                stack.append(new_path)                 #PUSH new path list to stack
                visited.append((new_x, new_y))         #adding the current cell x,y to visited list
        '''stack_copy = copy.deepcopy(stack)                #for visualizing elements in while traversing stack
            
        print("Elements in the stack before pop:")
        for item in stack_copy:
            print(item)'''

def display_bfsmaze(maze, path, Time):
    Time = Time


    os.system('cls' if os.name == 'nt' else 'clear')        #clear terminal

    # shallow copy leaves a trail while dispaying in dfs not sure why, should work fine 
    # but using that bug as a feature to leave path trail so bfs can be visualized
    m2 = [row[:] for row in maze]           #deepcopy
    '''m2=maze[:]'''                                      
    if( Time != 0 ):
        m2=maze[:]                                     #shallowcopy to visualize traversal     



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
    
    time.sleep(Time)    
 

    time.sleep(Time)


#to apply bfs traversal to find path to end
def bfs(maze, start, end, Time):
    Time = Time
    

    queue = deque([start])             #create a queue with dequeue (double-ended queue) type
    visited = [(start)]                #create visited list with start

    
    while queue:
        path = queue.popleft()                 #pop left, i,e pop oldest path list from queue
        cur = path[-1]                         ##set cur x,y to last element of path i,e current cell


        '''queue_copy = queue.copy()                            #for visualizing elements while traversing paths in queue
          
        print("Elements in the queue after pop:")
        for item in queue_copy:
            print(item)

        print("Elements in the path:")
        print(path)

        print("Elements in the visited:")
        print(visited)'''


        display_bfsmaze(maze, path, Time)

       # check if the current position is the goal
        if cur == end:
            finalpath = path        #final path = path 
            print("Solution found! Press Enter to finish")
            return finalpath

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(directions)  # Shuffle the order of directions randomly

        # explore neighboring cells in up,down,left,right
        for dx, dy in directions:
            new_x, new_y = cur[0] + dx, cur[1] + dy     #to traverse in matrix x,y+1; x,y-1; x+1,y; x-1,y

            # Check if the new cell is within bounds and not a wall/"1" and not in visited
            if (  0 <= new_x < len(maze) and 0 <= new_y < len(maze[0]) and maze[new_x][new_y] != "1" and (new_x, new_y) not in visited ):
                new_path = path + [(new_x, new_y)]   #if condition true then create the list of new path after adding new x,y then assign it to queue
                queue.append(new_path)               #append queue with newpath
                visited.append((new_x, new_y))          #add x,y to visited


        '''queue_copy = copy.deepcopy(queue)                #for visualizing queue
        print("Elements in the stack before pop:")
        for item in queue_copy:
            print(item)'''


def main():

    os.system('cls' if os.name == 'nt' else 'clear') 
    print("Given maze is:")
    display_maze(maze,[(0,0)],0)


    check = checkstartend(maze)
    start=[check[0]]
    end=check[1]

    print("Choose a search algorithm:")
    print("1 for. DFS (Depth-First Search)")
    print("2 for. BFS (Breadth-First Search)")
    choice = input("Enter your choice (1 or 2): ")

    print("Do you want to visualize the the whole traversal or just want the final path:")
    print("1. Visualize traversal")
    print("2. Final path")
    times = input("Enter your choice (1 or 2): ")

    # Record the start time
    start_time = time.time()

    if choice == "2" and times == "1":
        final_path = bfs(maze, start, end, 0.04)
    elif choice == "1" and times == "1":
        final_path = dfs(maze, start, end, 0.08)
    elif choice == "2" and times == "2":
        final_path = bfs(maze, start, end, 0)
    elif choice == "1" and times == "2":
        final_path = dfs(maze, start, end, 0)
    else:
        print("Invalid choice. Please enter 1 or 2.")
        return

    
    #print final path
    if final_path:
        print("Final Path from Start to End:")
        for (x, y) in final_path:            #print output
            print(f"({x}, {y})", end=' -> ')
            
    else:
        print("No solution found.")

    
    
    # Record the end time
    end_time = time.time()

    # Calculate the execution time
    execution_time = end_time - start_time

    print(f"Execution time: {execution_time:.3f} seconds")


if __name__ == "__main__":
    main()

