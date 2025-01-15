from flask import Flask, render_template, request, send_from_directory
import os
import cv2
import numpy as np

app = Flask(__name__)

UPLOAD_FOLDER = 'static/images'
PROCESSED_FOLDER = 'mask_images'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)

def custom_grayscale(image):
    return 0.299 * image[:,:,2] + 0.587 * image[:,:,1] + 0.114 * image[:,:,0]

@app.route('/')
def index():
    images = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', images=images)

@app.route('/process', methods=['POST'])
def process():
    img_name = request.form['image']
    threshold_type = request.form.get('threshold_type')
    threshold_value = int(request.form['threshold_value']) if request.form['threshold_value'] else 0
    apply_gaussian = request.form.get('apply_gaussian')
    gaussian_kernel = int(request.form['gaussian_kernel']) if request.form['gaussian_kernel'] else 5
    adaptive_method = request.form.get('adaptive_method')
    block_size = int(request.form['block_size']) if request.form['block_size'] else 11
    c_value = int(request.form['c_value']) if request.form['c_value'] else 2
    morph_operation = request.form.get('morph_operation')
    morph_kernel_size = int(request.form['morph_kernel_size']) if request.form['morph_kernel_size'] else 3
    edge_detection = request.form.get('edge_detection')
    canny_threshold1 = int(request.form['canny_threshold1']) if request.form['canny_threshold1'] else 100
    canny_threshold2 = int(request.form['canny_threshold2']) if request.form['canny_threshold2'] else 200

    img_path = os.path.join(UPLOAD_FOLDER, img_name)
    img = cv2.imread(img_path)
    gray_img = custom_grayscale(img).astype(np.uint8)

    if apply_gaussian:
        gray_img = cv2.GaussianBlur(gray_img, (gaussian_kernel, gaussian_kernel), 0)

    if threshold_type == 'adaptive':
        if adaptive_method == 'mean':
            thresh_img = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, c_value)
        elif adaptive_method == 'gaussian':
            thresh_img = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, c_value)
    else:
        _, thresh_img = cv2.threshold(gray_img, threshold_value, 255, int(threshold_type))

    if morph_operation != 'none':
        kernel = np.ones((morph_kernel_size, morph_kernel_size), np.uint8)
        if morph_operation == 'erode':
            thresh_img = cv2.erode(thresh_img, kernel, iterations=1)
        elif morph_operation == 'dilate':
            thresh_img = cv2.dilate(thresh_img, kernel, iterations=1)
        elif morph_operation == 'open':
            thresh_img = cv2.morphologyEx(thresh_img, cv2.MORPH_OPEN, kernel)
        elif morph_operation == 'close':
            thresh_img = cv2.morphologyEx(thresh_img, cv2.MORPH_CLOSE, kernel)

    if edge_detection == 'sobel':
        grad_x = cv2.Sobel(thresh_img, cv2.CV_16S, 1, 0, ksize=3)
        grad_y = cv2.Sobel(thresh_img, cv2.CV_16S, 0, 1, ksize=3)
        abs_grad_x = cv2.convertScaleAbs(grad_x)
        abs_grad_y = cv2.convertScaleAbs(grad_y)
        edge_img = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
        thresh_img = edge_img
    elif edge_detection == 'canny':
        thresh_img = cv2.Canny(thresh_img, canny_threshold1, canny_threshold2)

    save_path = os.path.join(PROCESSED_FOLDER, img_name)
    cv2.imwrite(save_path, thresh_img)

    return send_from_directory(PROCESSED_FOLDER, img_name)

@app.route('/save', methods=['POST'])
def save():
    img_name = request.form['image']
    # Saving is done in the process step. No need to move the file again.
    return '', 200

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return '', 204

@app.route('/preview', methods=['POST'])
def preview():
    img_name = request.form['image']
    threshold_type = request.form.get('threshold_type')
    threshold_value = int(request.form['threshold_value']) if request.form['threshold_value'] else 0
    apply_gaussian = request.form.get('apply_gaussian')
    gaussian_kernel = int(request.form['gaussian_kernel']) if request.form['gaussian_kernel'] else 5
    adaptive_method = request.form.get('adaptive_method')
    block_size = int(request.form['block_size']) if request.form['block_size'] else 11
    c_value = int(request.form['c_value']) if request.form['c_value'] else 2
    morph_operation = request.form.get('morph_operation')
    morph_kernel_size = int(request.form['morph_kernel_size']) if request.form['morph_kernel_size'] else 3
    edge_detection = request.form.get('edge_detection')
    canny_threshold1 = int(request.form['canny_threshold1']) if request.form['canny_threshold1'] else 100
    canny_threshold2 = int(request.form['canny_threshold2']) if request.form['canny_threshold2'] else 200

    img_path = os.path.join(UPLOAD_FOLDER, img_name)
    img = cv2.imread(img_path)
    gray_img = custom_grayscale(img).astype(np.uint8)

    if apply_gaussian:
        gray_img = cv2.GaussianBlur(gray_img, (gaussian_kernel, gaussian_kernel), 0)

    if threshold_type == 'adaptive':
        if adaptive_method == 'mean':
            thresh_img = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, c_value)
        elif adaptive_method == 'gaussian':
            thresh_img = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, c_value)
    else:
        _, thresh_img = cv2.threshold(gray_img, threshold_value, 255, int(threshold_type))

    if morph_operation != 'none':
        kernel = np.ones((morph_kernel_size, morph_kernel_size), np.uint8)
        if morph_operation == 'erode':
            thresh_img = cv2.erode(thresh_img, kernel, iterations=1)
        elif morph_operation == 'dilate':
            thresh_img = cv2.dilate(thresh_img, kernel, iterations=1)
        elif morph_operation == 'open':
            thresh_img = cv2.morphologyEx(thresh_img, cv2.MORPH_OPEN, kernel)
        elif morph_operation == 'close':
            thresh_img = cv2.morphologyEx(thresh_img, cv2.MORPH_CLOSE, kernel)

    if edge_detection == 'sobel':
        grad_x = cv2.Sobel(thresh_img, cv2.CV_16S, 1, 0, ksize=3)
        grad_y = cv2.Sobel(thresh_img, cv2.CV_16S, 0, 1, ksize=3)
        abs_grad_x = cv2.convertScaleAbs(grad_x)
        abs_grad_y = cv2.convertScaleAbs(grad_y)
        edge_img = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
        thresh_img = edge_img
    elif edge_detection == 'canny':
        thresh_img = cv2.Canny(thresh_img, canny_threshold1, canny_threshold2)

    _, buffer = cv2.imencode('.png', thresh_img)
    response = buffer.tobytes()
    return response

if __name__ == '__main__':
    app.run(debug=True)
# sdf