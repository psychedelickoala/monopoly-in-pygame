# Monopoly In Pygame
I wrote monopoly in pygame.

# Downloading Game
On Github, you can download the project as a zip folder by pressing the green button that says 'code' then pressing 'download as zip'

You should then create a new folder extract the contents of the zip folder to it.

# Creating an executable file
I tried to create an executable file to run without needing python. Unfortunately this didn't work.

Here are the steps to creating your own application from the files:

  1. Check that you have python installed on your computer. If not, you can download it from here: https://www.python.org/downloads/

  2. Open the Command Prompt (Windows) or Terminal (Mac). 
  
  3. Navigate to the folder that contains main.py in the Command Prompt. I can get to a certain directory, for example C:\username\Downloads\Games\monopoly in pygame\monopoly-in-pygame-main, with the following commands:
    
    cd Downloads
    cd Games
    cd monopoly in pygame
    cd monoply-in-pygame-main
    
  4. Check that you have pip installed. It should be automatically installed with newer versions of python. You can do this by entering the command:
  
    pip
    
  If the command prompt recognises pip, it will print information about pip commands. Otherwise, see the section below on installing pip.
  
  5. Install the pygame module and cx_freeze package (if you haven't already). In the Command Prompt, enter the following commands:
  
    pip install pygame
    pip install cx_freeze
    
  6. Now we can build the application. In the Command Prompt, enter the command:
  
    python setup.py build
    
  7. Close the command prompt. In the directory of main.py, you should notice a folder called build. Select all the files and folders 
  except for the 'build' folder, 'README.md', and any files ending with '.dll' and cut/copy them. Inside the build folder should be another folder, containing a file called main.exe.  Paste the files into this folder.
  
  8. You should be able to open the game and start playing by clicking on main.exe. Thank you for playing my monopoly!


# Installing pip

If you have python but don't have pip, you can install it to the directory of main.py with these steps:

  1. Create a python file in the same directory as main.py called 'get-pip.py'. 

  2. Go to https://bootstrap.pypa.io/get-pip.py. Use ctrl-A to select all the text, copy it, and paste it into get-pip.py. Save get-pip.py and close it.
  
  3. In the Command Prompt, navigate to the directory of get-pip.py.
  
  4. In the Command Prompt, enter the following command:
  
    python get-pip.py
   
  This should install pip. It may take some time.
  
  
