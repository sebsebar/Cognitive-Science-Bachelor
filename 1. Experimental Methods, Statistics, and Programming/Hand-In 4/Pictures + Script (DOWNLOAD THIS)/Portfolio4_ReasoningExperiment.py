 
 #import module that makes it possible to randomize the order of stimuli 
import random
from random import randint
#import module that fetches file names
import glob

# import modules 
from psychopy import visual, core, event, gui
import pandas as pd #import module to handle log file data frame 

#Make a popup information box as start of experiment to type in relevant data 
popup = gui.Dlg(title = "Reasoning Experiment") #add a title to the pop up  
popup.addField("Full Name: ")  #Empty text box to fill with full name
popup.addField("Age: ")  #Empty text box to fill with age
popup.addField("Gender: ", choices=["Female", "Male", "Other" ]) # Dropdown menu with 3 choices of gender
popup.addField("Condition: ", choices = ["1", "2","3"]) # Dropdown menu with 3 choices between the conditions
popup.show() #Show the pop up box with the boxes
#Collect the data from the popup window
if popup.OK: 
    ID = popup.data #save the data as ID, for example the first - Full Name - will be ID[0] and so on
#Cancel experiment if the popup window is closed in beginning 
elif popup.Cancel: 
    core.quit()

#Prepare log file data frame with columns including full name, age, gender, condition, picture, accuracy, and reaction time  
DATA = pd.DataFrame(columns = ['Full Name', 'Age', 'Gender', 'Condition', 'Picture', 'Accuracy', 'Reaction Time'])

#define a window called win
win = visual.Window(color = 'white', fullscr = True) #we want the background to be white
#and have the experiment run in full screen

#define a stop watch so we can record reaction time during the experiment 
stopwatch = core.Clock() 

#define a function for text messages in the window, so we have a short cut to make text messages 
def message(txt, c):  #define it as a message where we can have text and a specific color 
    message = visual.TextStim(win, text = txt, color = c, height = 0.08)  #a visual text stimulus, with text and color 
    message.draw() #draw it to a canvas
    win.flip() #flip the canvas 


#make an intro message to the experiments with instructions. use ''' to make a long text in multiple lines
intro = ''' 
Welcome to The Reasoning Experiment!
You will be presented with 10 logical statements.
Each statement consists of two premises and one conclusion.
Your task is to judge if the conclusion follows directly from the premises.

Don't guess - take your time thinking about them and respond when you have a confident answer.
But also don't take breaks, and don't fall asleep! ;-)

Press the 'a' key to ACCEPT the logical statement (if the conclusion follows directly from the premises)
Press the 'd' key to DENY the logical statement (if the conclusion does NOT follow directly from the premises)

Press any key to start the experiment. 
'''

#make an outro message to the experiment  
outro = '''
The experiment is now finished. 
Thank you for your for participation.

Goodbye!
''' 

#show intro message with instructions after filling in the pop up window
message(intro, "black") #use our message function to show our intro text with black text 
event.waitKeys() #wait for participant to press a key before moving forward 

#images = glob.glob('*.png') #fetch all pictures that are jpg. in the file and create a list with them 

#use if condition to decide which condition (1,2,3 equals different content in the logical statements) to show 
if ID[3] == "1": 
    images = glob.glob('*abs*.png')
elif ID[3] == "2":
    images = glob.glob('*mless*.png')
elif ID[3] == "3":
    images = glob.glob('*mfull*.png')

random.shuffle(images) #shuffle the list

#make a loop 
for i in images:
    stimulus = visual.ImageStim(win, image = i) #make a new variable 
    #draw the new variable on canvas
    stimulus.draw() 
    #flip canvas
    win.flip() 
    
    #reset stop watch as soon as the picture is shown so we can start recording reaction time 
    stopwatch.reset()
    
    #record key press when they press space - also add escape so it is possible to quit the experiment at any time
    key = event.waitKeys(keyList = ['a', 'd','escape'])
    
    #stop the stopwatch when participant presses 'a' or 'd' and get reaction time
    reaction_time = stopwatch.getTime()
    
    #record response of participant and give response
    if key[0] == 'escape':
        core.quit()  #makes it possible to quit test IMPORTANT 
    elif key[0] == 'a'and i[0] == 'a' or key[0] == 'd' and i[0] == 'd':
        correct = 1 #record accuracy
    else:
        correct = 0 #record accuracy
    
    #log the experiment data to panda data frame
    DATA = DATA.append({
        'Full Name': ID[0], #log to a column called Full Name using the data from ID 0 which is the full name from the pop up window 
        'Age': ID[1], #log to a column called Age using the data from ID1 which is the age from the pop up window
        'Gender': ID[2],#log to a column called Gender using the data from ID 2 which is the gender chosen from the pop up window
        'Condition': ID[3],#log to a column called Condition using the data from ID 3 which is the condition chosen from the pop up window
        'Picture' : i,
        'Accuracy': correct, #log to a column called Word using the data 'w' from our loop, which is each word in the text
        'Reaction Time': reaction_time #get the reaction time in a column
        }, ignore_index = True) 

#create a unique file name to a csv using the participants full name and the condition they had
file_name = 'logfile_' + ID[3] + ID[0]+'.csv' 

#save the data frame as a csv file 
DATA.to_csv(file_name)

#show outro message to participant 
message(outro, "black") #use our message function to show our outro text with black text 
core.wait(5) #wait 10 seconds before closing outro message 