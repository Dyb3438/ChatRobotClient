from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, QEvent, QObject, QTimer, pyqtSignal
import sys
try:
    from .AutoTextEditBox import Editor
except:
    from AutoTextEditBox import Editor

class ChatPiece(QtWidgets.QWidget):
    MouseLClick = pyqtSignal()
    RightIconLClick = pyqtSignal()

    def __init__(self, 
                 icon,
                 string,
                 type=1,
                 icon_size=30,
                 font_size=16,
                 font_family="Courier New",
                ):
        super().__init__()

        self.icon:str = icon
        self.string:str = string
        self.type:int = type
        self.icon_size:int = icon_size
        self.font_size:int = font_size
        self.font_family:str = font_family

        self.setAttribute(Qt.WA_TranslucentBackground)
        bodyLayout = self.createBody()
        self.setLayout(bodyLayout)
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)

        self.shortTimer = QTimer()
        self.shortTimer.setInterval(20)
        self.shortTimer.timeout.connect(self.mouseLClick)
        self.installEventFilter(self)
        return
    
    def createBody(self):
        bodyLayout = QtWidgets.QHBoxLayout()

        self.icon = self.createIcon()
        bodyLayout.addWidget(self.icon)

        self.text = self.createText()
        bodyLayout.addWidget(self.text)

        bodyLayout.addSpacerItem(QtWidgets.QSpacerItem(0, 0, hPolicy=QtWidgets.QSizePolicy.Policy.MinimumExpanding))

        bodyLayout.setSpacing(5)
        bodyLayout.setContentsMargins(0, 0, 0, 0)
        bodyLayout.setStretch(1, 10)
        return bodyLayout
    
    def createIcon(self):
        icon_space = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        icon = QtWidgets.QLabel()
        icon.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        icon.setFixedSize(self.icon_size, self.icon_size)
        icon.setPixmap(QtGui.QPixmap(self.icon))
        icon.setScaledContents(True)
        icon.setAttribute(Qt.WA_TranslucentBackground)
        layout.addWidget(icon)

        layout.addSpacerItem(QtWidgets.QSpacerItem(0, 0, vPolicy=QtWidgets.QSizePolicy.Policy.Expanding))

        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        icon_space.setLayout(layout)
        return icon_space
    
    def createText(self):
        if self.type == 1:
            font_color=(9, 17, 10)
            background_color=(89, 178, 105)
        elif self.type == 2:
            font_color=(235, 235, 235)
            background_color=(144, 84, 24)
        else:
            font_color=(171, 171, 171)
            background_color=(44, 44, 44)
        text = Editor(self.font_size, font_color, self.font_family, background_color)
        text.setText(self.string)
        return text
    
    def mouseLClick(self):
        self.shortTimer.stop()
        self.MouseLClick.emit()
        return
    
    def eventFilter(self, a0: 'QObject', a1: 'QEvent') -> bool:
        if a0 == self:
            if a1.type() == QEvent.Type.MouseButtonPress:
                self.shortTimer.start()
        return super().eventFilter(a0, a1)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    w = ChatPiece('./../icon/AI.png', 'hello world, How are you?fsjdkalfj')
    app.installEventFilter(w)
    w.show()
    sys.exit(app.exec_())