import sys
import webbrowser

import wx
import wx.html
import wx.lib.wxpTag

from html import WebbrowserHtml

class AboutBox(wx.Dialog):
    text = '''
<html>
<body bgcolor="#e3e3e3">
<center>
<h2>ccLookup</h2>
<p><font size="-1">version %s</font><br>
(c) 2004-2005, Creative Commons,<br>
Nathan R. Yergler &lt;nathan@creativecommons.org&gt;;<br>
licensed under the GNU GPL 2.
</p>
<p>For more information on Licensing Embedding, see
<a href="http://creativecommons.org/technology/embedding">http://creativecommons.org/technology/embedding</a>.
</p>

<p><wxp module="wx" class="Button">
    <param name="label" value="OK">
    <param name="id"    value="ID_OK">
</wxp></p>

</center>
</body>
</html>
'''
    def __init__(self, parent, version):
        wx.Dialog.__init__(self, parent, -1, 'About ccLookup',)
        html = WebbrowserHtml(self, -1, size=(420, -1))
        if "gtk2" in wx.PlatformInfo:
            html.NormalizeFontSizes()
        py_version = sys.version.split()[0]
        html.SetPage(self.text % version)
        btn = html.FindWindowById(wx.ID_OK)
        ir = html.GetInternalRepresentation()
        html.SetSize( (ir.GetWidth()+25, ir.GetHeight()+25) )
        self.SetClientSize(html.GetSize())
        self.CentreOnParent(wx.BOTH)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    app = wx.PySimpleApp()
    dlg = MyAboutBox(None)
    dlg.ShowModal()
    dlg.Destroy()
    app.MainLoop()

