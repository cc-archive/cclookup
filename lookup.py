#!/usr/bin/env python

"""
lookup.py
(c) 2004-2007, Nathan R. Yergler, Creative Commons
licensed to the public under the GNU GPL version 2
"""

import os
import sys
import webbrowser
import urllib2
import re
import xml.sax

import wx
import wx.xrc
from wx.xrc import XRCCTRL, XRCID

from cctagutils.metadata import metadata
import cctagutils.lookup
import cctagutils.const
from cctagutils.const import version

import tagger

import html
from html import WebbrowserHtml
from html import DETAILS_TEMPLATE


try:
   root_dir = os.path.abspath(os.path.dirname(__file__))
           
except NameError, e:
   root_dir = os.path.dirname(sys.executable)

XRC_SOURCE = os.path.join(root_dir, 'lookup.xrc')
ICON_FILE = os.path.join(root_dir, 'cc.ico')

class dropFileTarget(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self._window = window

    def OnDropFiles(self, x, y, filenames):
        for fn in filenames:
            self._window.selectFile(fn)

class CcLookupFrame(wx.Frame):
   def __init__(self, parent): 
      self.app = parent

      # create a handle to the XML resource file
      self.xrc = wx.xrc.EmptyXmlResource()
      self.xrc.InsertHandler(html.HyperlinkXmlHandler())
      self.xrc.Load(XRC_SOURCE)

      # create the frame's skeleton
      pre = wx.PreFrame()

      # load the actual definition from the XRC
      self.xrc.LoadOnFrame(pre, None, 'FRM_MAIN')
      
      # finish creation
      self.PostCreate(pre)

      self.SetDropTarget(dropFileTarget(self))
      XRCCTRL(self, "PNL_LICENSE").SetDropTarget(dropFileTarget(self))
      XRCCTRL(self, "PNL_DETAILS").SetDropTarget(dropFileTarget(self))

      menubar = self.xrc.LoadMenuBar("MB_MAIN")
      self.SetMenuBar(menubar)

      # _icon = wx.Icon(ICON_FILE, wx.BITMAP_TYPE_ICO)
      # self.SetIcon(_icon)

      # bind events
      self.Bind(wx.EVT_BUTTON, self.onHelp, XRCCTRL(self, "CMD_HELP"))
      self.Bind(wx.EVT_MENU, self.onMenu)

      self.initLayout()

   def initLayout(self):
      # check the background color
      if sys.platform != 'darwin':
          html.BGCOLOR = "%X" % \
                    wx.SystemSettings_GetColour(wx.SYS_COLOUR_BTNFACE).GetRGB()

      # create the HTML container
      self.__details = WebbrowserHtml(parent = XRCCTRL(self, "PNL_DETAILS"),
                                      id=-1)
      
      XRCCTRL(self, "PNL_DETAILS").GetSizer().Add(self.__details, 1, wx.GROW)
      
      self.SetAutoLayout(True)
      
      # do the final platform-specific layout
      self.__platformLayout()
      self.reset()
      self.updateInterface()
      
      self.Layout()

   def updateInterface(self):

      # update the basic panel information with the filename, claim, etc
      XRCCTRL(self, "LBL_FILENAME").SetLabel(self.fileInfo['short_filename'])
      XRCCTRL(self, "LBL_CLAIM").SetLabel(self.fileInfo['claim'])
      XRCCTRL(self, "LBL_STATUS").SetLabel(self.fileInfo['status'])
      
      # update the details page
      self.__details.SetPage(DETAILS_TEMPLATE % (html.BGCOLOR,
                                                  self.fileInfo['filename'],
                                                  self.__fileDetails(self.fileInfo['filename'])
                                                  )
                              )

   def __platformLayout(self):
       if sys.platform == 'darwin':
           self.__html.SetDropTarget(dropFileTarget(self))
           
           # add a border to the notebook
           self.GetSizer().FindItem(XRCCTRL(self, "NTB_MAIN")).SetBorder(10)

           # add a sizer @ the bottom for padding
           self.GetSizer().AddItem(wx.GBSizerItemSpacer(10, 10,
                                                        (3,0),(1,1),
                                                        flag=wx.EXPAND,
                                                        border=0) )

       self.Layout()
       self.SetSize((500,350))

   def onHelp(self, event):
       webbrowser.open('http://creativecommons.org/technology/embedding',
                       True, True)

   def onMenu(self, event):
       if event.GetId() == XRCID("MNU_FILE_OPEN"):
           browser = wx.FileDialog(self, wildcard="*.*", style=wx.OPEN)
           if browser.ShowModal() == wx.ID_OK:
               self.selectFile(browser.GetPaths()[0])
       elif event.GetId() == XRCID("wxID_ABOUT"):
           self.onAbout()
       else:
           self.Close()

   def reset(self):
       """Reset the GUI for another file."""
       # initialize file info
       self.fileInfo = {'filename':'',
                        'short_filename':'',
                        'claim':'',
                        'license':'&nbsp;',
                        'vurl':'&nbsp;',
                        'status':''
                       }

   def autolink(self,text):
        link_regex = re.compile('[a-z]*://[^ \t\n\r\f\v<>"]*')
        added_len = len('<a href=""></a>')

        link = link_regex.search(text,0)
        while link is not None:

           text = '%s<a href="%s">%s</a>%s' % (text[:link.start()], text[link.start():link.end()], text[link.start():link.end()], text[link.end():])

           link = link_regex.search(text, link.end() + added_len + (link.end() - link.start()) )

        return text

   def selectFile(self, filename):
       self.reset()
       
       # set the filename label
       self.fileInfo['filename'] = filename
       self.fileInfo['short_filename'] = os.path.basename(filename)
       self.fileInfo['status'] = 'working...'

       # reset the HTML UI
       self.updateInterface()

       # set the cursor to busy
       __cur_cursor = self.GetCursor()
       self.SetCursor(wx.StockCursor(wx.CURSOR_WAIT))
       
       # update the app
       wx.Yield()
       
       # retrieve the license claim
       mdata = metadata(filename)
       claim = mdata.getClaim()
       self.fileInfo['claim'] = self.autolink(claim)
       
       # check if it actually exists
       if not claim.strip():
           # no license; bail out
           self.fileInfo['license'] = "None."
           self.fileInfo['status'] = "No embedded license; nothing to verify."
       else:
           parts = cctagutils.lookup.parseClaim(claim)
           self.fileInfo['license'] = self.autolink(parts['license'])
           self.fileInfo['vurl'] = self.autolink(parts['verify at'])
           
           # verify the file
           try:
               status = cctagutils.lookup.verify(filename)
               
               print
               print 'status: ', status
               
               if status == 1:
                   self.fileInfo['status'] = 'Metadata at %s agrees with ' \
                                                        'embedded claim.' % (
                       self.fileInfo['vurl'])
                   
               elif status == 0:
                   self.fileInfo['status'] = \
                       "Unable to compare claims;<br>No embedded RDF found " \
                       "at information URL."
               elif status == -1:
                   self.fileInfo['status'] = \
                       "Unable to verify;\n" \
                       "RDF does not contain information for this work."
               elif status == -2:
                   self.fileInfo['status'] = \
                       "No match;<br>RDF license found at information URL " \
                       "does not match embedded claim."
           except urllib2.HTTPError, e:
               if e.code == 404:
                   # verification URL not found
                   self.fileInfo['status'] = \
                       "Unable to verify;<br>Information URL not found."
               else:
                   self.fileInfo['status'] = "A network error occurred while "\
                                             "attempting to retrieve the "\
                                             "information URL from the "\
                                             "server (%s)" % e.code
           except urllib2.URLError, e:
               self.fileInfo['status'] =  "A network error occurred while "\
                                          "attempting to retrieve the "\
                                          "information URL (%s)" % e.code
           except xml.sax.SAXParseException, e:
               self.fileInfo['status'] = "The verification page contains " \
                                         "invalid RDF; could not verify " \
                                         "the license."
           except Exception, e:
               # an error occurred while trying to verify the claim...
               # XXX handle errors intelligently here
               self.fileInfo['status'] = \
                   "An error occurred while attempting to retrieve " \
                   "the information page."

       self.updateInterface()
       self.SetCursor(__cur_cursor)
       self.Layout()

   def __fileDetails(self, filename):
       result = ["""
<tr>
  <td VALIGN="TOP" ALIGN="LEFT" height="1">
     <font size="-1"><strong>Tag&nbsp;Name</strong></font>
  </td>
  <td VALIGN="TOP" ALIGN="LEFT" height="1">
     <font size="-1"><strong>Tag Value</strong></font>
  </td>
</tr>"""]

       if filename:
           try:
               v2 = tagger.id3v2.ID3v2(filename,
                                       tagger.constants.ID3_FILE_READ)
               
               for frame in v2.frames:
                   if len(frame.strings) > 0:
                       oframe = frame.strings[0]
                   else:
                       oframe = frame.output_field()

                   oframe = self.autolink(oframe)
                       
                   result.append('<tr><td VALIGN="TOP" ALIGN="LEFT">'
                                 '<font size="-1">%s</font></td>'
                                 '<td VALIGN=TOP ALIGN=LEFT>'
                                 '<font size="-1">%s</font></td></tr>' % (
                       frame.fid,
                       oframe + "&nbsp;"
                       )
                                 )
           except:
               pass

       #if len(result) == 
       #result.append('<tr><td VALIGN=BOTTOM ALIGN=LEFT>&nbsp;</td>'
       #              '<td VALIGN=BOTTOM ALIGN=LEFT>&nbsp;</td></tr>')

       return "\n".join(result)

   def onAbout(self):
        # Create the About dialog and connect the button handler
        dlg = self.xrc.LoadDialog(self, "DLG_ABOUT")
        dlg.Bind(wx.EVT_BUTTON, lambda x: dlg.EndModal(0),
                  XRCCTRL(dlg, "CMD_OK"))


        # set the version number
        XRCCTRL(dlg, "LBL_VERSION").SetLabel("version %s" % version())
        
        # show the dialog, then destroy it once it's closed
        dlg.ShowModal()
        dlg.Destroy()

class LookupApp(wx.App):
   def OnInit(self):
      wx.InitAllImageHandlers()

      # take care of any custom settings here
      self.SetAppName('Lookup')

      # create the main window and set it as the top level window
      self.main = CcLookupFrame(self)
      self.main.Show(True)
      self.SetTopWindow(self.main)

      return True

   def OnExit(self):
       pass
       
   def MacOpenFile(self, filename):
      # pass the filename into the main form
      if self.main:
         self.main.selectFile(filename)

def main(argv=[]):
   # create the application and execute it
   app = LookupApp(filename='err.log')

   print argv

   if len(argv) > 1:
       app.main.selectFile(argv[-1])

   app.MainLoop()

if __name__ == '__main__':
    # set any platform-specific parameters
    if sys.platform == 'darwin':
        # set the file path to the XRC resource file
        # to handle the app bundle properly
        XRC_SOURCE = os.path.join(os.path.dirname(sys.argv[0]), XRC_SOURCE)
        ICON_FILE = os.path.join(os.path.dirname(sys.argv[0]),
                                 'resources', ICON_FILE)

    print sys.argv
    main(sys.argv[1:])
