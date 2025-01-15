import cv2
import numpy as np
import os

# Path to the directory containing cropped images
cropped_images_dir = 'croped_img'

# Ensure the output directory exists
output_dir = 'output_img'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Iterate through each cropped image
for img_file in os.listdir(cropped_images_dir):
    img_path = os.path.join(cropped_images_dir, img_file)

    # Read the image
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect circles using Hough Circle Transform
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1.9, minDist=200, param1=30, param2=30, minRadius=90,
                               maxRadius=180)

    # Create a white background image
    white_background = np.full_like(img, 255)

    if circles is not None:
        # Convert the circle coordinates to integers
        circles = np.round(circles[0, :]).astype("int")

        # Create a mask for the circle
        mask = np.zeros_like(gray)
        for (x, y, r) in circles:
            cv2.circle(mask, (x, y), r, 255, -1)  # Fill the circle with white in the mask

        # Invert the mask to get the background
        mask_inv = cv2.bitwise_not(mask)

        # Use the mask to keep the circle and set the rest to white
        img_circle = cv2.bitwise_and(img, img, mask=mask)
        white_outside = cv2.bitwise_and(white_background, white_background, mask=mask_inv)
        result = cv2.add(img_circle, white_outside)
    else:
        # If no circle is detected, use the white background
        result = white_background

    # Save the result
    output_path = os.path.join(output_dir, img_file)
    cv2.imwrite(output_path, result)

    # cv2.imshow("Result", result)
    # cv2.waitKey(0)

print(f"Processed images are saved in {output_dir}")
