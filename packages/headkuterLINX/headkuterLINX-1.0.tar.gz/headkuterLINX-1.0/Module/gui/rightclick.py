import subprocess
def copycontent1():
    '''script = f'sudo apt install python3-nutilus'
    naut = subprocess.run(script,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True)
    print(naut)'''
    #cop = subprocess.Popen(["cp", "~/CopyContent", "~/.local/share/nautilus/scripts/"])
    script = f'cp Module/gui/CopyContent ~/.local/share/nautilus/scripts/'
    cop = subprocess.run(script,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True)
    #print(cop)

    #cop.wait()
    script = 'chmod u+x ~/.local/share/nautilus/scripts/CopyContent'
    excu = subprocess.run(script,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True)
    #print(excu)

def stopcopycontent1():
    
    cop = subprocess.run("rm ~/.local/share/nautilus/scripts/CopyContent", stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell= True)
    
    