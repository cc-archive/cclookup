import webbrowser
import wx.lib.hyperlink
import wx.html

class HyperlinkXmlHandler(wx.xrc.XmlResourceHandler):
    def __init__(self):
        wx.xrc.XmlResourceHandler.__init__(self)
        
        # Specify the styles recognized by objects of this type
        self.AddStyle("wx.NO_3D", wx.NO_3D)
        self.AddStyle("wx.TAB_TRAVERSAL", wx.TAB_TRAVERSAL);
        self.AddStyle("wx.WS_EX_VALIDATE_RECURSIVELY",
                      wx.WS_EX_VALIDATE_RECURSIVELY);
        self.AddStyle("wx.CLIP_CHILDREN", wx.CLIP_CHILDREN);

        self.AddWindowStyles()

    def CanHandle(self, node):
        return self.IsOfClass(node, "wxHyperlinkCtrl")

    def DoCreateResource(self):
        # we only currently support creation from scratch
        assert self.GetInstance() is None
 
        # create the new instance and return it
        hyperlink = wx.lib.hyperlink.HyperLinkCtrl(self.GetParentAsWindow(),
                                     label = self.GetText('label'),
                                     URL = self.GetText('target'),
                                     )

        # turn on auto-browsing
        hyperlink.AutoBrowse()

        return hyperlink
    
class WebbrowserHtml(wx.html.HtmlWindow):
    def OnLinkClicked(self, linkinfo):
        webbrowser.open( linkinfo.GetHref(), True, True )

BGCOLOR = "e3e3e3"

HTML_TEMPLATE = """
<html><body bgcolor="#%s">
<table border="0" cellspacing="2" width="100%%">
  <tr><td colspan="2" ALIGN="CENTER">
  Drag and drop your MP3 file here to see if 
it has a valid Creative Commons license.
</td></tr>
  <tr><td colspan="2">&nbsp;</td></tr>
</table>
<table border="0" cellspacing="2" width="100%%">
  <tr>
      <td VALIGN=BOTTOM ALIGN=LEFT><font size="-1">File:</font></td>
      <td VALIGN=BOTTOM ALIGN=LEFT><font size="-1">%s</font></td>
  </tr>
  <tr>
      <td VALIGN=TOP ALIGN=LEFT><font size="-1">Embedded&nbsp;Claim:</font></td>
      <td VALIGN=TOP ALIGN=LEFT><font size="-1">%s</font></td>
  </tr>
  <tr>
      <td VALIGN=TOP ALIGN=LEFT><font size="-1">Status:</font></td>
      <td VALIGN=TOP ALIGN=LEFT><font size="-1">%s</font></td>
  </tr>
</table>
</body></html>
"""

DETAILS_TEMPLATE = """
<html><body bgcolor="#%s">
<table border="0" width="100%%">
  <tr>
    <td VALIGN="BOTTOM" ALIGN="LEFT" height="1%%">
       <table cellspacing="1" cellpadding="0" border="0">
         <tr VALIGN="BOTTOM" ALIGN="LEFT"><td VALIGN="BOTTOM" ALIGN="LEFT">
           <font size="-1">File:</font>
         </td>
         <td VALIGN="BOTTOM" ALIGN="LEFT">
           <font size="-1">%s</font>
         </td></tr>
       </table>
    </td>
  </tr>
  <tr height="1%%" VALIGN="TOP">
     <td ALIGN=LEFT VALIGN="TOP"  height="1">
        <font size="-1">Embedded <a href="http://id3.org">ID3</a> Information</font>
     </td>
  </tr>
  <tr>
      <td VALIGN="TOP" ALIGN="LEFT">
        <table width="100%%" border="1" cellspacing="0">
           %s
        </table>
      </td>
  </tr>
</table>
</body></html>
"""
