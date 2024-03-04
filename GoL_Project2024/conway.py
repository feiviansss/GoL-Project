import sys, argparse, os
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

ALIVE = 255
DEAD = 0
vals = [ALIVE,DEAD]

x_coords=[]
y_coords=[]

file= "Test.txt"

blocksCont=0
beehivesCont=0
blinkersCont=0
boatsCont=0
beaconsCont=0
glidersCont=0
spaceshipsCont=0
loafsCont=0
toadsCont=0
tubsCont=0
othersCont=0

if os.path.exists("Results.txt"):
  os.remove("Results.txt")

def paint(x,y,grid,newGrid):
    grid[x,y]=0
    newGrid[x,y]=255

def neighbors(grid, x, y,cont):
    if(grid[x+1,y]==255):cont+=1
    if(grid[x+1,y+1]==255):cont+=1
    if(grid[x+1,y-1]==255):cont+=1
    if(grid[x,y+1]==255):cont+=1
    if(grid[x,y-1]==255):cont+=1
    if(grid[x-1,y]==255):cont+=1
    if(grid[x-1,y-1]==255):cont+=1                    
    if(grid[x-1,y+1]==255):cont+=1

    return cont

def addGlider(i, j, grid,name):
    configuration = name
    x=configuration.shape[0]
    y=configuration.shape[1]
    grid[i:i+x, j:j+y] = configuration

def update(frameNum, img, grid, N, G):
    newGrid = grid.copy()
    
    global blocksCont
    global beehivesCont
    global blinkersCont
    global boatsCont
    global beaconsCont
    global glidersCont
    global spaceshipsCont
    global loafsCont
    global toadsCont
    global tubsCont
    global othersCont


    f = open("Results.txt", "a")
    alives=0
    deaths=0
    newAlives=0
    for x in range (0,N):
        for y in range (0,N):
            if(grid[x,y]==255):
                alives+=1
    
    f.write("Generation: "+ str(frameNum) + "\n")
    f.write("Alives: "+ str(alives) + "\n")
       
    blocks= 0
    beehives=0
    blinkers=0
    boats=0
    beacons=0
    gliders=0
    spaceships=0
    loafs=0
    toads=0
    tubs=0
    others=0
    

    for x in range (0,N):
        for y in range (0,N):
            if (x-1 >= 0 and y-1 >= 0 and x+1 < N and y+1 < N):
                if(grid[x,y]==255):
                    #Any live cell with two or three neighbors survives.
                    cont=0
                    cont= neighbors(grid, x, y,cont)
                    if(cont ==2 or cont==3):newGrid[x,y]=255

                    #All other live cells die in the next generation.
                    else:
                        newGrid[x,y]=0
                        deaths+=1
                else:
                    #Any dead cell with three live neighbors becomes a live cell.
                    cont=0
                    cont= neighbors(grid, x, y,cont)

                    if(cont==3):
                        newGrid[x,y]=255
                        newAlives+=1

    for x in range (0,N):
        for y in range (0,N):
            if (x-1 >= 0 and y-1 >= 0 and x+1 < N and y+1 < N):
                if(grid[x,y]==255): 
                    cont=0
                    cont= neighbors(grid, x, y,cont)
                    if(cont>=1):                       
                        #Blocks
                        if (x+3 < N and y+3 < N and y-2 >= 0 and x-2 >= 0):
                            if((grid[x+1,y]==255 and grid[x+1,y+1]==255 and grid[x,y+1]==255) and (grid[x-1,y-1]==0 and grid[x-1,y]==0 and grid[x-1,y+1]==0 and grid[x-1,y+2]==0 and grid[x,y-1]==0 and grid[x,y+2]==0 and grid[x+1,y-1]==0 and grid[x+1,y+2]==0 and grid[x+2,y-1]==0 and grid[x+2,y]==0 and grid[x+2,y-1]==0 and grid[x+2,y+2]==0) ):
                                blocks+=1  
                                grid[x+1,y]=0
                                grid[x,y+1]=0   
                                grid[x+1,y+1]=0

                        if (x+3 < N and y+2 < N and y-2 >= 0):
                            #Toads
                            if((grid[x+1,y+1]==255 and grid[x+2,y+1]==255 and grid[x+3,y-1]==255 and grid[x+1,y-2]==255 and grid[x+2,y-2]==255 and (grid[x+1,y]==0 and grid[x+2,y]==0 and grid[x+1,y-1]==0 and grid[x+2,y-1]==0))): 
                                toads+=1   
                                grid[x+1,y+1]=0
                                grid[x+2,y+1]=0
                                grid[x+3,y-1]=0
                                grid[x+1,y-2]=0
                                grid[x+2,y-2]=0

                            elif((grid[x,y+1]==255 and grid[x,y+2]==255 and grid[x+1,y]==255 and grid[x+1,y+1]==255 and grid[x+1,y-1]==255)):
                                toads+=1   
                                grid[x,y+1]=0
                                grid[x,y+2]=0
                                grid[x+1,y]=0
                                grid[x+1,y+1]=0
                                grid[x+1,y-1]=0

                        if (x+3 < N and y+3 < N ):
                            #Loafs
                            if(grid[x,y+1]==255 and grid[x+1,y-1]==255  and grid[x+1,y+2]==255 and grid[x+2,y]==255 and grid[x+2,y+2]==255 and grid[x+3,y+1]==255 and (grid[x+1,y]==0 and grid[x+1,y+1]==0 and grid[x+2,y+1]==0)): 
                                loafs+=1
                                grid[x,y+1]=0 
                                grid[x+1,y-1]=0 
                                grid[x+1,y+2]=0 
                                grid[x+2,y]=0 
                                grid[x+2,y+2]=0 
                                grid[x+3,y+1]=0
                                
                            #Beacon
                            elif((grid[x+1,y]==255 and grid[x+1,y+1]==255 and grid[x,y+1]==255 and grid[x+2,y+2]==255 and grid[x+3,y+3]==255 and grid[x+3,y+2]==255 and grid[x+2,y+3]==255)):
                                beacons+=1 
                                grid[x+1,y]=0 
                                grid[x+1,y+1]=0 
                                grid[x,y+1]=0 
                                grid[x+2,y+2]=0 
                                grid[x+3,y+3]=0 
                                grid[x+3,y+2]=0 
                                grid[x+2,y+3]=0

                            elif(grid[x+1,y]==255 and grid[x,y+1]==255 and grid[x+2,y+3]==255 and grid[x+3,y+2]==255 and grid[x+3,y+3]==255):
                                beacons+=1
                                grid[x+1,y]=0 
                                grid[x,y+1]=0 
                                grid[x+2,y+3]=0 
                                grid[x+3,y+2]=0 
                                grid[x+3,y+3]=0

                            #Blinker
                            elif((grid[x,y+1]==255 and grid[x,y+2]==255 and ( grid[x-1,y-1]==0 and grid[x+1,y-1]==0 and grid[x-1,y+3]==0 and grid[x+1,y+3]==0 and grid[x-1,y+2]==0 and grid[x+1,y+2]==0 ))):
                                blinkers+=1
                                grid[x,y+1]=0 
                                grid[x,y+2]=0

                            elif((grid[x+1,y]==255 and grid[x+2,y]==255 and (grid[x+3,y+1]==0 and grid[x+3,y-1]==0 and grid[x-1,y-1]==0 and grid[x-1,y+1]==0 and grid[x+2,y-1]==0))):
                                blinkers+=1
                                grid[x+1,y]=0 
                                grid[x+2,y]=0

                        if (x+2 < N and y+2 < N):
                            #Beehives
                            if(grid[x,y+1]==255 and grid[x+1,y-1]==255  and grid[x+1,y+2]==255 and grid[x+2,y]==255 and grid[x+2,y+1]==255 and grid[x+1,y]==0 and grid[x+1,y+1]==0): 
                                beehives+=1 
                                grid[x,y+1]=0
                                grid[x+1,y-1]=0
                                grid[x+1,y+2]=0
                                grid[x+2,y]=0
                                grid[x+2,y+1]=0
            
                            #Boats
                            if(grid[x,y+1]==255 and grid[x+1,y]==255  and grid[x+1,y+2]==255 and grid[x+2,y+1]==255 and (grid[x,y-1]==0 and grid[x,y+2]==0 and grid[x-1,y-1]==0 and grid[x+2,y+2]==0 and grid[x+2,y]==0)): 
                                boats+=1 
                                grid[x,y+1]=0
                                grid[x+1,y]=0
                                grid[x+1,y+2]=0
                                grid[x+2,y+1]=0
                        
                        #Tubs
                        if (x+2 < N):
                            if(grid[x+1,y+1]==255 and grid[x+2,y]==255  and grid[x+1,y-1]==255 and (grid[x,y-1]==0 and  grid[x,y+1]==0 and grid[x+1,y]==0 and  grid[x+2,y-1]==0 and grid[x+2,y+1]==0)): 
                                tubs+=1 
                                grid[x+1,y+1]=0
                                grid[x+2,y]=0
                                grid[x+1,y-1]=0
                        #Gliders
                        if (x+2 < N and y+2 < N and y-2 >= 0):
                            if(grid[x+1,y+1]==255 and grid[x+2,y+1]==255  and grid[x+2,y]==255 and grid[x+2,y-1]==255 and (grid[x,y+1]==0)): 
                                gliders+=1 
                                grid[x+1,y+1]=0
                                grid[x+2,y+1]=0
                                grid[x+2,y]=0
                                grid[x+2,y-1]=0
                                

                            elif(grid[x,y+2]==255 and grid[x+1,y+1]==255  and grid[x+1,y+2]==255 and grid[x+2,y+1]==255 and (grid[x+1,y]==0)):
                                gliders+=1 
                                grid[x,y+2]=0
                                grid[x+1,y+1]=0
                                grid[x+1,y+2]=0
                                grid[x+2,y+1]=0

                            elif(grid[x+1,y]==255 and grid[x+2,y]==255  and grid[x+2,y-1]==255 and grid[x+1,y-2]==255 and (grid[x,y-1]==0)):
                                gliders+=1 
                                grid[x+1,y]=0
                                grid[x+2,y]=0
                                grid[x+2,y-1]=0
                                grid[x+1,y-2]=0
                                

                            elif(grid[x+1,y+1]==255 and grid[x+2,y+1]==255  and grid[x+2,y]==255 and grid[x+1,y+2]==255 and (grid[x,y+1]==0 and grid[x+1,y]==0)):
                                gliders+=1 
                                grid[x+1,y+1]=0
                                grid[x+2,y+1]=0
                                grid[x+2,y]=0
                                grid[x+1,y+2]=0

                        #Spaceships
                        if (x+3 < N and y+4 < N and y-2 >= 0):
                            if(grid[x,y+1]==255 and grid[x+1,y+1]==255  and grid[x+1,y+2]==255 and grid[x+1,y-1]==255 and grid[x+1,y-2]==255 and grid[x+2,y-2]==255  and grid[x+2,y-1]==255 and grid[x+2,y]==255 and grid[x+2,y+1]==255  and grid[x+3,y-1]==255 and grid[x+3,y]==255): 
                                spaceships+=1 
                                grid[x+1,y+1]=0
                                grid[x+1,y+2]=0
                                grid[x+1,y-1]=0
                                grid[x+1,y-2]=0
                                grid[x+2,y-2]=0
                                grid[x+2,y-1]=0
                                grid[x+2,y]=0
                                grid[x+2,y+1]=0
                                grid[x+3,y-1]=0
                                grid[x+3,y]=0

                            elif(grid[x,y+1]==255 and grid[x,y+2]==255  and grid[x,y+3]==255 and grid[x+1,y-1]==255 and grid[x+1,y+3]==255 and grid[x+3,y-1]==255  and grid[x+2,y+3]==255 and grid[x+3,y+2]==255): 
                                spaceships+=1 
                                grid[x,y+1]=0
                                grid[x,y+2]=0
                                grid[x,y+3]=0
                                grid[x+1,y-1]=0
                                grid[x+1,y+3]=0
                                grid[x+3,y-1]=0
                                grid[x+2,y+3]=0
                                grid[x+3,y+2]=0

                            elif(grid[x,y+1]==255 and grid[x+1,y-1]==255  and grid[x+1,y]==255 and grid[x+1,y+1]==255 and grid[x+1,y+2]==255 and grid[x+2,y-1]==255  and grid[x+2,y]==255 and grid[x+2,y+2]==255 and grid[x+2,y+3]==255  and grid[x+3,y+1]==255 and grid[x+3,y+2]==255): 
                                spaceships+=1 
                                grid[x,y+1]=0
                                grid[x+1,y-1]=0
                                grid[x+1,y]=0
                                grid[x+1,y+1]=0
                                grid[x+1,y+2]=0
                                grid[x+2,y-1]=0
                                grid[x+2,y]=0
                                grid[x+2,y+2]=0
                                grid[x+2,y+3]=0
                                grid[x+3,y+1]=0
                                grid[x+3,y+2]=0
                        else:
                            others+=1
                  
                    else:
                        #Spaceships
                        if (x+3 < N and y+4 < N ):
                            if(grid[x,y+3]==255 and grid[x+1,y+4]==255  and grid[x+2,y+4]==255 and grid[x+3,y+4]==255 and grid[x+2,y]==255 and grid[x+3,y+1]==255  and grid[x+3,y+2]==255 and grid[x+3,y+3]==255): 
                                spaceships+=1 
                                grid[x,y+3]=0
                                grid[x+1,y+4]=0
                                grid[x+2,y+4]=0
                                grid[x+3,y+4]=0
                                grid[x+2,y]=0
                                grid[x+3,y+1]=0
                                grid[x+3,y+2]=0
                                grid[x+3,y+3]=0
                            else:
                                others+=1       
               
    
    #Create Report
    f.write("*************************************\n")
    f.write("New Alive: " + str(newAlives) + "\n")
    f.write("---------------------------------------\n")
    f.write("Deaths: " + str(deaths) + "\n")
    f.write("---------------------------------------\n")
    f.write("********CONFIGURATIONS********\n")
    f.write("---------------------------------------\n")
    f.write("Blocks:" + str(blocks) + "\n")
    f.write("---------------------------------------\n")
    f.write("Behives:" + str(beehives) + "\n")
    f.write("---------------------------------------\n")
    f.write("Loafs:" + str(loafs) + "\n")
    f.write("---------------------------------------\n")
    f.write("Boats:" + str(boats) + "\n")
    f.write("---------------------------------------\n")
    f.write("Tubs:" + str(tubs) + "\n")
    f.write("---------------------------------------\n")
    f.write("Blinkers:" + str(blinkers) + "\n")
    f.write("---------------------------------------\n")
    f.write("Toads:" + str(toads) + "\n")
    f.write("---------------------------------------\n")
    f.write("Beacons:" + str(beacons) + "\n")
    f.write("---------------------------------------\n")
    f.write("Gliders:" + str(gliders) + "\n")
    f.write("---------------------------------------\n")
    f.write("Light-weight Spaceships:" + str(spaceships) + "\n")
    f.write("---------------------------------------\n")
    f.write("Others:" + str(others) + "\n")
    f.write("---------------------------------------\n\n")
    

    blocksCont+=blocks
    beehivesCont+=beehives
    blinkersCont+=blinkers
    boatsCont+=boats
    beaconsCont+=beacons
    glidersCont+=gliders
    spaceshipsCont+=spaceships
    loafsCont+=loafs
    toadsCont+=toads
    tubsCont+=tubs
    othersCont+=others

    
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    
    if (frameNum==G-1):
        total= blocksCont + beaconsCont + beehivesCont + blinkersCont + boatsCont + glidersCont + spaceshipsCont + loafsCont + toadsCont + tubsCont + othersCont
        f.write("**********%PERCENT%***********\n")
        f.write("Blocks:" + str(round(blocksCont/total*100,2)) + "%\n")
        f.write("---------------------------------------\n")
        f.write("Beehives:" + str(round(beehivesCont/total*100,2)) + "%\n")
        f.write("---------------------------------------\n")
        f.write("Loafs:" + str(round(loafsCont/total*100,2)) + "%\n")
        f.write("---------------------------------------\n")
        f.write("Boats:" + str(round(boatsCont/total*100,2)) + "%\n")
        f.write("---------------------------------------\n")
        f.write("Tubs:" + str(round(tubsCont/total*100,2)) + "%\n")
        f.write("---------------------------------------\n")
        f.write("Blinkers:" + str(round(blinkersCont/total*100,2)) + "%\n")
        f.write("---------------------------------------\n")
        f.write("Toads:" + str(round(toadsCont/total*100,2)) + "%\n")
        f.write("---------------------------------------\n")
        f.write("Beacons:" + str(round(beaconsCont/total*100,2)) + "%\n")    
        f.write("---------------------------------------\n")    
        f.write("Gliders:" + str(round(glidersCont/total*100,2)) + "%\n")
        f.write("---------------------------------------\n")
        f.write("Light-weight Spaceships:" + str(round(spaceshipsCont/total*100,2)) + "%\n")       
        f.write("---------------------------------------\n")
        f.write("Others:" + str(round(othersCont/total*100,2)) + "%\n")
        f.write("---------------------------------------\n")
        f.close()
        os.startfile("Results.txt")
        exit()
    return img,
    
def main():    
    parser = argparse.ArgumentParser(description="Conway's Game of Life")
    grid = np.array([])
    try:
        f = open(file, "r")
        
        count = len(f.readlines())
    
        f = open(file, "r")
        for x in range (0,count):
            if x == 0:
                size= f.readline().split()
                N=int(size[0])
                G=int(size[1])
                grid = np.zeros(N*N).reshape(N, N)
            else:
                coords= f.readline().split()
                x=int(coords[1])
                y=int(coords[0])
                    
                if (x<N and y<N):
                    x_coords.append(x)
                    y_coords.append(y)
                else:
                    print ("Coordinate values out of range")
                    exit()

        for x in range (0, count-1):
            grid[x_coords[x],y_coords[x]] =255
    except:
        print("ERROR! WRONG FILE FORMAT")
        exit()

    updateInterval = 500
    
    #Simulation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, G), frames = G, interval=updateInterval, save_count=50)

    plt.show()

if __name__ == '__main__':
    main()