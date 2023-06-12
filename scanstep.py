import sys
from PySide6.QtCore import Qt, Slot
from ui_mainwindow import Ui_MainWindow
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsScene
from PySide6.QtGui import QPixmap, QImage, QPainter
from markupdialog import MarkupDialog
from parametersdialog import ParametersDialog

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # left setup
        self.leftScene = QGraphicsScene()
        self.ui.leftView.setScene(self.leftScene)
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
            'dpmm': 0,
        }
        # right setup
        self.rightScene = QGraphicsScene(0, 0, 400, 600)
        self.ui.rightView.setScene(self.rightScene)
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
            'dpmm': 0,
        }
        # connections
        self.ui.leftLoadButton.clicked.connect(self.loadLeftImage)
        self.ui.rightLoadButton.clicked.connect(self.loadRightImage)
        self.ui.leftMarkupButton.clicked.connect(self.callLeftMarkupDialog)
        self.ui.rightMarkupButton.clicked.connect(self.callRightMarkupDialog)
        self.ui.actionNewProject.triggered.connect(self.newProject)
        self.ui.leftParametersButton.clicked.connect(self.leftParametersMessage)
        self.ui.rightParametersButton.clicked.connect(self.rightParametersMessage)
        self.ui.actionSaveLeft.triggered.connect(self.saveLeftScene)
        self.ui.actionSaveRight.triggered.connect(self.saveRightScene)

    @Slot()
    def loadLeftImage(self):
        '''
        Load selected image and set it as leftView background.
        '''
        fileName = QFileDialog.getOpenFileName(self, 'Выбор изображения', filter='Файлы изображений (*.png *.jpg *jpeg);;Все файлы (*)')[0]
        if fileName != '':
            pixmap = QPixmap(fileName)
            self.leftScene.setSceneRect(0, 0, pixmap.width(), pixmap.height())
            self.leftScene.addPixmap(pixmap)
            self.leftParameters['dpmm'] = QImage(fileName).dotsPerMeterX() / 1000
            self.ui.leftMarkupButton.setEnabled(True)
            self.ui.leftParametersButton.setEnabled(True)
            self.ui.actionSaveLeft.setEnabled(True)

    @Slot()
    def loadRightImage(self):
        '''
        Load selected image and set it as leftView background.
        '''
        fileName = QFileDialog.getOpenFileName(self, 'Выбор изображения', filter='Файлы изображений (*.png *.jpg *jpeg);;Все файлы (*)')[0]
        if fileName != '':
            pixmap = QPixmap(fileName)
            self.rightScene.setSceneRect(0, 0, pixmap.width(), pixmap.height())
            self.rightScene.addPixmap(pixmap)
            self.rightParameters['dpmm'] = QImage(fileName).dotsPerMeterX() / 1000
            self.ui.rightMarkupButton.setEnabled(True)
            self.ui.rightParametersButton.setEnabled(True)
            self.ui.actionSaveRight.setEnabled(True)

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
        self.leftScene = QGraphicsScene()
        self.ui.leftView.setScene(self.leftScene)
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
            'dpmm': 0,
        }
        self.ui.leftMarkupButton.setEnabled(False)
        self.ui.leftParametersButton.setEnabled(False)
        self.ui.actionSaveLeft.setEnabled(False)
        # right setup
        self.rightScene = QGraphicsScene()
        self.ui.rightView.setScene(self.rightScene)
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
            'dpmm': 0,
        }
        self.ui.rightMarkupButton.setEnabled(False)
        self.ui.rightParametersButton.setEnabled(False)
        self.ui.actionSaveRight.setEnabled(False)
    
    @Slot()
    def leftParametersMessage(self):
        dialog = ParametersDialog(self.leftParameters, self)
        dialog.setWindowTitle('Характеристики левой стопы')
        dialog.show()
    
    @Slot()
    def rightParametersMessage(self):
        dialog = ParametersDialog(self.rightParameters, self)
        dialog.setWindowTitle('Характеристики правой стопы')
        dialog.show()
    
    def saveScene(self, scene):
        filename, format = QFileDialog.getSaveFileName(self, 'Сохранение изображения', filter='JPEG (*.jpeg);;PNG (*.png)')
        if filename != '':
            image = QImage(scene.sceneRect().size().toSize(), QImage.Format.Format_ARGB32)
            image.fill(Qt.GlobalColor.transparent)
            painter = QPainter(image)
            scene.render(painter)
            painter.end()
            image.save(filename, format.split(' ', 1)[0])

    @Slot()
    def saveLeftScene(self):
        self.saveScene(self.leftScene)
    
    @Slot()
    def saveRightScene(self):
        self.saveScene(self.rightScene)
                

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
