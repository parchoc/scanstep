from PySide6.QtCore import Slot, Signal, QPointF, Qt, QLineF
from ui_markupdialog import Ui_MarkupDialog
from PySide6.QtWidgets import QDialog, QGraphicsItem, QGraphicsScene
from InteractiveScene import InteractiveScene, PointItem
from PySide6.QtGui import QBrush, QPen

CONNECTIONS = {
    'Y': frozenset(('X', "Z", "W")),
    'X': frozenset(("Y",)),
    "Z": frozenset(("Y", "W")),
    'F': frozenset(("H", "B")),
    'H': frozenset(("G", "M", 'F')),
    'B': frozenset(("G", "F")),
    "G": frozenset(("B", "H", 'L')),
    'A': frozenset(),
    'D': frozenset(),
    'E': frozenset(),
    'L': frozenset(("G",)),
    'M': frozenset(("H",)),
    'N': frozenset(("G",)),
    'W': frozenset(("Z", "Y")),
    'K': frozenset(('I',)),
    'I': frozenset(('K',)),
}

class MarkupDialog(QDialog):
    markupDone = Signal(QGraphicsScene, dict, dict, dict)
    
    def __init__(self, parent=None, backgroundImage=None, points=None, lines=None, parameters=None) -> None:
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
        if lines:
            for key, item in lines.items():
                self.lines[key] = self.scene.addLine(item.line(), self.linePen)
        self.ui.markupView.setScene(self.scene)
        # connections
        self.accepted.connect(self.sendScene)
        self.scene.pointAdded.connect(self.updateGlobal)

    @Slot()
    def sendScene(self):
        self.markupDone.emit(self.scene, self.points, self.lines, self.parameters)
    
    def glueTo(self, point, line_item):
        line = line_item.line()
        perpendicular = self.perpendicularTo(point, line)
        _, intersectionPoint = line.intersects(perpendicular)
        point.setPos(intersectionPoint.x(), intersectionPoint.y())
        point.setParentItem(line_item)

    @Slot(QGraphicsItem)
    def updateGlobal(self, item):
        current_point = self.ui.pointsBox.currentText()
        # next points should be on lines
        if current_point == 'A' and 'XY' in self.lines:
            self.glueTo(item, self.lines['XY'])
        elif current_point == 'D' and 'IK' in self.lines:
            self.glueTo(item, self.lines['IK'])
        elif current_point == 'E' and 'IK' in self.lines:
            self.glueTo(item, self.lines['IK'])
        self.updatePoint(item, current_point)
        self.updateLines(current_point)
        self.updateParameters(current_point)
        self.updateParametersDisplay()
        # go to the next point if it not the last one
        if self.ui.pointsBox.currentIndex() < self.ui.pointsBox.count() - 1:
            self.ui.pointsBox.setCurrentIndex(self.ui.pointsBox.currentIndex() + 1)

    @Slot(QGraphicsItem, str)
    def updatePoint(self, point, name):
        # remove previous point if it exist
        if name in self.points:
            # if point alredy removed by removed perent than just pass
            try:
                self.scene.removeItem(self.points[name])
            except RuntimeError:
                pass
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
                self.addLine(line)

    @Slot(str)
    def updateParameters(self, updated_point):
        # check if all points for computetion exist and related point has been modified
        # length
        if updated_point in {'Y', "X", "Z"} and len({'Y', "X", "Z"}.intersection(self.points)) == 3:
            self.parameters['length'] = self.lengthFoot()
        # plot C
        if updated_point in {'Y', "A"} and len({'Y', "A"}.intersection(self.points)) == 2:
            self.plotC()
        # foot width
        if updated_point in {'H', 'G'} and len({'H', 'G'}.intersection(self.points)) == 2:
            self.parameters['width foot'] = self.widthFoot()
        # heel width
        if updated_point in {'B', 'F'} and len({'B', 'F'}.intersection(self.points)) == 2:
            self.parameters['width heel'] = self.widthHeel()
        # angle alpha(BG, GL)
        if updated_point in {'B', 'G', 'L' } and len({'B', 'G', 'L'}.intersection(self.points)) == 3:
            self.parameters['alpha'] = self.alpha()
        # angle beta(HM, FH)
        if updated_point in {'H', 'M', 'F'} and len({'H', 'M', 'F'}.intersection(self.points)) == 3:
            self.parameters['beta'] = self.beta()
        # angle gamma(BG, FH)
        if updated_point in {'B', 'G', 'F', 'H'} and len({'B', 'G', 'F', 'H'}.intersection(self.points)) == 4:
            self.parameters['gamma'] = self.gamma()
        # angle clark(GN, BG)
        if updated_point in {'G', 'N', 'B'} and len({'G', 'N', 'B'}.intersection(self.points)) == 3:
            self.parameters['clark'] = self.clark()
        # w = length/foot width
        if updated_point in {'Y', "X", "Z", 'H', 'G'} and len({'Y', "X", "Z", 'H', 'G'}.intersection(self.points)) == 5:
            self.parameters['w'] = self.w()

    @Slot()
    def updateParametersDisplay(self):
        self.ui.parametersDisplay.setPlainText(
            f'''
            Длина стопы: {self.parameters['length']:.2f}
            Ширина стопы: {self.parameters['width foot']:.2f}
            Ширина пятки: {self.parameters['width heel']:.2f}
            α: {self.parameters['alpha']:.2f}
            β: {self.parameters['beta']:.2f}
            γ: {self.parameters['gamma']:.2f}
            Угол Кларка: {self.parameters['clark']:.2f}
            Коэффициент Чижина: {self.parameters['chijin']:.2f}
            Коэффициент w: {self.parameters['w']:.2f}
            '''
        )

    def addLine(self, line):
        if line in self.lines:
            self.scene.removeItem(self.lines[line])
        self.lines[line] = self.scene.addLine(
                self.points[line[0]].x(), 
                self.points[line[0]].y(),
                self.points[line[1]].x(), 
                self.points[line[1]].y(), 
                self.linePen
            )
        self.lines[line].setToolTip(line)
        
    def perpendicularTo(self, point, line):
        angle = line.normalVector().angle()
        perpendicular = QLineF(point.pos(), point.pos() + QPointF(5, 5))
        perpendicular.setAngle(angle)
        return perpendicular

    def lengthFoot(self):
        XY = self.lines['XY'].line()
        # checking which line is longer
        if XY.length() > self.lines["YZ"].line().length():
            # if XY longer than accept it as the length
            length = XY.length()
            # remove perpendicular if it exists
            if 'WZ' in self.lines:
                self.scene.removeItem(self.lines['WZ'])
                self.scene.removeItem(self.lines['WY'])
                del self.lines['WZ']
                del self.lines['WY']
                self.scene.removeItem(self.points['W'])
                del self.points['W']
        else:
            # finding perpendicular from Z to XY
            perpendicular = self.perpendicularTo(self.points['Z'], XY)
            type, intersectionPoint = XY.intersects(perpendicular)
            if type:
                # adding intersection point to the scene
                point = PointItem(intersectionPoint.x(), intersectionPoint.y(), 3, self.circlePen, self.circleBrush)
                self.scene.addItem(point)
                self.updatePoint(point, 'W')
                # adding perpendicular line to the scene
                self.updateLines('W')
                length = self.lines['WY'].line().length()
            else:
                length = XY.length()
        return length
    
    def widthFoot(self):
        return self.lines['GH'].line().length()
    
    def widthHeel(self):
        return self.lines['BF'].line().length()
    
    def alpha(self):
        angle = self.lines['BG'].line().angleTo(self.lines['GL'].line())
        return min(angle, 360 - angle)
    
    def beta(self):
        angle = self.lines['HM'].line().angleTo(self.lines['FH'].line())
        return min(angle, 360 - angle)
    
    def gamma(self):
        angle = self.lines['BG'].line().angleTo(self.lines['FH'].line())
        return min(angle, 360 - angle)
    
    def clark(self):
        angle = self.lines['GN'].line().angleTo(self.lines['BG'].line())
        return min(angle, 360 - angle)
    
    def w(self):
        return self.parameters['length'] / self.parameters['width foot']
    
    def plotC(self):
        pos = (self.points['A'].pos() + self.points['Y'].pos()) / 2
        point = PointItem(pos.x(), pos.y(), 3, self.circlePen, self.circleBrush, self.lines['XY'])
        self.updatePoint(point, 'C')
