from .graph import GraphCursorZSeries
from matplotlib import pyplot as plt

class CookbookGraph(object):
    """ Cookbook of graph utilities

    This utilities are not directly called from the GUI, but are meant as
    wrapper to make GUI functionalities available also through JSON
    """

    def __init__(self):
        super(CookbookGraph, self).__init__()


    def menu_view(self, attr):
        getattr(self.sess._gui._panel_sess._menu._view, attr)(event=None)


    def menu_view_cursor_z_series(self, z=2.0, series="Ly_a"):
        gui = self.sess._gui
        menu = gui._panel_sess._menu

        # The following is needed to prevent toggling between cursor activation/
        # disactivation; if toggling is enabled, this method cannot be used more
        # than once in a JSON file
        key = 'cursor_z_series'
        sel = gui._graph_main._sel
        if key in sel:
            sel.remove(key)

        menu._on_graph(None, "Redshift cursor", key, gui._cursor,
                       'systems', GraphCursorZSeries)
        gui._dlg_mini_systems._ctrl_z.SetValue(str(z))
        gui._dlg_mini_systems._ctrl_series.SetValue(str(series))
        gui._dlg_mini_systems._on_apply(None)


    def menu_view_cursor_z_series_stick(self, z=2.0, series="Ly_a"):
        gui = self.sess._gui
        self.menu_view_cursor_z_series(z, series)
        gui._dlg_mini_systems._on_stick(None)


    def save(self, name='fig.pdf'):
        self.sess._gui._graph_main._graph._fig.savefig(name)
