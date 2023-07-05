from PySide6.QtWidgets import QDialog, QWidget

from ui_parametersdialog import Ui_ParametersDialog


class ParametersDialog(QDialog):
    """
    Foot parameters info dialog.

    Attributes
    ----------
    parameters : dict[str, float]
        Dictinary with foot parameters. Must have keys: 'length', 'width foot',
        'width heel', 'alpha', 'beta', 'gamma', 'clark', 'chijin', 'w'.
    parent : QWidjet, optional
        Parent of the dialog.
    """
    def __init__(self, parameters: dict[str, float],
                 parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_ParametersDialog()
        self.ui.setupUi(self)
        self.ui.textEdit.setPlainText(
            f'''
            Длина стопы: {parameters['length']:.2f}
            Ширина стопы: {parameters['width foot']:.2f}
            Ширина пятки: {parameters['width heel']:.2f}
            α: {parameters['alpha']:.2f}
            β: {parameters['beta']:.2f}
            γ: {parameters['gamma']:.2f}
            Угол Кларка: {parameters['clark']:.2f}
            Коэффициент Чижина: {parameters['chijin']:.2f}
            Коэффициент w: {parameters['w']:.2f}
            ''')
