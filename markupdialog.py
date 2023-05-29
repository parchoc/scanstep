from PySide6.QtCore import Slot
from ui_markupdialog import Ui_MarkupDialog
from PySide6.QtWidgets import QDialog

class MarkupDialog(QDialog):
    def __init__(self, parent) -> None:
        super(MarkupDialog, self).__init__(parent)
        self.ui = Ui_MarkupDialog()
        self.ui.setupUi(self)
