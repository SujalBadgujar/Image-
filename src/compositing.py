import cv2
import numpy as np

def composite_final(background: np.ndarray, shadow_rgba: np.ndarray, 
                    harmonized_fg: np.ndarray, fg_mask: np.ndarray) -> np.ndarray:
    """
    Composites all layers together: background, shadow, and foreground.
    
    Args:
        background (np.ndarray): The original BGR background image.
        shadow_rgba (np.ndarray): The RGBA shadow layer (float32).
        harmonized_fg (np.ndarray): The color-corrected BGR foreground layer.
        fg_mask (np.ndarray): The mask of the foreground on its layer.
        
    Returns:
        final_image (np.ndarray): The final BGR composite image.
    """
    # Convert background to float and normalize
    background_float = background.astype(np.float32) / 255.0
    
    # Extract alpha channel and BGR components from the shadow
    shadow_alpha = shadow_rgba[:, :, 3:4] / 255.0  # Normalize to [0, 1]
    shadow_bgr = shadow_rgba[:, :, :3]
    
    # Blend shadow onto the background
    bg_with_shadow = background_float * (1.0 - shadow_alpha) + shadow_bgr * shadow_alpha
    
    # Prepare foreground for blending
    fg_float = harmonized_fg.astype(np.float32) / 255.0
    fg_mask_float = (fg_mask[:, :, np.newaxis] / 255.0)
    
    # Composite foreground onto the shadowed background
    composite = bg_with_shadow * (1.0 - fg_mask_float) + fg_float * fg_mask_float

    # Add slight noise for unification, optional step
    noise = np.random.normal(0, 0.01, composite.shape).astype(np.float32)
    final_image_float = np.clip(composite + noise, 0.0, 1.0)
    
    # Convert final image to uint8
    final_image = (final_image_float * 255).astype(np.uint8)
    
    return final_image