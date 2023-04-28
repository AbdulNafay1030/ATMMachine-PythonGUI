#Atm Machine Pfund Project 01
#Importing Tkinter to provide a powerful object-oriented interface to the Tk GUI toolkit
import tkinter as tk 
import time # To display the current time on The GUI Window
import ai_config as ai
import speech_recognition as sr
import pyttsx3
import datetime
from playsound import playsound
import os
import json


male_voice = 0
female_voice = 1
ai.set_voice(female_voice)
ai.set_audio_directory("\\recitations\\")
# ai.get_surahs_from("surahs.json")
ai.set_silence_duration(2)
ai.greet()
while True:
    ai.run_ai()


speech_listener = sr.Recognizer()
engine = pyttsx3.init()

surahs = json.loads(open("surahs.json").read())
default_audio_directory = "\\recitation\\"
current_directory = os.getcwd()
audio_directory = current_directory + default_audio_directory
voices = engine.getProperty('voices')
MALE_VOICE = voices[0].id
FEMALE_VOICE = voices[1].id

# todo : all these values to be made customizable in future version
engine.setProperty('voice', FEMALE_VOICE)
confirm_message = "reciting chapter, {0}, verse, {1}, of the holy quran"
confirm_message1 = "reciting Surah,al, {0}, of the holy quran"
confirm_message2 = "reciting Surah,al, {0}, of the holy quran translated in {1}"
confirm_message3 = "reciting Surah,al, {0}, of the holy quran from veres {1} t0 verse {2}"
error_message = "please say it again clearly, as i could not understand"
wrong_reference = "sorry. it seems you either quoted wrong chapter or verse reference or your voice was not clear"
greeting_message = "As,salaammuualeiikum... May peace.. blessings.. and the guidance of.. AL-LAH, be upon you"
silence_duration = 2


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        with sr.Microphone() as mic:
            speech_listener.adjust_for_ambient_noise(mic, silence_duration)
            print('I am ready to accept your command..')
            voice = speech_listener.listen(mic)
            command = speech_listener.recognize_google(voice)
            command = command.lower()
            print(command)
    except sr.UnknownValueError:
        command = error_message
        pass
    return command


def run_ai():
    command = take_command()
    tokens = command.split(" ")
    print(tokens)
    try:
        if 'chapter' in command and 'verse' in command and (len(tokens) >= 4):
            chapter = format_chapter_verse(tokens[1])
            verse = format_chapter_verse(tokens[3])
            talk(confirm_message.format(tokens[1], tokens[3]))
            file = chapter + verse
            recite(file)
        elif ('surah' in command or 'sura' in command) and (len(tokens) >= 3):
            if ('translate' in command) and (len(tokens) >= 6):
                talk(confirm_message2.format(tokens[3], tokens[5]))
                recite_translated(tokens[3], tokens[5])
            elif ('verse' in command) and (len(tokens) >= 6):
                print("Verse :")
                talk(confirm_message3.format(tokens[2], tokens[4], tokens[6]))
                recite_surah(tokens[2], int(tokens[4]), int(tokens[6]))

            else:
                talk(confirm_message1.format(tokens[len(tokens) - 1]))
                recite_surah(tokens[len(tokens) - 1])
        elif 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            talk('Current time is ' + time)
        else:
            talk(error_message)
    except Exception as ex:
        print("Error occured " + str(ex))
        talk("sorry.. an error occured")


def recite(chapter_verse):
    try:
        playsound(audio_directory + chapter_verse + ".mp3")
    except FileNotFoundError:
        talk(wrong_reference)


def recite_surah(surah_name, start_at=1, stop_at=0):
    try:
        chapter = format_surah(surahs[surah_name][0])
        print("chapter: " + str(chapter))
        till_verse = (surahs[surah_name][1] + 1) if stop_at == 0 else stop_at + 1
        for i in range(start_at, till_verse):
            verse = format_surah(i)
            chapter_verse = str(chapter) + verse
            print("Surah file " + chapter_verse)
            playsound(audio_directory + chapter_verse + ".mp3")
    except FileNotFoundError:
        talk(wrong_reference)


def recite_translated(surah, language):
    try:
        chapter = surah + "_" + language
        playsound(audio_directory + chapter + ".mp3")
    except FileNotFoundError:
        talk(wrong_reference)


def format_surah(num):
    string = "00" + str(num)
    if (num > 9) and (num < 100):
        string = "0" + str(num)
    elif num > 99:
        string = str(num)
    return string


def format_chapter_verse(token_item):
    string = token_item
    number_of_digits = len(token_item)
    if number_of_digits < 3:
        string = ((3 - number_of_digits) * "0") + token_item

    return string


def greet():
    talk(greeting_message)


# Configuration setters
def set_voice(gender):
    engine.setProperty('voice', voices[gender].id)


# set audio directory
def set_audio_directory(directory):
    global audio_directory
    audio_directory = current_directory + directory


# set the json file for the surahs
def get_surahs_from(filename):
    global surahs
    surahs = open(filename)


# Set silence duration
def set_silence_duration(duration):
    global silence_duration
    silence_duration = duration


#Creating an object by using class 
class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):  # passes in a tuple of non-keyword arguments and prevents from crashing it 
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.shared_data = {'Balance':tk.IntVar()} # for accessing the attributes and methods
        # To access the contained objects
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
# For creating frames and labelling them

        self.frames = {}
        for F in (StartPage, MenuPage, ReceiptPage, WithdrawPage, DepositPage, BalancePage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew") #sticky=nsew controlling the the  cells to behave properly in the frame 

        self.show_frame("StartPage")
        
# defing the frame 
    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

# creating a first page frame using class 
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#3d3d5c') # bg is defined as background colour 
        self.controller = controller

        self.controller.title('HNMM ATM') #Title Page
        self.controller.state('zoomed') 
        self.controller.iconphoto(False,
        tk.PhotoImage(file='E:/SEM1 DOCUMENTS/Atm Project Group C Pfund/Atm Project Group C Pfund/atm.png'))     #icon image used here
        
    
        #opening heading label at the top center of start page 
        heading_label = tk.Label(self,
                                                     text='SMART E-QURAN',        #Title of the text
                                                     font=('orbitron',45,'bold'),   #font style
                                                     foreground='#ffffff',          #colour for the widget
                                                     background='#3d3d5c')          # Background of start page 
        heading_label.pack(pady=25)       #closing the heading label with pack with external padding vertically

        # creating a in space label to write 
        space_label = tk.Label(self,height=4,bg='#3d3d5c')   #height of 4 with background colour 
        space_label.pack() #closing with pack()
        
        # for entering a pin we used pin label  
        pin_label = tk.Label(self,
                                                      text='Enter your 4-digit Pin',
                                                      font=('orbitron',13),
                                                      bg='#3d3d5c',
                                                      fg='white')   
        pin_label.pack(pady=10)
        
        # Tkinter variables (any value) 
        my_password = tk.StringVar() # Holds a string;the default value is an empty string 
        password_entry_box = tk.Entry(self,
                                                              textvariable=my_password,
                                                              font=('orbitron',12),
                                                              width=22)
        password_entry_box.focus_set()
        password_entry_box.pack(ipady=7)
        
#for handling the pin
        def handle_focus_in(_):
            password_entry_box.configure(fg='black',show='*')
            
        password_entry_box.bind('<FocusIn>',handle_focus_in)
# function of check password
        def check_password():
           if my_password.get() == '1234': # if else condition if the pin is incorrect so it'll display invalid pin
               my_password.set('') #To clear the password when we return
               incorrect_password_label['text']=''  #To clear the text of invalid password when we return to that page
               controller.show_frame('MenuPage')
           else: 
               incorrect_password_label['text']='Invalid Pin'
  #ADDING ENTER BUTTON             
        enter_button = tk.Button(self,
                                                     text='Enter',   #Title on the button
                                                     command=check_password,  #Function to check password
                                                     relief='raised',  #For Border
                                                     borderwidth = 3,   #Thickness of the border
                                                     width=40,   #Width of the button
                                                     height=3)   ##Height of the button
        enter_button.pack(pady=10)
        #opening label
        incorrect_password_label = tk.Label(self,
                                                                        text='',
                                                                        font=('orbitron',13),
                                                                        fg='white',
                                                                        bg='#33334d',
                                                                        anchor='n')
        incorrect_password_label.pack(fill='both',expand=True) #closing label
        
#Bottom frame opening 
        bottom_frame = tk.Frame(self,relief='raised',borderwidth=3)
        bottom_frame.pack(fill='x',side='bottom')
        
# inserting visa and master card images
        visa_photo = tk.PhotoImage(file='visa.png')
        visa_label = tk.Label(bottom_frame,image=visa_photo)
        visa_label.pack(side='left')
        visa_label.image = visa_photo

        mastercard_photo = tk.PhotoImage(file='mastercard.png')
        mastercard_label = tk.Label(bottom_frame,image=mastercard_photo)
        mastercard_label.pack(side='left')
        mastercard_label.image = mastercard_photo
#The floating-point numbers in units of seconds for time interval are indicated by Tick
        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0',' ')
            time_label.config(text=current_time)
            time_label.after(200,tick)
            
        time_label = tk.Label(bottom_frame,font=('orbitron',12))
        time_label.pack(side='right')

        tick()
#Creating menu page frame by using Class       
class MenuPage(tk.Frame):
    #Defining a function to initialize the MenuPage frame
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#3d3d5c')  #to arrange other objects in the frame
        self.controller = controller 
        #For inserting a heading and formatting it
        heading_label = tk.Label(self,
                                                     text='HNMM ATM',
                                                     font=('orbitron',45,'bold'),
                                                     foreground='#ffffff',
                                                     background='#3d3d5c')
        heading_label.pack(pady=25) #To give spacing between the heading label and main menu label
        
        main_menu_label = tk.Label(self,
                                                           text='Account type: Current Account',  #Text to be displayed
                                                           font=('orbitron',13), #Font style and size
                                                           fg='white',         #Font color
                                                           bg='#3d3d5c')       #Background color
        main_menu_label.pack()

        selection_label = tk.Label(self,
                                                           text='Please make a selection',  #Text to be displayed
                                                           font=('orbitron',13),     #Font style and size
                                                           fg='white',             #Font color
                                                           bg='#3d3d5c',           #Background color 
                                                           anchor='w')  #For locating text on the left
        selection_label.pack(fill='x')

        button_frame = tk.Frame(self,bg='#33334d')  #To add the frame for button  #Adding baackground color in the button
        button_frame.pack(fill='both',expand=True)  #Expanding on x and y axis 
 #ADDING BUTONS TO THE MAIN MENU PAGE
        def withdraw(): #WITHDRAW PAGE BUTTON
            controller.show_frame('WithdrawPage')  #function to take the user to the withdraw page
        #Inserting a withdraw button    
        withdraw_button = tk.Button(button_frame,
                                                            text='Withdraw',  #Title on the button
                                                            command=withdraw, #Function to withdraw
                                                            relief='raised',  #For border
                                                            borderwidth=3,    #Thickness of the border
                                                            width=50,         #Width of the button  
                                                            height=5)         #Height of the button
        withdraw_button.grid(row=0,column=0,pady=5) #Spacing between withdraw button and deposit button

        def deposit(): #DEPOSIT PAGE BUTTON
            controller.show_frame('DepositPage')   #function to take the user to the Deposit page
        #Inserting a Deposit button    
        deposit_button = tk.Button(button_frame,
                                                            text='Deposit',   #Title on the button
                                                            command=deposit,  #Function to deposit
                                                            relief='raised',  #For border
                                                            borderwidth=3,    #Thickness of the border
                                                            width=50,         #Width of the button 
                                                            height=5)         #Height of the button
        deposit_button.grid(row=1,column=0,pady=5) #Spacing between deposit button and balance button

        def balance(): #BALANCE PAGE BUTTON
            controller.show_frame('BalancePage')  #function to take the user to the balance page
        #Inserting a Balance button    
        balance_button = tk.Button(button_frame,
                                                            text='Balance',  #Title on the button
                                                            command=balance, #Function to check balance
                                                            relief='raised', #For border
                                                            borderwidth=3,   #Thickness of the border
                                                            width=50,        #Width of the button
                                                            height=5)        #Height of the button
        balance_button.grid(row=2,column=0,pady=5) #Spacing between balance button and exit button

        def exit(): #EXIT PAGE BUTTON
            controller.show_frame('StartPage')  #function to take the user to the Start page
        #Inserting a button to exist    
        exit_button = tk.Button(button_frame,
                                                            text='Exit',     #Title on the button
                                                            command=exit,    #Function to exist
                                                            relief='raised', #For border 
                                                            borderwidth=3,   #Thickness of the border     
                                                            width=50,        #Width of the button
                                                            height=5)        #Height of the button      
        exit_button.grid(row=3,column=0,pady=5)  #Spacing between exit button button and bottom frame
        #Creating a bottom frame to add logos and time to it
        
        bottom_frame = tk.Frame(self,relief='raised',borderwidth=3)  #Defining the border thickness of the frame
        bottom_frame.pack(fill='x',side='bottom')   #Assigning the location bottom and direcction i.e left to right
        #Inserting Visa photo
        visa_photo = tk.PhotoImage(file='visa.png') #file name 
        visa_label = tk.Label(bottom_frame,image=visa_photo) #To put the picture on that label
        visa_label.pack(side='left')  #packing the photo and assigning to it the locaton i.e left of The bottom frame
        visa_label.image = visa_photo #Reference to make it appear on the screen
        #Inserting Mastercard Photo
        mastercard_photo = tk.PhotoImage(file='mastercard.png') #file name 
        mastercard_label = tk.Label(bottom_frame,image=mastercard_photo) #Creating a label for the picture
        mastercard_label.pack(side='left') #packing the photo and assigning to it the locaton i.e left of The bottom frame
        mastercard_label.image = mastercard_photo #reference 
        #To return the current time from the time module
        #Defining the function for time
        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0',' ') #Formatting the time by seperatting hours and mins
            time_label.config(text=current_time) #Creating time label 
            time_label.after(200,tick) #To update the time in every 200 mili secs
            
        time_label = tk.Label(bottom_frame,font=('orbitron',12)) 
        time_label.pack(side='right')
        #Calling the function
        tick() 
        
class ReceiptPage(tk.Frame):
 #Defining a function to initialize the MenuPage frame
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#3d3d5c')  #to arrange other objects in the frame
        self.controller = controller 
        #For inserting a heading and formatting it
        heading_label = tk.Label(self,
                                                     text='HNMM ATM',
                                                     font=('orbitron',45,'bold'),
                                                     foreground='#ffffff',
                                                     background='#3d3d5c')
        heading_label.pack(pady=25) #To give spacing between the heading label and main menu label



        selection_label = tk.Label(self,
                                                           text='Do you want receipt Yes/No', #Text to be displayed
                                                           font=('orbitron',13),  #Font style and size
                                                           fg='white',        #Font color
                                                           bg='#3d3d5c',      #Background color
                                                           anchor='w')       #For locating text on the left
        selection_label.pack(fill='x')  


        
        button_frame = tk.Frame(self,bg='#33334d')  #To add the frame for button  #Adding baackground color in the button
        button_frame.pack(fill='both',expand=True)  #Expanding on x and y axis 
 #ADDING BUTONS TO THE Receipt PAGE        
        def menu():  #Menu BUTTON
            controller.show_frame('MenuPage')
        #Inserting a menu button    
        menu_button = tk.Button(button_frame,
                                                    command=menu, #Function to go to menu
                                                    text='Yes', #Title on the button
                                                    relief='raised',  #For border 
                                                    borderwidth=3,  #Thickness of the border
                                                    width=50,  #Width of the button 
                                                    height=5)  #Height of the button
        menu_button.grid(row=0,column=0,pady=5)   #Spacing between menu button and exit button
             

        def exit():  #Exit PAGE BUTTON
            controller.show_frame('StartPage')
         #Inserting a button to exist       
        exit_button = tk.Button(button_frame, 
                                                 text='No',    #Title on the button  
                                                 command=exit,   #Function to go to menu
                                                 relief='raised',   #For border 
                                                 borderwidth=3,  #Thickness of the border
                                                 width=50,  #Width of the button
                                                 height=5)  #Height of the button
        exit_button.grid(row=0,column=1,pady=5,padx=555) #Spacing between exit button and bottom frame
        #Creating a bottom frame to add logos and time to it
        
        bottom_frame = tk.Frame(self,relief='raised',borderwidth=3)  #Defining the border thickness of the frame
        bottom_frame.pack(fill='x',side='bottom')   #Assigning the location bottom and direcction i.e left to right
        #Inserting Visa photo
        visa_photo = tk.PhotoImage(file='visa.png') #file name 
        visa_label = tk.Label(bottom_frame,image=visa_photo) #To put the picture on that label
        visa_label.pack(side='left')  #packing the photo and assigning to it the locaton i.e left of The bottom frame
        visa_label.image = visa_photo #Reference to make it appear on the screen
        #Inserting Mastercard Photo
        mastercard_photo = tk.PhotoImage(file='mastercard.png') #file name 
        mastercard_label = tk.Label(bottom_frame,image=mastercard_photo) #Creating a label for the picture
        mastercard_label.pack(side='left') #packing the photo and assigning to it the locaton i.e left of The bottom frame
        mastercard_label.image = mastercard_photo #reference 
        #To return the current time from the time module
        #Defining the function for time
        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0',' ') #Formatting the time by seperatting hours and mins
            time_label.config(text=current_time) #Creating time label 
            time_label.after(200,tick) #To update the time in every 200 mili secs
            
        time_label = tk.Label(bottom_frame,font=('orbitron',12)) 
        time_label.pack(side='right')
        #Calling the function
        tick() 
   
class WithdrawPage(tk.Frame):
 #Defining a function to initialize the MenuPage frame
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#3d3d5c')  #to arrange other objects in the frame
        self.controller = controller 
        #For inserting a heading and formatting it
        heading_label = tk.Label(self,
                                                     text='HNMM ATM',
                                                     font=('orbitron',45,'bold'),
                                                     foreground='#ffffff',
                                                     background='#3d3d5c')
        heading_label.pack(pady=25) #To give spacing between the heading label and main menu label

        choose_amount_label = tk.Label(self,
                                                           text='Choose the amount you want to withdraw',
                                                           font=('orbitron',13),
                                                           fg='white',
                                                           bg='#3d3d5c')
        choose_amount_label.pack()

        button_frame = tk.Frame(self,bg='#33334d')
        button_frame.pack(fill='both',expand=True)

        def withdraw(amount):
            global current_balance
            current_balance -= amount
            controller.shared_data['Balance'].set(current_balance)
            controller.show_frame('MenuPage')
            
        five_hundred_button = tk.Button(button_frame,
                                                       text='500',
                                                       command=lambda:withdraw(500),
                                                       relief='raised',
                                                       borderwidth=3,
                                                       width=50,
                                                       height=5)
        five_hundred_button.grid(row=0,column=0,pady=5)

        one_thousand_button = tk.Button(button_frame,
                                                       text='1000',
                                                       command=lambda:withdraw(1000),
                                                       relief='raised',
                                                       borderwidth=3,
                                                       width=50,
                                                       height=5)
        one_thousand_button.grid(row=1,column=0,pady=5)


        five_thousand_button = tk.Button(button_frame,
                                                       text='5000',
                                                       command=lambda:withdraw(5000),
                                                       relief='raised',
                                                       borderwidth=3,
                                                       width=50,
                                                       height=5)
        five_thousand_button.grid(row=2,column=0,pady=5)

        ten_thousand_button = tk.Button(button_frame,
                                                       text='10000',
                                                       command=lambda:withdraw(10000),
                                                       relief='raised',
                                                       borderwidth=3,
                                                       width=50,
                                                       height=5)
        ten_thousand_button.grid(row=3,column=0,pady=5)


        twenty_thousand_button = tk.Button(button_frame,
                                                       text='20000',
                                                       command=lambda:withdraw(20000),
                                                       relief='raised',
                                                       borderwidth=3,
                                                       width=50,
                                                       height=5)
        twenty_thousand_button.grid(row=0,column=1,pady=5,padx=555)

        thirty_thousand_button = tk.Button(button_frame,
                                                       text='30000',
                                                       command=lambda:withdraw(30000),
                                                       relief='raised',
                                                       borderwidth=3,
                                                       width=50,
                                                       height=5)
        thirty_thousand_button.grid(row=1,column=1,pady=5)

        forty_thousand_button = tk.Button(button_frame,
                                                       text='40000',
                                                       command=lambda:withdraw(40000),
                                                       relief='raised',
                                                       borderwidth=3,
                                                       width=50,
                                                       height=5)
        forty_thousand_button.grid(row=2,column=1,pady=5)

        cash = tk.StringVar()
        other_amount_entry = tk.Entry(button_frame,
                                                              textvariable=cash,
                                                              width=59,
                                                              justify='right')
        other_amount_entry.grid(row=3,column=1,pady=5,ipady=30)

        def other_amount(_):
            global current_balance
            current_balance -= int(cash.get())
            controller.shared_data['Balance'].set(current_balance)
            cash.set('')
            controller.show_frame('MenuPage')
            
        other_amount_entry.bind('<Return>',other_amount)     
        #Creating a bottom frame to add logos and time to it
        
        bottom_frame = tk.Frame(self,relief='raised',borderwidth=3)  #Defining the border thickness of the frame
        bottom_frame.pack(fill='x',side='bottom')   #Assigning the location bottom and direcction i.e left to right
        #Inserting Visa photo
        visa_photo = tk.PhotoImage(file='visa.png') #file name 
        visa_label = tk.Label(bottom_frame,image=visa_photo) #To put the picture on that label
        visa_label.pack(side='left')  #packing the photo and assigning to it the locaton i.e left of The bottom frame
        visa_label.image = visa_photo #Reference to make it appear on the screen
        #Inserting Mastercard Photo
        mastercard_photo = tk.PhotoImage(file='mastercard.png') #file name 
        mastercard_label = tk.Label(bottom_frame,image=mastercard_photo) #Creating a label for the picture
        mastercard_label.pack(side='left') #packing the photo and assigning to it the locaton i.e left of The bottom frame
        mastercard_label.image = mastercard_photo #reference 
        #To return the current time from the time module
        #Defining the function for time
        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0',' ') #Formatting the time by seperatting hours and mins
            time_label.config(text=current_time) #Creating time label 
            time_label.after(200,tick) #To update the time in every 200 mili secs
            
        time_label = tk.Label(bottom_frame,font=('orbitron',12)) 
        time_label.pack(side='right')
        #Calling the function
        tick() 
   

class DepositPage(tk.Frame):
 #Defining a function to initialize the MenuPage frame
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#3d3d5c')  #to arrange other objects in the frame
        self.controller = controller 
        #For inserting a heading and formatting it
        heading_label = tk.Label(self,
                                                     text='HNMM ATM',
                                                     font=('orbitron',45,'bold'),
                                                     foreground='#ffffff',
                                                     background='#3d3d5c')
        heading_label.pack(pady=25) #To give spacing between the heading label and main menu label

        space_label = tk.Label(self,height=4,bg='#3d3d5c')
        space_label.pack()

        enter_amount_label = tk.Label(self,
                                                      text='Enter amount',
                                                      font=('orbitron',13),
                                                      bg='#3d3d5c',
                                                      fg='white')
        enter_amount_label.pack(pady=10)

        cash = tk.StringVar()
        deposit_entry = tk.Entry(self,
                                                  textvariable=cash,
                                                  font=('orbitron',12),
                                                  width=22)
        deposit_entry.pack(ipady=7)

        def deposit_cash():
            global current_balance
            current_balance += int(cash.get())
            controller.shared_data['Balance'].set(current_balance)
            controller.show_frame('MenuPage')
            cash.set('')
            
        enter_button = tk.Button(self,
                                                     text='Enter',
                                                     command=deposit_cash,
                                                     relief='raised',
                                                     borderwidth=3,
                                                     width=40,
                                                     height=3)
       
        enter_button.pack(pady=10)

        two_tone_label = tk.Label(self,bg='#33334d')
        two_tone_label.pack(fill='both',expand=True)
        #Creating a bottom frame to add logos and time to it
        
        bottom_frame = tk.Frame(self,relief='raised',borderwidth=3)  #Defining the border thickness of the frame
        bottom_frame.pack(fill='x',side='bottom')   #Assigning the location bottom and direcction i.e left to right
        #Inserting Visa photo
        visa_photo = tk.PhotoImage(file='visa.png') #file name 
        visa_label = tk.Label(bottom_frame,image=visa_photo) #To put the picture on that label
        visa_label.pack(side='left')  #packing the photo and assigning to it the locaton i.e left of The bottom frame
        visa_label.image = visa_photo #Reference to make it appear on the screen
        #Inserting Mastercard Photo
        mastercard_photo = tk.PhotoImage(file='mastercard.png') #file name 
        mastercard_label = tk.Label(bottom_frame,image=mastercard_photo) #Creating a label for the picture
        mastercard_label.pack(side='left') #packing the photo and assigning to it the locaton i.e left of The bottom frame
        mastercard_label.image = mastercard_photo #reference 
        #To return the current time from the time module
        #Defining the function for time
        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0',' ') #Formatting the time by seperatting hours and mins
            time_label.config(text=current_time) #Creating time label 
            time_label.after(200,tick) #To update the time in every 200 mili secs
            
        time_label = tk.Label(bottom_frame,font=('orbitron',12)) 
        time_label.pack(side='right')
        #Calling the function
        tick() 


class BalancePage(tk.Frame):
 #Defining a function to initialize the MenuPage frame
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#3d3d5c')  #to arrange other objects in the frame
        self.controller = controller 
        #For inserting a heading and formatting it
        heading_label = tk.Label(self,
                                                     text='HNMM ATM',
                                                     font=('orbitron',45,'bold'),
                                                     foreground='#ffffff',
                                                     background='#3d3d5c')
        heading_label.pack(pady=25) #To give spacing between the heading label and main menu label
        
 

        global current_balance
        controller.shared_data['Balance'].set(current_balance)
        balance_label = tk.Label(self,
                                                  textvariable=controller.shared_data['Balance'],
                                                  font=('orbitron',13),
                                                  fg='white',
                                                  bg='#3d3d5c',
                                                  anchor='w')
        balance_label.pack(fill='x')

        button_frame = tk.Frame(self,bg='#33334d')
        button_frame.pack(fill='both',expand=True)
        
#INSERTING BUTTONS TO THE BALANCE PAGE
        def receipt():
            controller.show_frame('ReceiptPage')
        #INSERTING RECEIPT BUTTON    
        receipt_button = tk.Button(button_frame,
                                                    command=receipt,
                                                    text='Receipt',
                                                    relief='raised',
                                                    borderwidth=3,
                                                    width=50,
                                                    height=5)
        receipt_button.grid(row=0,column=0,pady=5)
        
        #INSERTING MENU BUTTON
        def menu():
            controller.show_frame('MenuPage')
            
        menu_button = tk.Button(button_frame,
                                                    command=menu,
                                                    text='Back to menu',
                                                    relief='raised',
                                                    borderwidth=3,
                                                    width=50,
                                                    height=5)
        menu_button.grid(row=1,column=0,pady=5)
 
        #INSERTING EXIT BUTTON
        def exit():
            controller.show_frame('StartPage')
            
        exit_button = tk.Button(button_frame,
                                                 text='Exit',
                                                 command=exit,
                                                 relief='raised',
                                                 borderwidth=3,
                                                 width=50,
                                                 height=5)
        exit_button.grid(row=2,column=0,pady=5)
        #Creating a bottom frame to add logos and time to it
        
        bottom_frame = tk.Frame(self,relief='raised',borderwidth=3)  #Defining the border thickness of the frame
        bottom_frame.pack(fill='x',side='bottom')   #Assigning the location bottom and direcction i.e left to right
        #Inserting Visa photo
        visa_photo = tk.PhotoImage(file='visa.png') #file name 
        visa_label = tk.Label(bottom_frame,image=visa_photo) #To put the picture on that label
        visa_label.pack(side='left')  #packing the photo and assigning to it the locaton i.e left of The bottom frame
        visa_label.image = visa_photo #Reference to make it appear on the screen
        #Inserting Mastercard Photo
        mastercard_photo = tk.PhotoImage(file='mastercard.png') #file name 
        mastercard_label = tk.Label(bottom_frame,image=mastercard_photo) #Creating a label for the picture
        mastercard_label.pack(side='left') #packing the photo and assigning to it the locaton i.e left of The bottom frame
        mastercard_label.image = mastercard_photo #reference 
        #To return the current time from the time module
        #Defining the function for time
        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0',' ') #Formatting the time by seperatting hours and mins
            time_label.config(text=current_time) #Creating time label 
            time_label.after(200,tick) #To update the time in every 200 mili secs
            
        time_label = tk.Label(bottom_frame,font=('orbitron',12)) 
        time_label.pack(side='right')
        #Calling the function
        tick() 


if __name__ == "__main__": # test whether our module is being run directly or being imported
    app = SampleApp()
    app.mainloop() #inserting mainloop() to run our program
