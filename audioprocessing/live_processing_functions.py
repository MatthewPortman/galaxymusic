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