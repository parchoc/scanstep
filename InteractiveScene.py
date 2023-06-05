from PySide6.QtWidgets import QGraphicsScene, QGraphicsItem, QGraphicsEllipseItem
from PySide6.QtCore import Signal, Qt, QPointF
from PySide6.QtGui import QBrush, QPen

class PointItem(QGraphicsEllipseItem):
    def __init__(self, x, y, radius, pen=None, brush=None, parent=None):
        super().__init__(0, 0, radius*2, radius*2, parent)
        self.radius = radius
        if pen:
            self.setPen(pen)
        if brush:
            self.setBrush(brush)
        self.setPos(x, y)
    
    def setPos(self, x, y):
        super().setPos(x - self.radius, y - self.radius)
    
    def pos(self):
        return super().pos() + QPointF(self.radius, self.radius)
    
    def x(self):
        return super().x() + self.radius
    
    def y(self):
        return super().y() + self.radius


class InteractiveScene(QGraphicsScene):
    pointAdded = Signal(QGraphicsItem)

    def __init__(self, width=100, height=100, parent=None, pen=None, brush=None):
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
        self.addPoint(event.scenePos().x(), event.scenePos().y())
        # super().mousePressEvent(event)
        event.accept()
    
    def addPoint(self, x, y, pen=None, brush=None):
        if pen and brush:
            item = PointItem(x, y, 3, pen, brush)
        else:
            item = PointItem(x, y, 3, self.circlePen, self.circleBrush)
        self.addItem(item)
        self.pointAdded.emit(item)
        return item
