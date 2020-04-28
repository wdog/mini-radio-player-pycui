import py_cui


class PyCUIExtra(py_cui.PyCUI):
    """description"""

    def __init__(self, *args, **keywords):
        super().__init__(*args, **keywords)
        self._title_bar.set_color(py_cui.BLACK_ON_GREEN)

    def add_scroll_menu_extra(self, *args, **keywords):
        c = super().add_scroll_menu(*args, **keywords)
        return c
