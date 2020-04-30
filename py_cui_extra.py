import py_cui
import curses
import logging
"""
File: py_cui_extra.py
Author: wdog
Github: https://github.com/wdog
Description: PyCUI extra funcs
"""


class PyCUIExtra(py_cui.PyCUI):
    """description"""
    def __init__(self, *args, **keywords):
        logging.info("PuCUIExtra")
        super().__init__(*args, **keywords)
        self._title_bar.set_color(py_cui.BLACK_ON_GREEN)

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

    def add_slider(self, title, row, column, row_span=1,
                   column_span=1, padx=1, pady=0, min_val=0, max_val=100,
                   step=1):

        id = 'Widget{}'.format(len(self._widgets.keys()))
        slider = Slider(id,
                        title,
                        self._grid,
                        row,
                        column,
                        row_span,
                        column_span,
                        padx,
                        pady,
                        self._logger,
                        min_val,
                        max_val,
                        step
                        )

        self._widgets[id] = slider
        if self._selected_widget is None:
            self.set_selected_widget(id)
        return slider


class ScrollMenuColors(py_cui.widgets.ScrollMenu):

    _current = -1

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
                # running
                if line_counter == self._current:
                    self._renderer.set_color_mode(self._item_active_color)
                    self._renderer.draw_text(self, "  " + line,
                                             self._start_y + counter,
                                             bordered=False)
                # current position
                elif line_counter == self._selected_item:
                    self._renderer.set_color_mode(self._item_selected_color)
                    self._renderer.draw_text(self, "  " + line,
                                             self._start_y + counter,
                                             bordered=False)
                    self._renderer.unset_color_mode(self._item_selected_color)
                else:
                    self._renderer.set_color_mode(self._color)
                    self._renderer.draw_text(self, line,
                                             self._start_y + counter,
                                             bordered=True)
                    self._renderer.unset_color_mode(self._color)

                counter = counter + 1
                line_counter = line_counter + 1
        self._renderer.unset_color_mode(self._color)
        self._renderer.reset_cursor(self)

    def set_item_selected_color(self, color):
        self._item_selected_color = color

    def set_item_active_color(self, color):
        self._item_active_color = color

    def set_current(self, value):
        self._current = value

    def _handle_key_press(self, key_pressed):

        super()._handle_key_press(key_pressed)

        if key_pressed == py_cui.keys.KEY_ENTER:
            self.set_current(self._selected_item)

        if key_pressed == curses.KEY_NPAGE:
            # if next jump is on the groud
            if self._selected_item + self._height - 2 < len(self._view_items):
                self._selected_item += self._height - 2
                self._top_view = self._selected_item

        if key_pressed == curses.KEY_PPAGE:
            self._selected_item -= self._height - 2
            self._top_view = self._selected_item
            if self._selected_item < 0:
                self._selected_item = 0


class Slider(py_cui.widgets.Label):

    _cur_val = 0
    _disabled = False
    _disabled_text = 'MUTED'

    def __init__(self, id, title, grid, row, column, row_span, column_span,
                 padx, pady, logger, min_val, max_val, step):

        super().__init__(id, title, grid, row, column,
                         row_span, column_span, padx, pady, logger)
        self._min_val = min_val
        self._max_val = max_val
        self._step = step

    def _draw(self):

        super()._draw()
        self._renderer.set_color_mode(self._color)
        target_y = self._start_y + int(self._height / 2)

        if self._disabled:
            self._renderer.draw_text(self,
                                     self._disabled_text,
                                     target_y, centered=True,
                                     bordered=self._draw_border)
        else:
            self._renderer.draw_text(self,
                                     "Volume {}%".format(self._cur_val),
                                     target_y-1, centered=True,
                                     bordered=self._draw_border,
                                     )

            fact = (self._max_val - self._min_val) / (self._width - 4)
            _len = int((self._cur_val - self._min_val)/fact)
            _bar = " " + "█" * _len
            self._renderer.draw_text(self,
                                     _bar,
                                     target_y, centered=False,
                                     bordered=self._draw_border,
                                     )

        self._renderer.unset_color_mode(self._color)

    def set_slider_value(self, val, direction):
        self._cur_val = val + (direction * self._step)
        if (self._cur_val <= self._min_val):
            self._cur_val = self._min_val
        if (self._cur_val >= self._max_val):
            self._cur_val = self._max_val

        return self._cur_val

    def disable(self, disabled=0):
        if disabled == 0:
            self._disabled = True
        else:
            self._disabled = False
