# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGraphicsView, QHBoxLayout,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.actionNewProject = QAction(MainWindow)
        self.actionNewProject.setObjectName(u"actionNewProject")
        self.actionNewProject.setShortcut(QKeySequence.StandardKey.New)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_3 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.leftView = QGraphicsView(self.centralwidget)
        self.leftView.setObjectName(u"leftView")
        self.leftView.viewport().setProperty("cursor", QCursor(Qt.ArrowCursor))
        self.leftView.setMouseTracking(True)
        self.leftView.setInteractive(False)

        self.verticalLayout_2.addWidget(self.leftView)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.leftLoadButton = QPushButton(self.centralwidget)
        self.leftLoadButton.setObjectName(u"leftLoadButton")

        self.horizontalLayout.addWidget(self.leftLoadButton)

        self.leftMarkupButton = QPushButton(self.centralwidget)
        self.leftMarkupButton.setObjectName(u"leftMarkupButton")
        self.leftMarkupButton.setEnabled(False)

        self.horizontalLayout.addWidget(self.leftMarkupButton)

        self.leftParametersButton = QPushButton(self.centralwidget)
        self.leftParametersButton.setObjectName(u"leftParametersButton")
        self.leftParametersButton.setEnabled(False)

        self.horizontalLayout.addWidget(self.leftParametersButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_3.addWidget(self.line)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.rightView = QGraphicsView(self.centralwidget)
        self.rightView.setObjectName(u"rightView")
        self.rightView.viewport().setProperty("cursor", QCursor(Qt.ArrowCursor))
        self.rightView.setMouseTracking(True)
        self.rightView.setInteractive(False)

        self.verticalLayout.addWidget(self.rightView)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.rightLoadButton = QPushButton(self.centralwidget)
        self.rightLoadButton.setObjectName(u"rightLoadButton")

        self.horizontalLayout_2.addWidget(self.rightLoadButton)

        self.rightMarkupButton = QPushButton(self.centralwidget)
        self.rightMarkupButton.setObjectName(u"rightMarkupButton")
        self.rightMarkupButton.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.rightMarkupButton)

        self.rightParametersButton = QPushButton(self.centralwidget)
        self.rightParametersButton.setObjectName(u"rightParametersButton")
        self.rightParametersButton.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.rightParametersButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.horizontalLayout_3.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.actionNewProject)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"ScanStep", None))
        self.actionNewProject.setText(QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439", None))
        self.leftLoadButton.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c", None))
        self.leftMarkupButton.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0430\u0437\u043c\u0435\u0442\u0438\u0442\u044c", None))
        self.leftParametersButton.setText(QCoreApplication.translate("MainWindow", u"\u0425\u0430\u0440\u0430\u043a\u0442\u0435\u0440\u0438\u0441\u0442\u0438\u043a\u0438", None))
        self.rightLoadButton.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c", None))
        self.rightMarkupButton.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0430\u0437\u043c\u0435\u0442\u0438\u0442\u044c", None))
        self.rightParametersButton.setText(QCoreApplication.translate("MainWindow", u"\u0425\u0430\u0440\u0430\u043a\u0442\u0435\u0440\u0438\u0441\u0442\u0438\u043a\u0438", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u0424\u0430\u0439\u043b", None))
    # retranslateUi

