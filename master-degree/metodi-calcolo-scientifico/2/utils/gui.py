import numpy as np
from PIL import Image, ImageQt
from utils.dct2 import lib_dct2
from utils.idct2 import lib_idct2
from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QSpinBox, QMessageBox, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt, QRectF
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

Image.MAX_IMAGE_PIXELS = None

class ZoomableGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScene(QGraphicsScene(self))
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

    def wheelEvent(self, event):
        factor = 1.2
        if event.angleDelta().y() > 0:
            self.scale(factor, factor)
        else:
            self.scale(1 / factor, 1 / factor)


class ImageCompressionDCT(QWidget):
    def __init__(self):
        """
        Initialize the GUI application.
        """
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Set up the user interface.
        """
        self.setWindowTitle('Compressione immagini tramite DCT')
        self.setFixedSize(800, 600)

        layout = QVBoxLayout()  # Main layout

        # Label to display the image size
        self.img_size_label = QLabel("Dimensioni immagine")
        self.img_size_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.img_size_label)

        image_layout = QHBoxLayout()  # Layout for original and processed images

        # Zoomable view for the original image
        self.original_image_view = ZoomableGraphicsView()
        self.original_image_view.setFixedSize(380, 380)
        image_layout.addWidget(self.original_image_view)

        # Zoomable view for the processed image
        self.processed_image_view = ZoomableGraphicsView()
        self.processed_image_view.setFixedSize(380, 380)
        image_layout.addWidget(self.processed_image_view)

        layout.addLayout(image_layout)

        # Button to open an image file
        self.open_button = QPushButton('Apri immagine')
        self.open_button.clicked.connect(self.open_image)
        layout.addWidget(self.open_button)

        f_layout = QHBoxLayout()  # Layout for F parameter
        self.f_label = QLabel('Dimensione macro-blocchi (F):')
        self.f_spinbox = QSpinBox()
        self.f_spinbox.setRange(1, 2147483647)
        self.f_spinbox.valueChanged.connect(self.update_d_spinbox_range)
        f_layout.addWidget(self.f_label)
        f_layout.addWidget(self.f_spinbox)
        layout.addLayout(f_layout)

        d_layout = QHBoxLayout()  # Layout for d parameter
        self.d_label = QLabel('Soglia taglio frequenze (d):')
        self.d_spinbox = QSpinBox()
        self.d_spinbox.setRange(0, 0)
        d_layout.addWidget(self.d_label)
        d_layout.addWidget(self.d_spinbox)
        layout.addLayout(d_layout)

        # Button to process the image
        self.process_button = QPushButton('Esegui')
        self.process_button.clicked.connect(self.process_image)
        layout.addWidget(self.process_button)

        self.setLayout(layout)

    def update_d_spinbox_range(self):
        """
        Update the range of the d_spinbox based on the current value of f_spinbox.
        """
        F = self.f_spinbox.value()
        self.d_spinbox.setRange(0, np.clip(2 * F - 2, 0, 2147483647))  # Ensure it doesn't overflow

    def open_image(self):
        """
        Open an image file and display it in the original_image_view.
        """
        options = QFileDialog.Option.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Apri immagine BMP", "", "BMP Files (*.bmp)", options=options)
        if file_name:
            self.image = Image.open(file_name).convert('L')  # Convert to grayscale
            if self.image is None:
                return QMessageBox.critical(self, "Errore", "Impossibile aprire l'immagine.")

            self.display_image(self.image, self.original_image_view)
            self.img_size_label.setText(f"{self.image.width}x{self.image.height}")
            self.f_spinbox.setRange(1, min(self.image.width, self.image.height))  # Ensure the F parameter is not too big

    def display_image(self, image, view):
        """
        Display an image in the specified QGraphicsView.

        Parameters:
        image (PIL.Image): The image to display.
        view (QGraphicsView): The view to display the image in.
        """
        qimage = ImageQt.ImageQt(image)  # Convert to QImage
        pixmap = QPixmap.fromImage(qimage)
        scene = view.scene()
        scene.clear()
        scene.addItem(QGraphicsPixmapItem(pixmap))
        view.setScene(scene)
        view.fitInView(QRectF(scene.itemsBoundingRect()), Qt.AspectRatioMode.KeepAspectRatio)

    def process_image(self):
        """
        Process the image using DCT, apply frequency cut-off, and display the result.

        This method applies the following steps:
        1. Divides the image into F x F blocks.
        2. Applies 2D DCT to each block.
        3. Eliminates frequencies based on the threshold d.
        4. Applies inverse 2D DCT to reconstruct the block.
        5. Reassembles the processed blocks into the full image.
        """
        if not (hasattr(self, 'image')) or self.image is None:
            return QMessageBox.critical(self, "Errore", "Apri un'immagine prima di eseguire.")

        F = self.f_spinbox.value()
        d = self.d_spinbox.value()
        image_array = np.array(self.image)
        height, width = image_array.shape

        # Crop the image, to avoid black pixels, if width mod F is not 0 or height mod F is not 0
        width = width - (width % F)
        height = height - (height % F)

        processed_array = np.zeros((height, width)).astype(np.uint8)
        error_array = np.zeros((height, width))

        try:
            # If d == 0, all frequencies must be eliminated, so all zeros must be kept
            if d > 0:
                for i in range(0, height, F):
                    for j in range(0, width, F):
                        # Extract the block
                        block = image_array[i:i + F, j:j + F]
                        # Apply 2D DCT
                        c = lib_dct2(block)
                        # Create a mask to zero out high frequencies
                        mask = np.add.outer(np.arange(F), np.arange(F)) >= d
                        c[mask] = 0
                        # Apply inverse 2D DCT
                        ff = lib_idct2(c)
                        # Clip values to be in the range [0, 255] and place the processed block back
                        processed_array[i:i + F, j:j + F] = np.clip(np.round(ff), 0, 255)
                        # Calculate the error introduced by the compression
                        error_array[i:i + F, j:j + F] = np.abs(block - processed_array[i:i + F, j:j + F])
        except Exception as e:
            return QMessageBox.critical(self, "Errore", f"Errore durante l'elaborazione dell'immagine: {e}")

        self.processed_image = Image.fromarray(processed_array)
        self.display_image(self.processed_image, self.processed_image_view)

        # Create and save the heatmap
        plt.figure(figsize=(10, 10))
        norm = mcolors.Normalize(vmin=0, vmax=np.max(error_array))
        plt.imshow(error_array, cmap='hot', norm=norm)
        plt.colorbar()
        heatmap_filename = 'heatmap.png'
        plt.savefig(heatmap_filename, bbox_inches='tight', pad_inches=0)
        plt.close()
