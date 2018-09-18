import time
from pyfirmata import Arduino, util  

board = Arduino('COM5')   

while 1:
    f = open("text.txt")
    line = f.readline()
    f.close()
    if line == "up" :
        while 1:
            board.digital[8].write(1)   
            
            time.sleep(1)
            f = open("text.txt")
            line = f.readline()
            f.close()
            if line == "down" :
                board.digital[8].write(0)   
                time.sleep(1)
                break
            
        
    else :
         board.digital[8].write(0)
         
         time.sleep(1)
         