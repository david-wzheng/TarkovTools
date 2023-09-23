# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PowerSearch.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
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
from PySide6.QtWidgets import (QApplication, QLineEdit, QListWidget, QListWidgetItem,
    QMainWindow, QSizePolicy, QWidget)

class Ui_PowerSearch(object):
    def setupUi(self, PowerSearch):
        if not PowerSearch.objectName():
            PowerSearch.setObjectName(u"PowerSearch")
        PowerSearch.resize(364, 439)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PowerSearch.sizePolicy().hasHeightForWidth())
        PowerSearch.setSizePolicy(sizePolicy)
        PowerSearch.setMinimumSize(QSize(364, 439))
        PowerSearch.setMaximumSize(QSize(364, 480))
        self.centralwidget = QWidget(PowerSearch)
        self.centralwidget.setObjectName(u"centralwidget")
        self.Search = QLineEdit(self.centralwidget)
        self.Search.setObjectName(u"Search")
        self.Search.setGeometry(QRect(10, 10, 341, 21))
        self.Search.setClearButtonEnabled(True)
        self.Results = QListWidget(self.centralwidget)
        self.Results.setObjectName(u"Results")
        self.Results.setGeometry(QRect(10, 40, 341, 391))
        sizePolicy.setHeightForWidth(self.Results.sizePolicy().hasHeightForWidth())
        self.Results.setSizePolicy(sizePolicy)
        self.Results.setMinimumSize(QSize(0, 0))
        self.Results.setMaximumSize(QSize(349, 391))
        PowerSearch.setCentralWidget(self.centralwidget)

        self.retranslateUi(PowerSearch)

        QMetaObject.connectSlotsByName(PowerSearch)
    # setupUi

    def retranslateUi(self, PowerSearch):
        PowerSearch.setWindowTitle(QCoreApplication.translate("PowerSearch", u"Power Search", None))
        self.Search.setText(QCoreApplication.translate("PowerSearch", u"Search by Id, name, or localized name", None))
    # retranslateUi

