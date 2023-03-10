from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtCore import Qt
import sys
from component import ScrollList, Icon, ChatPiece
from thread import SendMessage
import os

class ChatPage(QtWidgets.QWidget):
    
    def __init__(self, config, proxy_sites, font_family="Courier New"):
        super().__init__()
        self.setWindowTitle('ChatPage')
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.width_ = self.width()
        self.height_ = self.height()

        self.config = config
        self.proxy_sites = proxy_sites
        self.font_family = font_family

        self.prepareForPaint()
        
        self.body = self.createBody()
        self.setLayout(self.body)

        if len(self.config['QAs']) == 1:
            self.sendLE.setText(self.config['QAs'][0])
            self.config['QAs'] = []
            self.sendBtnEvent()
        return
    
    def __setattr__(self, __name: str, __value) -> None:
        if __name == 'width_' or __name == 'height_':
            if __name not in self.__dict__ or __value != self.__dict__[__name]:
                self.__dict__[__name] = __value
                self.updatePosition()
        return super().__setattr__(__name, __value)
    
    def updatePosition(self):
        if 'sendBox' in self.__dict__:
            self.sendBox.setFixedWidth(self.width())
            self.sendBox.move(0, self.height() - self.sendBox.height() - 20)
        return
    
    def prepareForPaint(self):
        self.room_title = self.config['chat_item'].string
        self.font_ = QtGui.QFont(self.font_family, 50, 500)
        fm = QtGui.QFontMetrics(self.font_)
        rect = fm.tightBoundingRect(self.room_title)
        self.font_rect = rect
        return
    
    def createBody(self):
        bodyLayout = QtWidgets.QVBoxLayout()

        self.chatSpace = self.createChatSpace()
        bodyLayout.addWidget(self.chatSpace)

        bodyLayout.addSpacing(60)
        bodyLayout.setSpacing(0)
        bodyLayout.setContentsMargins(0, 0, 0, 0)

        self.sendBox = self.createSendBox()
        
        return bodyLayout
    
    def createChatSpace(self):
        chatSpace = ScrollList.ScrollList(addBorder=False)
        chatSpace.widget().layout().setSpacing(15)

        return chatSpace
    
    def createSendBox(self):
        box = QtWidgets.QWidget(self)
        box.setFixedHeight(40)
        layout = QtWidgets.QHBoxLayout()
        layout.addSpacerItem(QtWidgets.QSpacerItem(0, 0, hPolicy=QtWidgets.QSizePolicy.Policy.Expanding))
        
        self.sendLE = QtWidgets.QLineEdit(self.chatSpace)
        self.sendLE.setFixedWidth(800)
        self.sendLE.setFixedHeight(40)
        self.sendLE.setStyleSheet("color: white; background: rgb(55, 65, 81); padding: 5px;")
        self.sendLE.setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, 0)
        self.sendLE.setPlaceholderText("Send messages to AI")
        self.sendLE.setFont(QtGui.QFont(self.font_family, 16))
        self.sendLE.returnPressed.connect(self.sendBtnEvent)
        layout.addWidget(self.sendLE)
        
        icon = Icon.Icon(os.path.join(os.path.dirname(__file__), "../icon/send.png"), 30, 30)
        icon.MouseLClick.connect(self.sendBtnEvent)
        layout.addWidget(icon)

        layout.addSpacerItem(QtWidgets.QSpacerItem(0, 0, hPolicy=QtWidgets.QSizePolicy.Policy.Expanding))
        
        layout.setContentsMargins(0, 0, 0, 0)

        box.setAttribute(Qt.WA_TranslucentBackground)
        box.setLayout(layout)
        return box
    
    def createChatPiece(self, content, type=1):
        if type == 0:
            icon = 'AI'
        elif type == 1:
            icon = 'speak'
        else:
            icon = 'no_server'
        icon = os.path.join(os.path.dirname(__file__), "../icon/%s.png" % icon)
        chatPiece = ChatPiece.ChatPiece(icon, content, type, font_family=self.font_family, icon_size=40, font_size=20)
        return chatPiece
    
    def sendBtnEvent(self):
        question = self.sendLE.text()
        if question == '':
            return
        self.sendLE.setEnabled(False)
        self.sendLE.clear()
        self.sendRequest(question)
        chatPiece = self.createChatPiece(question)
        self.chatSpace.addWidget(chatPiece)
        return
    
    def sendRequest(self, question):
        additional_text = ''
        for i in range(0, len(self.config['QAs']), 2):
            human = self.config['QAs'][i]
            AI = self.config['QAs'][i+1]
            additional_text += '{human}\nAI:{ai}\nHuman:'.format(human=human, ai=AI)
        self.t = SendMessage.SendMessage(self.proxy_sites, additional_text + question)
        self.t.ret.connect(self.receiveAnswer)
        self.config['QAs'].append(question)
        self.t.start()
        return
    
    def receiveAnswer(self, ret):
        if ret['result'] is None:
            chatPiece = self.createChatPiece('???????????????!', type=2)
            self.config['QAs'] = self.config['QAs'][:-1]
        elif 'error' not in ret['result']:
            chatPiece = self.createChatPiece(ret['result']['choices'][0]['text'], type=2)
            self.config['QAs'] = self.config['QAs'][:-1]
        else:
            answer = ret['result']['choices'][0]['text']
            self.config['QAs'].append(answer)
            answer = answer.strip('\n')
            chatPiece = self.createChatPiece(answer, type=0)
        self.chatSpace.addWidget(chatPiece)

        self.sendLE.setEnabled(True)
        self.sendLE.setFocus()
        return
    
    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        p = QtGui.QPainter(self)
        p.setPen(QtGui.QColor.fromRgb(107, 114, 128))
        p.setFont(self.font_)

        p.drawText((self.width() - self.font_rect.width()) / 2 - self.font_rect.x(), (self.height() - self.font_rect.height()) / 2 - self.font_rect.y(), self.room_title)
        if self.width() != self.width_:
            self.width_ = self.width()
        if self.height() != self.height_:
            self.height_ = self.height()
        return super().paintEvent(a0)
    



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    w = ChatPage()
    app.installEventFilter(w)
    w.show()
    sys.exit(app.exec_())