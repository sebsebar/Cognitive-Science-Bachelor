# this is the awesome experiment of group 9, specifically Sebastian Scott Engen <3
# First we import modules
from psychopy import visual, core, event, gui
# espacially we'll import the module that fetch file names
import glob
# and then we import we'll a module that allow us to write a log file with our data frame
import pandas as pd

# First we create a popup information box the participant should fill out
popup = gui.Dlg(title = "Reading Experiment")
popup.addField("Full Name: ") 
popup.addField("Age: ")
popup.addField("Gender: ", choices=["Female", "Male", "Other" ]) # Dropdown menu
popup.addField("Conditions: ", choices=["1","2"]) # Dropdown menu
# We show them the popup
popup.show()
# We retrieve the data from our popup window, we inscripe it to a list that we can use for later reference
if popup.OK: 
    ID = popup.data
# Then to make sure we don't get wierd empty data, we make it cancel the experiment if the popup is closed
elif popup.Cancel: 
    core.quit()

# We define a stopwatch
stopwatch = core.Clock()

# We define a window 
win = visual.Window(color ="white", fullscr = True)

# We define a message box with a full white-screen with black text
def msg(txt, c):
    msg = visual.TextStim(win, text=txt, color = c, height = 0.08) # we create a text
    msg.draw() # we draw the text stimulus in a "hidden screen" so that it is ready to be presented 
    win.flip() # we flip the screen to reveal the text stimulus

# We prepare a log file data frame with columns
DATA = pd.DataFrame(columns = ['Full Name', 'Age', 'Gender', 'Condition', 'Word', 'Reaction Time'])

# We prepare a intro message with instructions for the participant
intro = '''
<3 Welcome to our reading experiment <3

You'll soon be presented with a short story of approximately 200 words that we'll want you to read at your own pace.
Press space to move forward to the next word, in whatever speed feels suitable for you. '''


# we use the pre-defined msg-function to show the instructions to the participant
msg(intro,"black")
key = event.waitKeys(keyList = ['space', 'escape']) # we make it wait for a space key-press, and quit experiment with escape
if key[0] == 'escape':
    core.quit()


# Here we inscripe our Original fairytale with no alterations
txt1 = ''' Once in the wintertime when the snow was very deep, a poor boy had to go out and fetch wood on a sled. After he had gathered it together and loaded it, he did not want to go straight home, because he was so frozen, but instead to make a fire and warm himself a little first. So he scraped the snow away, and while he was thus clearing the ground he found a small golden key. Now he believed that where there was a key, there must also be a lock, so he dug in the ground and found a little iron chest. "If only the key fits!" he thought. "Certainly there are valuable things in the chest." He looked, but there was no keyhole. Finally he found one, but so small that it could scarcely be seen. He tried the key, and fortunately it fitted. Then he turned it once, and now we must wait until he has finished unlocking it and has opened the lid. Then we shall find out what kind of wonderful things there were in the little chest. '''
# txt1 has been split up into a word-list
word_list_text_1 = txt1.split()

# Here we inscripe our altered fairytale where the word 'unlocking' has been changed for 'licking'
txt2 = ''' Once in the wintertime when the snow was very deep, a poor boy had to go out and fetch wood on a sled. After he had gathered it together and loaded it, he did not want to go straight home, because he was so frozen, but instead to make a fire and warm himself a little first. So he scraped the snow away, and while he was thus clearing the ground he found a small golden key. Now he believed that where there was a key, there must also be a lock, so he dug in the ground and found a little iron chest. "If only the key fits!" he thought. "Certainly there are valuable things in the chest." He looked, but there was no keyhole. Finally he found one, but so small that it could scarcely be seen. He tried the key, and fortunately it fitted. Then he turned it once, and now we must wait until he has finished licking it and has opened the lid. Then we shall find out what kind of wonderful things there were in the little chest. '''
# txt2 has been split up into a word-list
word_list_text_2 = txt2.split()

# We let our program know which story has been chosen by the participant
if ID[3] == "1":
    story = word_list_text_1
else:
    story = word_list_text_2

# we loop through the words in our story with the our msg function
for word in story:
    # we present the word, aka. our stimulus
    msg(word, "black")
    stopwatch.reset() # we reset the clock to 0:0:0 
    key = event.waitKeys(keyList = ['space', 'escape']) # we wait for any space key-press or quit experiment with escape
    # we fetch the reaction time at a space key press
    reaction_time = stopwatch.getTime() # we ask the stopwatch for the time since reset and save to the variable Reaction Time
    # Here we define the way to escape the program if fx. the participant wants to quit before time
    if key[0] == 'escape':
        core.quit()
    # Here we append all recorded data to the pandas DATA that can write our logfile 
    DATA = DATA.append({
        'Full Name': ID[0],
        'Age': ID[1],
        'Gender': ID[2],
        'Condition': ID[3], 
        'Word':word,
        'Reaction Time': reaction_time 
        }, ignore_index=True)

# Here we designate all our data to a logfile, which we also name after the participant and their choice of text-condition
logfile_name = 'logfile_' + ID[0] + ID[3] +'.csv'
DATA.to_csv(logfile_name)

# we then prepare an outro with a small goodbye message for the participant
outro = '''The experiment has finished honey
<3 Thank you for your participatation <3 '''

    # show outro
msg(outro,"black")
core.wait(10)
