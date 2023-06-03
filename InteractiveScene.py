from PySide6.QtWidgets import QGraphicsScene, QGraphicsItem
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QBrush, QPen

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
            item = self.addEllipse(0, 0, 6, 6, pen, brush)
        else:
            item = self.addEllipse(0, 0, 6, 6, self.circlePen, self.circleBrush)
        item.setPos(x - 3, y - 3)
        self.pointAdded.emit(item)
        return item
