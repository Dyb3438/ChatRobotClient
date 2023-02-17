from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Editor(QTextEdit):
    doubleClicked = pyqtSignal(QTextEdit)
    def __init__(self, font_size, font_color=(9, 17, 10), font_family="Courier New", background_color=(89, 178, 105)):
        super().__init__()

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMinimumWidth(0)

        self.font_size = font_size
        self.background_color = background_color

        self.width_ = self.width()
        self.height_ = self.height()

        font = QFont(font_family, self.font_size)
        self.setReadOnly(True)
        self.setFont(font)
        self.setTextColor(QColor.fromRgb(*font_color))
        self.setContentsMargins(0, 0, 0, 0)
        self.document().setDocumentMargin(10)
        
        self.textChanged.connect(self.autoResize)
        self.margins = self.contentsMargins()

        self.viewport().setAttribute(Qt.WA_TranslucentBackground)
        self.setFrameStyle(QFrame.NoFrame)

    def __setattr__(self, __name: str, __value) -> None:
        if __name == 'width_' or __name == 'height_':
            if __name not in self.__dict__ or __value != self.__dict__[__name]:
                self.__dict__[__name] = __value
                self.autoResize()
        return super().__setattr__(__name, __value)

    @pyqtSlot(QMouseEvent)
    def mouseDoubleClickEvent(self, e: QMouseEvent) -> None:
        self.doubleClicked.emit(self)
    
    def autoResize(self):
        if 'margins' in self.__dict__ and self.document().textWidth() > 0:
            self.show()
            height = int(self.document().size().height() + self.margins.top() + self.margins.bottom())
            width = int(self.document().idealWidth() + self.margins.left() + self.margins.right())
            self.setFixedWidth(width + 2)
            self.setFixedHeight(height)

    def paintEvent(self, e: QPaintEvent) -> None:
        p = QPainter(self.viewport())
        p.setPen(QColor.fromRgb(*self.background_color))
        p.setBrush(QColor.fromRgb(*self.background_color))
        p.drawRoundedRect(0, 0, self.width(), self.height(), 5, 5)
        self.width_ = self.width()
        self.height_ = self.height()
        return super().paintEvent(e)