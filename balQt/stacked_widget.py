from typing import TypeVar
from balQt.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from balQt.QtCore import Qt

# Type variables to represent any subclass of QWidget
T = TypeVar('T', bound=QWidget)
U = TypeVar('U', bound=QWidget)

class StackedWidget(QWidget):
    """
    A custom widget that overlays one widget on top of another.

    This widget allows the positioning of a `top_widget` over a `bottom_widget` with flexible alignment options.

    Attributes:
        bottom_widget (QWidget): The underlying widget.
        top_widget (QWidget): The widget placed on top.
        margin (int): Margin between the widgets.
        alignment (Qt.Alignment): Alignment of the top widget relative to the bottom widget.
    """

    def __init__(self, bottom_widget: T, top_widget: U, parent: QWidget = None, margin: int = 0, alignment=Qt.AlignRight):
        """
        Initialize a StackedWidget.

        Args:
            bottom_widget (T): The widget at the base.
            top_widget (U): The widget overlaid on the bottom widget.
            parent (QWidget, optional): Parent widget. Defaults to None.
            margin (int, optional): Spacing between widgets. Defaults to 0.
            alignment (Qt.Alignment, optional): Alignment of the top widget. Defaults to Qt.AlignRight.
        """
        super().__init__(parent)
        self.margin = margin
        self.alignment = alignment
        self.bottom_widget = bottom_widget
        self.top_widget = top_widget

        # Main layout setup
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Container for both widgets
        container = QWidget(self)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(bottom_widget)
        layout.addWidget(container)

        # Set top widget as a child of the container
        self.top_widget.setParent(container)

        # Adjust bottom widget size based on alignment and margin
        if self.alignment in [Qt.AlignRight, Qt.AlignLeft, Qt.AlignLeading, Qt.AlignTrailing]:
            self.bottom_widget.setMinimumWidth(
                self.bottom_widget.sizeHint().width() + 2 * (self.top_widget.sizeHint().width() + self.margin)
            )
        elif self.alignment in [Qt.AlignTop, Qt.AlignBottom]:
            self.bottom_widget.setMinimumHeight(
                self.bottom_widget.sizeHint().height() + 2 * (self.top_widget.sizeHint().height() + self.margin)
            )
        else:
            if self.alignment in [Qt.AlignAbsolute, Qt.AlignJustify]:
                width = max(self.top_widget.sizeHint().width(), self.bottom_widget.sizeHint().width())
                self.top_widget.setMinimumWidth(width)
                self.bottom_widget.setMinimumWidth(width + self.margin)
                self.top_widget.setSizePolicy(QSizePolicy.MinimumExpanding, self.top_widget.sizePolicy().verticalPolicy())
            if alignment in [Qt.AlignBaseline, Qt.AlignJustify]:
                height = max(self.top_widget.sizeHint().height(), self.bottom_widget.sizeHint().height())
                self.top_widget.setMinimumHeight(height)
                self.bottom_widget.setMinimumHeight(height + self.margin)
                self.top_widget.setSizePolicy(self.top_widget.sizePolicy().horizontalPolicy(), QSizePolicy.MinimumExpanding)
            if alignment in [Qt.AlignCenter, Qt.AlignVCenter, Qt.AlignHCenter]:
                margin_horizontal = self.margin if self.alignment in [Qt.AlignCenter, Qt.AlignHCenter] else 0
                margin_vertical = self.margin if self.alignment in [Qt.AlignCenter, Qt.AlignVCenter] else 0
                self.bottom_widget.setMinimumWidth(
                    max(self.bottom_widget.sizeHint().width(), self.top_widget.sizeHint().width() + margin_horizontal)
                )
                self.bottom_widget.setMinimumHeight(
                    max(self.bottom_widget.sizeHint().height(), self.top_widget.sizeHint().height() + margin_vertical)
                )

    def showEvent(self, event):
        """Handle show event to adjust initial layout."""
        self.resizeEvent(None)
        super().showEvent(event)

    def resizeEvent(self, event):
        """Adjust the position and size of the top widget when resizing.

        Args:
            event: The resize event triggering this handler.
        """
        geometry = self.bottom_widget.geometry()
        top_width = self.top_widget.sizeHint().width()
        top_height = self.top_widget.sizeHint().height()

        if (self.alignment == Qt.AlignRight or
                (self.alignment == Qt.AlignLeading and self.bottom_widget.layoutDirection() == Qt.RightToLeft) or
                (self.alignment == Qt.AlignTrailing and self.bottom_widget.layoutDirection() == Qt.LeftToRight)):
            self.top_widget.setGeometry(
                geometry.right() - self.margin - top_width,
                geometry.top() + (geometry.height() - top_height) // 2,
                top_width,
                top_height
            )
        elif (self.alignment == Qt.AlignLeft or
                (self.alignment == Qt.AlignLeading and self.bottom_widget.layoutDirection() == Qt.LeftToRight) or
                (self.alignment == Qt.AlignTrailing and self.bottom_widget.layoutDirection() == Qt.RightToLeft)):
            self.top_widget.setGeometry(
                geometry.left() + self.margin,
                geometry.top() + (geometry.height() - top_height) // 2,
                top_width,
                top_height
            )
        elif self.alignment == Qt.AlignTop:
            self.top_widget.setGeometry(
                geometry.left() + (geometry.width() - top_width) // 2,
                geometry.top() + self.margin,
                top_width,
                top_height
            )
        elif self.alignment == Qt.AlignBottom:
            self.top_widget.setGeometry(
                geometry.left() + (geometry.width() - top_width) // 2,
                geometry.bottom() - self.margin - top_height,
                top_width,
                top_height
            )
        elif self.alignment in [Qt.AlignCenter, Qt.AlignVCenter, Qt.AlignHCenter]:
            self.top_widget.setGeometry(
                geometry.left() + (geometry.width() - top_width) // 2 + (0 if self.alignment == Qt.AlignVCenter else self.margin),
                geometry.top() + (geometry.height() - top_height) // 2 + (0 if self.alignment == Qt.AlignHCenter else self.margin),
                top_width,
                top_height
            )
        elif self.alignment == Qt.AlignJustify:
            self.top_widget.setGeometry(
                geometry.left() + self.margin // 2,
                geometry.top() + self.margin // 2,
                geometry.width() - self.margin,
                geometry.height() - self.margin
            )
        elif self.alignment == Qt.AlignAbsolute:
            self.top_widget.setGeometry(
                geometry.left() + self.margin // 2,
                geometry.top() + (geometry.height() - top_height) // 2,
                geometry.width() - self.margin,
                top_height
            )
        elif self.alignment == Qt.AlignBaseline:
            self.top_widget.setGeometry(
                geometry.left() + (geometry.width() - top_width) // 2,
                geometry.top() + self.margin // 2,
                top_width,
                geometry.height() - self.margin
            )

        if event is not None:
            super().resizeEvent(event)
