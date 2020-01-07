import pyglet
# import wx
# from pyautogui import Point
from math import sqrt
from PIL import Image

from pyglet.gl import glColor4f, glLineWidth, glBegin, glVertex2f, glEnd, GL_LINES, GL_COLOR_BUFFER_BIT, glClear, \
    glClearColor, GL_TRIANGLES
# from pyglet.gl import *
from pyglet.window import mouse


def line(x0, y0, x, y, color=(1, 0, 0, 1), thickness=1):
    glColor4f(*color)
    glLineWidth(thickness)
    glBegin(GL_LINES)
    glVertex2f(x0, y0)
    glVertex2f(x, y)
    glEnd()


class Quad:
    def __init__(self, x, y, w, h):
        self.indices = [0, 1, 2, 2, 3, 0]
        self.vertex = [-0.5, -0.5, 0.0, 0.5, -0.5, 0.0, 0.5, 0.5, 0.0, -0.5, 0.5, 0.0]
        self.color = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, ]

    def render(self):
        self.vertices = pyglet.graphics.draw_indexed(4, GL_TRIANGLES, self.indices, ('v3f', self.vertex),
                                                     ('c3f', self.color))


def dist(x0, y0, x, y, r):
    d = sqrt((x - x0) ** 2 + (y - y0) ** 2)
    return d < r


def mediana(x1, x2):
    return abs(x1 + x2) // 2


def border_polyline(points):
    print(points)
    if points == []:
        return 0, 0, 0, 0
    x_min = points[0]['x']
    y_min = points[0]['y']
    x_max = points[0]['x']
    y_max = points[0]['y']
    for p in points:
        if p['x'] > x_max:
            x_max = p['x']
        if p['y'] > y_max:
            y_max = p['y']
        if p['x'] < x_min:
            x_min = p['x']
        if p['y'] < y_min:
            y_min = p['y']

    return x_min, y_min, x_max, y_max


class ColorDialog(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.label = pyglet.text.Label("0" * 8,
                                       font_name="Times New Roman",
                                       font_size=18,
                                       color=(255, 0, 0, 255),
                                       x=50,
                                       y=50,
                                       anchor_x="center",
                                       anchor_y="center")

    def on_draw(self):
        # color_dialog.clear()
        self.label.draw()


class MyWindow(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(400, 30)
        glClearColor(0.2, 0.3, 0.2, 1.0)
        self.figures = []
        self.buttons = [
            {'id': 1, 'x': 5, 'y': 5, 'text': 'btn', 'image': pyglet.resource.image('img/pen.png'), 'tool': 1},
            {'id': 2, 'x': 40, 'y': 5, 'text': 'btn', 'image': pyglet.resource.image('img/err.png'), 'tool': 2},
        ]
        self.poly = []
        self.x0, self.y0 = 0, 0
        self.cx, self.cy = 0, 0
        self.penWidth = 1
        self.errSize = 20
        self.tool = 1
        self.f = True
        self.fullscr = False
        self.penColor = (1, 0, 0, 1)

    def on_key_press(self, symbol, modifiers):
        if symbol == 65307:
            window.close()
        elif symbol == 99:  # Change color
            pass
            # color_dialog.set_visible(True)
        elif symbol == 65451:  # Change thickness +
            self.penWidth += 2
        elif symbol == 65453:  # Change thickness
            self.penWidth -= 2
            if self.penWidth < 1:
                self.penWidth = 1
        elif symbol == 65362:  # move canvas up
            self.cy += 50
        elif symbol == 65364:  # Change canvas down
            self.cy -= 50
        elif symbol == 65361:  # Change canvas left
            self.cx -= 50
        elif symbol == 65363:  # Change canvas right
            self.cx += 50
        elif symbol == 102:  # full screen
            self.fullscr = not self.fullscr
            window.set_fullscreen(self.fullscr)
            window.clear()
        elif symbol == 112:  # set pen
            self.tool = 1
        elif symbol == 101:  # set erazer
            self.tool = 2
        else:
            print('A key was pressed')
            print(symbol)
        window.clear()

    def on_mouse_press(self, x, y, button, modifier):
        self.f = True
        if button == mouse.LEFT:
            for btn in self.buttons:
                if (btn['x'] < x < btn['x'] + 32) and (btn['y'] < y < btn['y'] + 32):
                    self.tool = btn['tool']
                    self.f = False
                    break
            if self.f:
                if self.tool == 1:
                    # window.clear()
                    self.x0, self.y0 = x-self.cx, y-self.cy
                    self.poly.clear()
                    self.poly.append({'x': self.x0, 'y': self.y0})

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        window.clear()
        if self.f:
            if self.tool == 1:
                # self.poli.append({'x':self.x0, 'y':self.y0})
                self.poly.append({'x': x - self.cx, 'y': y - self.cy})
                # %%%%%%%%%%%%% it is slowly
                # window.clear()
                x0 = self.poly[0]['x']
                y0 = self.poly[0]['y']
                for p in self.poly:
                    x_ = p['x']
                    y_ = p['y']
                    # line(x0 , y0 , x , y , color=self.penColor, thickness=self.penWidth)
                    line(x0 + self.cx, y0 + self.cy, x_ + self.cx, y_ + self.cy, color=self.penColor, thickness=self.penWidth)
                    x0, y0 = x_, y_

                # x0, y0 = self.x0, self.y0
                # line(x0 + self.cx, y0 + self.cy, x + self.cx, y + self.cy, color=self.penColor,
                #      thickness=self.penWidth)
                # %%%%%%%%%%%%%%%%
                self.x0, self.y0 = x, y
            elif self.tool == 2:
                for f in self.figures:
                    x_min, y_min, x_max, y_max = border_polyline(f['p'])
                    if dist((x_max + x_min) // 2, (y_max + y_min) // 2, x- self.cx, y- self.cy, self.errSize):
                        print('del')
                        f['fordel'] = True
                        break
                new_list = []
                for f in self.figures:
                    if not f['fordel']:
                        new_list.append(f)
                self.figures = new_list.copy()
                window.clear()

    def on_mouse_release(self, x, y, button, modifiers):
        if self.f:
            # window.clear()
            print("on_mouse_release")

            if self.tool == 1:
                k = {}
                k['name'] = 'polyline'
                k['p'] = self.poly.copy()
                k['color'] = self.penColor
                k['thickness'] = self.penWidth
                k['fordel'] = False
                self.figures.append(k)
        window.clear()

    def on_draw(self):
        # window.clear()
        for f in self.figures:
            if f['name'] == 'polyline':
                x0 = f['p'][0]['x']
                y0 = f['p'][0]['y']
                for p in f['p']:
                    x = p['x']
                    y = p['y']
                    # line(x0 , y0 , x , y , color=f['color'], thickness=f['thickness'])
                    line(x0 + self.cx, y0 + self.cy, x + self.cx, y + self.cy, color=f['color'], thickness=f['thickness'])
                    x0, y0 = x, y
        # Draw grid

        # Draw buttons

        for btn in self.buttons:
            btn['image'].blit(btn['x'], btn['y'])


if __name__ == "__main__":
    window = MyWindow(caption="WhiteBoard", resizable=True, fullscreen=False)
    # color_dialog = ColorDialog(200, 100, caption="Color dialog", resizable=False)
    # color_dialog.set_visible(False)
    window.clear()
    window.on_draw()
    # color_dialog.on_draw()
    pyglet.app.run()
