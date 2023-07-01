import sys
import json
from zipfile import ZipFile, ZipInfo, BadZipFile
from datetime import datetime

from PySide6.QtCore import Qt, Slot, QByteArray, QBuffer, QIODevice
from PySide6.QtWidgets import (QApplication, QMainWindow, QFileDialog,
                               QGraphicsScene, QMessageBox)
from PySide6.QtGui import QPixmap, QImage, QPainter, QPen

from ui_mainwindow import Ui_MainWindow
from markupdialog import MarkupDialog
from parametersdialog import ParametersDialog
from InteractiveScene import InteractiveScene


class MainWindow(QMainWindow):
    PARAMETERS = {
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

    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # left setup
        self.leftScene = InteractiveScene()
        self.ui.leftView.setScene(self.leftScene)
        self.leftPixmap = None
        self.leftParameters = self.PARAMETERS.copy()
        # right setup
        self.rightScene = InteractiveScene()
        self.ui.rightView.setScene(self.rightScene)
        self.rightPixmap = None
        self.rightParameters = self.PARAMETERS.copy()
        # connections
        self.ui.leftLoadButton.clicked.connect(self.loadLeftImage)
        self.ui.rightLoadButton.clicked.connect(self.loadRightImage)
        self.ui.leftMarkupButton.clicked.connect(self.callLeftMarkupDialog)
        self.ui.rightMarkupButton.clicked.connect(self.callRightMarkupDialog)
        self.ui.actionNewProject.triggered.connect(self.newProject)
        self.ui.leftParametersButton.clicked.connect(
            self.leftParametersMessage)
        self.ui.rightParametersButton.clicked.connect(
            self.rightParametersMessage)
        self.ui.actionSaveLeft.triggered.connect(self.saveLeftScene)
        self.ui.actionSaveRight.triggered.connect(self.saveRightScene)
        self.ui.actionSaveProject.triggered.connect(self.saveProject)
        self.ui.actionOpen.triggered.connect(self.loadProject)

    def loadImage(self):
        fileName = QFileDialog.getOpenFileName(self, 'Выбор изображения',
                                               filter='Файлы изображений '
                                                      '(*.png *.jpg *jpeg)'
                                                      ';;Все файлы (*)')[0]
        if fileName != '':
            pixmap = QPixmap(fileName)
            if pixmap.isNull():
                box = QMessageBox(QMessageBox.Icon.Warning,
                                  'Ошибка загрузки',
                                  'Невозможно загрузить файл',
                                  parent=self)
                box.show()
                return
            return pixmap

    def setupView(self, pixmap, scene, view, parameters):
        '''
        Set scene pixmap and compute image's dots per mm.
        '''
        scene.setSceneRect(0, 0, pixmap.width(), pixmap.height())
        scene.addPixmap(pixmap)
        view.setScene(scene)
        parameters['dpmm'] = (pixmap.toImage().dotsPerMeterX() / 1000)

    @Slot()
    def loadLeftImage(self):
        '''
        Load selected image and set it as leftView background.
        '''
        self.leftPixmap = self.loadImage()
        if self.leftPixmap is None:
            return
        self.leftParameters = self.PARAMETERS.copy()
        self.setupView(self.leftPixmap,
                       self.leftScene,
                       self.ui.leftView,
                       self.leftParameters)
        self.enableLeftMarkup(True)

    @Slot()
    def loadRightImage(self):
        '''
        Load selected image and set it as rightView background.
        '''
        self.rightPixmap = self.loadImage()
        if self.rightPixmap is None:
            return
        self.rightParameters = self.PARAMETERS.copy()
        self.setupView(self.rightPixmap,
                       self.rightScene,
                       self.ui.rightView,
                       self.rightParameters)
        self.enableRightMarkup(True)

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
        self.leftScene = InteractiveScene()
        self.ui.leftView.setScene(self.leftScene)
        self.leftParameters = self.PARAMETERS.copy()
        self.leftPixmap = None
        self.enableLeftMarkup(False)
        # right setup
        self.rightScene = InteractiveScene()
        self.ui.rightView.setScene(self.rightScene)
        self.rightParameters = self.PARAMETERS.copy()
        self.rightPixmap = None
        self.enableRightMarkup(False)

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
        filename, format = QFileDialog.getSaveFileName(
            self,
            'Сохранение изображения',
            filter='JPEG (*.jpeg);;PNG (*.png)')
        if filename != '':
            image = QImage(scene.sceneRect().size().toSize(),
                           QImage.Format.Format_ARGB32)
            image.fill(Qt.GlobalColor.transparent)
            painter = QPainter(image)
            scene.render(painter)
            painter.end()
            try:
                image.save(filename, format.split(' ', 1)[0])
            except OSError:
                box = QMessageBox(QMessageBox.Icon.Warning,
                                  'Ошибка сохранения',
                                  'Невозможно сохранить файл',
                                  parent=self)
                box.show()

    @Slot()
    def saveLeftScene(self):
        self.saveScene(self.leftScene)

    @Slot()
    def saveRightScene(self):
        self.saveScene(self.rightScene)

    @Slot()
    def saveProject(self):
        '''
        Save scene items and images as zip-file.
        Items stored in items.json file like:
            'left': {
                'points': {
                    'X': (100, 100),
                    'Y': (13, 42),
                    'Z': (123, 18),
                    ...
                }
                'lines': ['XY', 'XZ', ...]
                'parameters': {
                    'length': 1000,
                    'width foot': 300,
                    ...
                }
            }
            'right': ...
        Images saved as png files with names left.png and right.png
        corresponding if they exist.
        '''
        filename, _ = QFileDialog.getSaveFileName(
            self,
            'Сохранение проекта',
            filter='Project file (*.paw)')
        if filename != '':
            save_dict = {}
            # left scene
            save_dict['left'] = self.saveItems(self.leftScene)
            if self.leftPixmap:
                left_bytes = self.pixmapToBytes(self.leftPixmap)
            save_dict['left']['parameters'] = self.leftParameters
            # right scene
            save_dict['right'] = self.saveItems(self.rightScene)
            if self.rightPixmap:
                right_bytes = self.pixmapToBytes(self.rightPixmap)
            save_dict['right']['parameters'] = self.rightParameters
            # write resulted data to zip archive
            try:
                with ZipFile(filename, 'w') as savefile:
                    timetuple = datetime.now().timetuple()
                    # left pixmap
                    if self.leftPixmap:
                        savefile.writestr(ZipInfo('left.png', timetuple),
                                          left_bytes)
                    # right pixmap
                    if self.rightPixmap:
                        savefile.writestr(ZipInfo('right.png', timetuple),
                                          right_bytes)
                    # dictinary
                    savefile.writestr(ZipInfo('items.json', timetuple),
                                      json.dumps(save_dict))
            except OSError:
                box = QMessageBox(QMessageBox.Icon.Warning,
                                  'Ошибка сохранения',
                                  'Невозможно сохранить проект',
                                  parent=self)
                box.show()

    def saveItems(self, scene):
        save_dict = {
            'points': {},
            'lines': [],
        }
        for item in scene.items():
            # PointItem
            if item.type() == 65537:
                save_dict['points'][item.toolTip()] = (item.pos().x(),
                                                       item.pos().y())
            # QGraphicsLineItem
            elif item.type() == 6:
                save_dict['lines'].append(item.toolTip())
        return save_dict

    def pixmapToBytes(self, pixmap):
        b_array = QByteArray()
        buffer = QBuffer(b_array)
        buffer.open(QIODevice.OpenModeFlag.WriteOnly)
        pixmap.save(buffer, 'PNG')
        return b_array.data()

    @Slot()
    def loadProject(self):
        fileName = QFileDialog.getOpenFileName(
            self,
            'Загрузить проект',
            filter='Project file (*.paw)')[0]
        if fileName != '':
            try:
                with ZipFile(fileName, 'r') as loadfile:
                    # reseting environment
                    self.newProject()
                    # loading pixmap from png
                    try:
                        self.leftPixmap = QPixmap()
                        self.leftPixmap.loadFromData(loadfile.read('left.png'))
                        self.leftScene = InteractiveScene(
                            self.leftPixmap.width(),
                            self.leftPixmap.height())
                        self.leftScene.addPixmap(self.leftPixmap)
                        self.ui.leftView.setScene(self.leftScene)
                        self.enableLeftMarkup(True)
                    except KeyError:
                        pass
                    try:
                        self.rightPixmap = QPixmap()
                        self.rightPixmap.loadFromData(
                            loadfile.read('right.png'))
                        self.rightScene = InteractiveScene(
                            self.rightPixmap.width(),
                            self.rightPixmap.height())
                        self.rightScene.addPixmap(self.rightPixmap)
                        self.ui.rightView.setScene(self.rightScene)
                        self.enableRightMarkup(True)
                    except KeyError:
                        pass
                    items_dict = json.loads(loadfile.read('items.json'))
                    # adding points
                    self.loadPoints(self.leftScene,
                                    items_dict['left']['points'])
                    self.loadPoints(self.rightScene,
                                    items_dict['right']['points'])
                    # adding lines
                    linePen = QPen()
                    linePen.setColor(Qt.GlobalColor.red)
                    linePen.setWidth(1)
                    self.loadLines(self.leftScene,
                                   items_dict['left']['points'],
                                   items_dict['left']['lines'],
                                   linePen)
                    self.loadLines(self.rightScene,
                                   items_dict['right']['points'],
                                   items_dict['right']['lines'],
                                   linePen)
                    # adding parameters
                    self.leftParameters = items_dict['left']['parameters']
                    self.rightParameters = items_dict['right']['parameters']
            except BadZipFile:
                box = QMessageBox(QMessageBox.Icon.Warning,
                                  'Ошибка загрузки',
                                  'Невозможно открыть файл',
                                  parent=self)
                box.show()

    def loadPoints(self, scene, points):
        for name, pos in points.items():
            point = scene.addPoint(pos[0], pos[1], 3)
            point.setToolTip(name)
            point.setZValue(2)

    def loadLines(self, scene, points, lines, pen):
        for line in lines:
            item = scene.addLine(
                points[line[0]][0],
                points[line[0]][1],
                points[line[1]][0],
                points[line[1]][1],
                pen)
            item.setToolTip(line)
            item.setZValue(1)

    def enableLeftMarkup(self, enable: bool):
        self.ui.leftMarkupButton.setEnabled(enable)
        self.ui.leftParametersButton.setEnabled(enable)
        self.ui.actionSaveLeft.setEnabled(enable)

    def enableRightMarkup(self, enable: bool):
        self.ui.rightMarkupButton.setEnabled(enable)
        self.ui.rightParametersButton.setEnabled(enable)
        self.ui.actionSaveRight.setEnabled(enable)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
