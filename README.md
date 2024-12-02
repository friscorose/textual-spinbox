# A Textual Spinbox widget

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
        width: 13;
    }
    """

    def compose(self) -> ComposeResult:
        yield SpinBox()

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
