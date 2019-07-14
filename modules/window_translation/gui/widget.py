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
import inject
import functools
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from .suggestions import TranslationListWidget
from .browser import TranslationWidget
from .text import SearchField
from .button import PictureButtonFlat


class TranslatorContainerDescription(QtWidgets.QWidget):
    settings = QtCore.pyqtSignal(object)
    search = QtCore.pyqtSignal(object)

    def __init__(self):
        super(TranslatorContainerDescription, self).__init__()
        self.setLayout(QtWidgets.QGridLayout())

        self.text = SearchField(self)
        self.text.returnPressed.connect(lambda x=None: self.search.emit(self.text.text()))
        self.layout().addWidget(self.text, 0, 0, 1, 19)

        settings = PictureButtonFlat(QtGui.QIcon("icons/settings"))
        settings.clicked.connect(lambda event=None: self.settings.emit(settings))
        self.layout().addWidget(settings, 0, 19)

        self.translation = TranslationWidget(self)
        self.translation.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.layout().addWidget(self.translation, 1, 0, 1, 20)

    def clean(self):
        self.translation.clear()

    def append(self, translation=None, progress=None):
        self.translation.addTranslation(translation)

    def replace(self, collection):
        self.translation.setTranslation(collection)


class TranslatorWidget(QtWidgets.QWidget):
    translationClear = QtCore.pyqtSignal(object)
    translationReplace = QtCore.pyqtSignal(object)
    translationAppend = QtCore.pyqtSignal(str, int)
    translationRequest = QtCore.pyqtSignal(object)
    translationSuggestion = QtCore.pyqtSignal(object)

    suggestionClean = QtCore.pyqtSignal(object)
    suggestionFinished = QtCore.pyqtSignal(object)
    suggestionAppend = QtCore.pyqtSignal(object)

    settings = QtCore.pyqtSignal(object)

    def __init__(self):
        super(TranslatorWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)

        self.suggestions = TranslationListWidget(self)
        self.suggestions.selected.connect(self.translationSuggestion.emit)

        self.translations = TranslatorContainerDescription()
        self.translations.search.connect(self.translationRequest.emit)
        self.translations.settings.connect(self.settings.emit)

        self.translationClear.connect(self.translations.clean)
        self.suggestionClean.connect(self.suggestions.clean)
        self.translationAppend.connect(self.translations.append)
        self.suggestionAppend.connect(self.suggestions.append)
        self.translationReplace.connect(self.translations.replace)

        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        splitter = QtWidgets.QSplitter(self)
        splitter.setContentsMargins(0, 0, 0, 0)
        splitter.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        splitter.addWidget(self.suggestions)
        splitter.addWidget(self.translations)

        splitter.setStretchFactor(1, 2)
        splitter.setStretchFactor(2, 3)

        self.layout.addWidget(splitter, 1, 0)

    @inject.params(statusbar='widget.statusbar')
    def finished(self, progress=None, statusbar=None):
        model = self.suggestions.model()
        if model is None:
            return None

        statusbar.text('{} words found'.format(model.rowCount()))
