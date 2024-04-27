import sys
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
import cv2

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
        self.filter_button = QPushButton("Apply Filter")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.load_button)
        layout.addWidget(self.gray_button)
        layout.addWidget(self.contrast_button)
        layout.addWidget(self.filter_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Signals
        self.load_button.clicked.connect(self.load_image)
        self.gray_button.clicked.connect(self.convert_to_grayscale)
        self.contrast_button.clicked.connect(self.adjust_contrast)
        self.filter_button.clicked.connect(self.apply_filter)

        # Initialize variables
        self.image = None

    def load_image(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open Image", "C:\\Users\\lenovo\\Desktop\\ImageProcessingApp\\images", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            self.image = cv2.imread(file_path)
            self.display_image()

    def display_image(self):
        if self.image is not None:
            height, width, channel = self.image.shape
            bytes_per_line = 3 * width
            scale_factor = 3  # Adjust this factor to increase/decrease the size
        
            # Resize the image using OpenCV
            resized_image = cv2.resize(self.image, (width * scale_factor, height * scale_factor))
        
            # Convert the resized image to a QImage
            q_img = QImage(resized_image.data, resized_image.shape[1], resized_image.shape[0], resized_image.strides[0], QImage.Format_RGB888).rgbSwapped()
            pixmap = QPixmap.fromImage(q_img)
            #scaled_pixmap = pixmap.scaled(self.image_label.size(), aspectRatioMode=Qt.KeepAspectRatio)
            self.image_label.setPixmap(pixmap)

    def convert_to_grayscale(self):
        if self.image is not None:
            gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            self.image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
            self.display_image()

    def adjust_contrast(self):
        if self.image is not None:
            alpha = 1.5  # Contrast control (1.0-3.0)
            beta = 50    # Brightness control (0-100)
            self.image = cv2.convertScaleAbs(self.image, alpha=alpha, beta=beta)
            self.display_image()

    def apply_filter(self):
        if self.image is not None:
            kernel = np.ones((5, 5), np.float32) / 25
            self.image = cv2.filter2D(self.image, -1, kernel)
            self.display_image()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageProcessingApp()
    window.show()
    sys.exit(app.exec_())