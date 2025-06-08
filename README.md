# Image Masker

An interactive Python application for selective image editing using OpenCV. Draw masks on images to keep selected areas in color while converting the rest to grayscale.

## Features

- **Interactive Drawing**: Use your mouse to draw masks directly on images
- **Real-time Preview**: See inverted colors in masked areas with animated marching ants outline
- **Selective Processing**: Keep masked areas in color, convert unmasked areas to grayscale
- **Adjustable Brush**: Change brush size on the fly
- **Visual Feedback**: Brush cursor and marching ants animation for better user experience
- **Save Output**: Export your edited images

## Requirements

- Python 3.x
- OpenCV (`cv2`)
- NumPy

## Installation

1. Install the required dependencies:
```bash
pip install opencv-python numpy
```

2. Download the project files:
   - `masker.py` - Main application
   - `sketcher.py` - Drawing functionality

## Usage

Run the application from the command line:

```bash
python masker.py <image_path>
```

**Example:**
```bash
python masker.py sample.jpg
```

## Controls

### Mouse Controls
- **Left Click + Drag**: Draw mask on the image

### Keyboard Controls
- **R**: Process the mask and show the result (color mask, grayscale elsewhere)
- **C**: Clear the current mask
- **S**: Save the output image
- **I**: Show mask statistics (percentage of image masked)
- **M**: View the mask as a black and white image
- **+/=**: Increase brush size
- **-/_**: Decrease brush size
- **ESC/Q**: Quit the application

## How It Works

1. **Load Image**: The application loads your image and creates a blank mask
2. **Draw Mask**: Use your mouse to draw on areas you want to keep in color
3. **Process**: Press 'R' to apply the effect:
   - Masked areas remain in full color
   - Unmasked areas are converted to grayscale
4. **Save**: Press 'S' to save your edited image

## Visual Feedback

- **Inverted Colors**: Masked areas show inverted colors for easy identification
- **Marching Ants**: Animated dashed outline around masked regions
- **Brush Cursor**: Shows current brush size and position
- **Real-time Updates**: Changes appear immediately as you draw

## Output

The processed image will show:
- **Color regions**: Areas you drew on (masked)
- **Grayscale regions**: Areas you didn't draw on (unmasked)

Saved images are automatically named with the prefix `output_` followed by the original filename.

## File Structure

```
image-masker/
├─README.md             # This file
├─gorilla.jpg           # sample image
├─gorilla_output.jpg    # sample processed image
└─src/
    ├── masker.py       # Main application class
    └── sketcher.py     # Interactive drawing functionality
```

## Code Architecture

### ImageMasker Class (`masker.py`)
- Main application controller
- Handles image loading, processing, and file operations
- Manages the user interface and keyboard controls

### Sketcher Class (`sketcher.py`)
- Handles all drawing operations
- Manages mouse callbacks and drawing state
- Provides visual feedback (marching ants, brush cursor)
- Handles mask manipulation

## Example Workflow

1. Start the application: `python masker.py photo.jpg`
2. Draw on the parts of the image you want to keep in color
3. Press 'R' to see the color/grayscale effect
4. Adjust your mask by drawing more or pressing 'C' to clear and start over
5. Press 'S' to save when satisfied with the result

## Troubleshooting

**"Could not load image" error:**
- Check that the image path is correct
- Ensure the image format is supported by OpenCV (JPG, PNG, BMP, etc.)

**No output when pressing 'R':**
- Make sure you've drawn on the image first
- Check that the mask has white pixels by pressing 'M' to view the mask

**Application not responding:**
- Make sure the image window has focus when using keyboard controls
- Try clicking on the image window first

## License

This project is open source. Feel free to modify and distribute as needed.
