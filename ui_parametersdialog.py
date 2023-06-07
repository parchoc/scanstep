# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ParametersDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QPushButton,
    QSizePolicy, QSpacerItem, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_ParametersDialog(object):
    def setupUi(self, ParametersDialog):
        if not ParametersDialog.objectName():
            ParametersDialog.setObjectName(u"ParametersDialog")
        ParametersDialog.resize(263, 332)
        self.verticalLayout = QVBoxLayout(ParametersDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.textEdit = QTextEdit(ParametersDialog)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setReadOnly(True)

        self.verticalLayout.addWidget(self.textEdit)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton = QPushButton(ParametersDialog)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(ParametersDialog)
        self.pushButton.clicked.connect(ParametersDialog.close)

        QMetaObject.connectSlotsByName(ParametersDialog)
    # setupUi

    def retranslateUi(self, ParametersDialog):
        ParametersDialog.setWindowTitle(QCoreApplication.translate("ParametersDialog", u"Dialog", None))
        self.pushButton.setText(QCoreApplication.translate("ParametersDialog", u"Ok", None))
    # retranslateUi

