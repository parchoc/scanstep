from PySide6.QtCore import Slot, Signal, QPointF, Qt, QLineF
from ui_markupdialog import Ui_MarkupDialog
from PySide6.QtWidgets import QDialog, QGraphicsItem, QGraphicsScene
from InteractiveScene import InteractiveScene, PointItem
from PySide6.QtGui import QBrush, QPen, QPixmap
import res

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

PARENTS = {
    'A': 'XY',
    'C': 'XY',
    'D': 'IK',
    'E': 'IK',
    'I': 'BG',
    'K': 'FH',
}

SCHEME = {
    'Y': (171, 502),
    'X': (136, 25),
    "Z": (189, 21),
    'F': (84, 425),
    'H': (22, 195),
    'B': (235, 433),
    "G": (246, 148),
    'A': (141, 86),
    # 'D': (),
    'E': (127, 295),
    'L': (232, 66),
    'M': (27, 131),
    'N': (139, 207),
    'K': (49, 296),
    'I': (240, 291),
}


class MarkupDialog(QDialog):
    markupDone = Signal(QGraphicsScene, dict)

    def __init__(self, parent=None, scene=None, parameters=None) -> None:
        super(MarkupDialog, self).__init__(parent)
        self.ui = Ui_MarkupDialog()
        self.ui.setupUi(self)
        self.scene = InteractiveScene(scene.width(), scene.height())
        self.circlePen = QPen()
        self.circlePen.setWidth(2)
        self.circleBrush = QBrush(Qt.GlobalColor.red)
        self.hightlightBrush = QBrush(Qt.GlobalColor.blue)
        self.linePen = QPen()
        self.linePen.setColor(Qt.GlobalColor.red)
        self.linePen.setWidth(1)
        self.prevPoint = self.ui.pointsBox.currentText()
        if parameters:
            self.parameters = parameters
        else:
            self.parameters = {}
        self.updateParametersDisplay()
        items = {}
        for item in scene.items():
            # adding background image from initial scene
            name = item.toolTip()
            if item.type() == 7:
                self.scene.addPixmap(item.pixmap())
            # adding point items from initial scene
            if item.type() == 65537:
                items[name] = self.scene.addPoint(item.x(), item.y(), 3)
                items[name].setZValue(2)
                items[name].setToolTip(name)
            # adding lines
            if item.type() == 6:
                items[name] = self.scene.addLine(item.line(), self.linePen)
                items[name].setZValue(1)
                items[name].setToolTip(name)
        for point, line in PARENTS.items():
            if point in items and line in items:
                items[point].setParentItem(items[line])
        self.ui.markupView.setScene(self.scene)
        # scheme
        scheme = QPixmap(u":/img/foot_sheme.jpg")
        self.schemeScene = InteractiveScene(scheme.width(), scheme.height())
        self.schemeScene.addPixmap(scheme)
        for name, pos in SCHEME.items():
            item = self.schemeScene.addPoint(pos[0], pos[1], 4)
            item.setToolTip(name)
        self.ui.schemeView.setScene(self.schemeScene)
        self.hightlightPoint()
        # connections
        self.accepted.connect(self.sendScene)
        self.scene.pointAdded.connect(self.updateGlobal)
        self.ui.pointsBox.currentIndexChanged.connect(self.hightlightPoint)

    @Slot()
    def sendScene(self):
        # recolor hightlighted point before sending scene
        items = self.scene.itemsDict()
        if self.prevPoint in items:
            items[self.prevPoint].setBrush(self.circleBrush)
        self.markupDone.emit(self.scene, self.parameters)

    def glueTo(self, point, line_item):
        line = line_item.line()
        perpendicular = self.perpendicularTo(point, line)
        _, intersectionPoint = line.intersects(perpendicular)
        point.setPos(intersectionPoint.x(), intersectionPoint.y())
        point.setParentItem(line_item)

    @Slot(QGraphicsItem)
    def updateGlobal(self, item):
        current_point = self.ui.pointsBox.currentText()
        items = self.scene.itemsDict()
        # next points should be on lines
        if current_point == 'A' and 'XY' in items:
            self.glueTo(item, items['XY'])
        elif current_point == 'D' and 'IK' in items:
            self.glueTo(item, items['IK'])
        elif current_point == 'E' and 'IK' in items:
            self.glueTo(item, items['IK'])
        self.updatePoint(item, current_point)
        self.updateLines(current_point)
        self.updateParameters(current_point)
        self.updateParametersDisplay()
        # go to the next point if it not the last one
        if self.ui.pointsBox.currentIndex() < self.ui.pointsBox.count() - 1:
            self.ui.pointsBox.setCurrentIndex(
                self.ui.pointsBox.currentIndex() + 1)

    @Slot(QGraphicsItem, str)
    def updatePoint(self, point, name):
        # remove previous point if it exist
        items = self.scene.itemsDict()
        if name in items:
            self.scene.removeItem(items[name])
        # add new point to dict
        point.setToolTip(name)
        point.setZValue(2)

    @Slot(str)
    def updateLines(self, updated_point):
        items = self.scene.itemsDict()
        # go thro all points connected to updated_point
        for point in CONNECTIONS[updated_point]:
            # if connected point exists than build line
            if point in items:
                line = ''.join(sorted(updated_point + point))
                # remove old line if it exists
                self.addLine(line)

    @Slot(str)
    def updateParameters(self, updated_point):
        items = self.scene.itemsDict()
        # check if all points for computetion exist and
        # related point has been modified
        # length
        if (updated_point in {'Y', "X", "Z"}
                and len({'Y', "X", "Z"}.intersection(items)) == 3):
            self.parameters['length'] = self.lengthFoot()
        # plot C
        if (updated_point in {'Y', "A"}
                and len({'Y', "A"}.intersection(items)) == 2):
            self.plotC()
            items = self.scene.itemsDict()
        # remove IK if one of dependent points is relocated
        if updated_point in {'X', 'A', 'Y'} and 'IK' in items:
            self.scene.removeItem(items['I'])
            self.scene.removeItem(items['K'])
            self.scene.removeItem(items['IK'])
            del items['I']
            del items['K']
            del items['IK']
        # plot I
        if (updated_point in {'Y', 'A', "B", 'G'}
                and len({'C', "B", 'G'}.intersection(items)) == 3):
            self.plotI()
            items = self.scene.itemsDict()
        # plot K
        if (updated_point in {'Y', 'A', "F", 'H'}
                and len({'C', "F", 'H'}.intersection(items)) == 3):
            self.plotK()
            items = self.scene.itemsDict()
        # plot IK
        if (updated_point in {'Y', 'A', "F", 'H', 'B', 'G'}
                and len({'I', "K"}.intersection(items)) == 2):
            self.addLine('IK')
            items = self.scene.itemsDict()
        # foot width
        if (updated_point in {'H', 'G'}
                and len({'H', 'G'}.intersection(items)) == 2):
            self.parameters['width foot'] = self.widthFoot(items['GH'].line())
        # heel width
        if (updated_point in {'B', 'F'}
                and len({'B', 'F'}.intersection(items)) == 2):
            self.parameters['width heel'] = self.widthFoot(items['BF'].line())
        # angle alpha(BG, GL)
        if (updated_point in {'B', 'G', 'L'}
                and len({'B', 'G', 'L'}.intersection(items)) == 3):
            self.parameters['alpha'] = self.angle(items['BG'].line(),
                                                  items['GL'].line())
        # angle beta(HM, FH)
        if (updated_point in {'H', 'M', 'F'}
                and len({'H', 'M', 'F'}.intersection(items)) == 3):
            self.parameters['beta'] = self.angle(items['HM'].line(),
                                                 items['FH'].line())
        # angle gamma(BG, FH)
        if (updated_point in {'B', 'G', 'F', 'H'}
                and len({'B', 'G', 'F', 'H'}.intersection(items)) == 4):
            self.parameters['gamma'] = self.angle(items['BG'].line(),
                                                  items['FH'].line())
        # angle clark(GN, BG)
        if (updated_point in {'G', 'N', 'B'}
                and len({'G', 'N', 'B'}.intersection(items)) == 3):
            self.parameters['clark'] = self.angle(items['GN'].line(),
                                                  items['BG'].line())
        # w = length/foot width
        if (updated_point in {'Y', "X", "Z", 'H', 'G'}
                and len({'Y', "X", "Z", 'H', 'G'}.intersection(items)) == 5):
            self.parameters['w'] = self.w()
        # chijin = DE/EI
        if (updated_point in {'D', "E"}
                and len({'D', "E", 'I'}.intersection(items)) == 3):
            length_DE = QLineF(items['D'].pos(), items['E'].pos()).length()
            length_EI = QLineF(items['E'].pos(), items['I'].pos()).length()
            self.parameters['chijin'] = length_DE / length_EI

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
            ''')

    def addLine(self, line):
        items = self.scene.itemsDict()
        if line in items:
            self.scene.removeItem(items[line])
        items[line] = self.scene.addLine(
                items[line[0]].x(),
                items[line[0]].y(),
                items[line[1]].x(),
                items[line[1]].y(),
                self.linePen)
        items[line].setToolTip(line)
        items[line].setZValue(1)

    def perpendicularTo(self, point, line):
        angle = line.normalVector().angle()
        perpendicular = QLineF(point.pos(), point.pos() + QPointF(5, 5))
        perpendicular.setAngle(angle)
        return perpendicular

    def lengthFoot(self):
        items = self.scene.itemsDict()
        XY = items['XY'].line()
        # checking which line is longer
        if XY.length() > items["YZ"].line().length():
            # if XY longer than accept it as the length
            length = XY.length()
            # remove perpendicular if it exists
            if 'WZ' in items:
                self.scene.removeItem(items['WZ'])
                self.scene.removeItem(items['WY'])
                del items['WZ']
                del items['WY']
                self.scene.removeItem(items['W'])
                del items['W']
        else:
            # finding perpendicular from Z to XY
            perpendicular = self.perpendicularTo(items['Z'], XY)
            inter_type, intersectionPoint = XY.intersects(perpendicular)
            if inter_type:
                # adding intersection point to the scene
                point = PointItem(intersectionPoint.x(),
                                  intersectionPoint.y(),
                                  3,
                                  self.circlePen,
                                  self.circleBrush)
                self.scene.addItem(point)
                self.updatePoint(point, 'W')
                # adding perpendicular line to the scene
                self.updateLines('W')
                items = self.scene.itemsDict()
                length = items['WY'].line().length()
            else:
                length = XY.length()
        return length / self.parameters['dpmm']

    def widthFoot(self, line):
        return line.length() / self.parameters['dpmm']

    def angle(self, line_a, line_b):
        angle = line_a.angleTo(line_b)
        return min(angle, 360 - angle)

    def w(self):
        return self.parameters['length'] / self.parameters['width foot']

    def plotC(self):
        items = self.scene.itemsDict()
        pos = (items['A'].pos() + items['Y'].pos()) / 2
        point = PointItem(pos.x(), pos.y(), 3, self.circlePen,
                          self.circleBrush, items['XY'])
        self.updatePoint(point, 'C')

    def plotK(self):
        items = self.scene.itemsDict()
        perpendicular = self.perpendicularTo(items['C'], items['XY'].line())
        fh = items['FH'].line()
        inter_type, intersectionPoint = fh.intersects(perpendicular)
        if inter_type:
            point = PointItem(intersectionPoint.x(), intersectionPoint.y(),
                              3, self.circlePen, self.circleBrush, items['FH'])
            self.updatePoint(point, 'K')

    def plotI(self):
        items = self.scene.itemsDict()
        perpendicular = self.perpendicularTo(items['C'], items['XY'].line())
        bg = items['BG'].line()
        inter_type, intersectionPoint = bg.intersects(perpendicular)
        if inter_type:
            point = PointItem(intersectionPoint.x(), intersectionPoint.y(), 3,
                              self.circlePen, self.circleBrush, items['BG'])
            self.updatePoint(point, 'I')

    @Slot()
    def hightlightPoint(self):
        current_text = self.ui.pointsBox.currentText()
        items = self.scene.itemsDict()
        if self.prevPoint in items:
            items[self.prevPoint].setBrush(self.circleBrush)
        if current_text in items:
            items[current_text].setBrush(self.hightlightBrush)
        self.hightlightScheme()
        self.prevPoint = current_text

    @Slot()
    def hightlightScheme(self):
        items = self.schemeScene.itemsDict()
        items[self.prevPoint].setBrush(self.circleBrush)
        items[self.ui.pointsBox.currentText()].setBrush(self.hightlightBrush)
