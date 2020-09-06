from PyQt5 import QtCore, QtGui, QtWidgets
from image_encrypt import image_enc

url = ""


def selectImgOnClick(self):
    if self.selectImg.text() == "Select Image":
        a = QtWidgets.QFileDialog.getOpenFileName(
            filter="Image files(*.png *.jpg *.jpeg)")
        global url
        url = a[0]
        pixmap = QtGui.QPixmap(a[0])
        pixmap = pixmap.scaledToHeight(500)
        self.imgView.setPixmap(pixmap)
        if a[0] != "":
            self.selectImg.setText("Clear Image")
            self.decImg.setEnabled(True)
            self.encImg.setEnabled(True)
    else:
        pixmap = QtGui.QPixmap("")
        self.imgView.setPixmap(pixmap)
        self.selectImg.setText("Select Image")
        self.decImg.setEnabled(False)
        self.encImg.setEnabled(False)


def encImgOnClick(self):
    global url
    url = image_enc('e', url, "12345678")
    pixmap = QtGui.QPixmap(url)
    pixmap = pixmap.scaledToHeight(500)
    self.imgView.setPixmap(pixmap)


def encImgOnClick(self):
    global url
    url = image_enc('e', url, "12345678")
    pixmap = QtGui.QPixmap(url)
    pixmap = pixmap.scaledToHeight(500)
    self.imgView.setPixmap(pixmap)
