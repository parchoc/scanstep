from PySide6.QtCore import Slot, Signal, QPointF, Qt
from ui_markupdialog import Ui_MarkupDialog
from PySide6.QtWidgets import QDialog, QGraphicsItem, QGraphicsScene
from InteractiveScene import InteractiveScene
from PySide6.QtGui import QBrush, QPen

CONNECTIONS = {
    'Y': frozenset(('X', "X'")),
    'X': frozenset(("Y",)),
    "X'": frozenset(("Y",)),
    'Г': frozenset(("З", "L", "B", "N")),
    'З': frozenset(("Г", "M", "B'")),
    'B': frozenset(("B'", "Г")),
    "B'": frozenset(("B", "З")),
    'A': frozenset(("Y",)),
    'D': [],
    'E': [],
    'L': frozenset(("Г",)),
    'M': frozenset(("З",)),
    'N': frozenset(("Г",)),
}

class MarkupDialog(QDialog):
    markupDone = Signal(QGraphicsScene, dict, dict)
    
    def __init__(self, parent=None, backgroundImage=None, points=None, parameters=None) -> None:
        super(MarkupDialog, self).__init__(parent)
        self.ui = Ui_MarkupDialog()
        self.ui.setupUi(self)
        self.scene = InteractiveScene(backgroundImage.width(), backgroundImage.height())
        self.circlePen = QPen()
        self.circlePen.setWidth(2)
        self.circleBrush = QBrush(Qt.GlobalColor.red)
        self.linePen = QPen()
        self.linePen.setColor(Qt.GlobalColor.red)
        self.linePen.setWidth(1)
        if parameters:
            self.parameters = parameters
        else:
            self.parameters = {}
        self.updateParametersDisplay()
        # adding background image from initial scene
        if backgroundImage:
            self.scene.addPixmap(backgroundImage)
        # adding point items from initial scene
        self.points = {}
        if points:
            for key, item in points.items():
                self.points[key] = self.scene.addPoint(item.x(), item.y(), self.circlePen, self.circleBrush)
                self.points[key].setToolTip(key)            
        self.lines = {}
        self.ui.markupView.setScene(self.scene)
        # connections
        self.accepted.connect(self.sendScene)
        self.scene.pointAdded.connect(self.updateGlobal)

    @Slot()
    def sendScene(self):
        self.markupDone.emit(self.scene, self.points, self.parameters)

    @Slot(QGraphicsItem)
    def updateGlobal(self, item):
        current_point = self.ui.pointsBox.currentText()
        self.updatePoints(item, current_point)
        self.updateLines(current_point)
        # self.updateParameters(current_point)
        # self.updateParametersDisplay()
        # go to the next point if it not the last one
        if self.ui.pointsBox.currentIndex() < self.ui.pointsBox.count() - 1:
            self.ui.pointsBox.setCurrentIndex(self.ui.pointsBox.currentIndex() + 1)

    @Slot(QGraphicsItem, str)
    def updatePoints(self, point, name):
        # remove previous point if it exist
        if name in self.points:
            self.scene.removeItem(self.points[name])
        # add new point to dict
        point.setToolTip(name)
        point.setZValue(1)
        self.points[name] = point
    
    @Slot(str)
    def updateLines(self, updated_point):
        # go thro all points connected to updated_point
        for point in CONNECTIONS[updated_point]:
            # if connected point exists than build line
            if point in self.points:
                line = ''.join(sorted(updated_point + point))
                # remove old line if it exists
                if line in self.lines:
                    self.scene.removeItem(self.lines[line])
                item = self.scene.addLine(
                    self.points[line[0]].x(),
                    self.points[line[0]].y(),
                    self.points[line[1]].x(),
                    self.points[line[1]].y(),
                    self.linePen
                )
                self.lines[line] = item

    @Slot(str)
    def updateParameters(self, updated_point):
        # check if all points for length computetion exist and related point has been modified
        # length
        if updated_point in {'Y', "X", "X'"} and len({'Y', "X", "X'"}.intersection(self.points)) == 3:
            self.lengthFoot()

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

    def lengthFoot(self):
        YX = self.lines['YX'].line()
        if YX.length() > self.lines["YX'"].line().length():
            self.parameters['length'] = YX.length()
        else:
            # finding perpendicular from X' to YX
            normal = YX.normalVector()
            normal.translate(0, YX.length())
            intersectionPoint = QPointF()
            YX.intersects(normal, intersectionPoint)
            # adding intersection point to the scene
            point = self.scene.addEllipse(0, 0, 6, 6, self.circlePen, self.circleBrush)
            point.setPos(intersectionPoint.x() - 3, intersectionPoint.y() - 3)
            if 'Z' in self.points['Z']:
                self.scene.removeItem(self.points['Z'])
            self.points['Z'] = point
            # adding perpendicular line to the scene
            if 'YZ' in self.lines['YZ']:
                self.scene.removeItem(self.lines['YZ'])
                self.lines['YZ'] = self.scene.addLine(
                    self.points['Y'].x(), 
                    self.points['Y'].y(), 
                    point.x(),
                    point.y(),
                    self.linePen
                )
            self.parameters['length'] = self.lines['YZ'].line().length()
        return self.parameters['length']
