## :sound: Speech recognition using wav2vec 2.0 :notes: :speaker:
This repo provides code that records the user's voice and displays the transcript of the recording (:link: [Link of wav2vec 2.0 research paper](https://arxiv.org/pdf/2006.11477.pdf)).

## Structure

There are two scripts that achieve the mentioned task: speech_rec.py, which has the user interact with the program in the command line and tk_speech_rec.py, which creates an interactive window.

## Prerequisites

1. git
2. anaconda/miniconda

## Setup

1. Open Anaconda Powershell Prompt or a CLI with conda initialized
2. Clone repository: `git clone https://github.com/blasimark/speech-recognition`
2. Navigate into the project directory `cd path_to_repo`
3. Run `conda env create -f environment.yml` (while in project directory)
4. Run `conda activate speech`

The result is a conda environment with dependencies installed to run scripts. Since wav2vec is only used for inference, no GPU acceleration is required.

## Usage

During the first run, the script will download the model, which takes a while. The user should speak loud and clear for the best performance. 

1. command line version:

    - Run `python speech_rec.py`

    - The program will prompt the user to type in a character out of the set (`r`, `s`, `e`) into the command line

    - To start the recording, type in `r` and press `enter`. This will keep recording until `s` is typed in

    - To stop the recording, type `s` and hit `enter`. When the recording is stopped, the transcript is printed to the command line

    - To exit the program, type `e`

    - The user should always stop the current recording before starting a new one

2. tk version:

    - Run `python tk_speech_rec.py` 

    - The script creates a window with clickable buttons (only left mouse button clicks are registered) that display their purposes

    - The user can record their voice, and after stopping the recording, the transcript is displayed under the buttons

    - The user should always stop the current recording before starting a new one
