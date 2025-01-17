
## `stacked-widget`
![StackedWidget_Sample](images/screenshot.png)

**`StackedWidget`** is a custom PyQt/PySide widget that enables overlaying one widget on top of another with flexible alignment and margin configurations. This is particularly useful for GUI designs where layered widgets (e.g., buttons, labels, or overlays) are needed.

### Features
- Overlay a top widget on a bottom widget with alignment options (`Left`, `Right`, `Top`, `Bottom`, `Center`, etc.).
- Supports dynamic resizing and alignment adjustments on window resize.
- Easy to integrate with PyQt or PySide applications.
- Fully customizable margins and alignment settings.

---

### Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Examples](#examples)
4. [API Reference](#api-reference)
5. [Use Cases](#use-cases)
6. [Contributing](#contributing)
7. [License](#license)

---

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/bornalgo/stacked-widget.git
   cd StackedWidget
   ```
2. Install the required dependencies:
   ```bash
   pip install PySide2  # Or PySide6/PyQt6/PyQt5/PyQt4/PySide based on your preference
   ```
3. Install the package:
   ```bash
   python setup.py install
   ```


---

### Usage
```python
from PySide2.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QCheckBox, QWidget
from balQt.stacked_widget import StackedWidget

# Create the application
app = QApplication([])

# Main window setup
window = QMainWindow()
window.setWindowTitle("Stacked Widget Example")

# Create bottom and top widgets
button = QPushButton("Click Me!")
button.setEnabled(False)
checkbox = QCheckBox("Enable Button")

# Connect checkbox state change to toggle button enabled state
checkbox.stateChanged.connect(lambda: button.setEnabled(checkbox.isChecked()))

# Create a StackedWidget
stacked_widget = StackedWidget(button, checkbox)

# Setup layout
layout = QVBoxLayout()
layout.addWidget(stacked_widget)

container = QWidget()
container.setLayout(layout)
window.setCentralWidget(container)

# Show window
window.show()

# Run application
app.exec_()
```

---

### Examples
#### Example 1: Overlay a Checkbox on a Button
Overlay a checkbox on a button, where the checkbox controls the button's enabled state.

```python
def toggle_button_state(checkbox, button):
    button.setEnabled(checkbox.isChecked())

checkbox.stateChanged.connect(lambda: toggle_button_state(checkbox, button))
```

#### Example 2: Display a Loading Overlay
Use `StackedWidget` to overlay a "loading spinner" or a progress bar on top of an underlying content widget.

---

### API Reference
#### `class StackedWidget(QWidget)`
A custom widget for overlaying widgets.

**Parameters:**
- `bottom_widget (QWidget)`: Widget at the base.
- `top_widget (QWidget)`: Widget overlaid on the bottom widget.
- `parent (QWidget, optional)`: Parent widget. Defaults to `None`.
- `margin (int, optional)`: Space between the widgets. Defaults to `0`.
- `alignment (Qt.Alignment, optional)`: Alignment of the `top_widget` (e.g., `Qt.AlignRight`). Defaults to `Qt.AlignRight`.

**Methods:**
- `__init__(bottom_widget, top_widget, parent=None, margin=0, alignment=Qt.AlignRight)`: Initializes the `StackedWidget`.
- `resizeEvent(event)`: Dynamically adjusts widget alignment and size upon resizing.

---

### Use Cases
1. **Interactive User Interfaces:**
   - Overlay a checkbox or a label on a button or image.
2. **Loading Screens:**
   - Place a spinner or progress indicator on top of a widget.
3. **Advanced Layouts:**
   - Use layered designs for applications like form builders or dashboards.
4. **Dynamic States:**
   - Display dynamic states (e.g., "Processing", "Completed") over widgets.

---

### Contributing
Contributions are welcome! If you'd like to add features, fix bugs, or suggest improvements:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -m "Add new feature"`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Open a pull request.

---

### License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

### Keywords
- `PyQt`
- `PySide`
- `StackedWidget`
- `Qt Custom Widgets`
- `Overlays`
- `GUI Development`
- `Python GUI`

---

### Repository Structure
```
StackedWidget/
├── balQt
│   ├── __init__.py
│   └── stacked_widget.py
├── images
│   └── screenshot.png
├── .gitignore          # Ignore artifacts
├── example.py          # Usage example
├── LICENSE             # License file
├── README.md           # Documentation
└── setup.py            # Setup file
```