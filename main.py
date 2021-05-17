from kivy.app import App
from kivy.graphics import Color
from kivy.graphics.vertex_instructions import Line
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty


class MainWidget(Widget):
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    V_NB_LINES = 7
    V_LINES_SPACING = 0.1  #% of screen width 
    vertical_lines = []
    def __init__(self,**kwargs):
        super(MainWidget, self).__init__(**kwargs)
        # print("INIT W: " + str(self.width) + "INIT H: " + str(self.height))
        self.init_vertical_lines()

    def on_parent(self, widget, parent):
        # print("On Parent W: " + str(self.width) + "On Parent H: " + str(self.height))
        pass

    def on_size(self, *args):
        # print("On Size W: " + str(self.width) + "On Size H: " + str(self.height))
        # self.perspective_point_x = self.width/2
        # self.perspective_point_y = self.height*0.75
        self.update_vertical_lines()

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
        spacing = self.V_LINES_SPACING * self.width
        offset = -int(self.V_NB_LINES/2)
        for i in range(0, self.V_NB_LINES):
            line_X = int(centeral_line_x + offset * spacing)
            self.vertical_lines[i].points = [line_X, 0, line_X, self.height]
            offset += 1

class GalaxyApp(App):
    pass


GalaxyApp().run()