import datetime

from pyface.timer.api import CallbackTimer
from traits.api import Button, Datetime, HasTraits, Instance, Int, observe
from traitsui.api import HGroup, Item, View, spring
from traitsui.qt4.extra.led_editor import LEDEditor

class CountdownView(HasTraits):

    timer = Instance(CallbackTimer)

    countdown = Int(300)

    start = Button()

    stop = Button()

    reset = Button()

    def _update_time(self):
        self.countdown -= 1

    @observe('start')
    def _start_timer(self, event):
        self.timer.start()

    @observe('stop')
    def _stop_timer(self, event):
        self.timer.stop()

    @observe('reset')
    def _reset_timer(self, event):
        self.timer.stop()
        self.timer.repeat = 300

    def _timer_default(self):
        return CallbackTimer(
            interval=1.0,  # call roughly every second
            repeat=300,  # call this many times
            callback=self._update_time,
        )

    view = View(
        Item('countdown', editor=LEDEditor()),
        HGroup(
            spring,
            Item('start', enabled_when='not object.timer.active'),
            Item('stop', enabled_when='object.timer.active'),
            Item('reset', enabled_when='not object.timer.active'),
        )
    )

if __name__ == '__main__':
    countdown = CountdownView()
    countdown.configure_traits()
