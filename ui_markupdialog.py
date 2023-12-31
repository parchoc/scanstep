# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MarkupDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QFrame, QGraphicsView, QHBoxLayout,
    QSizePolicy, QTextEdit, QVBoxLayout, QWidget)
from interactiveview import InteractiveView

class Ui_MarkupDialog(object):
    def setupUi(self, MarkupDialog):
        if not MarkupDialog.objectName():
            MarkupDialog.setObjectName(u"MarkupDialog")
        MarkupDialog.resize(800, 800)
        MarkupDialog.setModal(True)
        self.verticalLayout_2 = QVBoxLayout(MarkupDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.pointsBox = QComboBox(MarkupDialog)
        self.pointsBox.addItem("")
        self.pointsBox.addItem("")
        self.pointsBox.addItem("")
        self.pointsBox.addItem("")
        self.pointsBox.addItem("")
        self.pointsBox.addItem("")
        self.pointsBox.addItem("")
        self.pointsBox.addItem("")
        self.pointsBox.addItem("")
        self.pointsBox.addItem("")
        self.pointsBox.addItem("")
        self.pointsBox.addItem("")
        self.pointsBox.addItem("")
        self.pointsBox.setObjectName(u"pointsBox")

        self.verticalLayout_2.addWidget(self.pointsBox)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.schemeView = InteractiveView(MarkupDialog)
        self.schemeView.setObjectName(u"schemeView")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.schemeView.sizePolicy().hasHeightForWidth())
        self.schemeView.setSizePolicy(sizePolicy)
        self.schemeView.setInteractive(False)

        self.verticalLayout.addWidget(self.schemeView)

        self.parametersDisplay = QTextEdit(MarkupDialog)
        self.parametersDisplay.setObjectName(u"parametersDisplay")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.parametersDisplay.sizePolicy().hasHeightForWidth())
        self.parametersDisplay.setSizePolicy(sizePolicy1)
        self.parametersDisplay.setReadOnly(True)

        self.verticalLayout.addWidget(self.parametersDisplay)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.line = QFrame(MarkupDialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.markupView = InteractiveView(MarkupDialog)
        self.markupView.setObjectName(u"markupView")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.markupView.sizePolicy().hasHeightForWidth())
        self.markupView.setSizePolicy(sizePolicy2)
        self.markupView.viewport().setProperty("cursor", QCursor(Qt.CrossCursor))

        self.horizontalLayout.addWidget(self.markupView)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(MarkupDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_2.addWidget(self.buttonBox)


        self.retranslateUi(MarkupDialog)
        self.buttonBox.accepted.connect(MarkupDialog.accept)
        self.buttonBox.rejected.connect(MarkupDialog.reject)

        QMetaObject.connectSlotsByName(MarkupDialog)
    # setupUi

    def retranslateUi(self, MarkupDialog):
        MarkupDialog.setWindowTitle(QCoreApplication.translate("MarkupDialog", u"Dialog", None))
        self.pointsBox.setItemText(0, QCoreApplication.translate("MarkupDialog", u"Y", None))
        self.pointsBox.setItemText(1, QCoreApplication.translate("MarkupDialog", u"X", None))
        self.pointsBox.setItemText(2, QCoreApplication.translate("MarkupDialog", u"Z", None))
        self.pointsBox.setItemText(3, QCoreApplication.translate("MarkupDialog", u"G", None))
        self.pointsBox.setItemText(4, QCoreApplication.translate("MarkupDialog", u"H", None))
        self.pointsBox.setItemText(5, QCoreApplication.translate("MarkupDialog", u"B", None))
        self.pointsBox.setItemText(6, QCoreApplication.translate("MarkupDialog", u"F", None))
        self.pointsBox.setItemText(7, QCoreApplication.translate("MarkupDialog", u"A", None))
        self.pointsBox.setItemText(8, QCoreApplication.translate("MarkupDialog", u"D", None))
        self.pointsBox.setItemText(9, QCoreApplication.translate("MarkupDialog", u"E", None))
        self.pointsBox.setItemText(10, QCoreApplication.translate("MarkupDialog", u"L", None))
        self.pointsBox.setItemText(11, QCoreApplication.translate("MarkupDialog", u"M", None))
        self.pointsBox.setItemText(12, QCoreApplication.translate("MarkupDialog", u"N", None))

    # retranslateUi

