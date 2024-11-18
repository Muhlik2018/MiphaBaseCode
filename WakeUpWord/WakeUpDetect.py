import openwakeword
from openwakeword.model import Model
import pyaudio
import numpy as np

def detection():
# One-time download of all pre-trained models (or only select models)
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1280
    audio = pyaudio.PyAudio()
    mic_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    owwModel = Model(wakeword_models=["./Resources/HotwordModel/Hi_Mipha.onnx"],inference_framework="onnx")
    maxiumWaitTime=int(RATE/CHUNK*3)
    counter=0
    while counter<maxiumWaitTime:
        speech = np.frombuffer(mic_stream.read(CHUNK), dtype=np.int16)
        counter+=1
        # Feed to openWakeWord model
        prediction = owwModel.predict(speech)
        if(prediction['Hi_Mipha']>0.2):
            mic_stream.stop_stream()
            mic_stream.close()
            audio.terminate()
            return True
    mic_stream.stop_stream()
    mic_stream.close()
    audio.terminate()
    return False


