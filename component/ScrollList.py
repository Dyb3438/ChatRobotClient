from PyQt5 import QtWidgets, QtCore
from .Widget import Widget
from PyQt5.QtCore import Qt, QEvent


class ScrollList(QtWidgets.QScrollArea):
    def __init__(self, addBorder=True, **kwargs):
        super().__init__(**kwargs)
        self.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        if addBorder:
            listWidget = Widget()
        else:
            listWidget = QtWidgets.QWidget()
        self.listVLayout = self.createLayout()
        listWidget.setLayout(self.listVLayout)
        listWidget.setAttribute(Qt.WA_TranslucentBackground)

        self.setWidget(listWidget)
        self.setWidgetResizable(True)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.installEventFilter(self)

        self.currentHeight = 0.
        return
    
    def createLayout(self):
        hostListVerticalLayout = QtWidgets.QVBoxLayout()
        hostListVerticalLayout.setSpacing(5)
        hostListVerticalLayout.setContentsMargins(10, 10, 10, 10)
        hostListVerticalLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        hostListVerticalLayout.addSpacerItem(QtWidgets.QSpacerItem(0, 0, vPolicy=QtWidgets.QSizePolicy.Policy.Expanding))
        return hostListVerticalLayout
    
    def addWidget(self, *args, **kwargs):
        spacer = self.listVLayout.takeAt(self.listVLayout.count() - 1)
        self.listVLayout.addWidget(*args, **kwargs)
        self.listVLayout.addItem(spacer)
        self.slideToBottom = True
        return
    
    def addItem(self, *args, **kwargs):
        spacer = self.listVLayout.takeAt(self.listVLayout.count() - 1)
        self.listVLayout.addItem(*args, **kwargs)
        self.listVLayout.addItem(spacer)
        return
    
    def addLayout(self, *args, **kwargs):
        spacer = self.listVLayout.takeAt(self.listVLayout.count() - 1)
        self.listVLayout.addLayout(*args, **kwargs)
        self.listVLayout.addItem(spacer)
        return
    
    def addSpacing(self, *args, **kwargs):
        spacer = self.listVLayout.takeAt(self.listVLayout.count() - 1)
        self.listVLayout.addSpacing(*args, **kwargs)
        self.listVLayout.addItem(spacer)
        return
    
    def count(self):
        return self.listVLayout.count() - 1
    
    def takeAt(self, index):
        if index >= self.count():
            return None
        return self.listVLayout.takeAt(index)
    
    def itemAt(self, index):
        if index >= self.count():
            return None
        return self.listVLayout.itemAt(index)
    
    def indexOf(self, a0):
        return self.listVLayout.indexOf(a0)
    
    def removeAll(self):
        for i in reversed(range(self.count())):
            self.itemAt(i).widget().deleteLater()
        self.update()
        return
    
    def eventFilter(self, a0: QtCore.QObject, a1: QtCore.QEvent) -> bool:
        if (a1.type() == QEvent.Resize):
            if self.widget().height() > self.currentHeight:
                self.verticalScrollBar().setMaximum(self.widget().height() - self.height())
                self.verticalScrollBar().setSliderPosition(self.widget().height() - self.height())
            self.currentHeight = self.widget().height()
        return super().eventFilter(a0, a1)