# A Textual Spinbox widget

## Demo a Textual spinbox 

Simply run from the repo with [uv](https://docs.astral.sh/uv/)

`uvx --from git+https://github.com/friscorose/textual-spinbox spinbox_demo`

now you can scroll wheel up or down, drag up or down and click the up or down arrows to change the value in the spinbox. A simple ctrl+c to quit.

## Use uv to build an app

Build a silly app with a custom Textual spinbox widget using uv.

`uv init sillyapp`

then

`cd sillyapp`

edit hello.py to contain the following source

```python
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Button, Label
from textual_spinbox import SpinBox

class Statement( Label ):
    silly = reactive( "...a silly statement.", recompose=True )

    def compose(self) -> ComposeResult:
        yield Label( self.silly )

class SpinboxApp(App):
    DEFAULT_CSS = """
    SpinBox {
        width: 13;
    }
    """

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    things = ['albatross', 'boomerang', 'cat', 'dodo', 'ewe', 'flotilla', 'geriatric', 'hopscotch', 'ice flow', 'jalopy', 'Kobayashi Maru', 'lava', 'mycelium', 'narwhal', 'oil tanker', 'pod', 'quaaltagh', 'rat', 'snail', 'tiptoe', 'ukulele', 'verb', 'wheeriemigo', 'xanthippe', 'yill', 'zymurgy']
    def compose(self) -> ComposeResult:
        yield SpinBox( id="pennies" )
        yield SpinBox( range(1,32), id="date" )
        yield SpinBox( self.months, id="month" )
        yield SpinBox( self.things, id="thing" )
        yield Button( "Make", variant="primary", id="make" )
        yield Statement()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "make":
            pennies = self.query_one("#pennies").value
            date = self.query_one("#date").value
            month = self.query_one("#month").value
            thing = self.query_one("#thing").value
            self.query_one("Statement").silly = f"""\
...my bank statement change by {pennies} cents on {month}/{date} \n\
Reason: compulsory {thing} race gambling."""

def exec_main():
    app = SpinboxApp()
    app.run() 

if __name__ == "__main__":
    exec_main()

```

make Textual available to the app

`uv add textual`

then make the textual-spinbox widget available

`uv add "textual-spinbox @ git+https://github.com/friscorose/textual-spinbox"`

now run it

`uv run hello.py`
