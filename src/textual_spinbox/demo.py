"""A silly demo of the SpinBox widget"""
from calendar import month_name
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Button, Label
from textual_spinbox import SpinBox

class Statement( Label ):
    """Make label reactive"""
    silly = reactive( "...a silly statement.", recompose=True )

    def compose(self) -> ComposeResult:
        yield Label( self.silly )

class SpinboxApp(App):
    """The main demo app"""
    DEFAULT_CSS = """
    SpinBox {
        width: 13;
    }
    """

    months = list(month_name)[1:]
    things = ['albatross', 'boomerang', 'cat', 'dodo', 'ewe', 'flotilla', 'geriatric', 'hopscotch', 'ice flow', 'jalopy', 'Kobayashi Maru', 'lava', 'mycelium', 'narwhal', 'oil tanker', 'pod', 'quaaltagh', 'rat', 'snail', 'tiptoe', 'ukulele', 'verb', 'wheeriemigo', 'xanthippe', 'yill', 'zymurgy']
    def compose(self) -> ComposeResult:
        yield SpinBox( id="pennies" )
        yield SpinBox( range(1,32), id="date" )
        yield SpinBox( self.months, id="month" )
        yield SpinBox( self.things, id="thing" )
        yield Button( "Make", variant="primary", id="make" )
        yield Statement()

    def on_button_pressed(self, event: Button.Pressed):
        """What to do when the button is clicked"""
        if event.button.id == "make":
            pennies = self.query_one("#pennies").value
            date = self.query_one("#date").value
            month = self.query_one("#month").value
            thing = self.query_one("#thing").value
            self.query_one("Statement").silly = f"""\
...my bank statement change by {pennies} cents on {month}/{date} \n\
Reason: compulsory {thing} race gambling."""

def exec_main():
    """Allow call by script handler in pyproject"""
    app = SpinboxApp()
    app.run()

if __name__ == "__main__":
    exec_main()
