import sys
from PySide6.QtCore import Qt, Slot
from ui_mainwindow import Ui_MainWindow
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsScene
from PySide6.QtGui import QPixmap, QBrush
from markupdialog import MarkupDialog

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # left setup
        self.leftScene = QGraphicsScene(0, 0, 400, 600)
        self.ui.leftView.setScene(self.leftScene)
        self.leftImage = None
        self.leftPoints = {}
        self.leftParameters = None
        # right setup
        self.rightScene = QGraphicsScene(0, 0, 400, 600)
        self.ui.rightView.setScene(self.rightScene)
        self.rightImage = None
        self.rightPoints = {}
        self.rightParameters = None
        # connections
        self.ui.leftLoadButton.clicked.connect(self.loadLeftImage)
        self.ui.rightLoadButton.clicked.connect(self.loadRightImage)
        self.ui.leftMarkupButton.clicked.connect(self.callLeftMarkupDialog)
        self.ui.rightMarkupButton.clicked.connect(self.callRightMarkupDialog)

    @Slot()
    def loadLeftImage(self):
        '''
        Load selected image and set it as leftView background.
        '''
        fileName = QFileDialog.getOpenFileName(self, 'Выбор изображения', filter='Файлы изображений (*.png *.jpg *jpeg);;Все файлы (*)')[0]
        if fileName != '':
            self.leftImage = QPixmap(fileName).scaled(self.leftScene.width(), self.leftScene.height(), Qt.AspectRatioMode.IgnoreAspectRatio)
            self.leftScene.setBackgroundBrush(QBrush(self.leftImage))
            self.ui.leftMarkupButton.setEnabled(True)

    @Slot()
    def loadRightImage(self):
        '''
        Load selected image and set it as leftView background.
        '''
        fileName = QFileDialog.getOpenFileName(self, 'Выбор изображения', filter='Файлы изображений (*.png *.jpg *jpeg);;Все файлы (*)')[0]
        if fileName != '':
            self.rightImage = QPixmap(fileName).scaled(self.rightScene.width(), self.rightScene.height(), Qt.AspectRatioMode.IgnoreAspectRatio)
            self.rightScene.setBackgroundBrush(QBrush(self.rightImage))
            self.ui.rightMarkupButton.setEnabled(True)

    @Slot()
    def callLeftMarkupDialog(self):
        dialog = MarkupDialog(self, self.leftImage, self.leftPoints)
        dialog.markupDone.connect(self.updateLeftScene)
        dialog.show()

    @Slot()
    def callRightMarkupDialog(self):
        dialog = MarkupDialog(self, self.rightImage, self.rightPoints)
        dialog.markupDone.connect(self.updateRightScene)
        dialog.show()
    
    @Slot(QGraphicsScene, dict)
    def updateLeftScene(self, newScene, newPoints):
        self.leftScene = newScene
        self.leftPoints = newPoints
        self.ui.leftView.setScene(self.leftScene)

    @Slot(QGraphicsScene, dict)
    def updateRightScene(self, newScene, newPoints):
        self.rightScene = newScene
        self.rightPoints = newPoints
        self.ui.rightView.setScene(self.rightScene)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
