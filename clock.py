import re
import time
import gobject
import terminatorlib.plugin as plugin
from terminatorlib.terminator import Terminator
from terminatorlib.terminal import Terminal

AVAILABLE = ['TitlebarClock']


def get_window_title_with_time(self):
    title = self.vte.get_window_title() or str(self.command)
    return TitlebarClock.get_title_with_time(title)

Terminal.get_window_title = get_window_title_with_time


class TitlebarClock(plugin.Plugin):
    capabilities = ['clock_titlebar']
    time_regex = re.compile('^\d{2}:\d{2} ')

    def __init__(self):
        plugin.Plugin.__init__(self)
        self.terminator = Terminator()
        gobject.timeout_add_seconds(5, self.update_clock)

    def update_clock(self):
        w = self.terminator.windows[0].title
        w.set_title(None, self.__class__.get_title_with_time(w.text))
        for t in self.terminator.terminals:
            new_title = self.__class__.get_title_with_time(t.titlebar.termtext)
            t.titlebar.set_terminal_title(None, new_title)
        return True

    @classmethod
    def get_title_with_time(self, title):
        if not re.match(self.time_regex, title):
            return "{} {}".format(time.strftime('%H:%M'), title)
        else:
            return "{} {}".format(time.strftime('%H:%M'), title[6:])
