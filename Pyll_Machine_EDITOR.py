import pygame, math
from time import sleep
from math import floor as flr, ceil
from copy import deepcopy as dcopy
try:
    from win32clipboard import OpenClipboard as OpenC, CloseClipboard as CloseC
    from win32clipboard import SetClipboardText as SetC, GetClipboardData as GetC
    from win32clipboard import EmptyClipboard as EmptyC
    clip = True
except:
    clip = False
    print("win32clipboard not working, switching to simple text I/O")


def render():
    global screen,disar,gx,gy,cellsA,colors,details,running,min_size,animation_move,calc_last,calc_gap
    global frame, play, UI_size, UI_base_gap, UI_button_gap, UI_cell_gap, UI, UI_positions
    global cosi, ms
    
    cur_time = pygame.time.get_ticks()
    tmult = (cur_time - calc_last)/calc_gap
    nub_rendered = 0
    screen.fill((0,0,0))
    key = [*cellsA.keys()]
    
    sx = gx/(disar[1][0]-disar[0][0])
    sy = gy/(disar[1][1]-disar[0][1])
    for i in key:
        cur = cellsA[i]
        color = cur[0]
        

        olds = cur[2:4]
        if tuple(olds) == i or not (animation_move and play):
            cur_x = i[0]
            cur_y = i[1]
        else:
            
            cur_x = (i[0]-olds[0])*(tmult)+olds[0]
            cur_y = (i[1]-olds[1])*(tmult)+olds[1]
            #print(tmult,olds[0]-i[0],cur_x)
        difx = cur_x - disar[0][0]
        dify = cur_y - disar[0][1]
        

        px = difx/(disar[1][0]-disar[0][0])*gx-sx/2
        py = dify/(disar[1][1]-disar[0][1])*gy-sy/2
        
        if (px >= -sx and px <= gx) and (py >= -sy and py <= gy):
            #print(cur,cur[4] != cur[5])
            nub_rendered += 1
            
            if  cur[4] == cur[5] or not animation_rotate:
                fpx = flr(px)
                fpy = flr(py)
                pygame.draw.rect(screen,colors[color],(fpx,fpy,flr(px+sx)-fpx,flr(py+sy)-fpy))
                rotate_base = cellsA[i][1]
                rotate = -rotate_base/2*math.pi
                
                co = math.cos(rotate)
                si = math.sin(rotate)
                
            if (animation_rotate or animation_rotate_half) and cur[4] != cur[5]: 
                rotate_base = (cur[4]-cur[5])*tmult+cur[5]
                rotate = -rotate_base/2*math.pi
                co = math.cos(rotate)
                si = math.sin(rotate)
                if animation_rotate:
                    cen = [px+sx/2,py+sy/2]
                    poly = []
                    for k in [[px,py],[px,py+sy],[px+sx,py+sy],[px+sx,py]]:
                        newx = (co*(k[0]-cen[0]))+(si*(k[1]-cen[1]))+cen[0]
                        newy = (co*(k[1]-cen[1]))-(si*(k[0]-cen[0]))+cen[1]
                        poly.append([newx,newy])
                    pygame.draw.polygon(screen,colors[color],poly)
            
                
            typ = cellsA[i][0]
            det = details[typ]
            if len(det) > 0 and (sx>=min_size or sy>=min_size):
                for j in det:
                    newdet = []
                    for k in j[1:]:
                        newx = (co*(k[0]-0.5))+(si*(k[1]-0.5))+0.5
                        newy = (co*(k[1]-0.5))-(si*(k[0]-0.5))+0.5
                        newx = newx*sx+px
                        newy = newy*sy+py
                        newdet.append([newx,newy])
                    pygame.draw.polygon(screen,j[0],newdet)

    # A bit to do the ghost block
    if cur_ghost[0] and not ms[2]:
        cur_x = cur_ghost[1]
        cur_y = cur_ghost[2]
        color = cur_ghost[3]
        difx = cur_x - disar[0][0]
        dify = cur_y - disar[0][1]
        px = difx/(disar[1][0]-disar[0][0])*gx-sx/2
        py = dify/(disar[1][1]-disar[0][1])*gy-sy/2
        #print(cur,cur[4] != cur[5])
        fpx = flr(px)
        fpy = flr(py)
        pygame.draw.rect(screen,colors[color],(fpx,fpy,flr(px+sx)-fpx,flr(py+sy)-fpy))
        
        rotate_base = cur_ghost[4]
        rotate = -rotate_base/2*math.pi
        co = math.cos(rotate)
        si = math.sin(rotate)
        typ = color
        det = details[typ]
        if len(det) > 0 and (sx>=min_size or sy>=min_size):
            for j in det:
                newdet = []
                for k in j[1:]:
                    newx = (co*(k[0]-0.5))+(si*(k[1]-0.5))+0.5
                    newy = (co*(k[1]-0.5))-(si*(k[0]-0.5))+0.5
                    newx = newx*sx+px
                    newy = newy*sy+py
                    newdet.append([newx,newy])
                pygame.draw.polygon(screen,j[0],newdet)

        
    
    # Now a bit to do the UI
    for i in range(len(UI_positions)):
        curpos = UI_positions[i]
        cur = UI[i]
        if curpos[2] or frame != 0:
            px = UI_base_gap*UI_size + (UI_button_gap * UI_size + UI_size)*curpos[0]
            py = gy - (UI_base_gap*UI_size + (UI_button_gap * UI_size + UI_size)*curpos[1] + UI_size)
            
            for j in cur:
                UI_new = []
                for k in j[1:]:
                    newx = k[0]*UI_size
                    newy = k[1]*UI_size
                    newx = newx+px
                    newy = newy+py
                    UI_new.append([newx,newy])
                pygame.draw.polygon(screen,j[0],UI_new)
            





    
    pygame.display.flip()
    #print(nub_rendered)
    sleep(0.01)

def V1IN(instr):
    dictout = {}
    V1map = [0,2,3,1,5,4,8,6,7,9]
    while len(dictout) == 0:
        try: #This try loop is the easiest way to make sure the output contains something
            split1 = instr.split(";")
            split1.pop(3)
            split1.pop(4)
            split1.pop(4)
            midx = int(split1[1])//2
            midy = int(split1[2])//2
            #print(split1)
            split2 = split1[3].split(",")
            #print(split2)
            for i in range(len(split2)):
                split2[i]=split2[i].split(".")
            #print(split2)
            #halt
            for i in split2:
                if len(i) > 2:
                    dictout[(int(i[2])-midx,(int(i[3])-midy)*-1)] = [V1map[int(i[0])],int(i[1])]
                else:
                        None # """"""handles"""""" build zone blocks
        except:
            print("Invalid level code, it must be V1")
            instr = "V1;50;50;;3.0.18.24,3.0.18.25,3.0.19.25,3.0.20.26,4.0.21.26,5.0.22.25,5.0.23.25,5.0.24.25,0.0.25.25,0.1.25.24,0.0.24.23,0.1.25.22,5.0.19.24,5.0.20.25,3.0.24.24,7.0.23.23,3.2.26.25,2.0.20.24,2.0.22.24,3.0.20.22,0.0.21.25,0.1.21.24,0.0.22.23,0.1.21.22,0.3.19.23,7.0.20.23,3.0.17.23,3.0.24.22,7.0.23.21;;"
    key = [*dictout.keys()]
    for i in key: #sets the stuff used for animations
        cur = dictout[i]
        dictout[i].append(i[0])
        dictout[i].append(i[1])
        dictout[i].append(cur[1])
        dictout[i].append(cur[1])

    return dictout

def V1OUT(dictin):
    V1map = [0,2,3,1,5,4,8,6,7,9]
    
    key = [*dictin.keys()]
    if len(key) > 0:
        up = key[0][1]
        down = key[0][1]
        left = key[0][0]
        right = key[0][0]
        for i in key:
            if i[0] > right:
                right = i[0]
            if i[0] < left:
                left = i[0]
            if i[1] < up:
                up = i[1]
            if i[1] > down:
                down = i[1]
        x = (right-left)+1
        y = (down-up)+1
        sx = left+(x//2)
        sy = up+(y//2)             
        outstr = "V1;"+str(x)+";"+str(y)+";;"
        for i in range(len(key)):
            cur = cellsA[key[i]]
            if i > 0:
                outstr += ","
            outstr += str(V1map.index(cur[0]))
            outstr += "."
            outstr += str(cur[1])
            outstr += "."
            outstr += str((key[i][0]-sx)+(x//2))
            outstr += "."
            outstr += str(((key[i][1]-sy))*-1+y//2)
        outstr += ";;"
    else:
        outstr = ""
    return outstr
    
    

gx,gy = 850,850

disar = [[-10,-10],[10,10],[0,0]]# The final one is for original middle co-ords
min_size = 5 #minimum size of a cell on screen before the details stop being rendered
zoom_speed = 1.5 #multiplier applied each time the scroll wheel moves
calc_gap = 400 #miliseconds between each compute
calc_mult = 2 #how much the calc gap is multiplied by when using  Shift + MsWheel
pan_speed = [1,1] #how many screens panning the camera via WASD moves per second
animation_move = True
animation_rotate = False
animation_rotate_half = False
play = False
skip = False
UI_size = 100 #all the folowing values are in some way controlled by this
UI_base_gap = 0.3
UI_button_gap = 0.1
UI_cell_gap = 0.1
cur_ghost = [False,0,0,0,0] #[display?,x,y,type,rotation]


calc_last = 0
delta1 = 0
delta2 = 0
delta = 0
old_ms = (False, False, False)
old_click = False
frame = 0
valid = False
place_valid = False
cosi = {}


cellsBASE = {}#[type,rotation,oldx,oldy,current rotation,old rotation]
#there is a separate current rotation, as the standard one goes from 0-4 and more than a 90* turn can't be animated well


#cellsBASE[(-7,0)] = [9,0]
#cellsBASE[(-9,0)] = [1,0]
#cellsBASE[(-4,0)] = [6,0]
#cellsBASE[(0,0)] = [9,0]
#cellsBASE[(9,0)] = [7,2]
'''
cellsBASE[(-1,0)] = [2,0]
cellsBASE[(0,-1)] = [2,0]
cellsBASE[(1,0)] = [2,0]
cellsBASE[(0,1)] = [2,0]
cellsBASE[(2,1)] = [2,0]
cellsBASE[(1,-2)] = [2,0]
cellsBASE[(-1,-2)] = [2,0]
cellsBASE[(0,0)] = [4,0]
cellsBASE[(2,0)] = [4,0]
cellsBASE[(0,-2)] = [4,0]
cellsBASE[(-2,0)] = [4,0]
'''
#cellsBASE[(-2,0)] = [6,0]
#cellsBASE[(-1,0)] = [0,0]
#cellsBASE[(0,0)] = [4,0]



V1 = ""
#V1 = "V1;50;50;;3.0.23.21,3.0.24.21;;"
#^Two pushers
#V1 = "V1;50;50;;2.0.16.18,2.0.17.18,2.0.22.18,3.1.16.19,3.0.20.19,2.0.15.20,1.0.17.20,4.0.19.20,1.0.9.21,1.0.11.21,4.0.17.21,0.1.19.21,3.3.22.21,3.0.24.21,4.0.25.21,2.0.26.21,3.2.9.22,0.0.12.22,3.0.15.22,1.0.17.22,0.3.19.22,1.0.21.22,3.0.25.22,1.0.9.23,1.0.11.23,8.0.13.23,7.0.14.24,7.0.15.24,7.0.16.24,2.0.17.24,4.0.19.24,2.0.21.24,3.0.23.24,4.0.24.24,2.0.25.24;;"
#^Sawtooth
#V1 = "V1;8;8;;6.0.7.0,6.0.6.0,6.0.5.0,6.0.4.0,6.0.3.0,6.0.2.0,6.0.1.0,6.0.0.0,6.0.0.1,6.0.0.2,6.0.0.3,6.0.0.4,6.0.0.5,6.0.0.6,6.0.0.7,6.0.1.7,6.0.2.7,6.0.3.7,6.0.4.7,6.0.5.7,6.0.6.7,6.0.7.7,6.0.7.6,6.0.7.5,6.0.7.4,6.0.7.3,6.0.7.2,6.0.7.1,0.3.3.2,0.3.3.5,0.1.4.2,0.1.4.5,0.2.2.3,0.0.2.4,0.0.5.4,5.0.4.3,5.0.3.3,5.0.3.4,5.0.4.4,5.0.3.1,5.0.4.6,5.0.1.4,0.2.5.3,5.2.6.3;;"
#^Test
#V1 = "V1;50;50;;3.0.27.22,4.0.28.22,3.0.28.23,3.0.21.24,5.0.22.24,1.0.23.24,3.0.28.24,3.0.24.25,5.0.25.25,0.2.26.25,0.2.27.25,0.1.28.25,5.0.29.25,3.0.24.26,5.0.25.26,0.2.26.26,0.2.27.26,0.3.28.26,5.0.29.26,3.0.21.27,5.0.22.27,2.0.23.27,3.0.28.27,3.0.28.28,3.0.27.29,4.0.28.29,6.0.0.0,6.0.1.0,6.0.2.0,6.0.3.0,6.0.4.0,6.0.5.0,6.0.6.0,6.0.7.0,6.0.8.0,6.0.9.0,6.0.10.0,6.0.11.0,6.0.12.0,6.0.13.0,6.0.14.0,6.0.15.0,6.0.16.0,6.0.17.0,6.0.18.0,6.0.19.0,6.0.20.0,6.0.21.0,6.0.22.0,6.0.23.0,6.0.24.0,6.0.25.0,6.0.26.0,6.0.27.0,6.0.28.0,6.0.29.0,6.0.30.0,6.0.31.0,6.0.32.0,6.0.33.0,6.0.34.0,6.0.35.0,6.0.36.0,6.0.37.0,6.0.38.0,6.0.39.0,6.0.40.0,6.0.41.0,6.0.42.0,6.0.43.0,6.0.44.0,6.0.45.0,6.0.46.0,6.0.47.0,6.0.48.0,6.0.49.0,6.0.49.1,6.0.49.2,6.0.49.3,6.0.49.4,6.0.49.5,6.0.49.6,6.0.49.7,6.0.49.8,6.0.49.9,6.0.49.10,6.0.49.11,6.0.49.12,6.0.49.13,6.0.49.14,6.0.49.15,6.0.49.16,6.0.49.17,6.0.49.18,6.0.49.19,6.0.49.20,6.0.49.21,6.0.49.22,6.0.49.23,6.0.49.24,6.0.49.25,6.0.49.26,6.0.49.27,6.0.49.28,6.0.49.29,6.0.49.30,6.0.49.31,6.0.49.32,6.0.49.33,6.0.49.34,6.0.49.35,6.0.49.36,6.0.49.37,6.0.49.38,6.0.49.39,6.0.49.40,6.0.49.41,6.0.49.42,6.0.49.43,6.0.49.44,6.0.49.45,6.0.49.46,6.0.49.47,6.0.49.48,6.0.49.49,6.0.48.49,6.0.47.49,6.0.46.49,6.0.45.49,6.0.44.49,6.0.43.49,6.0.42.49,6.0.41.49,6.0.40.49,6.0.39.49,6.0.38.49,6.0.37.49,6.0.36.49,6.0.35.49,6.0.34.49,6.0.33.49,6.0.32.49,6.0.31.49,6.0.30.49,6.0.29.49,6.0.28.49,6.0.27.49,6.0.26.49,6.0.25.49,6.0.24.49,6.0.23.49,6.0.22.49,6.0.21.49,6.0.20.49,6.0.19.49,6.0.18.49,6.0.17.49,6.0.16.49,6.0.15.49,6.0.14.49,6.0.13.49,6.0.12.49,6.0.11.49,6.0.10.49,6.0.9.49,6.0.8.49,6.0.7.49,6.0.6.49,6.0.5.49,6.0.4.49,6.0.3.49,6.0.2.49,6.0.1.49,6.0.0.49,6.0.0.48,6.0.0.47,6.0.0.46,6.0.0.45,6.0.0.44,6.0.0.43,6.0.0.42,6.0.0.41,6.0.0.40,6.0.0.39,6.0.0.38,6.0.0.37,6.0.0.36,6.0.0.35,6.0.0.34,6.0.0.33,6.0.0.32,6.0.0.31,6.0.0.30,6.0.0.29,6.0.0.28,6.0.0.27,6.0.0.26,6.0.0.25,6.0.0.24,6.0.0.23,6.0.0.22,6.0.0.21,6.0.0.20,6.0.0.19,6.0.0.18,6.0.0.17,6.0.0.16,6.0.0.15,6.0.0.14,6.0.0.13,6.0.0.12,6.0.0.11,6.0.0.10,6.0.0.9,6.0.0.8,6.0.0.7,6.0.0.6,6.0.0.5,6.0.0.4,6.0.0.3,6.0.0.2,6.0.0.1;;"
#^Nuke
#V1 = "V1;50;50;;7.0.23.24,0.0.24.24,0.1.25.23;;"
#^other test
#V1 = "V1;50;50;;4.3.24.23,4.3.23.23,5.0.24.25,5.0.23.25,2.0.23.24,1.0.24.24,1.0.23.26,2.0.24.26,3.1.23.27,3.1.24.27,4.1.22.28,4.1.22.27,4.1.25.28,4.1.25.27,3.0.22.24,3.2.25.24,5.0.24.22,5.0.23.22,5.0.23.21,5.0.23.20,5.0.24.20,3.3.24.19,3.3.23.19,1.3.24.21,3.0.17.24,4.1.17.27,4.1.17.28,4.3.18.23,2.0.18.24,5.0.18.25,1.0.18.26,3.1.18.27,4.3.19.23,1.0.19.24,5.0.19.25,2.0.19.26,3.1.19.27,3.2.20.24,4.1.20.27,4.1.20.28,3.3.19.22,3.3.18.22,4.0.27.27,4.0.28.27,4.0.29.27,4.0.30.27,4.0.31.27,4.0.32.27,4.0.33.27,2.0.27.28,2.0.28.28,2.0.29.28,2.0.30.28,2.0.31.28,2.0.32.28,2.0.33.28,1.0.27.26,1.0.28.26,1.0.29.26,1.0.30.26,1.0.31.26,1.0.32.26,1.0.33.26,5.0.33.25,5.0.32.25,5.0.31.25,5.0.30.25,5.0.29.25,5.0.28.25,5.0.27.25,3.3.27.24,3.3.28.24,3.3.29.24,3.3.30.24,3.3.31.24,3.3.32.24,3.3.33.24,5.0.23.13,5.0.23.15,5.0.23.17,5.0.24.13,5.0.24.14,5.0.24.15,5.0.24.16,5.0.24.17,3.3.35.24,5.0.35.25,1.0.35.26,4.0.35.27,2.0.35.28,3.3.36.24,5.0.36.25,1.0.36.26,4.3.36.27,2.0.36.28,3.3.34.24,5.0.34.25,1.0.34.26,4.0.34.27,2.0.34.28,5.0.27.22,5.0.27.21,5.0.27.20,5.0.27.19,5.0.27.18,5.0.29.18,5.0.29.19,5.0.30.20,5.0.30.21,5.0.30.22,5.0.32.18,5.0.32.19,5.0.32.20,5.0.32.21,5.0.32.22,5.0.34.18,5.0.34.19,5.0.34.20,5.0.34.21,5.0.34.22,5.0.35.18,5.0.35.22,5.0.36.18,5.0.36.19,5.0.36.20,5.0.36.21,5.0.36.22,5.0.21.17,5.0.21.16,5.0.21.15,5.0.20.14,5.0.20.13,5.0.18.13,5.0.18.14,5.0.18.15,5.0.18.16,5.0.18.17,5.0.13.25,1.0.13.26,3.1.13.27,3.3.14.22,4.3.14.23,1.0.14.24,5.0.14.25,2.0.14.26,3.1.14.27,3.3.11.22,4.3.11.23,2.0.11.24,5.0.11.25,1.0.11.26,3.1.11.27,5.0.12.25,2.0.12.26,3.1.12.27,3.2.15.24,4.1.15.27,4.1.15.28,4.3.13.24,4.3.12.24,3.0.7.24,4.1.7.27,4.1.7.28,3.3.8.22,4.3.8.23,2.0.8.24,5.0.8.25,1.0.8.26,3.1.8.27,4.3.9.24,5.0.9.25,2.0.9.26,3.1.9.27,4.3.10.24,5.0.10.25,1.0.10.26,3.1.10.27,3.3.9.23,3.3.10.23,3.3.13.23,3.3.12.23,5.0.7.20,5.0.7.19,5.0.7.17,5.0.7.18,5.0.7.16,5.0.9.16,5.0.13.16,5.0.13.18,5.0.13.20,5.0.14.16,5.0.14.18,5.0.14.20,5.0.15.16,5.0.15.17,5.0.15.18,5.0.15.19,5.0.15.20,5.0.10.18,5.0.11.20,5.0.10.17,5.0.11.19;;"
#^Slow things
#V1 = "V1;50;50;;2.0.16.18,2.0.22.18,1.0.11.21,0.0.12.22,1.0.21.22,1.0.11.23,2.0.21.24,4.0.12.19,1.2.8.21,1.2.8.23,3.0.11.22,3.1.16.19,3.0.22.19,8.0.12.23,8.0.13.21,8.0.14.21,7.0.14.24,7.0.13.24,1.0.17.22,2.0.17.24,5.0.17.21,4.0.17.20,4.0.19.20,0.1.19.21,0.3.19.22,4.0.19.24,3.0.23.21,3.0.23.24,3.0.24.20,5.1.24.21,3.0.25.22,5.1.24.24,3.0.24.25,5.0.25.20,2.0.25.21,2.0.25.24,5.0.25.25,4.0.26.20,5.0.26.21,3.0.26.22,3.0.26.23,5.0.26.24,4.0.26.25,3.3.27.19,1.0.27.20,5.0.27.21,5.0.27.22,5.0.27.23,5.0.27.24,2.0.27.25,3.1.27.26,5.0.28.20,4.0.28.21,4.0.28.22,4.0.28.23,4.0.28.24,5.0.28.25,2.0.29.20,1.0.29.21,2.0.29.22,1.0.29.23,2.0.29.24,1.0.29.25,4.0.30.19,3.2.30.20,3.2.30.21,3.2.30.22,3.2.30.23,3.2.30.24,3.2.30.25,4.0.30.26,4.0.31.19,4.0.31.26;;"
#^C/4 sawtooth
#V1 = "V1;50;50;;0.0.26.20,1.0.25.21,1.0.25.19,1.0.29.18,0.3.29.19,4.0.29.16,4.0.29.22,5.0.29.21,5.0.29.17,4.2.28.19,0.1.28.21,4.1.28.22,4.1.30.19,4.1.27.19,3.0.23.20,1.0.20.19,1.0.20.21;;"
#^C/2 synth
#V1 = "V1;50;50;;1.0.19.24,1.0.19.26,3.0.22.25,1.0.24.24,1.0.24.26,0.0.25.25,4.1.26.24,4.2.27.24,0.1.27.26,4.1.27.27,4.0.28.21,5.0.28.22,1.0.28.23,0.3.28.24,5.0.28.26,4.0.28.27,4.1.29.24;;"
#V1 = "V1;99;99;;0.2.48.50,0.3.49.50,0.1.48.49,0.0.49.49,1.0.50.48,6.0.98.1,6.0.98.2,6.0.98.3,6.0.98.4,6.0.98.5,6.0.98.6,6.0.98.7,6.0.98.8,6.0.98.9,6.0.98.10,6.0.98.14,6.0.98.15,6.0.98.13,6.0.98.12,6.0.98.11,6.0.98.16,6.0.98.17,6.0.98.18,6.0.98.19,6.0.98.20,6.0.98.21,6.0.98.22,6.0.98.23,6.0.98.24,6.0.98.25,6.0.98.26,6.0.98.27,6.0.98.28,6.0.98.29,6.0.98.30,6.0.98.31,6.0.98.32,6.0.98.33,6.0.98.34,6.0.98.35,6.0.98.36,6.0.98.37,6.0.98.38,6.0.98.39,6.0.98.40,6.0.98.41,6.0.98.42,6.0.98.43,6.0.98.44,6.0.98.45,6.0.98.46,6.0.98.47,6.0.98.48,6.0.98.49,6.0.98.50,6.0.98.51,6.0.98.52,6.0.98.53,6.0.98.54,6.0.98.55,6.0.98.56,6.0.98.57,6.0.98.58,6.0.98.59,6.0.98.60,6.0.98.61,6.0.98.62,6.0.98.63,6.0.98.64,6.0.98.65,6.0.98.66,6.0.98.67,6.0.98.68,6.0.98.69,6.0.98.70,6.0.98.71,6.0.98.72,6.0.98.73,6.0.98.74,6.0.98.75,6.0.98.76,6.0.98.77,6.0.98.78,6.0.98.79,6.0.98.80,6.0.98.81,6.0.98.82,6.0.98.83,6.0.98.84,6.0.98.85,6.0.98.86,6.0.98.87,6.0.98.88,6.0.98.89,6.0.98.90,6.0.98.91,6.0.98.92,6.0.98.93,6.0.98.94,6.0.98.95,6.0.98.96,6.0.98.97,6.3.98.98,6.3.97.98,6.3.96.98,6.3.95.98,6.3.94.98,6.3.93.98,6.3.92.98,6.3.91.98,6.3.90.98,6.3.89.98,6.3.88.98,6.3.87.98,6.3.86.98,6.3.85.98,6.3.84.98,6.3.83.98,6.3.82.98,6.3.81.98,6.3.80.98,6.3.79.98,6.3.78.98,6.3.77.98,6.3.76.98,6.3.75.98,6.3.74.98,6.3.73.98,6.3.72.98,6.3.71.98,6.3.70.98,6.3.69.98,6.3.68.98,6.3.67.98,6.3.66.98,6.3.65.98,6.3.64.98,6.3.63.98,6.3.62.98,6.3.61.98,6.3.60.98,6.3.59.98,6.3.58.98,6.3.57.98,6.3.56.98,6.3.55.98,6.3.54.98,6.3.53.98,6.3.52.98,6.3.51.98,6.3.50.98,6.3.49.98,6.3.48.98,6.3.47.98,6.3.46.98,6.3.45.98,6.3.44.98,6.3.43.98,6.3.42.98,6.3.41.98,6.3.40.98,6.3.39.98,6.3.38.98,6.3.37.98,6.3.36.98,6.3.35.98,6.3.34.98,6.3.33.98,6.3.32.98,6.3.31.98,6.3.30.98,6.3.29.98,6.3.28.98,6.3.27.98,6.3.26.98,6.3.25.98,6.3.24.98,6.3.23.98,6.3.22.98,6.3.21.98,6.3.20.98,6.3.19.98,6.3.18.98,6.3.17.98,6.3.16.98,6.3.15.98,6.3.14.98,6.3.13.98,6.3.12.98,6.3.11.98,6.3.10.98,6.3.9.98,6.3.8.98,6.3.7.98,6.3.6.98,6.3.5.98,6.3.4.98,6.3.3.98,6.3.2.98,6.3.1.98,6.2.0.1,6.2.0.2,6.2.0.3,6.2.0.4,6.2.0.5,6.2.0.6,6.2.0.7,6.2.0.8,6.2.0.9,6.2.0.10,6.2.0.11,6.2.0.12,6.2.0.13,6.2.0.14,6.2.0.15,6.2.0.16,6.2.0.17,6.2.0.18,6.2.0.19,6.2.0.20,6.2.0.21,6.2.0.22,6.2.0.23,6.2.0.24,6.2.0.25,6.2.0.26,6.2.0.27,6.2.0.28,6.2.0.29,6.2.0.30,6.2.0.31,6.2.0.32,6.2.0.33,6.2.0.34,6.2.0.35,6.2.0.36,6.2.0.37,6.2.0.38,6.2.0.39,6.2.0.40,6.2.0.41,6.2.0.42,6.2.0.43,6.2.0.44,6.2.0.45,6.2.0.46,6.2.0.47,6.2.0.48,6.2.0.49,6.2.0.50,6.2.0.51,6.2.0.52,6.2.0.53,6.2.0.54,6.2.0.55,6.2.0.56,6.2.0.57,6.2.0.58,6.2.0.59,6.2.0.60,6.2.0.61,6.2.0.62,6.2.0.63,6.2.0.64,6.2.0.65,6.2.0.66,6.2.0.67,6.2.0.68,6.2.0.69,6.2.0.70,6.2.0.71,6.2.0.72,6.2.0.73,6.2.0.74,6.2.0.75,6.2.0.76,6.2.0.77,6.2.0.78,6.2.0.79,6.2.0.80,6.2.0.81,6.2.0.82,6.2.0.83,6.2.0.84,6.2.0.85,6.2.0.86,6.2.0.87,6.2.0.88,6.2.0.89,6.2.0.90,6.2.0.91,6.2.0.92,6.2.0.93,6.2.0.94,6.2.0.95,6.2.0.96,6.2.0.97,6.2.0.98,6.1.98.0,6.1.97.0,6.1.96.0,6.1.95.0,6.1.94.0,6.1.93.0,6.1.92.0,6.1.91.0,6.1.90.0,6.1.89.0,6.1.88.0,6.1.87.0,6.1.86.0,6.1.85.0,6.1.84.0,6.1.83.0,6.1.82.0,6.1.81.0,6.1.80.0,6.1.79.0,6.1.78.0,6.1.77.0,6.1.76.0,6.1.75.0,6.1.74.0,6.1.73.0,6.1.72.0,6.1.71.0,6.1.70.0,6.1.69.0,6.1.68.0,6.1.67.0,6.1.66.0,6.1.65.0,6.1.64.0,6.1.63.0,6.1.62.0,6.1.61.0,6.1.60.0,6.1.59.0,6.1.58.0,6.1.57.0,6.1.56.0,6.1.55.0,6.1.54.0,6.1.53.0,6.1.52.0,6.1.51.0,6.1.50.0,6.1.49.0,6.1.48.0,6.1.47.0,6.1.46.0,6.1.45.0,6.1.44.0,6.1.43.0,6.1.42.0,6.1.41.0,6.1.40.0,6.1.39.0,6.1.38.0,6.1.37.0,6.1.36.0,6.1.35.0,6.1.34.0,6.1.33.0,6.1.32.0,6.1.31.0,6.1.30.0,6.1.29.0,6.1.28.0,6.1.27.0,6.1.26.0,6.1.25.0,6.1.24.0,6.1.23.0,6.1.22.0,6.1.21.0,6.1.20.0,6.1.19.0,6.1.18.0,6.1.17.0,6.1.16.0,6.1.15.0,6.1.14.0,6.1.13.0,6.1.12.0,6.1.11.0,6.1.10.0,6.1.9.0,6.1.8.0,6.1.7.0,6.1.6.0,6.1.5.0,6.1.4.0,6.1.3.0,6.1.2.0,6.1.1.0,6.1.0.0;;"
#^Bigger nuke
#V1 = "V1;24;9;;2.0.8.0,2.0.14.0,1.0.3.3,0.0.4.4,1.0.13.4,1.0.3.5,2.0.13.6,4.0.4.1,1.2.0.3,1.2.0.5,3.0.3.4,3.1.8.1,3.0.14.1,8.0.4.5,8.0.5.3,8.0.6.3,7.0.6.6,7.0.5.6,1.0.9.4,2.0.9.6,5.0.9.3,4.0.9.2,4.0.11.2,0.1.11.3,0.3.11.4,4.0.11.6,3.0.15.3,3.0.15.6,3.0.16.2,5.1.16.3,3.0.17.4,5.1.16.6,3.0.16.7,5.0.17.2,2.0.17.3,2.0.17.6,5.0.17.7,4.0.18.2,5.0.18.3,3.0.18.4,3.0.18.5,5.0.18.6,4.0.18.7,3.3.19.1,1.0.19.2,5.0.19.3,5.0.19.4,5.0.19.5,5.0.19.6,2.0.19.7,3.1.19.8,5.0.20.2,4.0.20.3,4.0.20.4,4.0.20.5,4.0.20.6,5.0.20.7,2.0.21.2,1.0.21.3,2.0.21.4,1.0.21.5,2.0.21.6,1.0.21.7,4.0.22.1,3.2.22.2,3.2.22.3,3.2.22.4,3.2.22.5,3.2.22.6,3.2.22.7,4.0.22.8,4.0.23.1,4.0.23.8;;"
#^Output test for... the output. Same as "C/4 sawtooth"
#V1 = "V1;99;99;;0.0.1.1,0.0.2.2,0.0.3.3,0.0.4.4,0.0.5.5,0.0.6.6,0.0.7.7,0.0.8.8,0.0.9.9,0.0.10.10,0.0.11.11,0.0.12.12,0.0.13.13,0.0.14.14,0.0.15.15,0.0.16.16,0.0.17.17,0.0.18.18,0.0.19.19,0.0.20.20,0.0.21.21,0.0.22.22,0.0.23.23,0.0.24.24,0.0.25.25,0.0.26.26,0.0.27.27,0.0.28.28,0.0.29.29,0.0.30.30,0.0.31.31,0.0.32.32,0.0.33.33,0.0.34.34,0.0.35.35,0.0.36.36,0.0.37.37,0.0.38.38,0.0.39.39,0.0.40.40,0.0.41.41,0.0.42.42,0.0.43.43,0.0.44.44,0.0.45.45,0.0.46.46,0.0.47.47,0.0.48.48,0.0.49.49,0.0.50.50,0.0.51.51,0.0.52.52,0.0.53.53,0.0.54.54,0.0.55.55,0.0.56.56,0.0.57.57,0.0.58.58,0.0.59.59,0.0.60.60,0.0.61.61,0.0.62.62,0.0.63.63,0.0.64.64,0.0.65.65,0.0.66.66,0.0.67.67,0.0.68.68,0.0.69.69,0.0.70.70,0.0.71.71,0.0.72.72,0.0.73.73,0.0.74.74,0.0.75.75,0.0.76.76,0.0.77.77,0.0.78.78,0.0.79.79,0.0.80.80,0.0.81.81,0.0.82.82,0.0.83.83,0.0.84.84,0.0.85.85,0.0.86.86,0.0.87.87,0.0.88.88,0.0.89.89,0.0.90.90,0.0.91.91,0.0.92.92,0.0.93.93,0.0.94.94,0.0.95.95,0.0.96.96,0.0.97.97,0.0.98.98,0.0.0.0,1.0.43.44;;"
#^Grid maker
#V1 = "V1;50;50;;3.0.18.24,3.0.18.25,3.0.19.25,3.0.20.26,4.0.21.26,5.0.22.25,5.0.23.25,5.0.24.25,0.0.25.25,0.1.25.24,0.0.24.23,0.1.25.22,5.0.19.24,5.0.20.25,3.0.24.24,7.0.23.23,3.2.26.25,2.0.20.24,2.0.22.24,3.0.20.22,0.0.21.25,0.1.21.24,0.0.22.23,0.1.21.22,0.3.19.23,7.0.20.23,3.0.17.23,3.0.24.22,7.0.23.21;;"
#^Enemy mover
#V1 = "V1;10;10;;3.3.5.0,3.3.4.0,1.0.4.2,2.0.5.2,1.0.3.4,2.0.6.4,3.0.4.3,3.2.5.3,4.0.5.1,4.0.4.1;;"
#^Small c/4 I made
V1 = "V1;20;7;;2.0.8.0,2.0.14.0,1.0.3.3,0.0.4.4,1.0.13.4,1.0.3.5,2.0.13.6,1.2.0.3,1.2.0.5,3.0.3.4,3.1.8.1,3.0.14.1,8.0.4.5,8.0.5.3,8.0.6.3,7.0.6.6,7.0.5.6,1.0.9.4,2.0.9.6,5.0.9.3,4.0.9.2,4.0.11.2,0.1.11.3,0.3.11.4,4.0.11.6,3.0.15.3,3.0.15.6,4.0.16.3,3.0.17.4,4.0.16.6,2.0.17.3,2.0.17.6,3.2.18.6,3.2.18.3,2.0.19.5,2.0.19.2;;"
#^Better C/4 sawtooth



cellsBASE = V1IN(V1)


            
    #print(cellsBASE)





cellsA = dcopy(cellsBASE)
cellsB = cellsA.copy()

colors = [
(0,255,0),
(0,0,255),
(255,75,0),
(50,200,50),
(255,200,0),
(255,200,0),
(255,0,0),
(255,0,255),
(100,100,100),
(100,100,100),
]

details = [
 [[(255,255,255),(0.1,0.4),(0.6,0.4),(0.6,0.2),(0.8,0.5),(0.6,0.8),(0.6,0.6),(0.1,0.6)]],#duplicator
 [[(255,255,255),(0.2,0.2),(0.8,0.5),(0.2,0.8)]],#pusher
 [[(255,255,255),(0.2,0.7),(0.2,0.2),(0.8,0.2),(0.8,0.7),(0.9,0.7),(0.7,0.9),(0.5,0.7),(0.6,0.7),(0.6,0.6),(0.6,0.4),(0.4,0.4),(0.4,0.7)]],#cw rotator
 [],#ccw rotator
 [[(255,255,255),(0.2,0.2),(0.2,0.8),(0.8,0.8),(0.8,0.2)]],#omni block
 [[(255,255,255),(0.2,0.4),(0.2,0.6),(0.8,0.6),(0.8,0.4)]],#one-way block
 [[(0,0,0),(0.2,0.2),(0.4,0.4),(0.2,0.4)],[(0,0,0),(0.8,0.2),(0.6,0.4),(0.8,0.4)],[(0,0,0),(0.2,0.6),(0.8,0.6),(0.8,0.8),(0.7,0.8),(0.7,0.7),(0.3,0.7),(0.3,0.8),(0.2,0.8)]],#bad blob
 [],#bin
 [],#wall
 [[(255,255,255),(0.15,0.15),(0.5,0.1),(0.85,0.15),(0.85,0.5),(0.5,0.95),(0.15,0.5)]],#invinci
]
for i in range(len(details[2])):
    details[3].append([])
    details[3][i].append(details[2][i][0])
    for j in details[2][i][1:]:
        details[3][i].append(((j[0]-0.5)*-1+0.5,j[1]))

UI = [
 [[(255,255,255),(0,0),(1,0.5),(0,1)]],
 [[(255,255,255),(0,0),(0.1,0),(0.1,1),(0,1)],[(255,255,255),(0.2,0),(1,0.5),(0.2,1)]],
 [[(255,255,255),(0.2,0.7),(0.2,0.2),(0.8,0.2),(0.8,0.7),(0.9,0.7),(0.7,0.9),(0.5,0.7),(0.6,0.7),(0.6,0.6),(0.6,0.4),(0.4,0.4),(0.4,0.7)]],
]
UI_positions = [(0,0,True),(1,0,True),(0,1,False)]



pygame.init()
pygame.display.set_caption("Cell Machine")
screen = pygame.display.set_mode((gx,gy))
dis = pygame.PixelArray(screen)

old_pressed = pygame.key.get_pressed()


running = True
while running:
    zom = 0
    msX,msY = 0,0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEWHEEL:
            zom = event.y
    input_key = -1
    pressed = pygame.key.get_pressed()
    if (pressed[pygame.K_LEFT] or pressed[pygame.K_a]):
        msX -= 1
    if (pressed[pygame.K_RIGHT] or pressed[pygame.K_d]):
        msX += 1
    if (pressed[pygame.K_UP] or pressed[pygame.K_w]):
        msY -= 1
    if (pressed[pygame.K_DOWN] or pressed[pygame.K_s]):
        msY += 1
    if pressed[pygame.K_0]:
        input_key = 0
    if pressed[pygame.K_1]:
        input_key = 1
    if pressed[pygame.K_2]:
        input_key = 2
    if pressed[pygame.K_3]:
        input_key = 3
    if pressed[pygame.K_4]:
        input_key = 4
    if pressed[pygame.K_5]:
        input_key = 5
    if pressed[pygame.K_6]:
        input_key = 6
    if pressed[pygame.K_7]:
        input_key = 7
    if pressed[pygame.K_8]:
        input_key = 8
    if pressed[pygame.K_9]:
        input_key = 9
    if pressed[pygame.K_q] and not old_pressed[pygame.K_q]:
        cur_ghost[4] = ((cur_ghost[4]-5)%4+4)%4
    if pressed[pygame.K_e] and not old_pressed[pygame.K_e]:
        cur_ghost[4] = ((cur_ghost[4]-3)%4+4)%4
    if pressed[pygame.K_COMMA] and not old_pressed[pygame.K_COMMA]:
        zom = -1
    if pressed[pygame.K_PERIOD] and not old_pressed[pygame.K_PERIOD]:
        zom = 1
    if (pressed[pygame.K_LCTRL] and pressed[pygame.K_v]) and not (old_pressed[pygame.K_LCTRL] and old_pressed[pygame.K_v]):
        if clip:
            OpenC()
            cellsBASE = V1IN(GetC())
            CloseC()
        else:
            cellsBASE = V1IN(input("Level code in V1 format:\n"))
        frame = 0
        play = False
        cellsA = dcopy(cellsBASE)
        cellsB = cellsA.copy()
        midx = (disar[0][0]+disar[1][0])/2
        midy = (disar[0][1]+disar[1][1])/2
        difx = midx - disar[2][0]
        dify = midy - disar[2][1]
        disar[0][0] -= difx
        disar[0][1] -= dify
        disar[1][0] -= difx
        disar[1][1] -= dify
        print("Level has been loaded")
    if (pressed[pygame.K_LCTRL] and pressed[pygame.K_c]) and not (old_pressed[pygame.K_LCTRL] and old_pressed[pygame.K_c]):
        
        if clip:
            OpenC()
            EmptyC()
            SetC(V1OUT(cellsA))
            CloseC()
            print("The V1 code has been copied to clipboard")
        else:
            print("The V1 code:\n"+V1OUT(cellsA))
            
    old_pressed = pressed
    
        

    key = [*cellsA.keys()]
    ms = pygame.mouse.get_pressed()
    ms_pos = pygame.mouse.get_pos()
    msx = ms_pos[0]
    msy = ms_pos[1]
    

    #UI detection

    if frame == 0:
        difx = abs(disar[0][0]-disar[1][0])
        dify = abs(disar[0][1]-disar[1][1])
        px = msx/gx*difx + disar[0][0]
        py = msy/gy*dify + disar[0][1]
        px = flr(px+0.5)
        py = flr(py+0.5)
        cur_ghost[0:3] = [True,px,py]
    else:
        cur_ghost[0] = False

    click = ms[0] or pressed[pygame.K_SPACE]
    if click or ms[2]:
        menu = not old_click
        if click:
            for i in range(len(UI_positions)):
                curpos = UI_positions[i]
                if (curpos[2] or frame != 0) and place_valid:
                    px = UI_base_gap*UI_size + (UI_button_gap * UI_size + UI_size)*curpos[0]
                    py = gy - (UI_base_gap*UI_size + (UI_button_gap * UI_size + UI_size)*curpos[1] + UI_size)
                    
                    top = py
                    bottom = py+UI_size
                    left = px
                    right = px+UI_size
                    if msy >= top and msy <= bottom and msx >= left and msx <= right:
                        place_valid = False
                        if menu:
                            if i == 0:
                                play = not play
                            elif i == 1:
                                play = False
                                skip = True
                            elif i == 2:
                                frame = 0
                                play = False
                                cellsA = dcopy(cellsBASE)
                                cellsB = cellsA.copy()
                                midx = (disar[0][0]+disar[1][0])/2
                                midy = (disar[0][1]+disar[1][1])/2
                                difx = midx - disar[2][0]
                                dify = midy - disar[2][1]
                                disar[0][0] -= difx
                                disar[0][1] -= dify
                                disar[1][0] -= difx
                                disar[1][1] -= dify
                            
        #print(valid)
    
        if place_valid: #does block placement
            
            #print(px,py,disar)
            #[type,rotation,oldx,oldy,current rotation,old rotation]
            difx = abs(disar[0][0]-disar[1][0])
            dify = abs(disar[0][1]-disar[1][1])
            px = msx/gx*difx + disar[0][0]
            py = msy/gy*dify + disar[0][1]
            px = flr(px+0.5)
            py = flr(py+0.5)
            if click:
                cellsBASE[(px,py)] = [cur_ghost[3],cur_ghost[4],px,py,cur_ghost[4],cur_ghost[4]]
            elif ms[2]:
                if (px,py) in cellsBASE:
                    cellsBASE.pop((px,py))
            if click or ms[2]:
                cellsA = dcopy(cellsBASE)
                cellsB = cellsA.copy()
    else:
        place_valid = True
    #print(play)
    #print(frame)
            
    old_click = click
    old_ms = ms
    #V1 = "V1;50;50;;3.0.23.21,3.0.24.21;;"
    #^Two pushers
    
    if msX != 0 or msY != 0:
        panx = msX*pan_speed[0]*delta/1000
        pany = msY*pan_speed[1]*delta/1000
        difx = abs(disar[0][0]-disar[1][0])
        dify = abs(disar[0][1]-disar[1][1])
        panx *= difx
        pany *= dify
        disar[0][0]+=panx
        disar[0][1]+=pany
        disar[1][0]+=panx
        disar[1][1]+=pany
    
    if input_key != -1:
        key_map = "1234567890"
        cur_ghost[3] = key_map.find(str(input_key))
        
    if zom != 0:
        if (pressed[pygame.K_LSHIFT]):
            if zom > 0:
                muli = 1/calc_mult
            else:
                muli = calc_mult
            calc_gap *= muli
            
        else:
            outx = (disar[0][0]+disar[1][0])/2
            outy = (disar[0][1]+disar[1][1])/2
            if zom > 0:
                muli = 1/zoom_speed
            else:
                muli = zoom_speed
            #print(muli,outx,disar)
            disar[0][0] = (disar[0][0]-outx)*muli+outx
            disar[0][1] = (disar[0][1]-outy)*muli+outy
            disar[1][0] = (disar[1][0]-outx)*muli+outx
            disar[1][1] = (disar[1][1]-outy)*muli+outy
            #print(disar)
            
            
        
    cellsA = cellsB.copy()
    key = [*cellsA.keys()]
    #print(key)
    #for i in key:
    #    print(i,cellsA[i])
    #halt

    
    render()
    
    if not (play or skip):
        calc_last = pygame.time.get_ticks()-calc_gap

    if pygame.time.get_ticks() > (calc_last+calc_gap) and (play or skip):
        skip = False
        #print("OK")
        calc_last = pygame.time.get_ticks()
        
        cellsA = cellsB.copy()
        #print(cellsB)
        key = [*cellsB.keys()]
        for i in key:
            cellsB[i][2:4] = list(i)
            cellsB[i][5] = cellsB[i][4]
        cellsA = cellsB.copy()
        
        
        for des in range(3): #checks for duplicators, rotators, then pushers in the same bowl of spaghetti
            frame += 1
            for rot in range(4):
                rot = [0,2,3,1][rot]
                cellsA = cellsB.copy()
                key = [*cellsA.keys()]
                key.sort(reverse=(rot<=1))
                #print(rot,(rot<=2))
                #render()
                for i in key:
                    #ini_dict['akash'] = ini_dict.pop('akshat')
                    #print(cellsA)
                    cur = cellsB[i]

                    xdif,ydif = 0,0
                    

                    if (cur[0] == 2 or cur[0] == 3) and des == 1: #does rotator logic
                        if rot == 0: #the same as the pusher one, but different so requires different code
                            xdif = 1
                        elif rot == 1:
                            ydif = 1
                        elif rot == 2:
                            xdif = -1
                        elif rot == 3:
                            ydif = -1
                        newx = i[0] + xdif
                        newy = i[1] + ydif
                        
                        if (newx,newy) in cellsA:
                            rotation = ((cur[0]-2)*2-1)*-1 #outputs a negative if ccw, positive if cw
                            
                            rotation = cellsA[(newx,newy)][4] + rotation #adds that to the curent rotation of the cell
                            cellsA[(newx,newy)][4] = rotation #outputs the raw value
                            rotation = ((rotation)%4+4)%4 #bodge job to get it in the 0-3 range, not nesesary but looks nicer
                            cellsA[(newx,newy)][1] = rotation #outputs it to the cell

                    if cur[1] == 0: #a line of ifs to see where it should be going, because... I cba to figure out the math
                        xdif = 1
                    elif cur[1] == 1:
                        ydif = 1
                    elif cur[1] == 2:
                        xdif = -1
                    elif cur[1] == 3:
                        ydif = -1
                    
                    pusher_check = (cur[0] == 1 and des == 2)
                    duplicator_check = (cur[0] == 0 and des == 0 and ((i[0]-xdif,i[1]-ydif) in cellsA))
                    
                    
                    if cur[1] == rot and (pusher_check or duplicator_check): #does pusher + duplicator logic
                        #if duplicator_check:
                        #    print(cur)
                        #render()
                        #print("OK",i)
                        power = 1 #controls the tests for counter-pushers
                        valid = True
                        cont = False
                        newx = i[0]
                        newy = i[1]
                        while valid and not cont: #checks the spaces in front to see if it should move
                            oldx = newx
                            oldy = newy
                            newx += xdif
                            newy += ydif
                            if (newx,newy) in cellsB:
                                tst = cellsB[(newx,newy)]
                                invinci_test = cellsB[(oldx,oldy)][0] != 9
                                if tst[0] == 8: #checks for wall
                                    valid = False
                                elif tst[0] == 5: #checks for one-way blocks
                                    if tst[1]%2 == cur[1]%2: #checks their rotation
                                        valid = True
                                    else:
                                        valid = False
                                elif ((tst[0] == 6 and invinci_test) or (cellsB[(oldx,oldy)][0] == 6 and tst[0] != 9) or tst[0] == 7): #checks for enemys, ignores them
                                    valid = True
                                    cont = True
                                elif cellsB[(newx,newy)][0] == 1: #checks for counter-pushers
                                    dif = abs(cur[1]-cellsB[(newx,newy)][1])
                                    filt = ((dif+1)%2) #results in a 0 if it's perpendicular to it
                                    dif = ((dif-1)*filt)*-1 #outputs a -1 if against it, 1 if with it, and 0 if perpendicular to it
                                    #print(dif)
                                    power += dif      
                            else:
                                valid = True
                                cont = True
                            #print(power)
                            if power == 0:
                                #print(power)
                                valid = False
                            elif power < 0:
                                print("BUG WITH THE POWER SYSTEM")
                            
                            
                        if valid:
                            if cur[0] == 0:
                                cur_key = (i[0]+xdif,i[1]+ydif)
                            elif cur[0] == 1:
                                cur_key = i
                            else:
                                print("BUG WITH THE CUR_KEY SYSTEM")
                            while newx != cur_key[0] or newy != cur_key[1]: #moves all the blocks along
                                if (newx,newy) in cellsB:
                                    tst = cellsB[(newx,newy)]
                                    if tst[0] == 7:
                                        cellsB.pop((newx-xdif,newy-ydif))
                                    elif tst[0] == 6 or (cellsB[(newx-xdif,newy-ydif)][0] == 6):
                                        #print("OK")
                                        cellsB.pop((newx,newy))
                                        cellsB.pop((newx-xdif,newy-ydif))
                                    
                                    else:
                                        print("BUG WITH THE MOVEMENT SYSTEM", cellsB[(newx-xdif,newy-ydif)],tst)
                                        #print((newx,newy))
                                        #cellsA[(newx,newy)] = cellsA.pop((newx-xdif,newy-ydif))
                                else:   
                                    cellsB[(newx,newy)] = cellsB.pop((newx-xdif,newy-ydif))
                                    #key[key.index((newx-xdif,newy-ydif))] = (newx,newy)
                                #print(key)
                                #key.pop(key.index((newx-xdif,newy-ydif)))
                                newx -= xdif
                                newy -= ydif
                            if cur[0] == 0: #extra bit to do the block duplication
                                valid = True
                                if cur_key in cellsB:
                                    if cellsB[cur_key][0] == 6:
                                        valid = False
                                if valid:
                                    cellsB[cur_key] = cellsA[(i[0]-xdif,i[1]-ydif)].copy()
                                    cellsB[cur_key][2:4] = list(i)
                                else:
                                    cellsB.pop(cur_key)
        cellsA = cellsB.copy()
        

        
    
    
    delta1 = pygame.time.get_ticks()
    delta = delta1 - delta2
    delta2 = pygame.time.get_ticks()
    
    
    
pygame.quit()
