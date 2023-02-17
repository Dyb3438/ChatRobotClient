from functools import partial
import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt

from component import ScrollList, ChatItem
from window import IntroductionPage, ChatPage


class AppView(QtWidgets.QWidget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setWindowTitle('ChatGPT Client')
        self.font_family = "SimSun"
        self.configuration = self.loadConfiguraton()

        # self.resize(1200, 800)
        self.center()
        self.setMinimumHeight(500)
        # self.setFixedSize(self.width(), self.height())
        # self.setWindowFlags(QtCore.Qt.WindowType.WindowMinMaxButtonsHint)
        
        self.body = self.createBody()
        self.setLayout(self.body)

        self.active_chat(self.home_item)
        self.chat_id = 1
        self.chats = {}
        return
    
    def center(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        # size = self.geometry()
        self.resize(screen.width(), screen.height() - 150)
        self.move(0, 0)
        return

    def loadConfiguraton(self):
        # load proxy sites
        from config.ChatGPT_proxy_sites import proxy_sites
        return {
            'proxy_sites': proxy_sites
            }

    def createBody(self):
        bodyLayout = QtWidgets.QHBoxLayout()

        self.leftBody = self.createChatList()
        bodyLayout.addWidget(self.leftBody)

        self.rightContentBody = self.createRightContentBody()
        bodyLayout.addWidget(self.rightContentBody)

        introductionPage = IntroductionPage.IntroductionPage()
        introductionPage.startChatEvent.connect(self.addNewChat)
        self.rightContentBody.addWidget(introductionPage)

        bodyLayout.setSpacing(0)
        bodyLayout.setContentsMargins(0, 0, 0, 0)
        return bodyLayout
    
    def createChatList(self):
        leftBody = QtWidgets.QWidget()
        leftBody.setStyleSheet('''
            background: rgb(32,33,35)
        ''')
        leftBody.setFixedWidth(300)
        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        leftBody.setLayout(layout)

        self.chatList = ScrollList.ScrollList(addBorder=False)
        self.chatList.widget().layout().setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.home_item = ChatItem.ChatItem(
            icon='./icon/home.png',
            string='Introduction',
            width=278,
            height=50,
            font_size=20,
            font_family=self.font_family
        )
        self.home_item.MouseLClick.connect(partial(self.active_chat, self.home_item))
        self.chatList.addWidget(self.home_item)

        self.add_item = ChatItem.ChatItem(
            icon='./icon/add.png',
            string='New Chat',
            width=278,
            height=50,
            font_size=20,
            font_family=self.font_family
        )
        self.add_item.MouseLClick.connect(self.addNewChat)
        self.chatList.addWidget(self.add_item)

        layout.addWidget(self.chatList)
        return leftBody
    
    def createAddItem(self):
        self.add_item = ChatItem.ChatItem(
            icon='./icon/add.png',
            string='New Chat',
            width=278,
            height=50,
            font_size=20,
            font_family=self.font_family
        )
        self.add_item.MouseLClick.connect(self.addNewChat)
        self.chatList.addWidget(self.add_item)
        return
        
    def addNewChat(self, question=None):
        self.rm_chat(self.add_item)
        self.add_item = None

        chat_item = ChatItem.ChatItem(
            icon='./icon/chat.png',
            string='Chat %d' % self.chat_id,
            chat_id=self.chat_id,
            width=278,
            height=50,
            font_size=20,
            right_hidden=False,
            right_icon='./icon/delete.png',
            font_family=self.font_family
        )
        chat_item.MouseLClick.connect(partial(self.active_chat, chat_item))
        chat_item.RightIconLClick.connect(partial(self.rm_chat, chat_item))
        self.chatList.addWidget(chat_item)

        self.chats[self.chat_id] = {
            'chat_item': chat_item,
            'QAs': [] if question is None else [question],
            'widget': None
        }

        chatWidget = self.createChatPage(self.chats[self.chat_id])
        
        self.chats[self.chat_id]['widget'] = chatWidget

        self.active_chat(chat_item)

        self.chat_id += 1
        self.createAddItem()
        return
    
    def active_chat(self, widget):
        for i in range(self.chatList.count()):
            if widget == self.chatList.itemAt(i).widget():
                self.chatList.itemAt(i).widget().setActive(True)
            else:
                self.chatList.itemAt(i).widget().setActive(False)
        
        if widget.string == "Introduction":
            self.rightContentBody.setCurrentIndex(0)
        else:
            self.rightContentBody.setCurrentIndex(self.rightContentBody.indexOf(self.chats[widget.chat_id]['widget']))
        return
    
    def rm_chat(self, widget):
        if widget.active:
            self.active_chat(self.home_item)
        if widget.chat_id > 0:
            self.rightContentBody.removeWidget(self.chats[widget.chat_id]['widget'])
            del self.chats[widget.chat_id]
        self.chatList.takeAt(self.chatList.indexOf(widget)).widget().deleteLater()
        return
    
    def createRightContentBody(self):
        contentBody = QtWidgets.QStackedWidget()
        
        contentBody.setStyleSheet('''
                background: rgb(52,53,65)
            ''')
        contentBody.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        return contentBody
    
    def createChatPage(self, chat_config):
        chatPage = ChatPage.ChatPage(chat_config, self.configuration['proxy_sites'], self.font_family)
        self.rightContentBody.addWidget(chatPage)
        return chatPage
    


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    w = AppView()
    app.installEventFilter(w)
    w.show()
    sys.exit(app.exec_())