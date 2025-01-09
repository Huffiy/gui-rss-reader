import wx
import wx.html2
import feedparser
import requests

class RSSReaderFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(RSSReaderFrame, self).__init__(*args, **kw)

        self.InitUI()
        self.Centre()
        self.SetSize(800, 600)

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.listbox = wx.ListBox(panel, style=wx.LB_SINGLE)
        self.listbox.Bind(wx.EVT_LISTBOX, self.OnSelect)
        vbox.Add(self.listbox, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        self.browser = wx.html2.WebView.New(panel)
        vbox.Add(self.browser, proportion=2, flag=wx.EXPAND | wx.ALL, border=10)

        panel.SetSizer(vbox)

        self.load_rss_feed()

    def load_rss_feed(self):
        url = "http://slashdot.org/slashdot.rss"
        response = requests.get(url)
        feed = feedparser.parse(response.content)

        self.entries = feed.entries
        for entry in self.entries:
            self.listbox.Append(entry.title)

    def OnSelect(self, event):
        selection = event.GetSelection()
        if selection != wx.NOT_FOUND:
            entry = self.entries[selection]
            html_content = f"<h1>{entry.title}</h1><p>{entry.description}</p>"
            self.browser.SetPage(html_content, "")

def main():
    app = wx.App(False)
    frame = RSSReaderFrame(None, title="Slashdot RSS Reader")
    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()