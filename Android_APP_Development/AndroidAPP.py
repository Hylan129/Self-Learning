from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse


class PaintWidget(Widget):
    
    # react to user input
    def on_touch_down(self, touch):
        with self.canvas:
            Color(1,1,0)
            d = 30.
            Ellipse(pos=(touch.x - d/2, touch.y - d/2), size=(d, d))


class PaintApp(App):
    def build(self):
        return PaintWidget()


if __name__ == '__main__':
    PaintApp().run()
"""
title = <paint_hylan>
author = <Hylan>
orientaion = <portrait>
/storage/emulated/0/kivy
"""