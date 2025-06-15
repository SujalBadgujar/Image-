# Image Compositing Pipeline

## Overview
This project is an image compositing pipeline that removes the background from a person's image, places them in a new background, generates a cast shadow, harmonizes colors, and composites the final image. It is designed to create realistic composite images by seamlessly integrating a person into a new scene.

## Workflow
1. **Background Removal**: 
   - The background is removed from the person's image using the `rembg` library. This step isolates the person from their original background, allowing them to be placed in a new scene.

2. **Placement**: 
   - The person is resized and placed in the new background scene. This involves scaling the person to fit the new scene and positioning them at the desired location.

3. **Shadow Generation**: 
   - A cast shadow is generated based on the person's mask and the specified light direction. This adds realism to the composite by simulating how shadows would naturally fall in the scene.

4. **Color Harmonization**: 
   - The colors of the foreground (the person) are adjusted to better match the background. This step ensures that the lighting and color tones of the person blend seamlessly with the new scene.

5. **Final Compositing**: 
   - All layers (background, shadow, and harmonized foreground) are composited to create the final image. This step combines all elements into a single, cohesive image.
  
Original Image:
![person_original](https://github.com/user-attachments/assets/ee3d372a-2ff7-45ac-bae0-8ff788a1b476)
Background:
![background](https://github.com/user-attachments/assets/4cd0b5cd-f88b-4d24-ac37-5704f20cbc8f)
Final Output:
![final_composite](https://github.com/user-attachments/assets/848e07c1-a4f7-4710-9e32-2b229f22649a)





## License
This project is licensed under the MIT License - see the LICENSE file for details. 
