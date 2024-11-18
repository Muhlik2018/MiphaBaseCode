import sys
import live2d.v3 as live2d
import random
from datetime import datetime, timedelta
from GPTInteract import GPTReply
from GPTInteract import GPTToText
from GPTInteract import QianfanReply
from WakeUpWord import WakeUpDetect
from SupportingFunction import EditAudioFile
from SupportingFunction import RecordAudio
from Desktop import L2DView
from SupportingFunction import RecordAudio
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import threading
from SupportingFunction import ReadFile

lock = threading.Lock()

def gptApi(controlView,key, character="You are mipha, a character from legends of Zelda"):
# Example usage
    chatHistory=[{'role': 'system', 'content': character}]
    print("start")
    controlView.setIdling()
    key=key[0]
    while True:
        # frames=record_audio(0.5)
        # if  not frames is False:
        # print("start catch hot word")
        isHotword=WakeUpDetect.detection()
        # isHotword= False
        if isHotword:
            now = datetime.now()
            current_time = now.strftime("%H%M%S")
            txt_time = now.strftime("%H:%M:%S")
            controlView.setTalking(txt="Hi, I'm listening~")
            if not controlView.getMute():
                EditAudioFile.multiOsSound("./Resources/Audio/Hear.mp3",False)
            controlView.setThinking()
            # print("catch question...")
            main_frames =RecordAudio.record_audio(10,5)
            while not main_frames is False:
                controlView.setLabelText(txt="Let me think...")
                audio_file_path="MAIN"+current_time+".wav"
                RecordAudio.save_audio(main_frames,audio_file_path)
                print("to text...")
                maintext=GPTToText.speechToText(audio_file_path,key)
                controlView.setLabelText(txt="So you just said: "+ maintext + " ?")
                print("get answer...")
                EditAudioFile.multiOsRm(audio_file_path)
                GPTOutput=GPTReply.getGPTReply(maintext,chatHistory,key)
                chatHistory=GPTOutput[0]
                controlView.setTalking(txt=GPTOutput[1])
                if not controlView.getMute():
                    EditAudioFile.multiOsSound(GPTOutput[2])
                else:
                    EditAudioFile.multiOsRm(GPTOutput[2])
                if len(chatHistory)>=10:
                    chatHistory.pop(1)
                    chatHistory.pop(2)
                main_frames =RecordAudio.record_audio(10,5)
            controlView.setLabelText(txt="Bye bye---")
            if not controlView.getMute():
                EditAudioFile.multiOsSound("./Resources/Audio/Goodbye2.mp3",False)
            controlView.setIdling(txt=txt_time)
            # print("No sound detected in this round")



def yifanApi(controlView,key, character="You are mipha, a character from legends of Zelda"):
    refreshTime=datetime.now()
    while True:
        now = datetime.now()
        txt_time = now.strftime("%H:%M:%S")
        if (now-refreshTime).total_seconds()>20:
            funnyWords=QianfanReply.getQianfanReply(text="请随便分享些日常吧。",character=character,key=key)
            controlView.refreshMotion(txt=funnyWords)
            refreshTime=datetime.now()+timedelta(seconds=5)
        elif (now-refreshTime).total_seconds()>1:
            controlView.setLabelText(txt=txt_time)

def noApi(controlView,key, character="You are mipha, a character from legends of Zelda"):
    wordList=ReadFile.getIdleWord()
    refreshTime=datetime.now()+timedelta(seconds=5)
    random.seed(int(refreshTime.second))
    controlView.setLabelText(txt="You seems forgot my api key...")
    while True:
        now = datetime.now()
        txt_time = now.strftime("%H:%M:%S")
        if (now-refreshTime).total_seconds()>20:
            wordNo=random.randint(0,len(wordList)-1)
            idleWord=wordList[wordNo]
            controlView.refreshMotion(txt=idleWord)
            refreshTime= datetime.now()+timedelta(seconds=5)
        if (now-refreshTime).total_seconds()>1:
            controlView.setLabelText(txt=txt_time)

def timeUpdate(controlView,key, character="You are mipha, a character from legends of Zelda"):
    print("Start T2")
    refreshTime=datetime.now()
    avoidNextSentence=True
    while True:
        if controlView.motion=="Idle":
            now = datetime.now()
            txt_time = now.strftime("%H:%M:%S")
            if (now-refreshTime).total_seconds()>20 and not avoidNextSentence:
               funnyWords=GPTReply.getGPTReply("Say something random about life, work or holiday",[{'role': 'system', 'content': character}],key[0],False)
               controlView.refreshMotion(txt=funnyWords)
               refreshTime= datetime.now()+timedelta(seconds=5)
            elif (now-refreshTime).total_seconds()>1:
                if avoidNextSentence is True:
                    avoidNextSentence=False
                    refreshTime= datetime.now()+timedelta(seconds=2)
                else:
                    controlView.setLabelText(txt=txt_time)
        else:
            avoidNextSentence=True

class recordThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):     
        lock.acquire()       #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
        apiKey=ReadFile.getKey()
        character=ReadFile.getCharacter()
        lock.release()
        if apiKey[0] is None or apiKey[0]=="" or apiKey[0]==" ":
            noApi(win,key=apiKey,character=character)
        elif len(apiKey)>1:
            yifanApi(win,key=apiKey,character=character)
        else:
            thread2 = updateTimeThread(2, "Thread-2", 2)   
            thread2.start()
            gptApi(win,key=apiKey,character=character)


class updateTimeThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        lock.acquire()       
        apiKey=ReadFile.getKey()
        character=ReadFile.getCharacter()
        lock.release()            #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
        timeUpdate(win,key=apiKey,character=character)

thread1 = recordThread(1, "Thread-1", 1)

live2d.init()

app = QApplication(sys.argv)
win = L2DView.Win()
win.show()
thread1.start()


app.exec()
live2d.dispose()

