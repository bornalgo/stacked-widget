import os.path
from balQt.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QCheckBox, QWidget
from balQt.QtGui import QPainter, QImage
from balQt.QtCore import QSize, QPoint
from balQt.stacked_widget import StackedWidget


def toggle_button_state(checkbox, button):
    """Enable or disable the button based on the checkbox state."""
    button.setEnabled(checkbox.isChecked())

def capture_screenshot(window):
    if os.path.exists("images\\screenshot.png"):
        return
    # Define a higher resolution (scaling factor)
    scale_factor = 2  # Change to a higher value for better quality
    original_size = window.size()
    high_quality_size = QSize(original_size.width() * scale_factor, original_size.height() * scale_factor)

    # Render to a high-resolution QImage
    image = QImage(high_quality_size, QImage.Format_ARGB32)
    image.setDevicePixelRatio(scale_factor)  # Account for scale factor
    painter = QPainter(image)
    window.render(painter, QPoint(0, 0))
    painter.end()

    # Save the image
    image.save("images\\screenshot.png", "PNG")
    print("Screenshot saved as 'images\\screenshot.png'")

def main():
    # Create the application
    app = QApplication([])

    # Main window setup
    window = QMainWindow()
    window.setWindowTitle("Stacked Widget Example")

    # Create a bottom button and a top checkbox
    button = QPushButton("Click Me!")
    button.setEnabled(False)
    checkbox = QCheckBox("Enable Button")

    # Connect checkbox state change to toggle button enabled state
    checkbox.stateChanged.connect(lambda: toggle_button_state(checkbox, button))

    button.clicked.connect(lambda: capture_screenshot(window))

    # Create a StackedWidget instance
    stacked_widget = StackedWidget(button, checkbox)

    # Main layout setup
    layout = QVBoxLayout()
    layout.addWidget(stacked_widget)

    container = QWidget()
    container.setLayout(layout)

    window.setCentralWidget(container)
    window.show()

    # Start the application
    app.exec_()


if __name__ == "__main__":
    main()