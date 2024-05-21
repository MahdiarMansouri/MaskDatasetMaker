
# Image Mask Preparation App for Segmentation Tasks

This mini app is designed to help you prepare image masks for segmentation tasks efficiently.

## Features

- **Real-Time Processing:** Generate image masks in real-time as you upload your images.
- **Custom Grayscale Conversion:** Apply a custom grayscale conversion to enhance the image processing pipeline.
- **Multiple Thresholding Methods:** Choose from various thresholding methods including adaptive and fixed thresholding.
  - **Adaptive Thresholding:** Utilize adaptive mean or Gaussian methods for local thresholding.
  - **Fixed Thresholding:** Apply a global threshold value for consistent mask creation.
- **Gaussian Blur:** Option to apply Gaussian blur to smooth images before thresholding.
- **Morphological Operations:** Perform morphological operations such as dilation and erosion to refine the masks.
- **Edge Detection:** Apply Canny edge detection to highlight edges within the images.
- **Parameter Customization:** Customize parameters for block size, constant value, kernel size, and more to fine-tune the mask generation process.
- **Automated Mask Saving:** Automatically save processed masks in the `mask_images` folder for easy access.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/image-mask-preparation.git
    ```

2. Navigate to the project directory:

    ```bash
    cd image-mask-preparation
    ```

3. Install the necessary dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Ensure your images are saved in the `static/images` folder.

2. Run the app:

    ```bash
    python app.py
    ```

3. Open your browser and navigate to `http://127.0.0.1:5000`.

4. Upload your photo through the provided interface. The processed (masked) images will be saved in the `mask_images` folder.

### Example Workflow

1. **Upload Image:** Select an image from your local machine to upload.
2. **Select Processing Options:** Choose the desired thresholding method, apply Gaussian blur if needed, and select any morphological operations.
3. **Adjust Parameters:** Customize the parameters such as threshold value, block size, and kernel size for optimal mask generation.
4. **Process Image:** Click the process button to generate the mask in real-time.
5. **Save Mask:** The generated mask will be automatically saved in the `mask_images` folder.

## Requirements

- Flask
- opencv-python
- numpy

You can install these dependencies using the following command:

```bash
pip install Flask opencv-python numpy
```

## Contributing

Feel free to open issues or submit pull requests for improvements or bug fixes.

---

