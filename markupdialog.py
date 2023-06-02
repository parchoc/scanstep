from PySide6.QtCore import Slot, Signal
from ui_markupdialog import Ui_MarkupDialog
from PySide6.QtWidgets import QDialog, QGraphicsItem, QGraphicsScene
from InteractiveScene import InteractiveScene
from PySide6.QtGui import QBrush

class MarkupDialog(QDialog):
    markupDone = Signal(QGraphicsScene, dict)
    
    def __init__(self, parent=None, backgroundImage=None, points=None) -> None:
        super(MarkupDialog, self).__init__(parent)
        self.ui = Ui_MarkupDialog()
        self.ui.setupUi(self)
        self.scene = InteractiveScene(backgroundImage.width(), backgroundImage.height())
        self.points = {}
        # adding background image from initial scene
        if backgroundImage:
            self.scene.setBackgroundBrush(QBrush(backgroundImage))
        # adding point items from initial scene
        if points:
            for key, item in points.items():
                self.points[key] = self.scene.addPoint(item.x(), item.y())
                self.points[key].setToolTip(key)
        self.ui.markupView.setScene(self.scene)
        # connections
        self.accepted.connect(self.sendScene)
        self.scene.pointAdded.connect(self.updatePointsDict)

    @Slot()
    def sendScene(self):
        self.markupDone.emit(self.scene, self.points)

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
