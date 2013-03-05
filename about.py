#!/usr/bin/env python

import gtk

class Me(gtk.AboutDialog):
    def __init__(self):
        gtk.AboutDialog.__init__(self)
        self.set_program_name("write4ten")
        self.set_version("1.0.0")
        self.set_copyright("(c) Nurul Huda <pruls34@gmail.com>")
        self.set_comments("write4ten - it's lightweight editor")
        self.set_website("http://github.com/nurulhuda/write4ten")
