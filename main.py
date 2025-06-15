import cv2
import os
from src.segmentation import remove_background
from src.transformation import place_person
from src.shadow import create_shadow
from src.compositing import composite_final
import logging
import numpy as np

# --- CONFIGURATION ---
INPUT_DIR = "input"
OUTPUT_DIR = "output"
PERSON_IMAGE_FILE = "person_original.jpg"
BACKGROUND_IMAGE_FILE = "background.jpg"

DEST_COORDS = (450, 280)
SCALE_FACTOR = 0.85

LIGHT_DIRECTION = (0.7, 0.3)
SHADOW_BLUR_KERNEL = 91
SHADOW_OPACITY = 0.65

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def adjust_color_shades(fg, bg, mask):
    """ Adjust the color shades of the foreground person to match the average background brightness. """

    # Convert both images to the LAB color space
    fg_lab = cv2.cvtColor(fg, cv2.COLOR_BGR2LAB)
    bg_lab = cv2.cvtColor(bg, cv2.COLOR_BGR2LAB)

    # Calculate the mean for the L channel (brightness) of the entire background
    l_mean_bg = cv2.meanStdDev(bg_lab[:,:,0])[0][0]

    # Calculate the mean for the L channel of the masked foreground
    l_mean_fg = cv2.meanStdDev(fg_lab[:,:,0], mask=mask)[0][0]

    # Calculate the difference in brightness
    l_adjust = l_mean_bg - 1.7*l_mean_fg

    # Adjust the L channel of the foreground
    fg_lab[:,:,0] = np.clip(fg_lab[:,:,0] + l_adjust, 0, 255)

    # Convert back to the BGR color space
    adjusted_fg = cv2.cvtColor(fg_lab, cv2.COLOR_LAB2BGR)

    return adjusted_fg

def main():
    setup_logging()

    person_path = os.path.join(INPUT_DIR, PERSON_IMAGE_FILE)
    background_path = os.path.join(INPUT_DIR, BACKGROUND_IMAGE_FILE)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    logging.info("Starting Image Compositing Pipeline")

    try:
        logging.info("Removing background from person...")
        person_fg, person_mask = remove_background(person_path)
        
        if person_fg is None:
            logging.error("Background removal failed.")
            return
        
        cv2.imwrite(os.path.join(OUTPUT_DIR, "1_person_foreground.png"), 
                    cv2.merge((person_fg[:,:,0], person_fg[:,:,1], person_fg[:,:,2], person_mask)))
        
        logging.info("Resizing and placing person in the scene...")
        background_img = cv2.imread(background_path)
        if background_img is None:
            logging.error("Failed to load background image.")
            return
        
        placed_fg_layer, placed_mask_layer = place_person(
            person_fg, person_mask, background_img.shape, DEST_COORDS, SCALE_FACTOR
        )
        
        logging.info("Generating cast shadow...")
        shadow_layer_rgba = create_shadow(
            placed_mask_layer, LIGHT_DIRECTION, SHADOW_BLUR_KERNEL, SHADOW_OPACITY
        )
        cv2.imwrite(os.path.join(OUTPUT_DIR, "2_shadow_layer.png"), (shadow_layer_rgba * 255).astype('uint8'))
        
        # Adjust color shades
        logging.info("Adjusting color shades of foreground...")
        harmonized_fg_layer = adjust_color_shades(placed_fg_layer, background_img, placed_mask_layer)

        logging.info("Compositing all layers...")
        final_image = composite_final(
            background_img, shadow_layer_rgba, harmonized_fg_layer, placed_mask_layer
        )
        
        final_output_path = os.path.join(OUTPUT_DIR, "final_composite.jpg")
        cv2.imwrite(final_output_path, final_image)
        logging.info(f"Pipeline complete! Final image saved to: {final_output_path}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()