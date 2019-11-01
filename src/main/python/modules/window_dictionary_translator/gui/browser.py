# -*- coding: utf-8 -*-
# Copyright 2015 Alex Woroschilow (alex.woroschilow@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import Qt


class TranslationWidget(QtWidgets.QTextEdit):
    content = []

    def __init__(self, parent):
        super(TranslationWidget, self).__init__(parent)
        self.setWordWrapMode(QtGui.QTextOption.WordWrap)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.setAcceptRichText(True)
        self.setAcceptDrops(True)
        self.setFontPointSize(14)
        self.setReadOnly(True)

        self.resize(self.sizeHint())

        effect = QtWidgets.QGraphicsDropShadowEffect()
        effect.setBlurRadius(5)
        effect.setOffset(0)

        self.setGraphicsEffect(effect)

    def addTranslation(self, translation):
        self.content.append(translation)
        self.setHtml('<br/>'.join(self.content))

    def setTranslation(self, collection):
        self.content = []
        for translation in collection:
            self.content.append(translation)
        self.setHtml('<br/>'.join(self.content))

    def clear(self):
        self.setHtml('')
        self.content = []

    def setHtml(self, string):
        string = string.replace('<k>', '<h3 style="color: green;">')
        string = string.replace('</k>', '</h3>')
        string = string.replace('<ex>', '<p style="color: #707070;">')
        string = string.replace('</ex>', '</p>')
        string = string.replace('<kref>', '<span>')
        string = string.replace('</kref>', '</span><br/>')

        string = string.replace('<tr>', '<i>')
        string = string.replace('</tr>', '</i><br/>')
        string = string.replace('<c>', '<i>')
        string = string.replace('</c>', '</i>')

        string = string.replace('</dtrn>', '</dtrn><br/>')

        super(TranslationWidget, self).setHtml(string)

    def event(self, QEvent):
        if QEvent.type() == QtCore.QEvent.Enter:
            effect = QtWidgets.QGraphicsDropShadowEffect()
            effect.setColor(QtGui.QColor('#6cccfc'))
            effect.setBlurRadius(20)
            effect.setOffset(0)
            self.setGraphicsEffect(effect)

        if QEvent.type() == QtCore.QEvent.Leave:
            effect = QtWidgets.QGraphicsDropShadowEffect()
            effect.setBlurRadius(5)
            effect.setOffset(0)
            self.setGraphicsEffect(effect)

        return super(TranslationWidget, self).event(QEvent)