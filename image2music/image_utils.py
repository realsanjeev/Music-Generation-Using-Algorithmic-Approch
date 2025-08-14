import cv2
import numpy as np
from typing import Union

def load_image(image: Union[str, np.ndarray], size: tuple = (26, 26)) -> np.ndarray:
    """
    Load an image and convert it to HSV format with specified size.

    Parameters
    ----------
    image : str or np.ndarray
        File path to image or raw image array (in BGR).
    size : tuple
        Size to resize the image to (width, height).

    Returns
    -------
    np.ndarray
        HSV image resized to specified shape.
    """
    if isinstance(image, str):
        img = cv2.imread(image)
        if img is None:
            raise FileNotFoundError(f"Image not found: {image}")
    elif isinstance(image, np.ndarray):
        img = image
    else:
        raise ValueError(f"Unsupported image type: {type(image)}")

    # Resize and convert to HSV
    resized_img = cv2.resize(img, size)
    hsv_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2HSV)
    return hsv_img


def extract_hues(hsv_img: np.ndarray) -> np.ndarray:
    """
    Extract and flatten the hue channel from an HSV image.

    Parameters
    ----------
    hsv_img : np.ndarray
        HSV image of shape (H, W, 3)

    Returns
    -------
    np.ndarray
        1D array of hue values (0–179 in OpenCV)
    """
    return hsv_img[:, :, 0].flatten()
