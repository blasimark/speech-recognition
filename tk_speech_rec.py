import tkinter as tk
import sys
import sounddevice as sd
import numpy as np
import torch
import torchaudio

bundle = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H
model = bundle.get_model()

RATE = 44100
CHANNELS = 2
data = []

def callback(indata, frames, time, status):
    data.append(indata.copy())

stream = sd.InputStream(samplerate=RATE, channels=CHANNELS, callback=callback)

class GreedyCTCDecoder(torch.nn.Module):
    def __init__(self, labels, blank=0):
        super().__init__()
        self.labels = labels
        self.blank = blank

    def forward(self, emission):
        indices = torch.argmax(emission, dim=-1)
        indices = torch.unique_consecutive(indices, dim=-1)
        indices = [i for i in indices if i != self.blank]
        return "".join([self.labels[i] for i in indices])

def start_recording(event):
    global data
    data = []
    print("Recording...")
    stream.start()


def end_recording_and_write(event):
    global text

    stream.stop()
    print("Stopped recording")
    text.destroy()
    global data
    data = np.concatenate(data)

    x = torch.FloatTensor(data)
    x = torch.permute(x, (1,0))

    if RATE != bundle.sample_rate:
        x = torchaudio.functional.resample(x, RATE, bundle.sample_rate)

    with torch.inference_mode():
        emission, _ = model(x)

    decoder = GreedyCTCDecoder(labels=bundle.get_labels())

    transcript = decoder(emission[0])

    text = tk.Label(None, text=transcript, font=font)
    text.pack()

    data = []

def quit(event):    
    print("Exiting")                     
    sys.exit() 

font = ("Times", 18)

start_recording_button = tk.Button(None, text="Start audio recording", font = font)
start_recording_button.pack()

end_recording_button = tk.Button(None, text="End audio recording", font=font)
end_recording_button.pack()

quit_button = tk.Button(None, text="Exit", font=font)
quit_button.pack()

text = tk.Label(None, text="The transcript of the recorded audio will be displayed here", font=font)
text.pack()

start_recording_button.bind('<Button-1>', start_recording)
end_recording_button.bind('<Button-1>', end_recording_and_write)
quit_button.bind('<Button-1>', quit) 

start_recording_button.mainloop()
