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
    
