import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
from cv2 import *
import datetime
from tkinter import *
import pygame
import pygame.mixer
import random
import requests
import re
from time import ctime
from googletrans import Translator



window = Tk()

global var
global var1

var = StringVar()
var1 = StringVar()


engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wish():
    speak("hello ankit sir, swayam here. how can i help you")

def myCommand():
    "listens for commands"

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('listening...')
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print('recognizing')
        query = r.recognize_google(audio, language='en-IN')
        print('user said:', query )
    except Exception as e:

        print('say that again')
        return 'none'
    return query


def play():
    btn1.configure(bg='orange')
    wish()
    while True:
        query = myCommand().lower()

        if 'wikipedia' in query:
            speak('searching wikipedia')
            query = query.replace('wikipedia', '')
            results = wikipedia.summary(query, sentences=2)
            speak('according  to wikipedia')
            print(results)
            speak(results)
        if 'how are you' in query:
            speak('i am fine sir. what about you')
        if 'what is your name' in query:
            speak('my name is swayam')
        if 'what time it is' in query:
            speak(ctime())
        elif 'open website' in query:
            reg_ex = re.search('open website (.+)', query)
            if reg_ex:
                domain = reg_ex.group(1)
                url = 'https://www.' + domain + '.com'
                webbrowser.open(url)
                print('Done!')
            else:
                pass
        if 'exit' in query:
            speak('thank you sir')
            exit()
        if 'who made you' in query:
            speak('i am made by sir ankit sharma')
        if 'shutdown' in query:
            speak('do you really want to shutdown')
            sss = myCommand()

            if 'yes' in sss:
                hour = int(datetime.datetime.now().hour)
                if hour >= 6 and hour < 20:
                    speak('thank you sir. have a goad day')
                    os.system("shutdown /s /t 1")
                else:
                    speak('thank you sir. good night')
                    os.system("shutdown /s /t 1")

            else:
                pass

        if 'click photo' in query:
            camera = cv2.VideoCapture(0)
            while True:
                return_value, image = camera.read()
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                cv2.imshow('image', gray)
                if cv2.waitKey(1) & 0xFF == ord('s'):
                    cv2.imwrite('test.jpg', image)
                    break
            camera.release()
            cv2.destroyAllWindows()


        if 'play music' in query:
            music = 'F:\\songs'
            pygame.mixer.init()
            songs = os.listdir(music)
            filename = random.choice(songs)
            os.startfile(os.path.join(music, filename))


        if 'call alexa' in query:
            speak('thank you sir, now alexa will help you')
            engine.setProperty('voice', voices[1].id)
            speak('hello sir alexa here, how can i help you')

        if 'swayam again' in query:
            speak('thank you sir, now swayam will help you')
            engine.setProperty('voice', voices[0].id)
            speak('hello sir swayam here, how can i help you')

        if 'joke' in query:
            res = requests.get(
                'https://icanhazdadjoke.com/',
                headers={"Accept": "application/json"}
            )
            if res.status_code == requests.codes.ok:
                speak(str(res.json()['joke']))
            else:
                speak('oops!I ran out of jokes')


        if 'translate' in query:
            speak('what you want to translate')
            sentence = myCommand()
            translator = Translator()
            translated_sentence = translator.translate(sentence, src='en', dest='cs')
            speak(translated_sentence.text)


def update(ind):
    frame = frames[(ind)%100]
    ind += 1
    label.configure(image=frame)
    window.after(100, update, ind)

label2 = Label(window, textvariable = var1, bg = '#FAB60C')
label2.config(font=("Courier", 20))
var1.set('User Said:')
label2.pack()

label1 = Label(window, textvariable = var, bg = '#ADD8E6')
label1.config(font=("Courier", 20))
var.set('Welcome')
label1.pack()

frames = [PhotoImage(file='Assistant.gif',format = 'gif -index %i' %(i)) for i in range(100)]
window.title('JARVIS')

label = Label(window, width = 500, height = 500)
label.pack()
window.after(0, update, 0)

btn1 = Button(text = 'RUN',width = 20,command = play, bg = '#5C85FB')
btn1.config(font=("Courier", 12))
btn1.pack()


window.mainloop()



