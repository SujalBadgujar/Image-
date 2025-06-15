import cv2
import numpy as np
from typing import Tuple

def create_shadow(person_mask: np.ndarray, 
                  light_direction_vector: Tuple[float, float], 
                  blur_kernel_size: int, opacity: float) -> np.ndarray:
    """
    Creates a cast shadow from the person's mask.
    
    Args:
        person_mask (np.ndarray): The alpha mask of the placed person.
        light_direction_vector (tuple): A (dx, dy) vector for shear transformation.
        blur_kernel_size (int): The kernel size for Gaussian blur (must be odd).
        opacity (float): The opacity of the final shadow (0.0 to 1.0).
        
    Returns:
        shadow_rgba (np.ndarray): An RGBA image of the shadow layer.
    """
    # Validate inputs
    if not (0.0 <= opacity <= 1.0):
        raise ValueError("Opacity must be between 0.0 and 1.0.")
    if blur_kernel_size % 2 == 0:
        raise ValueError("Blur kernel size must be odd.")
    
    shear_x, shear_y = light_direction_vector
    shear_matrix = np.float32([[1, shear_x, 0], [shear_y, 1, 0]])
    
    h, w = person_mask.shape
    shadow = cv2.warpAffine(person_mask, shear_matrix, (w, h))
    shadow = cv2.GaussianBlur(shadow, (blur_kernel_size, blur_kernel_size), 0)
    
    shadow_alpha = (shadow / 255.0) * opacity
    shadow_alpha = (shadow_alpha * 255).astype(np.uint8)  # scale to 0-255 and uint8
    shadow_bgr = np.zeros((h, w, 3), dtype=np.uint8)
    shadow_rgba = cv2.merge((shadow_bgr[:,:,0], shadow_bgr[:,:,1], shadow_bgr[:,:,2], shadow_alpha))
    
    return shadow_rgba.astype(np.float32)