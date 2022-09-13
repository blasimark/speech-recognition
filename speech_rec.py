import sounddevice as sd
import numpy as np
import torch
import torchaudio
import sys

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

def event():
    global data

    key = input("Type one of r/s/e\n")

    if key == 'r':
        print("Recording, type 's' to stop recording\n")
        data = []
        stream.start()

    if key == 's':
        print("Stopped recording\n")
        stream.stop()
        data = np.concatenate(data)

        x = torch.FloatTensor(data)
        x = torch.permute(x, (1,0))

        if RATE != bundle.sample_rate:
            x = torchaudio.functional.resample(x, RATE, bundle.sample_rate)

        with torch.inference_mode():
            emission, _ = model(x)

        decoder = GreedyCTCDecoder(labels=bundle.get_labels())
         

        transcript = decoder(emission[0])

        print(transcript)

        data = []

    if key == 'e':
        print("Exiting\n")
        sys.exit()

while True:
    event()