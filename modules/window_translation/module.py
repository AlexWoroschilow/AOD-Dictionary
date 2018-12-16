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

from lib.plugin import Loader

from .thread import TranslatorThread
from .actions import TranslatorActions
from .gui.widget import TranslatorWidget


class Loader(Loader):

    @property
    def enabled(self):
        if hasattr(self._options, 'converter'):
            return not self._options.converter
        return True

    def config(self, binder=None):
        binder.bind_to_provider('widget.translator', self._provider)

    @inject.params(window='window', widget='widget.translator')
    def boot(self, options, args, window=None, widget=None):
        window.addTab(0, widget, 'Translation')

    @inject.params(kernel='kernel', window='window')
    def _provider(self, kernel=None, window=None):

        actions = TranslatorActions(TranslatorWidget(), TranslatorThread())
        actions.widget.onSuggestionSelected(actions.onSuggestionSelected)
        actions.thread.started.connect(actions.onTranslationStarted)
        actions.thread.translation.connect(actions.onTranslationProgress)
        actions.thread.suggestion.connect(actions.onTranslationProgressSuggestion)
        actions.thread.finished.connect(actions.onTranslationFinished)

        kernel.listen('translate_clipboard', actions.onActionTranslateClipboard)
        kernel.listen('translate_text', actions.onActionTranslate)

        actions.thread.translate('welcome')
        
        return actions.widget
    
