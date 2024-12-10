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
from textual_spinbox import SpinBox

class SpinboxApp(App):
    DEFAULT_CSS = """
    SpinBox {
        width: 10;
    }
    """

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    def compose(self) -> ComposeResult:
        yield SpinBox( id="pennies" )
        yield SpinBox( range(1,32), id="date" )
        yield SpinBox( self.months, id="month" )

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
