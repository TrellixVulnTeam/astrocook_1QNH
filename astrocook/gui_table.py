from .gui_graph import GUIGraphDetail
from collections import OrderedDict
import pprint
import wx
import wx.grid as gridlib
import wx.lib.mixins.listctrl as listmix
import numpy as np

prefix = "GUI:"

class GUITable(wx.Frame):
    """ Class for the GUI table frame """

    def __init__(self,
                 gui,
                 attr,
                 title="Table",
                 size_x=wx.DisplaySize()[0]*0.5,
                 size_y=wx.DisplaySize()[1]*0.9):

        self._gui = gui
        self._attr = attr
        self._title = title
        self._size_x = size_x
        self._size_y = size_y

    def _init(self):
        super(GUITable, self).__init__(parent=None, title=self._title,
                                       size=(self._size_x, self._size_y))
        self._panel = wx.Panel(self)
        self._tab = gridlib.Grid(self._panel)
        self._tab.CreateGrid(0, 0)

    def _on_close(self, event):
        self.Destroy()

    def _on_right_click(self, event):
        self.PopupMenu(GUITablePopup(self._gui, self, event), event.GetPosition())

    def _on_view(self, event):
        self._data = getattr(self._gui._sess_sel, self._attr)
        try:
            self._tab.DeleteCols(pos=0, numCols=self._tab.GetNumberCols())
            #self._tab.DeleteRows(pos=0, numRows=self._tab.GetNumberRows())
            print(prefix, "I'm updating table...")
        except:
            print(prefix, "I'm loading table...")
        coln = len(self._data.t.colnames)
        #if not hasattr(self, '_tab'):
        self._init()
        rown = len(self._data.t)-self._tab.GetNumberRows()
        self._tab.AppendCols(coln)
        self._tab.AppendRows(rown)
        for j, r in enumerate(self._data.t):
            for i, n in enumerate(self._data.t.colnames):
                if j == 0:
                    self._tab.SetColSize(i, 150)
                    self._tab.SetColLabelValue(i, "%s\n%s" \
                                              % (n, str(self._data.t[n].unit)))
                """
                try:
                    self._tab.SetCellValue(j, i, "%3.5f" % r[n])
                except:
                    if type(r[n]) == str:
                        self._tab.SetCellValue(j, i, r[n])
                    if type(r[n]) == OrderedDict:
                        self._tab.SetCellValue(j, i, pprint.pformat(r[n]))
                    if type(r[n]) == dict:
                        self._tab.SetCellValue(j, i, pprint.pformat(r[n]))
                """
                if type(r[n]) == np.int64:
                    self._tab.SetCellValue(j, i, "%4i" % r[n])
                elif type(r[n]) == str:
                    self._tab.SetCellValue(j, i, r[n])
                elif type(r[n]) == OrderedDict:
                    self._tab.SetCellValue(j, i, pprint.pformat(r[n]))
                elif type(r[n]) == dict:
                    self._tab.SetCellValue(j, i, pprint.pformat(r[n]))
                else:
                    self._tab.SetCellValue(j, i, "%3.5f" % r[n])

        self._tab.AutoSizeColumns(True)
        self._box = wx.BoxSizer(wx.VERTICAL)
        self._box.Add(self._tab, 1, wx.EXPAND)
        self._panel.SetSizer(self._box)
        self._tab.Bind(wx.grid.EVT_GRID_LABEL_RIGHT_CLICK, self._on_right_click)
        self.Bind(wx.EVT_CLOSE, self._on_close)
        self.Centre()
        self.Show()



class GUITableLineList(GUITable):
    """ Class for the GUI line list """

    def __init__(self,
                 gui,
                 title="Line table",
                 size_x=wx.DisplaySize()[0]*0.5,
                 size_y=wx.DisplaySize()[1]*0.9):

        super(GUITableLineList, self).__init__(gui, 'lines', title, size_x,
                                               size_y)

        self._gui = gui
        self._gui._tab_lines = self

    def _on_show(self, event):
        pass

class GUITableModelList(GUITable):
    """ Class for the GUI model list """

    def __init__(self,
                 gui,
                 title="Model table",
                 size_x=wx.DisplaySize()[0]*0.5,
                 size_y=wx.DisplaySize()[1]*0.9):

        super(GUITableModelList, self).__init__(gui, 'mods', title,
                                                size_x, size_y)

        self._gui = gui
        self._gui._tab_mods = self

class GUITablePopup(wx.Menu):
    """ Class for the GUI table popup menu """

    def __init__(self, gui, parent, event):
        super(GUITablePopup, self).__init__()
        self._parent = parent
        self._event = event
        self._gui = gui
        self._gui._tab_popup = self
        self._parent = parent
        self._event = event

        show = wx.MenuItem(self, wx.NewId(), 'Show')
        #try:
        self.Bind(wx.EVT_MENU, self._parent._on_show, show)
        #except
        #    pass
        self.Append(show)

        delete = wx.MenuItem(self, wx.NewId(), 'Delete')
        self.Append(delete)

#class GUITableGraph(wx.Frame):


class GUITableSpectrum(GUITable):
    """ Class for the GUI spectrum table """

    def __init__(self,
                 gui,
                 title="Spectrum table",
                 size_x=wx.DisplaySize()[0]*0.5,
                 size_y=wx.DisplaySize()[1]*0.9):

        super(GUITableSpectrum, self).__init__(gui, 'spec', title, size_x,
                                               size_y)

        self._gui = gui
        self._gui._tab_spec = self

    def _on_show(self, event, span=10):
        if not hasattr(self._gui, '_graph_det'):
            GUIGraphDetail(self._gui)
        row = self._data.t[self._gui._tab_popup._event.GetRow()]
        xlim, ylim = self._gui._graph_det._define_lim(row, span)
        self._gui._graph_det._refresh(self._gui._sess_items, xlim=xlim)


class GUITableSystList(GUITable):
    """ Class for the GUI system list """

    def __init__(self,
                 gui,
                 title="System table",
                 size_x=wx.DisplaySize()[0]*0.5,
                 size_y=wx.DisplaySize()[1]*0.9):

        super(GUITableSystList, self).__init__(gui, 'systs', title, size_x,
                                               size_y)

        self._gui = gui
        self._gui._tab_systs = self
