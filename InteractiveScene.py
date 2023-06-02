from PySide6.QtWidgets import QGraphicsScene, QGraphicsItem, QGraphicsEllipseItem
from PySide6.QtGui import QPen, QBrush
from PySide6.QtCore import Qt, Signal

class InteractiveScene(QGraphicsScene):
    pointAdded = Signal(QGraphicsItem)

    def __init__(self, width=100, height=100, parent=None):
        super().__init__(0, 0, width, height, parent)
        self.circlePen = QPen()
        self.circlePen.setWidth(2)
        self.circleBrush = QBrush(Qt.GlobalColor.red)
        self.linePen = QPen()
        self.linePen.setColor(Qt.GlobalColor.red)
        self.linePen.setWidth(2)

    def mousePressEvent(self, event) -> None:
        self.addPoint(event.scenePos().x(), event.scenePos().y())
        # super().mousePressEvent(event)
        event.accept()
    
    def addPoint(self, x, y):
        item = self.addEllipse(0, 0, 6, 6, self.circlePen, self.circleBrush)
        item.setPos(x - 3, y - 3)
        self.pointAdded.emit(item)
        return item
