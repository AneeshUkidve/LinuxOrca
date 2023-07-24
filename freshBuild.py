import os
import time

def wipeAll(jobDir, fileName):
    os.system(f"cp {jobDir}/{fileName}.inp {jobDir}/{fileName}.gbw {jobDir}/{fileName}.xyz temp/")
    os.system(f"cp {jobDir}/{fileName}.out outFiles/")
    os.system(f"rm {jobDir}/*")
    os.system(f"mv temp/{fileName}.gbw temp/old.gbw")

    print("done")   



#Takes one line from the xyz file as input and returns the extracted element name, coords as a list
def createTup(line):
    line = line.replace('\n', '')
    rud = line.split('     ') #breaks line into 3 rudimentary strings [(name + x), (y), (z)] and stores  in rud

    #extracts the atom name and x coordinate from the first string of rud
    rud[0] = rud[0].lstrip()
    rud[0] = rud[0].replace('  ', ']')
    rud[0] = rud[0].replace(' ', '')
    a,b = rud[0].split(']')
    
    return [a, b, rud[1].lstrip(), rud[2].lstrip()]


def recreate(jobDir, fileName):
    #Scrape through xyz file and get raw coordinates
    coords = []
    with open(f"temp/{fileName}.xyz", 'r') as f:
        a = f.readlines()
    for i in range(2, len(a)):
        coords.append(createTup(a[i]))

    #repackage the extracted coordinates into the format for inp file
    coordLines = ''
    for coord in coords:
        #This essentially boils down to 3 things: 
        
        #Step 1) Make all the coords to be exactly 5 decimal digits
        for i in range(1,4):
            coord[i] = str(round(float(coord[i]), 5))
            zeros = 5 - len(coord[i].split('.')[1])
            coord[i] = coord[i] + "0"*zeros
        
        #Step 2) Calculate the number of spaces in between each segment
        sp1 = 4 - len(coord[0])
        sp2 = 9 - len(coord[1].split('.')[0])
        sp3 = 9 - len(coord[2].split('.')[0])
        sp4 = 9 - len(coord[3].split('.')[0])

        #slap everything together with a newline character at the end
        line = ' '*sp1 + coord[0] + ' '*sp2 + coord[1] + ' '*sp3 + coord[2] + ' '*sp4 + coord[3] + '\n'
        coordLines += line
    coordLines += "*"

    #extract the commands et al from the original input file
    with open(f"temp/{fileName}.inp", 'r') as f:
        a = f.readlines()
    commandLines = ''
    for i in a:
        if i[0] == '*':
            commandLines += i
            break
        commandLines += i

    #Make a new inp file and put everything in it
    with open(f"{jobDir}/{fileName}.inp", 'w') as f:
        f.write(commandLines + coordLines)

    #transfer everything back to jobDir and wipe temp
    os.system(f"mv temp/old.gbw {jobDir}/old.gbw")
    os.system("rm temp/*")

    print("Successful Reboot")

