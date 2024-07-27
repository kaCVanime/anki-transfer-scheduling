# -*- coding:utf-8 -*-
#
# https://github.com/sirius-fan/FastWordQuery/blob/master/src/gui/progress.py
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version; http://www.gnu.org/copyleft/gpl.html.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import time

from aqt.qt import *


__all__ = ["ProgressWindow"]

_INFO_TEMPLATE = "".join(
    [
        "<strong>" + "transferring" + "</strong>",
        "<p>" + 45 * "-" + "</p>",
        "<p>" + "{}" + " processed" + "</p>",
    ]
)


class ProgressWindow(object):
    """
    Query progress window
    """

    def __init__(self, mw):
        self.mw = mw
        self.app = QApplication.instance()
        self._win = None
        self._count = 0
        self._last_update = 0
        self._first_time = 0
        self._disabled = False

    def update_labels(self, count):
        if self.abort():
            return

        self._count = count

        number_info = _INFO_TEMPLATE.format(self._count)
        self._update(number_info, self._count)
        self._win.adjustSize()
        self.app.processEvents()

    def update_title(self, title):
        if self.abort():
            return
        self._win.setWindowTitle(title)

    def start(self, max=0, min=0, label=None, parent=None):
        self._count = 0
        # setup window
        label = label or "Processing..."
        parent = parent or self.app.activeWindow() or self.mw
        self._win = QProgressDialog(label, "", min, max, parent)
        self._win.setWindowModality(Qt.WindowModality.ApplicationModal)
        self._win.setCancelButton(None)
        self._win.canceled.connect(self.finish)
        self._win.setWindowTitle("Processing")
        # TODO
        self._win.setModal(True)
        self._win.setWindowFlags(
            self._win.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint
        )
        self._win.setAutoReset(True)
        self._win.setAutoClose(True)
        self._win.setMinimum(0)
        self._win.setMaximum(max)
        # we need to manually manage minimum time to show, as qt gets confused
        # by the db handler
        # self._win.setMinimumDuration(100000)
        self._first_time = time.time()
        self._last_update = time.time()
        self._disabled = False
        self._win.show()
        self._win.setValue(0)
        self.app.processEvents()

    def abort(self):
        # self.aborted = True
        return self._win.wasCanceled()

    def finish(self):
        self._unset_busy()
        if self._win:
            self._win.hide()
            self._win.destroy()

    def _update(self, label, value, process=True):
        elapsed = time.time() - self._last_update
        if label:
            self._win.setLabelText(label)
        if value:
            self._win.setValue(value)
        if process and elapsed >= 0.2:
            self.app.processEvents(QEventLoop.ProcessEventsFlag.ExcludeUserInputEvents)
            self._last_update = time.time()

    def _set_busy(self):
        self._disabled = True
        self.mw.app.setOverrideCursor(QCursor(Qt.WaitCursor))

    def _unset_busy(self):
        self._disabled = False
        self.app.restoreOverrideCursor()
