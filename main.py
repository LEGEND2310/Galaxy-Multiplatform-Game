from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

from kivy import platform
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import Clock
from kivy.graphics import Color
from kivy.graphics.vertex_instructions import Line
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty


class MainWidget(Widget):
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    V_NB_LINES = 10
    V_LINES_SPACING = 0.25  #% of screen width 
    vertical_lines = []

    H_NB_LINES = 15
    H_LINES_SPACING = 0.1  #% of screen height 
    horizontal_lines = []

    speed = 4
    current_offset_y = 0

    speed_x = 12
    current_speed_x = 0
    current_offset_x = 0

    def __init__(self,**kwargs):
        super(MainWidget, self).__init__(**kwargs)
        # print("INIT W: " + str(self.width) + "INIT H: " + str(self.height))
        self.init_vertical_lines()
        self.init_horizontal_lines()

        if self.is_desktop:
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)

        Clock.schedule_interval(self.update, 1/60)

    def keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None
        
    def is_desktop(self):
        if platform in('linux','win', 'macosx'):
            return True
        else:
            return False

    def on_parent(self, widget, parent):
        # print("On Parent W: " + str(self.width) + "On Parent H: " + str(self.height))
        pass

    def on_size(self, *args):
        # print("On Size W: " + str(self.width) + "On Size H: " + str(self.height))
        # self.perspective_point_x = self.width/2
        # self.perspective_point_y = self.height*0.75
        # self.update_vertical_lines()
        # self.update_horizontal_lines()
        pass


    def on_perspective_point_x(self, widget, value):
        print("Perspective_X: "+ str(value))

    def on_perspective_point_y(self, widget, value):
        print("Perspective_Y: "+ str(value))

    def init_vertical_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            # self.line = Line(points=[100, 0, 100, 100])
            for i in range(0, self.V_NB_LINES):
                self.vertical_lines.append(Line())

    def update_vertical_lines(self):
        centeral_line_x = int(self.width/2)
        spacing_x = self.V_LINES_SPACING * self.width
        offset = -int(self.V_NB_LINES/2) + 0.5
        for i in range(0, self.V_NB_LINES):
            line_X = int(centeral_line_x + offset * spacing_x + self.current_offset_x)

            x1, y1 = self.transform(line_X, 0)
            x2, y2 = self.transform(line_X, self.height)
            self.vertical_lines[i].points = [x1, y1, x2, y2]
            offset += 1
    
    def init_horizontal_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.H_NB_LINES):
                self.horizontal_lines.append(Line())

    def update_horizontal_lines(self):
        centeral_line_x = int(self.width/2)
        spacing = self.V_LINES_SPACING * self.width
        offset = int(self.V_NB_LINES/2) - 0.5

        xmin = centeral_line_x - offset*spacing + self.current_offset_x
        xmax = centeral_line_x + offset*spacing + self.current_offset_x
        spacing_y = self.H_LINES_SPACING * self.height

        for i in range(0, self.H_NB_LINES):
            line_Y = i * spacing_y - self.current_offset_y
            x1, y1 = self.transform(xmin, line_Y)
            x2, y2 = self.transform(xmax, line_Y)
            self.horizontal_lines[i].points = [x1, y1, x2, y2]

    def transform(self, x, y):
        # return self.transform_2D(x, y)
        return self.transform_perspective(x, y)

    def transform_2D(self, x, y):
        return int(x), int(y)

    def transform_perspective(self, x, y):
        lin_y = (y / self.height)*self.perspective_point_y
        if lin_y  > self.perspective_point_y:
            lin_y = self.perspective_point_y

        diff_x = x - self.perspective_point_x
        diff_y = self.perspective_point_y - lin_y
        factor_y = diff_y / self.perspective_point_y
        factor_y = pow(factor_y, 3)

        tr_x = self.perspective_point_x + diff_x * factor_y
        tr_y = self.perspective_point_y - factor_y * self.perspective_point_y

        return int(tr_x), int(tr_y)
    
    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.current_speed_x = self.speed_x
        elif keycode[1] == 'right':
            self.current_speed_x = -self.speed_x
        return True

    def on_keyboard_up(self, keyboard, keycode):
        self.current_speed_x = 0
        return True

    def on_touch_down(self, touch):
        if touch.x < self.width/2:
            # print("<-")
            self.current_speed_x = self.speed_x 
        else:
            # print("->")
            self.current_speed_x = -self.speed_x 

    
    def on_touch_up(self, touch):
        print("UP")
        self.current_speed_x = 0

    def update(self, dt):
        # print("update")
        time_factor = dt * 60
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.current_offset_y += self.speed * time_factor

        spacing_y = self.H_LINES_SPACING * self.height
        if self.current_offset_y >= spacing_y:
            self.current_offset_y -= spacing_y

        self.current_offset_x += self.current_speed_x * time_factor


class GalaxyApp(App):
    pass


GalaxyApp().run()