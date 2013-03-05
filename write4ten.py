#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import gobject
import about
import time

class Write4Ten:
    def close_window(self, widget, data=None):
        # self.timer = 0
        if self.timer_on == True:
            gobject.source_remove(self.timer)
        gtk.main_quit()
        
    def about_me(self, widget):
        aboutme = about.Me()
        aboutme.run()
        aboutme.destroy()

    def txtbuffer_change(self, widget):
        if self.timer_on == False:
            self.timer_start()
        self.btnsave.set_sensitive(widget.get_char_count() != 0)

    def timer_start(self):
        self.timer_on = True
        self.timer = gobject.timeout_add(100, self.progress_timeout)
        
    def progress_timeout(self):
        if self.timeStart == 0:
            self.timeStart = time.time()
        seconds = time.time() - self.timeStart
        self.pgbar.set_text(time.strftime("%M:%S", time.gmtime(seconds)))
        
        newFract = seconds / self.duration
        
        if newFract > 1:
            self.txtView.set_editable(False)
            self.txtView.set_cursor_visible(False)
            #grey = gdk.color_parse("grey")
            #self.txtView.modify_text(gtk.STATE_NORMAL, grey)
            return False
        
        self.pgbar.set_fraction(newFract)
        
        return True

    def getFileName(self, path):
        list_of_split = path.split("/")
        rev_list_of_split = list_of_split[::-1]
        file_name = rev_list_of_split[0]
        
        return file_name
        
    def newdoc(self, widget):
        #reset
        self.win.set_title("[untitled] - write4ten")
        
        self.txtbuffer.set_text("")
        self.txtView.set_editable(True)
        self.txtView.set_cursor_visible(True)
        
        self.timeStart = 0
        if self.timer_on == True:
            self.timer_on = False
            gobject.source_remove(self.timer)
            
        self.pgbar.set_fraction(0)
        self.pgbar.set_text("00:00")
        
        self.btnsave.set_sensitive(False)
        
        self.txtView.grab_focus()
       
    def save(self, widget):

        file_name = ""
        dialog = gtk.FileChooserDialog("Save..",
                                     None,
                                     gtk.FILE_CHOOSER_ACTION_SAVE,
                                     (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                     gtk.STOCK_SAVE, gtk.RESPONSE_OK))

        txt_filter=gtk.FileFilter()
        txt_filter.set_name("Text files")
        txt_filter.add_mime_type("text/*")
        all_filter=gtk.FileFilter()
        all_filter.set_name("All files")
        all_filter.add_pattern("*")

        dialog.add_filter(txt_filter)
        dialog.add_filter(all_filter)
        
        dialog.set_current_name("untitled.txt")

        response = dialog.run()

        if response == gtk.RESPONSE_OK:
            file_name = dialog.get_filename()

        dialog.destroy()

        if file_name != "":
            file_save = open(file_name,"w")  
            file_save.write(self.txtbuffer.get_text(self.txtbuffer.get_start_iter(), self.txtbuffer.get_end_iter()))
            file_save.close()
            
            self.win.set_title(self.getFileName(file_name) + " - write4ten")
            
            self.txtView.set_editable(False)
            self.txtView.set_cursor_visible(False)
            
            try:
                gobject.source_remove(self.timer)
                
            except Exception, e:
                pass

    def getIcon(self, stock):
        tema = gtk.icon_theme_get_default()
        return tema.load_icon(stock, 48, 0)
        
    def __init__(self):
        """ init """
        self.timeStart = 0
        self.timer_on = False
        self.duration = 10 * 60
        
        self.win = gtk.Window(gtk.WINDOW_TOPLEVEL)
#        self.win.set_resizable(True)
        self.win.set_title("[untitled] - write4ten")
        self.win.set_border_width(0)
        self.win.set_size_request(600, 450)
        self.win.set_position(gtk.WIN_POS_CENTER)
        self.win.connect("destroy", self.close_window)
        
        vbox = gtk.VBox(False, 5)
        vbox.set_border_width(5)
        self.win.add(vbox)
        vbox.show()
        
        toolbar = gtk.Toolbar()
        toolbar.set_style(gtk.TOOLBAR_BOTH)
        
        iconNew = gtk.image_new_from_stock(gtk.STOCK_NEW, 32)
        iconSave = gtk.image_new_from_stock(gtk.STOCK_SAVE, 32)
        iconAbout = gtk.image_new_from_stock(gtk.STOCK_ABOUT, 32)
        iconQuit = gtk.image_new_from_stock(gtk.STOCK_QUIT, 32)
        
        toolbar.append_item("New","Start a new document","Start a new document",iconNew, self.newdoc)
        self.btnsave = toolbar.append_item("Save","Save current document","Save current document",iconSave, self.save)
        toolbar.append_item("About","About this application","About this application",iconAbout, self.about_me)
        toolbar.append_space()
        toolbar.append_item("Quit","Quit aplication","Quit aplication",iconQuit, self.close_window)
        
        # disable the save button
        self.btnsave.set_sensitive(False)
        
        #TODO:
        #add a pause button
        
        vbox.pack_start(toolbar, False, False, 0)
        toolbar.show()
        
        scwin = gtk.ScrolledWindow()
        scwin.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        vbox.pack_start(scwin, True, True, 0)
        scwin.show()
        
        self.txtbuffer = gtk.TextBuffer()
        self.txtbuffer.connect("changed", self.txtbuffer_change)
        
        self.txtView = gtk.TextView(self.txtbuffer)
        self.txtView.set_left_margin(5)
        self.txtView.set_right_margin(5)
        self.txtView.set_wrap_mode(gtk.WRAP_WORD)
        
        scwin.add_with_viewport(self.txtView)
        #scwin.add(txtView)
        self.txtView.show()
        
        self.pgbar = gtk.ProgressBar()
        self.pgbar.set_text("00:00")
        vbox.pack_start(self.pgbar, False, True, 0)
        self.pgbar.show()
        
        self.txtView.grab_focus()
        
        self.win.show()

def main():
    gtk.main()

if __name__ == "__main__":
    Write4Ten()
    main()
    
