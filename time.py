
import time
import wx
import wx.gizmos as gizmos

class LED_clock(wx.Frame):
    """
    create nice LED clock showing the current time
    """
    def __init__(self, parent, id):
        pos = wx.DefaultPosition
        wx.Frame.__init__(self, parent, id, title='LED Clock', pos=pos, size=(350, 100))
        size = wx.DefaultSize
        style = gizmos.LED_ALIGN_CENTER
        self.led = gizmos.LEDNumberCtrl(self, -1, pos, size, style)
        # default colours are green on black
        self.led.SetBackgroundColour("blue")
        self.led.SetForegroundColour("yellow")
        self.OnTimer(None)
        self.timer = wx.Timer(self, -1)
        # update clock digits every second (1000ms)
        self.timer.Start(1000)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        #self.Centre()

    def OnTimer(self, event):
        # get current time from computer
        current = time.localtime(time.time())
        # time string can have characters 0..9, -, period, or space
        ts = time.strftime("%H %M %S", current)
        self.led.SetValue(ts)

# test the clock ...
if __name__ == '__main__':
    app = wx.App()
    frame = LED_clock(None, -1)
    frame.Show(True)
    app.SetTopWindow(frame)
    app.MainLoop()