##############################################################################
##
##  nymp - a graphical xmms2 cli frontend
##  Copyright 2010 Thammi
##
##  nymp is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##
##  nymp is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with nymp.  If not, see <http://www.gnu.org/licenses/>.
##
##############################################################################

import urwid

class ScrollableList(urwid.ListBox):
    '''A ListBox with mouse scrolling and smoother scrolling with offset'''

    SCROLL_SPACE = 2

    def mouse_event(self, size, event, button, col, row, focus):
        if event == 'mouse press' and (button == 4 or button == 5):
            if button == 4:
                self.move_focus(size, -1)
            else:
                self.move_focus(size, 1)
        else:
            return urwid.ListBox.mouse_event(self, size, event, button, col, row, focus)

    def keypress(self, size, key):
        return key

    def command(self, size, command, args):
        commands = {
                'nav_up': lambda: self.move_focus(size, -1),
                'nav_down': lambda: self.move_focus(size, 1),
                'nav_page_down': lambda: self.move_focus(size, size[1] - self.SCROLL_SPACE),
                'nav_page_up': lambda: self.move_focus(size, -(size[1] - self.SCROLL_SPACE)),
                'nav_top': lambda: self.move_top(size),
                'nav_bottom': lambda: self.move_bottom(size),
            }

        if command in commands:
            commands[command]()
            return True
        else:
            return False

    def move_top(self, size):
        walker = self.body
        _, cur_pos = walker.get_focus()

        # keep walking
        while True:
            _, new_pos = walker.get_prev(cur_pos)

            # 'till the end
            if new_pos != None:
                cur_pos = new_pos
            else:
                break

        self.change_focus(size, cur_pos)

    def move_bottom(self, size):
        walker = self.body
        _, cur_pos = walker.get_focus()

        # keep walking
        while True:
            _, new_pos = walker.get_next(cur_pos)

            # 'till the end
            if new_pos != None:
                cur_pos = new_pos
            else:
                break

        self.change_focus(size, cur_pos)

    def move_focus(self, size, delta):
        walker = self.body

        # starting point
        _, cur_pos = walker.get_focus()

        if cur_pos == None:
            return

        # where is the focus displayed?
        offset, inset = self.get_focus_offset_inset(size)

        # stepping the desired amount of steps
        for _ in xrange(abs(delta)):
            # up or down
            if delta > 0:
                _, new_pos = walker.get_next(cur_pos)
            else:
                _, new_pos = walker.get_prev(cur_pos)

            # stopping at the end
            if new_pos != None:
                cur_pos = new_pos
            else:
                break

        # calculating the new position (display)
        new_offset = offset + delta
        new_offset = min(new_offset, size[1] - 1 - self.SCROLL_SPACE)
        new_offset = max(new_offset, self.SCROLL_SPACE)

        # actually setting the new focus
        self.change_focus(size, cur_pos, new_offset)

class SelectableText(urwid.Text):

    def selectable(self):
        return True

    def keypress(self, size, key):
        return key

class TextProgress(urwid.FlowWidget):

    def __init__(self, normal, complete, current=0, done=100, satt=None):
        self.normal = normal
        self.complete = complete
        self.current = current
        self.done = done
        self.satt = satt

        self.eighths = [' '] + map(unichr, range(0x258f, 0x2589 - 1, -1))

    def text(self):
        return "%s / %s" % (str(self.current), str(self.done))

    def set_completion(self, value):
        self.current = value
        self._invalidate()

    def set_done(self, value):
        self.done = value
        self._invalidate()

    def rows(self, size, focus=False):
        return 1

    def render(self, size, focus=False):
        (width,) = size

        current = self.current
        done = self.done

        normal = self.normal
        complete = self.complete
        satt = self.satt

        txt = urwid.Text(self.text(), 'center', 'clip')
        canvas = txt.render(size)

        progress = float(current) * width / done if done else 0
        prog_i = int(progress)

        if progress <= 0:
            canvas._attr = [[(normal, width)]]
        elif progress >= width:
            canvas._attr = [[(complete, width)]]
        elif satt and canvas._text[0][prog_i] == ' ':
            # find partial symbol
            part = self.eighths[int(progress % 1 * 8)].encode('utf-8')

            # replace the space
            raw = canvas._text[0]
            canvas._text[0] = raw[:prog_i] + part + raw[prog_i+1:]

            # gather attribute data
            attr = []

            # completed part if it exists
            if prog_i:
                attr.append((complete, prog_i))

            # the partial symbol
            attr.append((satt, len(part)))

            # normal part if it exists
            normal_size = width - prog_i - 1
            if normal_size > 0:
                attr.append((normal, normal_size))

            # set the attributes
            canvas._attr = [attr]

            # adjust new length
            canvas._cs = [[(None, len(canvas._text[0]))]]
        else:
            canvas._attr = [[(complete, prog_i), (normal, width - prog_i)]]

        return canvas

class Prompt(urwid.Edit):

    def __init__(self, prompt, cb, instant=None):
        urwid.Edit.__init__(self, prompt)

        self.cb = cb
        self.instant = instant

    def keypress(self, size, key):
        overwrite = {
                'esc': lambda: self.cb(None),
                'enter': lambda: self.cb(self.get_edit_text()),
                }

        if key in overwrite:
            overwrite[key]()
        else:
            urwid.Edit.keypress(self, size, key)

            if self.instant:
                self.instant(self.get_edit_text())

