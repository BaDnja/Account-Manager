import os

def makeFilesPath():
    if os.path.exists("files"):
        pass
    else:
        os.mkdir("./files")

def txtFile():
    if os.path.exists("files/user.txt"):
        pass
    else:
        file= open("files/user.txt","w")
        file.writelines("Demo\n")
        file.writelines("demo123")

makeFilesPath()
txtFile()