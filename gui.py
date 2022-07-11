import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QIcon, QImage
from urllib.request import urlopen
from PyQt5 import QtCore

#import urllib

class QCustomQWidget (QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(QCustomQWidget, self).__init__(parent)

        self.allBoxLayout  = QtWidgets.QHBoxLayout()



        self.textQVBoxLayout  = QtWidgets.QVBoxLayout()
        self.textUpQLabel     = QtWidgets.QLabel()
        self.textMiddleQLabel = QtWidgets.QLabel()
        self.textDownQLabel   = QtWidgets.QLabel()

        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.textQVBoxLayout.addWidget(self.textMiddleQLabel)
        self.textQVBoxLayout.addWidget(self.textDownQLabel)

        self.allQHBoxLayout  = QtWidgets.QHBoxLayout()

        self.bgQLabel         = QtWidgets.QLabel()
        #self.allQHBoxLayout.addWidget(self.bgQLabel, 0)
        self.allBoxLayout.addWidget(self.bgQLabel)


        self.iconQLabel      = QtWidgets.QLabel()
        #self.iconQLabel.setMinimumSize(80, 80)                   # +++
        #self.iconQLabel.setMaximumSize(80, 80)                   # +++

        self.allQHBoxLayout.addWidget(self.iconQLabel, 0)
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)

        self.allBoxLayout.addLayout(self.allQHBoxLayout, 0)


        self.setLayout(self.allBoxLayout)


    def setTextUp (self, text):
        self.textUpQLabel.setText(text)

    def setTextMiddle (self, text):
        self.textMiddleQLabel.setText(text)

    def setTextDown (self, text):
        self.textDownQLabel.setText(text)

    def setIcon (self, img_icon):
        with urlopen(img_icon) as url:
            data = url.read()

        pixmap = QPixmap()
        pixmap.loadFromData(data)

        self.iconQLabel.setPixmap(QtGui.QPixmap(pixmap).scaled(80, 80))  # + scaled(80, 80)
        #self.bgQLabel.setPixmap(QtGui.QPixmap(pixmap).scaled(80, 80))  # + scaled(80, 80)
        #self.bgQLabel.setPixmap(QtGui.QPixmap(pixmap).scaled(80, 80))
        #self.iconQLabel.setPixmap(QtGui.QPixmap(pixmap))  # + scaled(80, 80)





    def setBg_backup (self, img_bg):
        with urlopen(img_bg) as url:
            data = url.read()

        pixmap = QPixmap()
        pixmap.loadFromData(data)
        self.setPixmap(pixmap)

    def setPixmap(self, pixmap):
        item = QtWidgets.QGraphicsPixmapItem(pixmap)
        item.setTransformationMode(QtCore.Qt.SmoothTransformation)
        self.scene().addItem(item)


    def setBg (self, img_icon='https://beta.kemono.party/banners/patreon/2521159'):
        with urlopen(img_icon) as url:
            data = url.read()

        pixmap = QPixmap()
        pixmap.loadFromData(data)

        #self.iconQLabel.setPixmap(QtGui.QPixmap(pixmap).scaled(80, 80))  # + scaled(80, 80)
        #self.bgQLabel.setPixmap(QtGui.QPixmap(pixmap).scaled(80, 80))  # + scaled(80, 80)
        self.bgQLabel.setPixmap(QtGui.QPixmap(pixmap).scaled(80, 80))
        self.allQHBoxLayout.setStyleSheet("background-color:black;")


    def setImage(self, filename):
        self.setPixmap(QtGui.QPixmap(filename))




class exampleQMainWindow (QtWidgets.QListWidget):    #QMainWindow):     # +++ / ---
    def __init__(self):
        super(exampleQMainWindow, self).__init__()
        #self.myQListWidget = QtWidgets.QListWidget(self)

        # +++
        self.resize(420, 300)
        self.setFrameShape(self.NoFrame) # Нет границы
        self.setFlow(self.LeftToRight)   # Слева направо
        self.setWrapping(True)           # Эти 3 комбинации могут достичь того же эффекта, что и FlowLayout
        self.setResizeMode(self.Adjust)

        data_list = [ #id, name, service, img_icon, img_bg
            (
                '2521159',
                'patreon',
                'cavitees',
                'https://beta.kemono.party/icons/patreon/2521159',
                'https://beta.kemono.party/banners/patreon/2521159',
            ),
        ]

        for index, huindex, name, img_icon, img_bg in data_list:
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setBg(img_bg)
            myQCustomQWidget.setTextUp(index)
            myQCustomQWidget.setTextMiddle(huindex)
            myQCustomQWidget.setTextDown(name)
            myQCustomQWidget.setIcon(img_icon)
            myQListWidgetItem = QtWidgets.QListWidgetItem(self)  #.myQListWidget)
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            #self.myQListWidget.addItem(myQListWidgetItem)
            self.addItem(myQListWidgetItem)
            #self.myQListWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)
            self.setItemWidget(myQListWidgetItem, myQCustomQWidget)
        #self.setCentralWidget(self.myQListWidget)

        '''
        for index, name, icon in [
            ('No.1', 'Лена', 'E:/_Qt/Python-Examples/_PyQt5/Image/lena.png'),
            ('No.2', 'Петя', 'E:/_Qt/img/qt-logo.png'),
            ('No.3', 'Вася', 'E:/_Qt/img/avatar2.jpeg'),
            ('No.4', 'Петя', 'E:/_Qt/img/qt-logo.png'),
            ('No.5', 'Вася', 'E:/_Qt/img/avatar2.jpeg'),
            ('No.6', 'Лена', 'E:/_Qt/Python-Examples/_PyQt5/Image/lena.png'),
            ('No.7', 'Петя', 'E:/_Qt/img/qt-logo.png'),
            ('No.8', 'Вася', 'E:/_Qt/img/avatar2.jpeg'),
            ('No.9', 'Петя', 'E:/_Qt/img/qt-logo.png'),
            ('No.10', 'Вася', 'E:/_Qt/img/avatar2.jpeg'),
        ]:
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setTextUp(index)
            myQCustomQWidget.setTextDown(name)
            myQCustomQWidget.setIcon(icon)
            myQListWidgetItem = QtWidgets.QListWidgetItem(self)  #.myQListWidget)
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            #self.myQListWidget.addItem(myQListWidgetItem)
            self.addItem(myQListWidgetItem)
            #self.myQListWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)
            self.setItemWidget(myQListWidgetItem, myQCustomQWidget)
        #self.setCentralWidget(self.myQListWidget)
        '''


app = QtWidgets.QApplication([])
window = exampleQMainWindow()
window.show()
sys.exit(app.exec_())