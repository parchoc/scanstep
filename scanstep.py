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
        # left setup
        self.leftScene = QGraphicsScene(0, 0, 400, 600)
        self.ui.leftView.setScene(self.leftScene)
        self.leftImage = None
        self.leftParameters = {
            'length': .0,
            'width foot': .0,
            'width heel': .0,
            'alpha': .0,
            'beta': .0,
            'gamma': .0,
            'clark': .0,
            'chijin': .0,
            'w': .0,
        }
        # right setup
        self.rightScene = QGraphicsScene(0, 0, 400, 600)
        self.ui.rightView.setScene(self.rightScene)
        self.rightImage = None
        self.rightParameters = {
            'length': .0,
            'width foot': .0,
            'width heel': .0,
            'alpha': .0,
            'beta': .0,
            'gamma': .0,
            'clark': .0,
            'chijin': .0,
            'w': .0,
        }
        # connections
        self.ui.leftLoadButton.clicked.connect(self.loadLeftImage)
        self.ui.rightLoadButton.clicked.connect(self.loadRightImage)
        self.ui.leftMarkupButton.clicked.connect(self.callLeftMarkupDialog)
        self.ui.rightMarkupButton.clicked.connect(self.callRightMarkupDialog)
        self.ui.actionNewProject.triggered.connect(self.newProject)

    @Slot()
    def loadLeftImage(self):
        '''
        Load selected image and set it as leftView background.
        '''
        fileName = QFileDialog.getOpenFileName(self, 'Выбор изображения', filter='Файлы изображений (*.png *.jpg *jpeg);;Все файлы (*)')[0]
        if fileName != '':
            self.leftImage = QPixmap(fileName).scaled(self.leftScene.width(), self.leftScene.height(), Qt.AspectRatioMode.IgnoreAspectRatio)
            self.leftScene.addPixmap(self.leftImage)
            self.ui.leftMarkupButton.setEnabled(True)
            self.ui.leftParametersButton.setEnabled(True)

    @Slot()
    def loadRightImage(self):
        '''
        Load selected image and set it as leftView background.
        '''
        fileName = QFileDialog.getOpenFileName(self, 'Выбор изображения', filter='Файлы изображений (*.png *.jpg *jpeg);;Все файлы (*)')[0]
        if fileName != '':
            self.rightImage = QPixmap(fileName).scaled(self.rightScene.width(), self.rightScene.height(), Qt.AspectRatioMode.IgnoreAspectRatio)
            self.rightScene.addPixmap(self.rightImage)
            self.ui.rightMarkupButton.setEnabled(True)
            self.ui.rightParametersButton.setEnabled(True)

    @Slot()
    def callLeftMarkupDialog(self):
        dialog = MarkupDialog(self, self.leftScene, self.leftParameters)
        dialog.markupDone.connect(self.updateLeftScene)
        dialog.show()

    @Slot()
    def callRightMarkupDialog(self):
        dialog = MarkupDialog(self, self.rightScene, self.rightParameters)
        dialog.markupDone.connect(self.updateRightScene)
        dialog.show()
    
    @Slot(QGraphicsScene, dict)
    def updateLeftScene(self, newScene, newParameters):
        self.leftScene = newScene
        self.ui.leftView.setScene(self.leftScene)
        self.leftParameters = newParameters

    @Slot(QGraphicsScene, dict)
    def updateRightScene(self, newScene, newParameters):
        self.rightScene = newScene
        self.ui.rightView.setScene(self.rightScene)
        self.rightParameters = newParameters

    @Slot()
    def newProject(self):
        # left setup
        self.leftScene = QGraphicsScene(0, 0, 400, 600)
        self.ui.leftView.setScene(self.leftScene)
        self.leftImage = None
        self.leftParameters = {
            'length': .0,
            'width foot': .0,
            'width heel': .0,
            'alpha': .0,
            'beta': .0,
            'gamma': .0,
            'clark': .0,
            'chijin': .0,
            'w': .0,
        }
        self.ui.leftMarkupButton.setEnabled(False)
        self.ui.leftParametersButton.setEnabled(False)
        # right setup
        self.rightScene = QGraphicsScene(0, 0, 400, 600)
        self.ui.rightView.setScene(self.rightScene)
        self.rightImage = None
        self.rightParameters = {
            'length': .0,
            'width foot': .0,
            'width heel': .0,
            'alpha': .0,
            'beta': .0,
            'gamma': .0,
            'clark': .0,
            'chijin': .0,
            'w': .0,
        }
        self.ui.rightMarkupButton.setEnabled(False)
        self.ui.rightParametersButton.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
