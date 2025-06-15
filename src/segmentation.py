from rembg import remove
from PIL import Image
import numpy as np
import cv2
import io
from typing import Tuple, Optional

def remove_background(image_path: str) -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
    """
    Removes the background from an image using the rembg library.
    
    Args:
        image_path (str): The path to the input image.
        
    Returns:
        A tuple containing:
        - foreground_bgr (np.ndarray): The foreground image in BGR format.
        - alpha_mask (np.ndarray): The alpha mask of the foreground (0-255).
    """
    try:
        with open(image_path, 'rb') as f:
            input_bytes = f.read()
            output_bytes = remove(input_bytes)
        
        foreground_pil = Image.open(io.BytesIO(output_bytes)).convert("RGBA")
        foreground_np = np.array(foreground_pil)
        
        alpha_mask = foreground_np[:, :, 3]
        foreground_bgr = cv2.cvtColor(foreground_np, cv2.COLOR_RGBA2BGR)
        
        return foreground_bgr, alpha_mask

    except Exception as e:
        print(f"Error in background removal: {e}")
        raise