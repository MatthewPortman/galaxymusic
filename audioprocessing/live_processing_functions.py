import numpy as np
import time
from collections import Counter
from random import seed, randint

import sounddevice as sd

from _galfitlib.functions.helper_functions import pj, exists
from _galfitlib.utilities.music.galfit_with_music_update import galfitting, process_galfit_output
from audioprocessing.audio_processing_functions import load_audio, time_step_analysis

def play_audio(signal, sample_rate):
    # Play the audio file
    sd.play(signal, sample_rate)

    # Keep the script running while the audio is playing
    sd.wait()


def record_audio(sampling_frequency, duration):
    # Some nifty ideas here
    # https://daehnhardt.com/blog/2023/03/05/python-audio-signal-processing-with-librosa/
    recording = sd.rec(
            int(sampling_frequency * duration),
            samplerate = sampling_frequency,
            channels = 1,
            blocking = True
    )[:, 0]

    sd.wait()
    return recording

# import pyaudio
# # Initialize PyAudio
# p = pyaudio.PyAudio()
#
# # Open audio stream (e.g., microphone)
# stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, input=True, frames_per_buffer=1024)
#
# while True:
#     # Read audio data from stream
#     data = np.frombuffer(stream.read(1024), dtype=np.float32)

# import pygame
#
# def play_audio(file_path):
#     # Initialize Pygame mixer
#     pygame.mixer.init()
#
#     # Load the audio file
#     pygame.mixer.music.load(file_path)
#
#     # Play the audio file
#     pygame.mixer.music.play()
#
#     # Keep the script running while the audio is playing
#     while pygame.mixer.music.get_busy():
#         pygame.time.Clock().tick(10)
#
#
# audio_file = "brown_alma_mater.mp3"
# play_audio(audio_file)

def live(IN_DIR, OUT_DIR, gname = "template"):
    music_filename = "brown_alma_mater.mp3"

    height = 1000
    width = 1000
    # square
    model_dim = 200
    model_offset = model_dim // 2

    initial_seed_value = 42

    image_array = np.zeros((height, width))

    list_o_notes = []
    volumes = []
    all_models = []

    if not exists(pj(OUT_DIR, gname)):
        pj(OUT_DIR, gname).mkdir()

    feedme_0 = pj(OUT_DIR, gname, f"{gname}.in")
    input_filename_0 = pj(IN_DIR, f"{gname}.fits")
    output_filename_0 = pj(OUT_DIR, gname, f"{gname}.fits")

    delay = 0.5
    signal, sample_rate, time_array = load_audio(music_filename, delay = delay)

    # song_duration = librosa.get_duration(path = music_filename)

    # Every 0.5 seconds for determination of peaks
    small_time_step = 0.5

    # A new galaxy every 2 seconds
    big_time_step = 2

    play_audio(signal, sample_rate)

    def callback(in_data, frames, time, status):
        """
        Callback function for the audio stream
        """
        # global signal
        signal = np.frombuffer(in_data, dtype = np.float32)
        return signal  # , pyaudio.paContinue)

    with sd.InputStream(
            samplerate = sample_rate,
            channels = 1,
            callback = callback
    ):
        # signal = record_audio(sample_rate, small_time_step)

        # Start a timer to process the audio every small_time_step seconds
        start_time = time.time()
        while True:
            current_time = time.time()
            if current_time - start_time >= small_time_step:
                peak_notes, volume = time_step_analysis(signal, sample_rate)

                if peak_notes is None:
                    continue

                list_o_notes.append(peak_notes)
                volumes.append(volume)

                start_time = current_time

            # Create a new galaxy based on the processed audio data
            if current_time - start_time >= big_time_step:

                # Flatten the list of lists of notes for Counter
                flattened_list_o_notes = [note[0] for sublist in list_o_notes for note in sublist]

                # Counter does not sort by frequency, so we need to sort it
                sorted_counter = {
                    k: v for k, v in sorted(
                            Counter(flattened_list_o_notes).items(), key = lambda item: item[1],
                            reverse = True
                    )
                }

                note_priority_map = {
                    note: priority_num
                    for priority_num, note in enumerate(
                            sorted_counter.keys()
                    )
                }

                # Normalize volumes
                volumes = np.array(volumes)
                max_volume = np.max(volumes)
                min_volume = np.min(volumes)

                norm_volumes = (volumes - min_volume) / (max_volume - min_volume)

                seed_value = initial_seed_value
                for i, (notes_chunk, norm_volume) in enumerate(zip(list_o_notes, norm_volumes)):
                    # Leaving this as such can allow me to debug things later
                    # Based on their coordinates in the image
                    seed(seed_value)
                    x_pos = randint(model_offset, width - model_offset)
                    y_pos = randint(model_offset, height - model_offset)
                    seed_value += 1

                    output_filename = galfitting(
                            feedme_0,
                            input_filename_0,
                            output_filename_0,
                            gname,
                            x_pos,
                            y_pos,
                            model_offset,
                            notes_chunk,
                            norm_volume,
                            i
                    )

                    image_array += process_galfit_output(
                            output_filename,
                            height,
                            width,
                            x_pos,
                            y_pos,
                            model_dim,
                            model_offset
                    )

                start_time = current_time
            sd.sleep(100)  # Sleep for a short duration to prevent high CPU usage