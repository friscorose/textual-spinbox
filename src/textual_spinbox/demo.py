from textual.app import App, ComposeResult
from textual_spinbox import SpinBox

class SpinboxApp(App):
    DEFAULT_CSS = """
    SpinBox {
        width: 10;
    }
    """

    def compose(self) -> ComposeResult:
        yield SpinBox()

def exec_main():
    app = SpinboxApp()
    app.run() 

if __name__ == "__main__":
    exec_main()

