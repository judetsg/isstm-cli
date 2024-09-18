import vosk
import pyaudio
import json
from text_to_num import text2num# The following has been taken from here https://medium.com/@nimritakoul01/offline-speech-to-text-in-python-f5d6454ecd02

# this start a message storage on port 5555
import zmq
context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.bind("tcp://*:5555")

# Here I have downloaded this model to my PC, extracted the files
# and saved it in local directory
# Set the model path
model_path = "stt-models/vosk-model-small-fr-0.22"
# Initialize the model with model-path
model = vosk.Model(model_path)


# if you don't want to download the model, just mention "lang" argument
# in vosk.Model() and it will download the right  model, here the language is
# US-English
# model = vosk.Model(lang="en-us")
# Create a recognizer
rec = vosk.KaldiRecognizer(model, 16000)
# Open the microphone stream
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=8192)

# Start streaming and recognize speech
while True:
    # input("Press Enter to start...")
    data = stream.read(4096)  # read in chunks of 4096 bytes
    if rec.AcceptWaveform(data):  # accept waveform of input voice
        # Parse the JSON result and get the recognized text
        result = json.loads(rec.Result())
        recognized_text = result['text']
        try:
            # print(recognized_text)
            output = text2num(recognized_text, "fr")
            if str(output) == "0":
                continue
            socket.send_string(str(output))
            print("Sent ", output)
        except Exception as e:
            print("Non reconnu: ", e)
            continue

        # Check for the termination keyword
        if "999" in recognized_text.lower():
            print("Termination keyword detected. Stopping...")
            break
