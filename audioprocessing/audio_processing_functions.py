
def rms(data, width):
    """
    audioop.rms() using numpy; since audioop will be deprecated
    Thanks https://stackoverflow.com/q/9763471 !
    """

    if len(data) == 0:
        return None

    from_type = (np.int8, np.int16, np.int32)[width // 2]
    d = np.frombuffer(data, from_type).astype(float)

    return int(np.sqrt(np.mean(d ** 2)))


def load_audio(music_filename, delay = 0.5):
    # Load the audio file
    signal, sample_rate = librosa.load(music_filename)
    time_array = np.arange(librosa.get_duration(path = music_filename), step = 1 / sample_rate)

    signal = signal[time_array > delay]
    time_array = time_array[time_array > delay]

    return signal, sample_rate, time_array


def select_peaks(
        signal: np.ndarray,
        sample_rate: int,
        # Want 5 but add 1 for check for duplicates otherwise things get thrown off
        num_notes_to_pick = 5 + 1,
        num_notes_to_check = 10,
        # A blurring parameter
        seconds = 0.01
) -> list[float]:
    """
    Selects the peaks in the signal
    :param signal:
    :param sample_rate:
    :param num_notes_to_pick:
    :param num_notes_to_check:
    :param seconds:
    :return:
    """

    # Extracting chords and duration

    # There's no pretty way to represent this...
    denominator = (
            np.sqrt(
                    2 * np.pi * seconds ** 2
            ) *
            np.exp(
                -0.5 *
                (
                        np.linspace(
                            -3 * seconds, 3 * seconds, int(6 * seconds * sample_rate)
                            ) / seconds
                ) ** 2
                )
    )

    # blur(abs(signal)) to find peaks
    blurProfile = (1 / denominator)

    signalBlurred = np.convolve(signal ** 2, blurProfile, mode = 'same')

    chord_range = signalBlurred > 100
    if not np.any(chord_range):
        return None

    # FT first peak to get note
    fourier_transform = fft.fft(signal[chord_range])
    frequencies = fft.fftfreq(len(signal[chord_range]), d = 1 / sample_rate)

    fourier_transform = fourier_transform[frequencies >= 0]
    frequencies = frequencies[frequencies >= 0]
    # fmask = (frequencies > 10) & (frequencies < 2000)

    # TODO: Note duration?
    # noteBins = 220*(2**((np.arange(12*3)-0.5)/12)) # starting from A below middle

    # Basic peak detection method
    # This works because the FT is so good at picking frequency peaks out
    all_peaks = frequencies[np.argsort(fourier_transform)]
    selected_peaks = all_peaks[-num_notes_to_pick:]
    while len(set(selected_peaks)) < num_notes_to_pick:
        num_notes_to_check += 1
        selected_peaks = all_peaks[-num_notes_to_check:]

    return selected_peaks


def time_step_analysis(signal, sample_rate):
    """
    Analyzes the signal at a given time step
    :param signal:
    :param sample_rate:
    :param time_array:
    :param delay:
    :return:
    """
    signal_cut = signal[t_step - t_step_size: t_step]
    volume = rms(signal_cut, 2)

    selected_peaks = select_peaks(signal_cut, sample_rate)
    if selected_peaks is None:
        return None, None

    peak_notes = binary_search_ranges(ranges_for_search, selected_peaks)

    return peak_notes, volume