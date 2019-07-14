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

from .gui.widget import HistoryWidget
from .service import SQLiteHistory
from .actions import HistoryActions


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    actions = HistoryActions()

    @inject.params(config='config')
    def _constructor(self, config=None):
        return SQLiteHistory()

    @inject.params(history='history', window='window')
    def _provider(self, history, window):
        widget = HistoryWidget()

        widget.reload = functools.partial(self.actions.onActionReload, widget=widget)
        widget.table.keyReleaseEvent = functools.partial(widget.table.keyReleaseEvent,
                                                         action_remove=self.actions.onActionUpdate)

        action = functools.partial(self.actions.onActionExportCsv, widget=widget)
        widget.toolbar.csv.triggered.connect(action)

        action = functools.partial(self.actions.onActionExportAnki, widget=widget)
        widget.toolbar.anki.triggered.connect(action)

        action = functools.partial(self.actions.onActionHistoryClean, widget=widget)
        widget.toolbar.clean.triggered.connect(action)

        action = functools.partial(widget.table.onActionHistoryUpdate, action=self.actions.onActionUpdate)
        widget.table.itemChanged.connect(action)

        action = functools.partial(widget.table.onActionMenuClean, action=self.actions.onActionUpdate)
        widget.table.clean.triggered.connect(action)

        action = functools.partial(widget.table.onActionMenuRemove, action=self.actions.onActionRemove)
        widget.table.remove.triggered.connect(action)

        widget.history(history.history, history.count())

        return widget

    @inject.params(config='config')
    def _widget_settings(self, config=None):
        from .gui.settings.widget import SettingsWidget

        widget = SettingsWidget()

        return widget

    def enabled(self, options=None, args=None):
        if hasattr(self._options, 'converter'):
            return not self._options.converter
        return True

    def configure(self, binder, options=None, args=None):
        binder.bind_to_constructor('history', self._constructor)
        binder.bind_to_constructor('widget.history', self._provider)

    @inject.params(window='window', widget='widget.history', factory='settings.factory')
    def boot(self, options, args, window=None, widget=None, factory=None):
        factory.addWidget((self._widget_settings, 2))

        window.translationClipboardResponse.connect(functools.partial(
            self.actions.onActionTranslationRequest, widget=widget
        ))
        window.suggestionClipboardResponse.connect(functools.partial(
            self.actions.onActionTranslationRequest, widget=widget
        ))

        window.translationResponse.connect(functools.partial(
            self.actions.onActionTranslationRequest, widget=widget
        ))

        window.suggestionResponse.connect(functools.partial(
            self.actions.onActionTranslationRequest, widget=widget
        ))

        window.addTab(1, widget, 'History', False)
