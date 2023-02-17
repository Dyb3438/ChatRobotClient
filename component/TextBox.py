from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, QRect, QEvent, QObject, QTimer, pyqtSignal
from PyQt5.QtGui import QCursor
import sys


class TextBox(QtWidgets.QWidget):
    MouseLClick = pyqtSignal()

    def __init__(self, 
                 string, 
                 minWidth=10, 
                 minHeight=10, 
                 maxWidth=200, 
                 padding=5,
                 border_radius=5,
                 background_color=(127, 127, 127), 
                 font_color=(243, 244, 246), 
                 hover_color=(17, 24, 39),
                 available_hover_action=True,
                 font_size=16,
                 alignment="center",
                ):
        super().__init__()
        assert alignment in ['left', 'center', 'right'], "alignment: " + str(alignment) + " in TextBox is unexpected"
        assert maxWidth >= minWidth and maxWidth > 2 * padding, "incorrect params"
        self.string:str = string
        self.minWidth:int = minWidth
        self.minHeight:int = minHeight
        self.maxWidth:int = maxWidth
        self.padding:int = padding
        self.border_radius:int = border_radius
        self.background_color:tuple = background_color
        self.font_color:tuple = font_color
        
        self.hover_color:tuple = hover_color
        self.available_hover_action: bool = available_hover_action
        self.font_size:int = font_size
        self.alignment:str = alignment

        self.is_hover = False

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.prepareForPainting()
        self.setFixedSize(self.box_width + 5, self.box_height + 5)

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

    
    def prepareForPainting(self):
        line_rects = []

        font = QtGui.QFont("Courier New", self.font_size)
        fm = QtGui.QFontMetrics(font)

        # split string into words
        words = self.string.split(" ")
        lines = []
        current_line = words[0]
        words = words[1:]
        while len(words) > 0:
            rect = fm.tightBoundingRect(current_line + " " + words[0])
            if rect.width() < self.maxWidth - self.padding * 2:
                current_line += " " + words[0]
            else:
                lines.append(current_line)
                rect = fm.tightBoundingRect(current_line)
                line_rects.append(rect)
                current_line = words[0]

            words = words[1:]

        rect = fm.tightBoundingRect(current_line)
        lines.append(current_line)
        line_rects.append(rect)

        self.lines = lines
        self.line_rects = line_rects
        self.font_ = font

        # box size
        box_width = self.minWidth
        box_height = self.minHeight
        max_line_height = 0.

        if len(self.line_rects) > 1:
            box_width = self.maxWidth
        else:
            r_w = rect[0].width()

            if r_w > self.maxWidth - 2 * self.padding:
                r_w = self.maxWidth - 2 * self.padding
                box_width = self.maxWidth
            elif r_w > box_width - 2 * self.padding:
                box_width = r_w + 2 * self.padding
        
        max_line_height = self.font_size

        if len(self.line_rects) * (max_line_height * 1.5) - 0.5 * max_line_height > box_height - 2 * self.padding:
            box_height = len(self.line_rects) * (max_line_height * 1.5) - 0.5 * max_line_height + 2 * self.padding
        
        self.box_width = int(box_width)
        self.box_height = int(box_height)
        self.max_line_height = max_line_height
        return

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        p = QtGui.QPainter(self)

        if self.is_hover and self.available_hover_action:
            p.setPen(QtGui.QColor.fromRgb(*self.hover_color))
            p.setBrush(QtGui.QColor.fromRgb(*self.hover_color))
            self.font_.setUnderline(True)
            self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        else:
            p.setPen(QtGui.QColor.fromRgb(*self.background_color))
            p.setBrush(QtGui.QColor.fromRgb(*self.background_color))
            self.font_.setUnderline(False)
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))


        p.drawRoundedRect(0, 0, self.box_width, self.box_height, self.border_radius, self.border_radius)
        
        p.setPen(QtGui.QColor.fromRgb(*self.font_color))
        p.setFont(self.font_)
        for idx, (rect, line) in enumerate(zip(self.line_rects, self.lines)):
            line_start_y = self.padding + (idx + 1) * self.max_line_height * 1.5 - self.max_line_height * 0.7

            if self.alignment == 'left':
                line_start_x = self.padding - rect.x()
            elif self.alignment == 'center':
                line_start_x = (self.box_width - rect.width()) / 2
            elif self.alignment == 'right':
                line_start_x = self.box_width - rect.width() - self.padding
            p.drawText(int(line_start_x), int(line_start_y), line)

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
    w = TextBox('hello world, How are you?')
    app.installEventFilter(w)
    w.show()
    sys.exit(app.exec_())