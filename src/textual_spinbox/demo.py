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

