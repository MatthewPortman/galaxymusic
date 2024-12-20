# From the twelve-tone tuning system
# Taken from
# https://master-studios.com/how-to-program-a-music-note-detector-in-python3-in-27-minutes/
notes_and_ranges = [
    ['C0', 16.35],
    ['C#0/Db0', 17.32],
    ['D0', 18.35],
    ['D#0/Eb0', 19.45],
    ['E0', 20.60],
    ['F0', 21.83],
    ['F#0/Gb0', 23.12],
    ['G0', 24.50],
    ['G#0/Ab0', 25.96],
    ['A0', 27.50],
    ['A#0/Bb0', 29.14],
    ['B0', 30.87],
    ['C1', 32.70],
    ['C#1/Db1', 34.65],
    ['D1', 36.71],
    ['D#1/Eb1', 38.89],
    ['E1', 41.20],
    ['F1', 43.65],
    ['F#1/Gb1', 46.25],
    ['G1', 49.00],
    ['G#1/Ab1', 51.91],
    ['A1', 55.00],
    ['A#1/Bb1', 58.27],
    ['B1', 61.74],
    ['C2', 65.41],
    ['C#2/Db2', 69.30],
    ['D2', 73.42],
    ['D#2/Eb2', 77.78],
    ['E2', 82.41],
    ['F2', 87.31],
    ['F#2/Gb2', 92.50],
    ['G2', 98.00],
    ['G#2/Ab2', 103.83],
    ['A2', 110.00],
    ['A#2/Bb2', 116.54],
    ['B2', 123.47],
    ['C3', 130.81],
    ['C#3/Db3', 138.59],
    ['D3', 146.83],
    ['D#3/Eb3', 155.56],
    ['E3', 164.81],
    ['F3', 174.61],
    ['F#3/Gb3', 185.00],
    ['G3', 196.00],
    ['G#3/Ab3', 207.65],
    ['A3', 220.00],
    ['A#3/Bb3', 233.08],
    ['B3', 246.94],
    ['C4', 261.63],
    ['C#4/Db4', 277.18],
    ['D4', 293.66],
    ['D#4/Eb4', 311.13],
    ['E4', 329.63],
    ['F4', 349.23],
    ['F#4/Gb4', 369.99],
    ['G4', 392.00],
    ['G#4/Ab4', 415.30],
    ['A4', 440.00],
    ['A#4/Bb4', 466.16],
    ['B4', 493.88],
    ['C5', 523.25],
    ['C#5/Db5', 554.37],
    ['D5', 587.33],
    ['D#5/Eb5', 622.25],
    ['E5', 659.25],
    ['F5', 698.46],
    ['F#5/Gb5', 739.99],
    ['G5', 783.99],
    ['G#5/Ab5', 830.61],
    ['A5', 880.00],
    ['A#5/Bb5', 932.33],
    ['B5', 987.77],
    ['C6', 1046.50],
    ['C#6/Db6', 1108.73],
    ['D6', 1174.66],
    ['D#6/Eb6', 1244.51	],
    ['E6', 1318.51],
    ['F6', 1396.91],
    ['F#6/Gb6', 1479.98],
    ['G6', 1567.98],
    ['G#6/Ab6', 1661.22],
    ['A6', 1760.00	],
    ['A#6/Bb6', 1864.66],
    ['B6', 1975.53	],
    ['C7', 2093.00],
    ['C#7/Db7', 2217.46],
    ['D7', 2349.32],
    ['D#7/Eb7', 2489.02],
    ['E7', 2637.02],
    ['F7', 2793.83],
    ['F#7/Gb7 ', 2959.96],
    ['G7', 3135.96],
    ['G#7/Ab7', 3322.44],
    ['A7', 3520.00],
    ['A#7/Bb7', 3729.31],
    ['B7', 3951.07],
    ['C8', 4186.01],
    ['C#8/Db8', 4434.92],
    ['D8', 4698.63],
    ['D#8/Eb8', 4978.03],
    ['E8', 5274.04],
    ['F8', 5587.65],
    ['F#8/Gb8', 5919.91],
    ['G8', 6271.93],
    ['G#8/Ab8', 6644.88	],
    ['A8', 7040.00],
    ['A#8/Bb8', 7458.62],
    ['B8', 7902.13],
]

def create_note_dict_ranges(notes : list) -> list[dict]:
    """
    Creates an alternate representation of the above list of lists.

    Parameters
    ----------
    notes : list
        List of lists containing the note names and their frequencies.

    Returns
    -------
    list
        List of dictionaries containing the start and end frequencies of each note.
    """
    note_dict_ranges = {}
    previous_tone_number = "0"
    previous_name = None
    for name, freq in notes:
        name = name.replace("#", "").replace("b", "").strip()

        current_tone_number = name[-1]

        # There are gaps when jumping to different numbers
        if current_tone_number != previous_tone_number:
            note_dict_ranges[previous_name].append(freq)

        note_letter_1 = name
        note_letter_2 = None

        # If there is a slash in the name, it is a frequency with two possible names
        if "/" in name:
            note_letter_1, note_letter_2 = name.split("/")
            # note_letter_1 = note_letter_1[0]
            # note_letter_2 = note_letter_2[0]

            # Note 1 has to exist (iterating in order)
            # Note 2 will not.
            note_dict_ranges[note_letter_1].append(freq)
            note_dict_ranges[note_letter_2] = [freq]

        else:
            # Avoid overwriting note and range if it already exists
            if note_letter_1 not in note_dict_ranges:
                note_dict_ranges[note_letter_1] = [freq]
            else:
                note_dict_ranges[note_letter_1].append(freq)

        previous_tone_number = current_tone_number
        previous_name = name

    # Reformat the results to be used by the binary search function.
    ranges_for_search = [
        {
            "start": freqs[0],
            "end"  : freqs[-1],
            "value": note
        }
        for note, freqs in note_dict_ranges.items()
    ]

    return ranges_for_search

note_ranges_for_search = create_note_dict_ranges(notes_and_ranges)
