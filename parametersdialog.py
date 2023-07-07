from PySide6.QtWidgets import QDialog, QWidget

from ui_parametersdialog import Ui_ParametersDialog

PARAMETERS_MESSAGE = '''Длина стопы: {length:.2f}
Ширина стопы: {width_foot:.2f}
Ширина пятки: {width_heel:.2f}
α: {alpha:.2f}
β: {beta:.2f}
γ: {gamma:.2f}
Угол Кларка: {clark:.2f}
Коэффициент Чижина: {chijin:.2f}
Коэффициент W: {w:.2f}'''


class ParametersDialog(QDialog):
    """
    Foot parameters info dialog.

    Attributes
    ----------
    parameters : dict[str, float]
        Dictinary with foot parameters. Must have keys: 'length', 'width_foot',
        'width_heel', 'alpha', 'beta', 'gamma', 'clark', 'chijin', 'w'.
    parent : QWidjet, optional
        Parent of the dialog.
    """
    def __init__(self, parameters: dict[str, float],
                 parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_ParametersDialog()
        self.ui.setupUi(self)
        self.ui.textEdit.setPlainText(PARAMETERS_MESSAGE.format(**parameters))
