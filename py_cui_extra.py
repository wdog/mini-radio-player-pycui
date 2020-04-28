import py_cui
import py_cui.widgets as widgets
import logging


class PyCUIExtra(py_cui.PyCUI):
    """description"""

    def __init__(self, *args, **keywords):
        super().__init__(*args, **keywords)
        self._title_bar.set_color(py_cui.BLACK_ON_GREEN)

    def add_scroll_menu_extra2(self, *args, **keywords):
        new_scroll_menu = super().add_scroll_menu(*args, **keywords)
        return new_scroll_menu

    def add_scroll_menu_extra(self, title, row, column, row_span=1,
                              column_span=1, padx=1, pady=0):

        id = 'Widget{}'.format(len(self._widgets.keys()))
        new_scroll_menu = ScrollMenuColors(id,
                                           title,
                                           self._grid,
                                           row,
                                           column,
                                           row_span,
                                           column_span,
                                           padx,
                                           pady,
                                           self._logger,
                                           )

        self._widgets[id] = new_scroll_menu
        if self._selected_widget is None:
            self.set_selected_widget(id)
        self._logger.debug('Adding widget {} w/ ID {} \
                of type {}'.format(title, id, str(type(new_scroll_menu))))
        return new_scroll_menu


class ScrollMenuColors(py_cui.widgets.ScrollMenu):

    def __init__(self, *args):
        super().__init__(*args)

    def _draw(self):
        """Overrides base class draw function
        """

        super()._draw()
        self._renderer.set_color_mode(self._color)
        self._renderer.draw_border(self)
        counter = self._pady + 1
        line_counter = 0
        for line in self._view_items:
            if line_counter < self._top_view:
                line_counter = line_counter + 1
            else:
                if counter >= self._height - self._pady - 1:
                    break
                if line_counter == self._selected_item:
                    self._renderer.set_color_mode(self._item_selected_color)
                    self._renderer.draw_text(self, line,
                                             self._start_y + counter)
                    self._renderer.set_color_mode(self._color)
                else:
                    self._renderer.draw_text(self, line,
                                             self._start_y + counter)
                counter = counter + 1
                line_counter = line_counter + 1
        self._renderer.unset_color_mode(self._color)
        self._renderer.reset_cursor(self)

    def set_item_selected_color(self, color):
        logging.info(color)
        self._item_selected_color = color
