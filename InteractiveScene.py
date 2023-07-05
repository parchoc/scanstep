from PySide6.QtCore import QObject, QPointF, Qt, Signal
from PySide6.QtGui import QBrush, QPen
from PySide6.QtWidgets import (QGraphicsEllipseItem, QGraphicsItem,
                               QGraphicsScene)


class PointItem(QGraphicsEllipseItem):
    """
    QGraphicsEllipseItem subclass for circles.

    Override coordinates functions.
    The current coordinates of the item refer to the center of the circle
    rather then upper left corner.

    Attributes
    ----------
    x : float
        x coordinate of the circle center.
    y : float
        y coordinate of the circle center.
    radius : float
        Circle radius in pixels.
    pen : QPen, optional
        QPen for painting circle line.
    brush : QBrush, optional
        QBrush for filling the circle.
    parent : QGraphicsItem, optional
        Parent item for the circle.
    """

    def __init__(self, x: float, y: float, radius: float, pen: QPen = None,
                 brush: QBrush = None, parent: QGraphicsItem = None) -> None:
        super().__init__(0, 0, radius*2, radius*2, parent)
        self.radius = radius
        if pen:
            self.setPen(pen)
        if brush:
            self.setBrush(brush)
        self.setPos(x, y)

    def setPos(self, x: float, y: float) -> None:
        """
        Set circle center to the given `x` and `y` coordinates.

        Parameters
        ----------
        x : float
            New x coordinate of the circle center.
        y : float
            New y coordinate of the circle center.
        """
        super().setPos(x - self.radius, y - self.radius)

    def pos(self) -> QPointF:
        """
        Return circle center coordinates.

        Returns
        -------
        QPointF
        """
        return super().pos() + QPointF(self.radius, self.radius)

    def x(self) -> float:
        """Return x coordinate of the circle center."""
        return super().x() + self.radius

    def y(self) -> float:
        """Return y coordinate of the circle center."""
        return super().y() + self.radius

    def type(self) -> int:
        return 65537


class InteractiveScene(QGraphicsScene):
    """
    QGraphicsScene subclass. Add points to the scene by clicking on it.

    Attributes
    ----------
    width : int
        Scene width in pixels.
    height: int
        Scene height in pixels.
    parent : QObject, optional
        Scene parent object.
    pen : QPen, optional
        Pen for painting PointItem. Default is black with width 2.
    brush : QBrush, optional
        Brush for painting PointItem. Default is red.
    """

    pointAdded = Signal(QGraphicsItem)

    def __init__(self, width: int = 100, height: int = 100,
                 parent: QObject | None = None, pen: QPen | None = None,
                 brush: QBrush | None = None) -> None:
        super().__init__(0, 0, width, height, parent)
        if pen:
            self.circlePen = pen
        else:
            self.circlePen = QPen()
            self.circlePen.setWidth(2)
        if brush:
            self.circleBrush = brush
        else:
            self.circleBrush = QBrush(Qt.GlobalColor.red)

    def mousePressEvent(self, event) -> None:
        """Add PointItem to the scene by click coordinates."""
        self.addPoint(event.scenePos().x(), event.scenePos().y(), 3)
        event.accept()

    def addPoint(self, x: float, y: float, radius: float,
                 pen: QPen | None = None,
                 brush: QBrush | None = None) -> PointItem:
        """
        Add PointItem to the scene.

        Parameters
        ----------
        x : float
            x coordinate of the PointItem.
        y : float
            y coordinate of the PointItem.
        radius : float
            PointItem radius in pixels.
        pen : QPen, optional
            Pen for painting PointItem. By default use scene `pen`.
        brush : QBrush, optional
            Brush for painting PointItem. By default use scene `brush`.

        Returns
        -------
        item : PointItem
            Created item.
        """
        if pen and brush:
            item = PointItem(x, y, radius, pen, brush)
        else:
            item = PointItem(x, y, radius, self.circlePen, self.circleBrush)
        self.addItem(item)
        self.pointAdded.emit(item)
        return item

    def itemsDict(self) -> dict[str, type[QGraphicsItem]]:
        """
        Construct dictinary with scene items.

        Dictinary keys are equal to items tool tips and values are items
        themself.

        Returns
        -------
        items : dict[str, QGraphicsItem]
        """
        items = {}
        for item in self.items():
            items[item.toolTip()] = item
        return items
