from PySide6.QtCore import Slot, Signal
from ui_markupdialog import Ui_MarkupDialog
from PySide6.QtWidgets import QDialog, QGraphicsItem, QGraphicsScene
from InteractiveScene import InteractiveScene
from PySide6.QtGui import QBrush

CONNECTIONS = {
    'Y': ('X',),
    'X': ('Y', 'Z'),
    'Z': ('X',),
    'J': [],
    'F': [],
    'B': [],
    'G': [],
    'A': [],
    'D': [],
    'E': [],
    'L': [],
    'M': [],
    'N': [],
}

class MarkupDialog(QDialog):
    markupDone = Signal(QGraphicsScene, dict, dict)
    
    def __init__(self, parent=None, backgroundImage=None, points=None, parameters=None) -> None:
        super(MarkupDialog, self).__init__(parent)
        self.ui = Ui_MarkupDialog()
        self.ui.setupUi(self)
        self.scene = InteractiveScene(backgroundImage.width(), backgroundImage.height())
        if parameters:
            self.parameters = parameters
        else:
            self.parameters = {}
        self.updateParametersDisplay()
        # adding background image from initial scene
        if backgroundImage:
            self.scene.addPixmap(backgroundImage)
        # adding point items from initial scene
        if points:
            for key, item in points.items():
                self.points[key] = self.scene.addPoint(item.x(), item.y())
                self.points[key].setToolTip(key)
        else:
            self.points = {}
        self.ui.markupView.setScene(self.scene)
        # connections
        self.accepted.connect(self.sendScene)
        self.scene.pointAdded.connect(self.updatePointsDict)

    @Slot()
    def sendScene(self):
        self.markupDone.emit(self.scene, self.points, self.parameters)

    @Slot(QGraphicsItem)
    def updatePointsDict(self, item):
        # remove previous point if it exist
        if self.ui.pointsBox.currentText() in self.points:
            self.scene.removeItem(self.points[self.ui.pointsBox.currentText()])
        # add new point to dict
        item.setToolTip(self.ui.pointsBox.currentText())
        self.points[self.ui.pointsBox.currentText()] = item
        # go to the next point if it not the last one
        if self.ui.pointsBox.currentIndex() < self.ui.pointsBox.count() - 1:
            self.ui.pointsBox.setCurrentIndex(self.ui.pointsBox.currentIndex() + 1)

    @Slot()
    def updateParametersDisplay(self):
        self.ui.parametersDisplay.setPlainText(
            f'''
            Длина стопы: {self.parameters['length']}
            Ширина стопы: {self.parameters['foot width']}
            Ширина пятки: {self.parameters['heel width']}
            α: {self.parameters['alpha']}
            β: {self.parameters['beta']}
            γ: {self.parameters['gamma']}
            Угол Кларка: {self.parameters['clark']}
            Коэффициент Чижина: {self.parameters['chijin']}
            Коэффициент w: {self.parameters['w']}
            '''
        )
