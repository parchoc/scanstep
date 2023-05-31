from PySide6.QtCore import Slot, Signal
from ui_markupdialog import Ui_MarkupDialog
from PySide6.QtWidgets import QDialog, QGraphicsScene
from InteractiveScene import InteractiveScene

class MarkupDialog(QDialog):
    markupDone = Signal(QGraphicsScene)
    
    def __init__(self, parent, scene) -> None:
        super(MarkupDialog, self).__init__(parent)
        self.ui = Ui_MarkupDialog()
        self.ui.setupUi(self)
        self.scene = InteractiveScene(scene=scene)
        self.ui.markupView.setScene(self.scene)
        self.ui.buttonBox.accepted.connect(self.sendScene)

    @Slot()
    def sendScene(self):
        self.markupDone.emit(self.scene)
