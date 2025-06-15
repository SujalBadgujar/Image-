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



## License
This project is licensed under the MIT License - see the LICENSE file for details. 