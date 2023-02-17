from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, QRect, QEvent, QObject, QTimer, pyqtSignal
from PyQt5.QtGui import QCursor
import sys


class ChatItem(QtWidgets.QWidget):
    MouseLClick = pyqtSignal()
    RightIconLClick = pyqtSignal()

    def __init__(self, 
                 icon,
                 string,
                 chat_id=-1,
                 width=230,
                 height=50,
                 font_size=16,
                 font_family="Courier New",
                 right_icon=None,
                 right_hidden=True
                ):
        super().__init__()
        assert width > height, "incorrect params: width must be greater or equal to height"
        assert height > 10
        self.icon:str = icon
        self.string:str = string
        self.chat_id:int = chat_id
        self.width:int = width
        self.height:int = height
        self.font_size:int = font_size
        self.font_family:str = font_family
        self.right_icon:str = right_icon
        self.right_hidden:bool = right_hidden

        self.is_hover = False
        self.above_right_icon = False
        self.active = False

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.prepareForPainting()
        self.setFixedSize(self.width + 2, self.height + 2)
        bodyLayout = self.createBody()
        self.setLayout(bodyLayout)

        self.shortTimer = QTimer()
        self.shortTimer.setInterval(20)
        self.shortTimer.timeout.connect(self.mouseLClick)
        self.installEventFilter(self)
        self.setMouseTracking(True)
        return
    
    def __setattr__(self, __name, __value):
        if __name == 'is_hover':
            if 'is_hover' not in self.__dict__ or __value != self.__dict__['is_hover']:
                self.__dict__['is_hover'] = __value
                self.update()
        elif __name == 'above_right_icon':
            if 'above_right_icon' not in self.__dict__ or __value != self.__dict__['above_right_icon']:
                self.__dict__['above_right_icon'] = __value
                if not self.right_hidden:
                    self.update()
        else:
            return super().__setattr__(__name, __value)
    
    def setActive(self, active):
        self.active = active
        self.update()

    def prepareForPainting(self):
        self.right_icon_width = int(0.8 * (self.height - 20))

        self.right_icon_rect = QRect(self.width - self.right_icon_width - 20, (self.height - self.right_icon_width) / 2, self.right_icon_width, self.right_icon_width)

        self.show_right_icon = (not self.right_hidden) and self.width >= self.height + self.right_icon_width + 10
        if self.show_right_icon:
            self.text_width = (self.width - self.height - self.right_icon_width - 10) if self.width - self.height - self.right_icon_width - 10 > 0 else 0
        else:
            self.text_width = (self.width - self.height) if self.width - self.height > 0 else 0

        font = QtGui.QFont(self.font_family, self.font_size, 500)
        fm = QtGui.QFontMetrics(font)
        show_text = ""
        words = self.string
        while len(words) > 0:
            rect = fm.tightBoundingRect(show_text + words[0])
            if rect.width() > self.text_width:
                show_text = show_text[:-2] + "..."
                break
            else:
                show_text += words[0]
                words = words[1:]
        self.text_rect = fm.tightBoundingRect(show_text)
        self.show_text = show_text
        self.font_ = font
        return
    
    def createBody(self):
        bodyLayout = QtWidgets.QHBoxLayout()

        self.icon = self.createIcon()
        bodyLayout.addWidget(self.icon)

        self.text = self.createText()
        bodyLayout.addWidget(self.text)

        bodyLayout.addSpacerItem(QtWidgets.QSpacerItem(0, 0, hPolicy=QtWidgets.QSizePolicy.Policy.Expanding))
        bodyLayout.setSpacing(5)
        bodyLayout.setContentsMargins(10, 10, 10, 10)
        return bodyLayout
    
    def createIcon(self):
        icon = QtWidgets.QLabel()
        icon.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        icon.setFixedSize(self.height - 20, self.height - 20)
        icon.setPixmap(QtGui.QPixmap(self.icon))
        icon.setScaledContents(True)
        icon.setAttribute(Qt.WA_TranslucentBackground)
        return icon
    
    def createText(self):
        text = QtWidgets.QLabel()
        text.setText(self.show_text)
        text.setFont(self.font_)
        text.setStyleSheet("color: white;")
        text.setFixedSize(self.text_width, self.height - 20)
        text.setAttribute(Qt.WA_TranslucentBackground)
        return text
    
    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

        p = QtGui.QPainter(self)
        p.setPen(QtGui.QColor.fromRgb(107, 114, 128))

        if self.active:
            p.setBrush(QtGui.QColor.fromRgb(91, 91, 91))
        elif self.is_hover and not (not self.right_hidden and self.above_right_icon):
            p.setBrush(QtGui.QColor.fromRgb(51, 51, 51))
            self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        p.drawRoundedRect(0, 0, self.width + 2, self.height + 2, 10, 10)

        if not self.right_hidden:
            if self.above_right_icon:
                p.setBrush(QtGui.QColor.fromRgb(107, 114, 128))
                p.drawRoundedRect(self.right_icon_rect.x(), self.right_icon_rect.y(), self.right_icon_rect.width(), self.right_icon_rect.height(), 5, 5)
                self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

            p.drawPixmap(self.right_icon_rect, QtGui.QPixmap(self.right_icon))
        return super().paintEvent(a0)
    
    def mouseEnter(self):
        self.is_hover = True
        return
    
    def mouseLeave(self):
        self.is_hover = False
        return

    def mouseLClick(self):
        self.shortTimer.stop()
        if self.above_right_icon:
            self.RightIconLClick.emit()
        else:
            self.MouseLClick.emit()
        return
    
    def mouseMove(self, e:QEvent):
        if not self.right_hidden:
            self.above_right_icon = self.right_icon_rect.contains(e.localPos().x(), e.localPos().y())
        return
    
    def eventFilter(self, a0: 'QObject', a1: 'QEvent') -> bool:
        if a0 == self:
            if a1.type() == QEvent.Type.Enter:
                self.mouseEnter()
                self.above_right_icon = False
            elif a1.type() == QEvent.Type.Leave:
                self.mouseLeave()
                self.above_right_icon = False
            elif a1.type() == QEvent.Type.MouseButtonPress:
                self.shortTimer.start()
                self.mouseMove(a1)
            elif a1.type() == QEvent.Type.MouseMove:
                self.mouseMove(a1)
        return super().eventFilter(a0, a1)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    w = ChatItem('./../icon/home.png', 'hello world, How are you?')
    app.installEventFilter(w)
    w.show()
    sys.exit(app.exec_())