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
import os
import functools

from PyQt5 import QtWidgets as QtGui
from PyQt5 import QtCore

from .bar import ToolbarWidget
from .bar import StatusbarWidget
from .list import TranslationListWidget
from .browser import TranslationWidget


class TranslatorWidget(QtGui.QWidget):
    _bright = False
    _actions = False

    def __init__(self):
        """

        :param actions: 
        """
        super(TranslatorWidget, self).__init__()
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

        self.toolbar = ToolbarWidget()
        self.status = StatusbarWidget()

        self.translation = TranslationWidget(self)
        self.translations = TranslationListWidget(self)

        self.layout = QtGui.QVBoxLayout(self)
        self.layout.addWidget(self.toolbar, -1)

        splitter = QtGui.QSplitter(self)
        splitter.addWidget(self.translations)
        splitter.addWidget(self.translation)
        self.layout.addWidget(splitter, 1)

        self.layout.addWidget(self.status, -1)

    def cleanTranslation(self):
        """
        
        :return: 
        """
        self.translation.cleanTranslation()

    def addTranslation(self, translation):
        """
        
        :param translation: 
        :return: 
        """
        self.translation.addTranslation(translation)

    def setTranslation(self, collection):
        """
        
        :param translation: 
        :return: 
        """
        self.translation.setTranslation(collection)

    def setSuggestions(self, suggestions):
        """

        :param translation: 
        :return: 
        """
        self.translations.setSuggestions(suggestions)
        self.status.text('Total: %s words(s)' % self.translations.model().rowCount())

    def onSearchString(self, action):
        """
        
        :param action: 
        :return: 
        """
        self.toolbar.onActionSearch(functools.partial(
            self._onSearchString, action=action, textfield=(self.toolbar.search)
        ))

    def _onSearchString(self, action, textfield):
        """
        
        :param event: 
        :return: 
        """
        if action is not None:
            action(textfield.text())

    def onSuggestionSelected(self, action):
        """
        
        :param action: 
        :return: 
        """
        self.translations.selectionChanged = functools.partial(
            self._onSuggestionSelected, action=(action)
        )

    def _onSuggestionSelected(self, current, previous, action):
        for index in self.translations.selectedIndexes():
            entity = self.translations.model().itemFromIndex(index)
            if action is not None:
                action(entity.text())

    def onActionLoadStart(self, progress):
        """

        :param progress: 
        :return: 
        """
        self.status.start(progress)

    def onActionLoadProgress(self, progress):
        """

        :param progress: 
        :return: 
        """
        self.status.setProgress(progress)

        if self._bright == True:
            return self.preview.layout(4)

        if len(self.preview.widgets) <= self.preview._rows:
            return self.preview.layout(1)
        return self.preview.layout(2)

    def onActionLoadStop(self, progress):
        """

        :param progress: 
        :return: 
        """
        self.status.stop(progress)
        message = '%s document(s)' % len(self.preview.widgets)
        self.status.text('Total: %s' % message)

        if self._bright == True:
            return self.preview.layout(4)

        if len(self.preview.widgets) <= self.preview._rows:
            return self.preview.layout(1)
        return self.preview.layout(2)