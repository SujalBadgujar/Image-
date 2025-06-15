import cv2
import numpy as np

def harmonize_color(foreground: np.ndarray, background: np.ndarray, fg_mask: np.ndarray) -> np.ndarray:
    """
    Harmonizes the foreground color to the background using L*a*b* color space.
    
    Args:
        foreground (np.ndarray): The BGR foreground image layer.
        background (np.ndarray): The BGR background image.
        fg_mask (np.ndarray): The mask of the foreground on its layer.
        
    Returns:
        harmonized_fg (np.ndarray): The color-corrected BGR foreground layer.
    """
    if foreground is None or background is None or fg_mask is None:
        print("Invalid input: One or more required inputs are None")
        return foreground

    # Convert images to L*a*b* color space
    fg_lab = cv2.cvtColor(foreground, cv2.COLOR_BGR2LAB).astype("float32")
    bg_lab = cv2.cvtColor(background, cv2.COLOR_BGR2LAB).astype("float32")

    # Ensure that fg_mask has the same height and width as the foreground
    if fg_mask.shape[:2] != foreground.shape[:2]:
        print("Foreground mask size mismatch.")
        return foreground

    # Flatten mask; ensure dimensions match for logical indexing
    fg_pixels = fg_lab[fg_mask > 0]

    if fg_pixels.size == 0:
        print("No foreground pixels found.")
        return foreground

    # Analyze all background pixels
    bg_pixels = bg_lab.reshape(-1, 3)

    # Calculate means and standard deviations
    fg_mean, fg_std = cv2.meanStdDev(fg_pixels)
    bg_mean, bg_std = cv2.meanStdDev(bg_pixels)

    # Ensure fg_mean, fg_std, bg_mean, bg_std are correctly shaped
    fg_mean = fg_mean.reshape(-1)
    fg_std = fg_std.reshape(-1)
    bg_mean = bg_mean.reshape(-1)
    bg_std = bg_std.reshape(-1)

    # Avoid division by zero
    fg_std = np.where(fg_std == 0, 1, fg_std)

    l, a, b = cv2.split(fg_lab)

    # Apply mean and standard deviation adjustments
    l = np.clip((l - fg_mean[0]) * (bg_std[0] / fg_std[0]) + bg_mean[0], 0, 255)
    a = np.clip((a - fg_mean[1]) * (bg_std[1] / fg_std[1]) + bg_mean[1], 0, 255)
    b = np.clip((b - fg_mean[2]) * (bg_std[2] / fg_std[2]) + bg_mean[2], 0, 255)

    harmonized_lab = cv2.merge([l, a, b])
    harmonized_bgr = cv2.cvtColor(harmonized_lab.astype("uint8"), cv2.COLOR_LAB2BGR)

    # Create composite image using mask
    result = np.where(fg_mask[:, :, None] > 0, harmonized_bgr, foreground)

    return result

