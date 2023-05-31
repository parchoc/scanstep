import sys
from PySide6.QtCore import Qt, Slot
from ui_mainwindow import Ui_MainWindow
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsScene
from PySide6.QtGui import QPixmap
from markupdialog import MarkupDialog

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # inner setup
        self.leftScene = QGraphicsScene(0, 0, 400, 600)
        self.ui.leftView.setScene(self.leftScene)
        self.rightScene = QGraphicsScene(0, 0, 400, 600)
        self.ui.rightView.setScene(self.rightScene)
        self.leftParameters = None
        self.rightParameters = None
        # connections
        self.ui.leftLoadButton.clicked.connect(self.loadLeftImage)
        self.ui.rightLoadButton.clicked.connect(self.loadRightImage)
        self.ui.leftMarkupButton.clicked.connect(self.callLeftMarkupDialog)
        self.ui.rightMarkupButton.clicked.connect(self.callRightMarkupDialog)

    @Slot()
    def loadLeftImage(self):
        fileName = QFileDialog.getOpenFileName(self, 'Выбор изображения', filter='Файлы изображений (*.png *.jpg *jpeg);;Все файлы (*)')[0]
        if fileName != '':
            image = QPixmap(fileName).scaled(self.leftScene.width(), self.leftScene.height(), Qt.AspectRatioMode.IgnoreAspectRatio)
            self.leftScene.addPixmap(image)
            self.ui.leftMarkupButton.setEnabled(True)

    @Slot()
    def loadRightImage(self):
        fileName = QFileDialog.getOpenFileName(self, 'Выбор изображения', filter='Файлы изображений (*.png *.jpg *jpeg);;Все файлы (*)')[0]
        if fileName != '':
            image = QPixmap(fileName).scaled(self.rightScene.width(), self.rightScene.height(), Qt.AspectRatioMode.IgnoreAspectRatio)
            self.rightScene.addPixmap(image)
            self.ui.rightMarkupButton.setEnabled(True)

    @Slot()
    def callLeftMarkupDialog(self):
        dialog = MarkupDialog(self, self.leftScene)
        dialog.markupDone.connect(self.updateLeftScene)
        dialog.show()

    @Slot()
    def callRightMarkupDialog(self):
        dialog = MarkupDialog(self, self.rightScene)
        dialog.markupDone.connect(self.updateRightScene)
        dialog.show()
    
    @Slot()
    def updateLeftScene(self, newScene):
        self.leftScene = newScene
        self.ui.leftView.setScene(self.leftScene)

    @Slot()
    def updateRightScene(self, newScene):
        self.rightScene = newScene
        self.ui.rightView.setScene(self.rightScene)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
