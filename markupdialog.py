from PySide6.QtCore import QLineF, QPointF, Qt, Signal, Slot
from PySide6.QtGui import QBrush, QPen, QPixmap
from PySide6.QtWidgets import (QDialog, QGraphicsItem, QGraphicsLineItem,
                               QGraphicsScene, QWidget)

import res
from InteractiveScene import InteractiveScene, PointItem
from ui_markupdialog import Ui_MarkupDialog

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

# parents of the points {child: parent}
PARENTS = {
    'A': 'XY',
    'C': 'XY',
    'D': 'IK',
    'E': 'IK',
    'I': 'BG',
    'K': 'FH',
}

# points positions on the scheme
SCHEME = {
    'Y': (171, 502),
    'X': (136, 25),
    "Z": (189, 21),
    'F': (84, 425),
    'H': (22, 195),
    'B': (235, 433),
    "G": (246, 148),
    'A': (141, 86),
    'D': (49, 296),
    'E': (127, 295),
    'L': (232, 66),
    'M': (27, 131),
    'N': (139, 207),
    # 'K': (49, 296),
    # 'I': (240, 291),
}

PARAMETERS_MESSAGE = '''Длина стопы: {length:.2f}
Ширина стопы: {width_foot:.2f}
Ширина пятки: {width_heel:.2f}
α: {alpha:.2f}
β: {beta:.2f}
γ: {gamma:.2f}
Угол Кларка: {clark:.2f}
Коэффициент Чижина: {chijin:.2f}
Коэффициент w: {w:.2f}'''


class MarkupDialog(QDialog):
    """
    Markup dialog widget for foot markup.

    Attributes
    ----------
    parent : QWidget, optional
        Object parent widget.
    scene : QGraphicsScene, optional
        Scene for markup scene initializing.
        Add pixmaps, lines and points from `scene` to the markup scene.
    parameters : dict[str, float], optional
        Foot parameters.
    """

    markupDone = Signal(QGraphicsScene, dict)

    def __init__(self, parent: type[QWidget] | None = None,
                 scene: type[QGraphicsScene] | None = None,
                 parameters: dict[str, float] | float = None) -> None:
        super(MarkupDialog, self).__init__(parent)
        self.ui = Ui_MarkupDialog()
        self.ui.setupUi(self)
        if scene:
            self.scene = InteractiveScene(scene.width(), scene.height())
        else:
            self.scene = InteractiveScene()
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
        # adding items to the scene
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
        """Emit signal with `scene` and `parameters`."""
        # recolor hightlighted point before sending scene
        items = self.scene.itemsDict()
        if self.prevPoint in items:
            items[self.prevPoint].setBrush(self.circleBrush)
        self.markupDone.emit(self.scene, self.parameters)

    def glueTo(self, point: PointItem, line_item: QGraphicsLineItem) -> None:
        """
        Move given point to the closest point on the line.

        Find closest point on the `line_item` from the given `point`
        by plotting perpendicular. Than move `point` to the
        intersection point and set `line_item` as parent.

        Parameters
        ----------
        point : PointItem
            Point to move.
        line_item : QGraphicsLineItem
            Line on which move point.
        """
        line = line_item.line()
        perpendicular = self.perpendicularTo(point, line)
        _, intersectionPoint = line.intersects(perpendicular)
        point.setPos(intersectionPoint.x(), intersectionPoint.y())
        point.setParentItem(line_item)

    @Slot(QGraphicsItem)
    def updateGlobal(self, item: type[QGraphicsItem]) -> None:
        """
        Update connected items on the scene when user add new point.

        Parameters
        ----------
        item : QGraphicsItem
            Added item.
        """
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
    def updatePoint(self, point: PointItem, name: str) -> None:
        """
        Remove old point if the new one with the same name was added.

        Point z value set as 2.

        Parameters
        ----------
        point : PointItem
            Added point.
        name : str
            Added point name.
        """
        # remove previous point if it exist
        items = self.scene.itemsDict()
        if name in items:
            self.scene.removeItem(items[name])
        # add new point to dict
        point.setToolTip(name)
        point.setZValue(2)

    @Slot(str)
    def updateLines(self, updated_point: str) -> None:
        """
        Plot lines connected to the updated point.

        Parameters
        ----------
        updated_point : str
            Point name.
        """
        items = self.scene.itemsDict()
        # go thro all points connected to updated_point
        for point in CONNECTIONS[updated_point]:
            # if connected point exists than build line
            if point in items:
                line = ''.join(sorted(updated_point + point))
                # remove old line if it exists
                self.addLine(line)

    @Slot(str)
    def updateParameters(self, updated_point: str) -> None:
        """
        Compute parameters, points and lines that depend on the updated point.

        List of dependencies:
        * C - A, Y;
        * I - A, B, G, Y;
        * K - A, F, H, Y;
        * IK - A, B, F, H, G, Y;
        * length - X, Y, Z;
        * foot width - H, G;
        * heel width - B, F;
        * alpha - B, G, L;
        * beta - F, H, M;
        * gamma - B, G, F, H;
        * clark - B, G, N;
        * w - G, H, X, Y, Z;
        * chikin - D, E.

        Parameters
        ----------
        updated_point : str
            Point name.
        """
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
            self.parameters['width_foot'] = self.widthFoot(items['GH'].line())
        # heel width
        if (updated_point in {'B', 'F'}
                and len({'B', 'F'}.intersection(items)) == 2):
            self.parameters['width_heel'] = self.widthFoot(items['BF'].line())
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
            gb = QLineF(
                items['G'].pos(),
                items['B'].pos()
            )
            self.parameters['clark'] = self.angle(items['GN'].line(), gb)
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
    def updateParametersDisplay(self) -> None:
        """Update parameters display."""
        self.ui.parametersDisplay.setPlainText(
            PARAMETERS_MESSAGE.format(**self.parameters))

    def addLine(self, line: str) -> None:
        """
        Add line to the scene.

        Scene must have all points from which line name consists.
        Line z-value is 1.

        Parameters
        ----------
        line : str
            Line name. Must be two charecters.
        """
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

    def perpendicularTo(self, point: PointItem, line: QLineF) -> QLineF:
        """
        Find perpendicular from the point to the line.

        Parameters
        ----------
        point : PointItem
            The point from which find the perpendicular.
        line : QLineF
            The line to which find the perpendicular.

        Returns
        -------
        perpendicular : QLineF
            Perpendicular line from the point to the line.
        """
        angle = line.normalVector().angle()
        perpendicular = QLineF(point.pos(), point.pos() + QPointF(5, 5))
        perpendicular.setAngle(angle)
        return perpendicular

    def lengthFoot(self) -> float:
        """
        Compute foot length.

        Length is equal to XY if XY > YZ. Otherwise, a perpendicular is
        plotted from point Z to XY. They intersection point is called
        W and WY accepted as foot length. Foot length converted from
        pixels to mm by divading on the image dpmm value.

        Returns
        -------
        length : float
            Foot length in mm.
        """
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

    def widthFoot(self, line: QLineF) -> float:
        """
        Convert line length from pixels to mm.

        Divide line length on image dpmm value for conversion.

        Parameters
        ----------
        line : QLineF
            Line.

        Returns
        -------
        float
            Line length in mm.
        """
        return line.length() / self.parameters['dpmm']

    def angle(self, line_a: QLineF, line_b: QLineF) -> float:
        """
        Compute minimal angle between two lines.

        Calculate angle without considering the line direction.
        Returned value can't be greater than 360 or lower than 0.

        Parameters
        ----------
        line_a : QLineF
            First line.
        line_b : QLineF
            Second line.

        Returns
        -------
        angle : float
            Angle between lines in degrees.
        """
        angle = line_a.angleTo(line_b)
        return min(angle, 360 - angle)

    def w(self) -> float:
        """
        Compute w coefficient.

        w coefficient is equal to: foot_length / foot_width.

        Returns
        ------
        float
            w coefficient.
        """
        return self.parameters['length'] / self.parameters['width_foot']

    def plotC(self) -> None:
        """
        Add C point to the scene.

        С point is located in the middle of the AY line.
        """
        items = self.scene.itemsDict()
        pos = (items['A'].pos() + items['Y'].pos()) / 2
        point = PointItem(pos.x(), pos.y(), 3, self.circlePen,
                          self.circleBrush, items['XY'])
        self.updatePoint(point, 'C')

    def plotK(self) -> None:
        """
        Add K point to the scene.

        K point is located on the intersection between perpendicular from C to
        HF.
        """
        items = self.scene.itemsDict()
        perpendicular = self.perpendicularTo(items['C'], items['XY'].line())
        fh = items['FH'].line()
        inter_type, intersectionPoint = fh.intersects(perpendicular)
        if inter_type:
            point = PointItem(intersectionPoint.x(), intersectionPoint.y(),
                              3, self.circlePen, self.circleBrush, items['FH'])
            self.updatePoint(point, 'K')

    def plotI(self) -> None:
        """
        Add I point to the scene.

        I point is located on the intersection between perpendicular from C to
        BG.
        """
        items = self.scene.itemsDict()
        perpendicular = self.perpendicularTo(items['C'], items['XY'].line())
        bg = items['BG'].line()
        inter_type, intersectionPoint = bg.intersects(perpendicular)
        if inter_type:
            point = PointItem(intersectionPoint.x(), intersectionPoint.y(), 3,
                              self.circlePen, self.circleBrush, items['BG'])
            self.updatePoint(point, 'I')

    @Slot()
    def hightlightPoint(self) -> None:
        """
        Hightlight current point if it exists. Currrent point is equal to the
        current value in `pointsBox` widget.
        """
        current_text = self.ui.pointsBox.currentText()
        items = self.scene.itemsDict()
        if self.prevPoint in items:
            items[self.prevPoint].setBrush(self.circleBrush)
        if current_text in items:
            items[current_text].setBrush(self.hightlightBrush)
        self.hightlightScheme()
        self.prevPoint = current_text

    @Slot()
    def hightlightScheme(self) -> None:
        """
        Hightlight current point on the example scheme.
        Currrent point is equal to the current value in `pointsBox` widget.
        """
        items = self.schemeScene.itemsDict()
        items[self.prevPoint].setBrush(self.circleBrush)
        items[self.ui.pointsBox.currentText()].setBrush(self.hightlightBrush)
