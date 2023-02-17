from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtCore import Qt, pyqtSignal
import sys
from component import TextBox
from functools import partial

class IntroductionPage(QtWidgets.QWidget):
    startChatEvent = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.setWindowTitle('IntroductionPage')
        
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        self.body = self.createBody()
        self.setLayout(self.body)
        return
    
    def createBody(self):
        bodyLayout = QtWidgets.QVBoxLayout()

        bodyLayout.addSpacerItem(QtWidgets.QSpacerItem(0, 0, vPolicy=QtWidgets.QSizePolicy.Policy.Expanding))

        self.title = self.createTitle()
        bodyLayout.addWidget(self.title)
        
        bodyLayout.addSpacing(56)

        self.contentBody = self.createContentBody()
        bodyLayout.addWidget(self.contentBody)

        bodyLayout.addSpacerItem(QtWidgets.QSpacerItem(0, 0, vPolicy=QtWidgets.QSizePolicy.Policy.Expanding))

        bodyLayout.setSpacing(0)
        bodyLayout.setContentsMargins(0, 0, 0, 0)
        return bodyLayout

    def createTitle(self):
        titleLabel = QtWidgets.QLabel('ChatGPT')
        titleLabel.setStyleSheet('''
            color:white;
            font-size: 35px;
            font-weight: 500
        ''')
        titleLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        titleLabel.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        return titleLabel

    def createContentBody(self):
        contentBody = QtWidgets.QWidget()
        contentLayout = QtWidgets.QHBoxLayout()

        list_width = 320
        contentLayout.addWidget(self.createExampleList(list_width=list_width))
        contentLayout.addWidget(self.createCapList(list_width=list_width))
        contentLayout.addWidget(self.createLimitList(list_width=list_width))

        contentLayout.setSpacing(10)
        contentLayout.setContentsMargins(10, 10, 10, 10)
        contentBody.setLayout(contentLayout)
        return contentBody
    
    def createExampleList(self, list_width=250):

        exampleList = QtWidgets.QWidget()
        exampleList.setMaximumWidth(list_width)
        exampleLayout = QtWidgets.QVBoxLayout()

        # ICON
        exampleICON_widget = QtWidgets.QWidget()
        exampleICON_layout = QtWidgets.QHBoxLayout()
        exampleICON_layout.addSpacerItem(QtWidgets.QSpacerItem(0, 0, hPolicy=QtWidgets.QSizePolicy.Policy.Expanding))
        exampleICON = QtWidgets.QLabel()
        exampleICON.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        exampleICON.setFixedSize(30, 30)
        exampleICON.setPixmap(QtGui.QPixmap("./icon/sun.png"))
        exampleICON.setScaledContents(True)
        exampleICON_layout.addWidget(exampleICON)
        exampleICON_layout.addSpacerItem(QtWidgets.QSpacerItem(0, 0, hPolicy=QtWidgets.QSizePolicy.Policy.Expanding))
        exampleICON_layout.setSpacing(0)
        exampleICON_layout.setContentsMargins(0, 0, 0, 0)
        exampleICON_widget.setLayout(exampleICON_layout)
        exampleLayout.addWidget(exampleICON_widget)

        # spacing
        exampleLayout.addSpacing(15)

        # Head
        exampleHead = QtWidgets.QLabel("Examples")
        exampleHead.setStyleSheet('''
            color:white;
            font-size: 24px;
        ''')
        exampleHead.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        exampleLayout.addWidget(exampleHead)

        # spacing
        exampleLayout.addSpacing(15)

        # patches
        example_patch_1 = TextBox.TextBox(
            "Explain quantum computing in simple terms →",
            minWidth=16,
            minHeight=16,
            maxWidth=list_width,
            padding=10,
            border_radius=10,
            background_color=(127, 127, 127),
            font_color=(243, 244, 246),
            hover_color=(17, 24, 39),
            available_hover_action=True,
            font_size=20,
            alignment="center"
        )
        example_patch_1.MouseLClick.connect(partial(self.startChat, 'Explain quantum computing in simple terms'))

        example_patch_2 = TextBox.TextBox(
            "Got any creative ideas for a 10 year old’s birthday? →",
            minWidth=16,
            minHeight=16,
            maxWidth=list_width,
            padding=10,
            border_radius=10,
            background_color=(127, 127, 127),
            font_color=(243, 244, 246),
            hover_color=(17, 24, 39),
            available_hover_action=True,
            font_size=20,
            alignment="center"
        )
        example_patch_2.MouseLClick.connect(partial(self.startChat, 'Got any creative ideas for a 10 year old’s birthday?'))

        example_patch_3 = TextBox.TextBox(
            "How do I make an HTTP request in Javascript? →",
            minWidth=16,
            minHeight=16,
            maxWidth=list_width,
            padding=10,
            border_radius=10,
            background_color=(127, 127, 127),
            font_color=(243, 244, 246),
            hover_color=(17, 24, 39),
            available_hover_action=True,
            font_size=20,
            alignment="center"
        )
        example_patch_3.MouseLClick.connect(partial(self.startChat, 'How do I make an HTTP request in Javascript?'))

        exampleLayout.addWidget(example_patch_1)
        exampleLayout.addSpacing(10)
        exampleLayout.addWidget(example_patch_2)
        exampleLayout.addSpacing(10)
        exampleLayout.addWidget(example_patch_3)

        exampleLayout.setSpacing(0)
        exampleLayout.setContentsMargins(0, 0, 0, 0)
        exampleLayout.addSpacerItem(QtWidgets.QSpacerItem(0, 0, vPolicy=QtWidgets.QSizePolicy.Policy.Expanding))
        exampleList.setLayout(exampleLayout)
        return exampleList
    
    def startChat(self, question):
        self.startChatEvent.emit(question)
        return
    
    def createCapList(self, list_width=250):
        capList = QtWidgets.QWidget()
        capList.setMaximumWidth(list_width)

        capLayout = QtWidgets.QVBoxLayout()

        # ICON
        capICON_widget = QtWidgets.QWidget()
        capICON_layout = QtWidgets.QHBoxLayout()
        capICON_layout.addSpacerItem(QtWidgets.QSpacerItem(0, 0, hPolicy=QtWidgets.QSizePolicy.Policy.Expanding))
        capICON = QtWidgets.QLabel()
        capICON.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        capICON.setFixedSize(30, 30)
        capICON.setPixmap(QtGui.QPixmap("./icon/light.png"))
        capICON.setScaledContents(True)
        capICON_layout.addWidget(capICON)
        capICON_layout.addSpacerItem(QtWidgets.QSpacerItem(0, 0, hPolicy=QtWidgets.QSizePolicy.Policy.Expanding))
        capICON_layout.setSpacing(0)
        capICON_layout.setContentsMargins(0, 0, 0, 0)
        capICON_widget.setLayout(capICON_layout)
        capLayout.addWidget(capICON_widget)

        # spacing
        capLayout.addSpacing(15)

        # Head
        capHead = QtWidgets.QLabel("Capabilities")
        capHead.setStyleSheet('''
            color:white;
            font-size: 24px;
        ''')
        capHead.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        capLayout.addWidget(capHead)

        # spacing
        capLayout.addSpacing(15)

        # patches
        cap_patch_1 = TextBox.TextBox(
            "Remembers what user said earlier in the conversation",
            minWidth=16,
            minHeight=16,
            maxWidth=list_width,
            padding=10,
            border_radius=10,
            background_color=(127, 127, 127),
            font_color=(243, 244, 246),
            available_hover_action=False,
            font_size=20,
            alignment="center"
        )
        cap_patch_2 = TextBox.TextBox(
            "Allows user to provide follow-up corrections",
            minWidth=16,
            minHeight=16,
            maxWidth=list_width,
            padding=10,
            border_radius=10,
            background_color=(127, 127, 127),
            font_color=(243, 244, 246),
            available_hover_action=False,
            font_size=20,
            alignment="center"
        )
        cap_patch_3 = TextBox.TextBox(
            "Trained to decline inappropriate requests",
            minWidth=16,
            minHeight=16,
            maxWidth=list_width,
            padding=10,
            border_radius=10,
            background_color=(127, 127, 127),
            font_color=(243, 244, 246),
            available_hover_action=False,
            font_size=20,
            alignment="center"
        )

        capLayout.addWidget(cap_patch_1)
        capLayout.addSpacing(10)
        capLayout.addWidget(cap_patch_2)
        capLayout.addSpacing(10)
        capLayout.addWidget(cap_patch_3)

        capLayout.setSpacing(0)
        capLayout.setContentsMargins(0, 0, 0, 0)
        capLayout.addSpacerItem(QtWidgets.QSpacerItem(0, 0, vPolicy=QtWidgets.QSizePolicy.Policy.Expanding))
        capList.setLayout(capLayout)
        return capList


    def createLimitList(self, list_width=250):
        limitList = QtWidgets.QWidget()
        limitList.setMaximumWidth(list_width)

        limitLayout = QtWidgets.QVBoxLayout()

        # ICON
        limitICON_widget = QtWidgets.QWidget()
        limitICON_layout = QtWidgets.QHBoxLayout()
        limitICON_layout.addSpacerItem(QtWidgets.QSpacerItem(0, 0, hPolicy=QtWidgets.QSizePolicy.Policy.Expanding))
        limitICON = QtWidgets.QLabel()
        limitICON.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        limitICON.setFixedSize(30, 30)
        limitICON.setPixmap(QtGui.QPixmap("./icon/limit.png"))
        limitICON.setScaledContents(True)
        limitICON_layout.addWidget(limitICON)
        limitICON_layout.addSpacerItem(QtWidgets.QSpacerItem(0, 0, hPolicy=QtWidgets.QSizePolicy.Policy.Expanding))
        limitICON_layout.setSpacing(0)
        limitICON_layout.setContentsMargins(0, 0, 0, 0)
        limitICON_widget.setLayout(limitICON_layout)
        limitLayout.addWidget(limitICON_widget)

        # spacing
        limitLayout.addSpacing(15)

        # Head
        limitHead = QtWidgets.QLabel("Limitations")
        limitHead.setStyleSheet('''
            color:white;
            font-size: 24px;
        ''')
        limitHead.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        limitLayout.addWidget(limitHead)

        # spacing
        limitLayout.addSpacing(15)

        # patches
        limit_patch_1 = TextBox.TextBox(
            "May occasionally generate incorrect information",
            minWidth=16,
            minHeight=16,
            maxWidth=list_width,
            padding=10,
            border_radius=10,
            background_color=(127, 127, 127),
            font_color=(243, 244, 246),
            available_hover_action=False,
            font_size=20,
            alignment="center"
        )
        limit_patch_2 = TextBox.TextBox(
            "May occasionally produce harmful instructions or biased content",
            minWidth=16,
            minHeight=16,
            maxWidth=list_width,
            padding=10,
            border_radius=10,
            background_color=(127, 127, 127),
            font_color=(243, 244, 246),
            available_hover_action=False,
            font_size=20,
            alignment="center"
        )
        limit_patch_3 = TextBox.TextBox(
            "Limited knowledge of world and events after 2021",
            minWidth=16,
            minHeight=16,
            maxWidth=list_width,
            padding=10,
            border_radius=10,
            background_color=(127, 127, 127),
            font_color=(243, 244, 246),
            available_hover_action=False,
            font_size=20,
            alignment="center"
        )

        limitLayout.addWidget(limit_patch_1)
        limitLayout.addSpacing(10)
        limitLayout.addWidget(limit_patch_2)
        limitLayout.addSpacing(10)
        limitLayout.addWidget(limit_patch_3)

        limitLayout.setSpacing(0)
        limitLayout.setContentsMargins(0, 0, 0, 0)
        limitLayout.addSpacerItem(QtWidgets.QSpacerItem(0, 0, vPolicy=QtWidgets.QSizePolicy.Policy.Expanding))
        limitList.setLayout(limitLayout)
        return limitList






if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    w = IntroductionPage()
    app.installEventFilter(w)
    w.show()
    sys.exit(app.exec_())