import pyaudio
import wave
import struct
import math

# Audio configuration
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 320
SHORT_NORMALIZE = (1.0/32768.0)
RECORD_SECONDS = 3



# Initialize PyAudio


# Open stream


def get_rms( block ):
    # RMS amplitude is defined as the square root of the 
    # mean over time of the square of the amplitude.
    # so we need to convert this string of bytes into 
    # a string of 16-bit samples...

    # we will get one short out for each 
    # two chars in the string.
    count = len(block)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, block )

    # iterate over the block.
    sum_squares = 0.0
    for sample in shorts:
        # sample is a signed short in +/- 32768. 
        # normalize it to 1.0
        n = sample * SHORT_NORMALIZE
        sum_squares += n*n

    return math.sqrt( sum_squares / count )

# depracated
def is_speech(frame, sample_rate):
    return True

def record_audio(audioSeconds,slienceAllowance):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    frames = []
    recording = False
    buffer = [] # int(RATE/CHUNK*0.5)
    print("Listening for speech...")
    framesNeed=int(RATE/CHUNK*audioSeconds)
    framesCount=0
    silenceCount=0
    recordCount=0
    slienceAllowance=int(RATE/CHUNK*slienceAllowance)
    while framesCount<framesNeed/2:
        frame = stream.read(CHUNK)
        amplitutde=get_rms(frame)
        # print(frame)
        if (is_speech(frame, RATE) and amplitutde>0.02 and recordCount<framesNeed) or (recording and silenceCount<slienceAllowance and recordCount<framesNeed):
            if amplitutde<0.015:
                silenceCount=silenceCount+1
            else:
                silenceCount=0
            # print(amplitutde)
            if not recording:
                print("Recording started")
                recording = True
            frames.append(frame)
            recordCount=recordCount+1
            # for i in range(0,int(RATE/CHUNK*audioSeconds)):
                # frame = stream.read(CHUNK)
                # frames.append(frame)
            # return frames
        else:
            if recording:
                stream.stop_stream()
                stream.close()
                audio.terminate()
                return buffer+frames
            else:
                if len(buffer)<25:
                    buffer.append(frame)
                else:
                    buffer.pop()
                    buffer.append(frame)
                framesCount=framesCount+1
    stream.stop_stream()
    stream.close()
    audio.terminate()
    return False


def save_audio(frames, filename="output.wav"):
    audio = pyaudio.PyAudio()
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    audio.terminate()

