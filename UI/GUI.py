import sys
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QMenu
from PyQt5.QtGui import QPixmap, QImage
import cv2 as cv

class ImageProcessingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Processing App")
        self.setGeometry(100, 100, 800, 600)

        # Widgets
        self.image_label = QLabel()
        self.load_button = QPushButton("Load Image")
        self.gray_button = QPushButton("Convert to Grayscale")
        self.contrast_button = QPushButton("Adjust Contrast")
        self.brightness_button = QPushButton("Brightness")
        self.filter_button = QPushButton("Apply Filter")

        self.contrast_menu = QMenu(self.contrast_button)
        self.increase_contrast_action = self.contrast_menu.addAction("+ Increase Contrast")
        self.decrease_contrast_action = self.contrast_menu.addAction("- Decrease Contrast")
        self.contrast_button.setMenu(self.contrast_menu)

        self.brightness_menu = QMenu(self.brightness_button)
        self.increase_brightness_action = self.brightness_menu.addAction("+ Increase Brightness")
        self.decrease_brightness_action = self.brightness_menu.addAction("- Decrease Brightness")
        self.brightness_button.setMenu(self.brightness_menu)

        self.filter_menu = QMenu(self.filter_button)
        self.filter_average_action = self.filter_menu.addAction("apply average filter")
        self.filter_median_action = self.filter_menu.addAction("apply median filter")
        self.filter_min_action = self.filter_menu.addAction("apply min filter")
        self.filter_max_action = self.filter_menu.addAction("apply max filter")
        self.filter_button.setMenu(self.filter_menu)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.load_button)
        layout.addWidget(self.gray_button)
        layout.addWidget(self.contrast_button)
        layout.addWidget(self.brightness_button)
        layout.addWidget(self.filter_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Signals
        self.load_button.clicked.connect(self.load_image)
        self.gray_button.clicked.connect(self.convert_to_grayscale)
        self.increase_contrast_action.triggered.connect(self.increase_contrast)
        self.decrease_contrast_action.triggered.connect(self.decrease_contrast)
        self.increase_brightness_action.triggered.connect(self.increase_brightness)
        self.decrease_brightness_action.triggered.connect(self.decrease_brightness)
        self.filter_average_action.triggered.connect(self.apply_filter_average)
        self.filter_average_action.triggered.connect(self.apply_filter_median)
        self.filter_average_action.triggered.connect(self.apply_filter_min)
        self.filter_average_action.triggered.connect(self.apply_filter_max)


        # Initialize variables
        self.image = None

    def load_image(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open Image", "images", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            self.image = cv.imread(file_path)
            self.display_image()

    def display_image(self):
        if self.image is not None:
            height, width, channel = self.image.shape
            bytes_per_line = 3 * width
            scale_factor = 1  # Adjust this factor to increase/decrease the size
        
            # Resize the image using OpenCV
            resized_image = cv.resize(self.image, (width * scale_factor, height * scale_factor))
        
            # Convert the resized image to a QImage
            q_img = QImage(resized_image.data, resized_image.shape[1], resized_image.shape[0], resized_image.strides[0], QImage.Format_RGB888).rgbSwapped()
            pixmap = QPixmap.fromImage(q_img)
            #scaled_pixmap = pixmap.scaled(self.image_label.size(), aspectRatioMode=Qt.KeepAspectRatio)
            self.image_label.setPixmap(pixmap)

    def convert_to_grayscale(self):
        if self.image is not None:
            gray_image = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
            self.image = cv.cvtColor(gray_image, cv.COLOR_GRAY2BGR)
            self.display_image()

    def increase_contrast(self):
        if self.image is not None:
            alpha = 1.2  # Increase contrast factor (1-3)
            beta = 0    # Keep brightness unchanged (0-100)
            self.image = cv.convertScaleAbs(self.image, alpha=alpha, beta=beta)
            self.display_image()

    def decrease_contrast(self):
        if self.image is not None:
            alpha = 0.8  # Decrease contrast factor
            beta = 0     # Keep brightness unchanged
            self.image = cv.convertScaleAbs(self.image, alpha=alpha, beta=beta)
            self.display_image()
    
    def increase_brightness(self):
        if self.image is not None:
            alpha = 1  # Increase contrast factor (1-3)
            beta = 10     # Keep brightness unchanged (0-100)
            self.image = cv.convertScaleAbs(self.image, alpha=alpha, beta=beta)
            self.display_image()

    def decrease_brightness(self):
        if self.image is not None:
            alpha = 1  # Decrease contrast factor
            beta = -10     # Keep brightness unchanged
            self.image = cv.convertScaleAbs(self.image, alpha=alpha, beta=beta)
            self.display_image()

    def apply_filter_average(self):
        if self.image is not None:
            kernel = np.ones((5, 5), np.float32) / 25
            self.image= cv.filter2D(self.image, -1, kernel)
            self.display_image()

    def apply_filter_median(self):
        if self.image is not None:
            self.image = cv.medianBlur(self.image, 9)
            self.display_image()
    
    def apply_filter_min(self):
        if self.image is not None:
            self.image = cv.erode(self.image, None, iterations=3)
            self.display_image()

    def apply_filter_max(self):
        if self.image is not None:
            self.image= cv.dilate(self.image, None, iterations=3)
            self.display_image()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageProcessingApp()
    window.show()
    sys.exit(app.exec_())