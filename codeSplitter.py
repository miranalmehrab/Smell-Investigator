import os
import glob
import shutil


def deleteAndRecreateFolder(folder):

    try:
        shutil.rmtree(folder)
        os.mkdir(folder)
    except:
        print('error in recreating dir '+folder)


def createFolderAfterInterval(pFolder,cFolder,interval):
    
    deleteAndRecreateFolder(cFolder)
    
    srcCodeFiles =  glob.glob(pFolder+"/*.py")
    print(len(srcCodeFiles))
    counter = 0
    
    for srcFile in srcCodeFiles:

        if counter % interval == 0 : os.mkdir(cFolder+"/"+"srcs-"+str(int(counter/interval)))    
        rf = open(srcFile, "r")
        sFileNameFromDir = srcFile.split("/")[-1]
        
        wf = open(cFolder+"/srcs-"+str(int(counter/interval))+"/"+sFileNameFromDir, "w")
        wf.write(rf.read())
        wf.close()

        counter = counter + 1


def main():
    createFolderAfterInterval("gist-src","src-codes",10)

if __name__ == "__main__":
    main()



