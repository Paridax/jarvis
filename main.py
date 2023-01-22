import io
from pydub import AudioSegment
import speech_recognition as sr
import whisper
import queue
import tempfile
import os
import threading
import torch
import numpy as np

model = "tiny"
english = True
verbose = False
energy = 300
pause = 0.8
dynamic_energy = False
save_file = False
trigger_phrase = "windows"


def main(model, english, verbose, energy, pause, dynamic_energy, save_file):
    temp_dir = tempfile.mkdtemp() if save_file else None
    # there are no english models for large
    if model != "large" and english:
        model = model + ".en"
    audio_model = whisper.load_model(model)
    audio_queue = queue.Queue()
    result_queue = queue.Queue()
    threading.Thread(target=record_audio,
                     args=(audio_queue, energy, pause, dynamic_energy, save_file, temp_dir)).start()
    threading.Thread(target=transcribe_forever,
                     args=(audio_queue, result_queue, audio_model, english, verbose, save_file)).start()
    threading.Thread(target=listen_for_commands, args=(result_queue,)).start()

    # while True:
        # print(result_queue.get())


def record_audio(audio_queue, energy, pause, dynamic_energy, save_file, temp_dir):
    # load the speech recognizer and set the initial energy threshold and pause threshold
    r = sr.Recognizer()
    r.energy_threshold = energy
    r.pause_threshold = pause
    r.dynamic_energy_threshold = dynamic_energy

    with sr.Microphone(sample_rate=16000) as source:
        print("Say something!")
        i = 0
        while True:
            # get and save audio to wav file
            audio = r.listen(source)
            if save_file:
                data = io.BytesIO(audio.get_wav_data())
                audio_clip = AudioSegment.from_file(data)
                filename = os.path.join(temp_dir, f"temp{i}.wav")
                audio_clip.export(filename, format="wav")
                audio_data = filename
            else:
                torch_audio = torch.from_numpy(np.frombuffer(audio.get_raw_data(), np.int16).flatten().astype(np.float32) / 32768.0)
                audio_data = torch_audio

            audio_queue.put_nowait(audio_data)
            i += 1


def transcribe_forever(audio_queue, result_queue, audio_model, english, verbose, save_file):
    while True:
        audio_data = audio_queue.get()
        if english:
            result = audio_model.transcribe(audio_data,language='english')
        else:
            result = audio_model.transcribe(audio_data)

        if not verbose:
            predicted_text = result["text"]
            result_queue.put_nowait("You said: " + predicted_text)
            # check if the trigger phrase was said
            if trigger_phrase.lower() in predicted_text.lower():
                # select all text after the first character of the first use of the trigger phrase
                message_start = predicted_text.lower().find(trigger_phrase.lower())
                message = predicted_text[message_start:]
                result_queue.put_nowait("&M " + message)
        else:
            result_queue.put_nowait(result)

        if save_file:
            os.remove(audio_data)


def make_new_parsing_process():


main(model, english, verbose, energy, pause, dynamic_energy, save_file)