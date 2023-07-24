import os
import time
import freshBuild


jobDir = str(input("\n\nProvide Job Directory Relative To This Script: "))
fileName = str(input("Name of input file: "))


orcaPath = "~/orca/orca"

inpFile = jobDir + "/" + fileName + '.inp'

def preCheck():
    try:
        with open(inpFile, 'r') as f:
            pass
        return 0
    except:
        print(f"{inpFile} couldn't be accessed")
        return 1
    
if preCheck():
    input("Press Enter To Exit\n")
    quit()

#Assumes one failure (existence of a gbw file named {fileName}.gbw, {fileName}.xyz)

def isSuccess(jobDir, fileName):
    os.system(f"tail -n 2 {jobDir}/{fileName}.out > temp.txt")
    with open("temp.txt", 'r') as f:
        a = f.readlines()[0]
    b = a.strip(" *\n")
    if b == "ORCA TERMINATED NORMALLY":
        return True
    return False

execLine = orcaPath + " " + inpFile + f" > {jobDir}/{fileName}.out"

fail = 0

normalExit = False
while not normalExit:
    os.system(execLine)
    if isSuccess(jobDir, fileName):
        normalExit = True
    else:
        fail += 1
        print(f"Failure number {fail}")
    freshBuild.wipeAll(jobDir, fileName)
    freshBuild.recreate(jobDir, fileName)

print(f"\nJob ran successfully after failing {fail} times")
input("Press Enter To Exit\n")
