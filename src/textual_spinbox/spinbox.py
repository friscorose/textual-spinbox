from textual import events, on
from textual.pad import HorizontalPad
from rich.text import Text, TextType
from textual.app import RenderResult

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Input, Label

class CellButton( Button, can_focus=False ):
    def render(self) -> RenderResult:
            assert isinstance(self.label, Text)
            label = self.label.copy()
            label.stylize_before(self.rich_style)
            return HorizontalPad(
                label,
                0,
                0,
                self.rich_style,
                self._get_justify_method() or "center",
            )


class SpinBox(Horizontal):

    def on_mouse_scroll_up(self):
        self.delta_v( 1 )

    def on_mouse_scroll_down(self):
        self.delta_v( -1 )

    @on( Button.Pressed )
    def click_handler(self, event):
        if event.button.id == "sb_up":
            self.delta_v( 1 )
        if event.button.id == "sb_dn":
            self.delta_v( -1 )

    def delta_v( self, dv ):
        foo = int( self.query_one("#sb_field").value ) + dv
        self.query_one("#sb_field").value = str( foo )
        self.refresh(layout=True)

    def compose(self) -> ComposeResult:
        with Horizontal( id="sb_box" ):
            yield Input("0", type="integer", id="sb_field")
            with Vertical( id="sb_control" ):
                yield CellButton("▲", id="sb_up" )
                yield Label("|")
                yield CellButton("▼", id="sb_dn" )

class SpinboxApp(App):
    CSS_PATH = "spinbox.tcss"

    def compose(self) -> ComposeResult:
        yield Label(" A SpinBox")
        yield SpinBox()

def exec_main():
    app = SpinboxApp()
    app.run() 

if __name__ == "__main__":
    exec_main()
