# image2music/midi_synthesis.py

import numpy as np
import pandas as pd
import librosa
from music21 import stream, note, tempo
from tqdm.auto import tqdm
from typing import Union

from .logger import get_logger

logger = get_logger(__name__)


def frequencies_to_midi_stream(
    pixel_df: pd.DataFrame,
    bpm: int = 120,
    note_duration: float = 0.5,
    filter_repeats: bool = True
) -> stream.Stream:
    """
    Convert a DataFrame of pixel frequencies into a MIDI stream.

    Parameters
    ----------
    pixel_df : pd.DataFrame
        DataFrame with at least a 'frequencies' column.
    bpm : int
        Beats per minute for the MIDI file.
    note_duration : float
        Duration of each note in quarter lengths.
    filter_repeats : bool
        Whether to remove consecutive duplicate notes.

    Returns
    -------
    stream.Stream
        A music21 Stream containing the MIDI notes.
    """
    if "frequencies" not in pixel_df.columns:
        raise ValueError("pixel_df must contain a 'frequencies' column.")

    logger.info("Converting frequencies to musical notes...")
    pixel_df = pixel_df.copy()
    pixel_df["notes"] = pixel_df["frequencies"].apply(librosa.hz_to_note)
    pixel_df["midi_number"] = pixel_df["notes"].apply(librosa.note_to_midi)

    notes_array = pixel_df["notes"].to_numpy()

    if filter_repeats:
        logger.info("Filtering consecutive duplicate notes...")
        filtered_notes = []
        for element in notes_array:
            if not filtered_notes or element != filtered_notes[-1]:
                filtered_notes.append(element)
        notes_array = np.array(filtered_notes)

    logger.info("Creating MIDI stream with %d notes...", len(notes_array))
    midi_stream = stream.Stream()
    midi_stream.append(tempo.MetronomeMark(number=bpm))

    for element in tqdm(notes_array, desc="Adding notes"):
        pitch = element.replace('♯', "#")  # Ensure sharp symbol is MIDI-friendly
        midi_note = note.Note(pitch)
        midi_note.quarterLength = note_duration
        midi_stream.append(midi_note)

    return midi_stream


def save_midi(midi_stream: stream.Stream, file_path: Union[str, bytes]) -> None:
    """
    Save a music21 Stream to a MIDI file.

    Parameters
    ----------
    midi_stream : stream.Stream
        The music21 stream to save.
    file_path : str or bytes
        Path to save the MIDI file.
    """
    midi_stream.write("midi", fp=file_path)
    logger.info("Saved MIDI file: %s", file_path)
