from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QRect

class Widget(QtWidgets.QWidget):
    def __init__(self, borderColor=Qt.GlobalColor.gray, borderRadius=5, borderSize=2, **kwargs):
        super().__init__(**kwargs)
        self.borderRadius = borderRadius
        self.borderColor = borderColor
        self.borderSize = borderSize
        self.setAttribute(Qt.WA_TranslucentBackground)
        return
        
    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        p = QtGui.QPainter(self)
        pen = QtGui.QPen(self.borderColor, self.borderSize)
        p.setPen(pen)

        pen_offset = self.borderSize // 2 

        p.drawLine(self.borderRadius + pen_offset, pen_offset, self.width() - self.borderRadius - pen_offset, pen_offset)
        p.drawLine(self.borderRadius + pen_offset, self.height() - pen_offset, self.width() - self.borderRadius - pen_offset, self.height() - pen_offset)
        p.drawLine(pen_offset, self.borderRadius + pen_offset, pen_offset, self.height() - self.borderRadius - pen_offset)
        p.drawLine(self.width() - pen_offset, self.borderRadius + pen_offset, self.width() - pen_offset, self.height() - self.borderRadius - pen_offset)

        p.drawArc(QRect(pen_offset, pen_offset, self.borderRadius * 2, self.borderRadius * 2), 90 * 16, 90 * 16)
        p.drawArc(QRect(self.width() - self.borderRadius * 2 - pen_offset, pen_offset, self.borderRadius * 2, self.borderRadius * 2), 0 * 16, 90 * 16)
        p.drawArc(QRect(pen_offset, self.height() - self.borderRadius * 2 - pen_offset, self.borderRadius * 2, self.borderRadius * 2), 180 * 16, 90 * 16)
        p.drawArc(QRect(self.width() - self.borderRadius * 2 - pen_offset, self.height() - self.borderRadius * 2 - pen_offset, self.borderRadius * 2, self.borderRadius * 2), 270 * 16, 90 * 16)

        return super().paintEvent(a0)