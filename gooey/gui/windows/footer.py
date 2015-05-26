'''
Created on Dec 23, 2013

@author: Chris
'''

import wx
import wx.animate

from wx.lib.pubsub import pub

from gooey.gui.lang import i18n
from gooey.gui import imageutil, image_repository, events


class AbstractFooter(wx.Panel):
  '''
  Abstract class for the Footer panels.
  '''

  def __init__(self, parent, **kwargs):
    wx.Panel.__init__(self, parent, **kwargs)
    self.SetMinSize((30, 53))

    self._controller = None

    # components
    self.cancel_button = None
    self.start_button = None
    self.running_animation = None
    self.close_button = None
    self.stop_button = None
    self.restart_button = None
    self.buttons = None

    self._init_components()
    self._init_pages()
    self._do_layout()


  def _init_components(self):
    self.cancel_button      = self.button(i18n._('cancel'),  wx.ID_CANCEL,  event_id=int(events.WINDOW_CANCEL))
    self.stop_button        = self.button(i18n._('stop'),    wx.ID_OK,      event_id=int(events.WINDOW_STOP))
    self.start_button       = self.button(i18n._('start'),   wx.ID_OK,      event_id=int(events.WINDOW_START))
    self.close_button       = self.button(i18n._("close"),   wx.ID_OK,      event_id=int(events.WINDOW_CLOSE))
    self.restart_button     = self.button(i18n._('restart'), wx.ID_OK,      event_id=int(events.WINDOW_RESTART))
    self.running_animation  = wx.animate.GIFAnimationCtrl(self, -1, image_repository.loader)

    self.buttons = [self.cancel_button, self.start_button, self.stop_button, self.close_button, self.restart_button]

  def _init_pages(self):
    if self.restart_button.IsShown(): self.restart_button.Hide()
    if self.close_button.IsShown(): self.close_button.Hide()

    def PageOne():
      self.cancel_button.Hide()
      self.start_button.Hide()
      self.running_animation.Show()
      self.running_animation.Play()
      self.Layout()

    def PageTwo():
      self.running_animation.Stop()
      self.running_animation.Hide()
      self.restart_button.Show()
      self.close_button.Show()
      self.restart_button.Show()
      self.Layout()

    self._pages = iter([PageOne, PageTwo])


  def _do_layout(self):
    self.stop_button.Hide()
    self.restart_button.Hide()

    v_sizer = wx.BoxSizer(wx.VERTICAL)
    h_sizer = wx.BoxSizer(wx.HORIZONTAL)

    h_sizer.AddStretchSpacer(1)
    h_sizer.Add(self.cancel_button, 0, wx.ALIGN_RIGHT | wx.RIGHT, 20)
    h_sizer.Add(self.start_button, 0, wx.ALIGN_RIGHT | wx.RIGHT, 20)

    v_sizer.AddStretchSpacer(1)
    v_sizer.Add(h_sizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
    v_sizer.Add(self.running_animation, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT, 20)
    self.running_animation.Hide()

    v_sizer.Add(self.restart_button, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT, 20)
    v_sizer.Add(self.close_button, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT, 20)
    self.restart_button.Hide()
    self.close_button.Hide()

    v_sizer.AddStretchSpacer(1)
    self.SetSizer(v_sizer)

  def button(self, label=None, style=None, event_id=-1):
    return wx.Button(
      parent=self,
      id=event_id,
      size=(90, 24),
      label=label,
      style=style)

  def RegisterController(self, controller):
    if self._controller is None:
      self._controller = controller

  def NextPage(self):
    try:
      next(self._pages)()
    except:
      self._init_pages()
      next(self._pages)()

  def _load_image(self, img_path, height=70):
    return imageutil.resize_bitmap(self, imageutil._load_image(img_path), height)


class Footer(AbstractFooter):
  '''
  Footer section used on the configuration
  screen of the application

  args:
    parent: wxPython parent windows
    controller: controller class used in delagating all the commands
  '''

  def __init__(self, parent, **kwargs):
    AbstractFooter.__init__(self, parent, **kwargs)
    for button in self.buttons:
      print button.GetId()
      self.Bind(wx.EVT_BUTTON, self.dispatch_click, button)

  def dispatch_click(self, event):
    pub.sendMessage(str(event.GetId()))
    event.Skip()



