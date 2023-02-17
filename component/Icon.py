from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, QEvent, QObject, QTimer, pyqtSignal
from PyQt5.QtGui import QCursor
import sys


class Icon(QtWidgets.QWidget):
    MouseLClick = pyqtSignal()

    def __init__(self, 
                 icon,
                 width=30,
                 height=30,
                 hover_color=(17, 24, 39),
                 available_hover_action=True,
                ):
        super().__init__()
        self.icon:str = icon
        self.width:int = width
        self.height:int = height
        
        self.hover_color:tuple = hover_color
        self.available_hover_action: bool = available_hover_action

        self.is_hover = False

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(self.width + 10, self.height + 10)

        self.shortTimer = QTimer()
        self.shortTimer.setInterval(20)
        self.shortTimer.timeout.connect(self.mouseLClick)
        if self.available_hover_action:
            self.installEventFilter(self)
        return
    
    def __setattr__(self, __name, __value):
        if __name == 'is_hover':
            if 'is_hover' not in self.__dict__ or __value != self.__dict__['is_hover']:
                self.__dict__['is_hover'] = __value
                if self.available_hover_action:
                    self.update()
        else:
            return super().__setattr__(__name, __value)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        p = QtGui.QPainter(self)

        if self.is_hover and self.available_hover_action:
            p.setPen(QtGui.QColor.fromRgb(*self.hover_color))
            p.setBrush(QtGui.QColor.fromRgb(*self.hover_color))
            self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            p.drawRoundedRect(0, 0, self.width + 10, self.height + 10, 5, 5)
        else:
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

        p.drawPixmap(5, 5, self.width, self.height, QtGui.QPixmap(self.icon))

        return super().paintEvent(a0)
    
    
    def mouseEnter(self):
        self.is_hover = True
        return
    
    def mouseLeave(self):
        self.is_hover = False
        return

    def mouseLClick(self):
        self.shortTimer.stop()
        self.MouseLClick.emit()
        return
    
    def eventFilter(self, a0: 'QObject', a1: 'QEvent') -> bool:
        if a0 == self:
            if a1.type() == QEvent.Type.Enter:
                self.mouseEnter()
            elif a1.type() == QEvent.Type.Leave:
                self.mouseLeave()
            elif a1.type() == QEvent.Type.MouseButtonPress:
                self.shortTimer.start()
        return super().eventFilter(a0, a1)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    w = Icon('hello world, How are you?')
    app.installEventFilter(w)
    w.show()
    sys.exit(app.exec_())