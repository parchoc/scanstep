from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtGui import QPen, QBrush
from PySide6.QtCore import Qt

class InteractiveScene(QGraphicsScene):
    def __init__(self, width=100, height=100, parent=None, scene=None):
        if scene:
            super().__init__(0, 0, scene.width(), scene.height(), parent)
            for item in scene.items():
                self.addItem(item)
        else:
            super().__init__(0, 0, width, height, parent)
        self.circlePen = QPen()
        self.circlePen.setWidth(2)
        self.circleBrush = QBrush(Qt.GlobalColor.red)

    def mousePressEvent(self, event) -> None:
        self.addPoint(event)
        # super().mousePressEvent(event)
        event.accept()
    
    def addPoint(self, event):
        self.addEllipse(
            event.scenePos().x(), 
            event.scenePos().y(),
            5,
            5, 
            self.circlePen,
            self.circleBrush
            )
