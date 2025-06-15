import cv2
import numpy as np
from typing import Tuple

def place_person(foreground_bgr: np.ndarray, alpha_mask: np.ndarray, 
                 bg_shape: Tuple[int, int, int], dest_coords: Tuple[int, int], 
                 scale_factor: float) -> Tuple[np.ndarray, np.ndarray]:
    """
    Resizes and places the foreground onto a blank canvas matching the background size.

    Args:
        foreground_bgr (np.ndarray): The person's image (BGR).
        alpha_mask (np.ndarray): The person's alpha mask.
        bg_shape (tuple): The shape (height, width, channels) of the background image.
        dest_coords (tuple): The (x, y) coordinates for the top-left corner of the person.
        scale_factor (float): The factor by which to scale the person.
        
    Returns:
        A tuple containing:
        - final_fg_layer (np.ndarray): The transformed BGR foreground on a full-sized canvas.
        - final_mask_layer (np.ndarray): The transformed alpha mask on a full-sized canvas.
    """
    # Validate scale factor
    if scale_factor <= 0:
        raise ValueError("Scale factor must be positive.")
    
    # Resize the foreground and mask
    resized_fg = cv2.resize(foreground_bgr, (0, 0), fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_AREA)
    resized_mask = cv2.resize(alpha_mask, (0, 0), fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_AREA)

    # Create blank canvas for the final output
    bg_h, bg_w, _ = bg_shape
    final_fg_layer = np.zeros((bg_h, bg_w, 3), dtype=np.uint8)
    final_mask_layer = np.zeros((bg_h, bg_w), dtype=np.uint8)

    # Calculate placement coordinates
    x_offset, y_offset = dest_coords
    y1, y2 = max(0, y_offset), min(bg_h, y_offset + resized_fg.shape[0])
    x1, x2 = max(0, x_offset), min(bg_w, x_offset + resized_fg.shape[1])

    # Place the resized foreground and mask on the canvas
    final_fg_layer[y1:y2, x1:x2] = resized_fg[:y2-y1, :x2-x1]
    final_mask_layer[y1:y2, x1:x2] = resized_mask[:y2-y1, :x2-x1]

    return final_fg_layer, final_mask_layer