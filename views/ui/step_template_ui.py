# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'step_template.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_StepTemplate(object):
    def setupUi(self, StepTemplate):
        if not StepTemplate.objectName():
            StepTemplate.setObjectName(u"StepTemplate")
        StepTemplate.resize(796, 551)
        self.verticalLayout = QVBoxLayout(StepTemplate)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.stepTitleLabel = QLabel(StepTemplate)
        self.stepTitleLabel.setObjectName(u"stepTitleLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stepTitleLabel.sizePolicy().hasHeightForWidth())
        self.stepTitleLabel.setSizePolicy(sizePolicy)
        self.stepTitleLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)

        self.verticalLayout.addWidget(self.stepTitleLabel)

        self.stepSubtitleLabel = QLabel(StepTemplate)
        self.stepSubtitleLabel.setObjectName(u"stepSubtitleLabel")
        sizePolicy.setHeightForWidth(self.stepSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.stepSubtitleLabel.setSizePolicy(sizePolicy)
        self.stepSubtitleLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)

        self.verticalLayout.addWidget(self.stepSubtitleLabel)

        self.stepFrame = QFrame(StepTemplate)
        self.stepFrame.setObjectName(u"stepFrame")
        self.stepFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.stepFrame.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.stepFrame)


        self.retranslateUi(StepTemplate)

        QMetaObject.connectSlotsByName(StepTemplate)
    # setupUi

    def retranslateUi(self, StepTemplate):
        StepTemplate.setWindowTitle(QCoreApplication.translate("StepTemplate", u"Form", None))
        self.stepTitleLabel.setText(QCoreApplication.translate("StepTemplate", u"Step Label", None))
        self.stepSubtitleLabel.setText(QCoreApplication.translate("StepTemplate", u"Subtitle Label", None))
    # retranslateUi

