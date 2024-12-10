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
        width: 10;
    }
    """

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    def compose(self) -> ComposeResult:
        yield SpinBox( id="pennies" )
        yield SpinBox( range(1,32), id="date" )
        yield SpinBox( self.months, id="month" )
        yield Button( "Make", variant="primary", id="make" )
        yield Statement()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "make":
            pennies = self.query_one("#pennies").value
            date = self.query_one("#date").value
            month = self.query_one("#month").value
            self.query_one("Statement").silly = f"""\
...my bank statement change by {pennies} cents on {month}/{date} \n\
Reason: compulsory snail race gambling."""

def exec_main():
    app = SpinboxApp()
    app.run() 

if __name__ == "__main__":
    exec_main()

