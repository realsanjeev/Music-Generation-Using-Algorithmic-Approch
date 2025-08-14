from typing import List, Sequence
import pandas as pd
import numpy as np

from .logger import get_logger

logger = get_logger(__name__)


def hue2freq(hue: int, scale_freqs: Sequence[float]) -> float:
    """
    Map a hue value to a frequency in the given musical scale.

    Parameters
    ----------
    hue : int
        Hue value (0–255) from an HSV image.
    scale_freqs : Sequence[float]
        Sequence of frequencies for the scale (e.g., Harmonic Minor).

    Returns
    -------
    float
        The frequency corresponding to the hue value.
    """
    thresholds = [26, 52, 78, 104, 128, 154, 180]
    # thresholds = [25, 50, 75, 101, 126, 151, 179]  # 7 thresholds for 0-179 hue range

    if not scale_freqs:
        raise ValueError("scale_freqs must not be empty")
    if not 0 <= hue <= 255:
        logger.warning(f"Hue value {hue} out of range [0, 255], returning default frequency")
        return scale_freqs[0]
    
    if len(thresholds) > len(scale_freqs):
        logger.warning(
            "Number of thresholds (%d) exceeds number of scale frequencies (%d). "
            "Wrapping frequencies using modulo.",
            len(thresholds), len(scale_freqs)
        )
    
    index = np.searchsorted(thresholds, hue, side='right')
    return scale_freqs[index % len(scale_freqs)]

def hues_to_frequencies(hues: Sequence[int], scale_freqs: List[float]) -> np.ndarray:
    """
    Convert a sequence of hue values into an array of frequencies.

    Parameters
    ----------
    hues : Sequence[int]
        Sequence of hue values (0-255).
    scale_freqs : Sequence[float]
        Frequencies for the chosen musical scale.

    Returns
    -------
    np.ndarray
        Array of mapped frequencies.
    """
    if not scale_freqs:
        raise ValueError("scale_freqs must not be empty")
    logger.debug("Mapping %d hues to frequencies...", len(hues))
    freqs = [hue2freq(h, scale_freqs) for h in hues]
    freqs_array = np.array(freqs, dtype=float)
    logger.info("Converted hues to frequencies array of shape %s", freqs_array.shape)
    return freqs_array

def hues_dataframe(hues: Sequence[int], scale_freqs: List[float]) -> pd.DataFrame:
    """
    Create a pandas DataFrame with hues and their corresponding frequencies.

    Parameters
    ----------
    hues : Sequence[int]
        List or array of hue values.
    scale_freqs : List[float]
        Frequencies for the chosen musical scale.

    Returns
    -------
    pd.DataFrame
        DataFrame with 'hues' and 'frequencies' columns.
    """
    if not scale_freqs:
        raise ValueError("scale_freqs must not be empty")
    logger.debug("Creating DataFrame for %d hues", len(hues))
    df = pd.DataFrame({"hues": hues})
    df["frequencies"] = df["hues"].apply(lambda h: hue2freq(h, scale_freqs))
    logger.info("Generated DataFrame with %d rows", len(df))
    return df
