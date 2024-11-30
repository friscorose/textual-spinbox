from rich.text import Text, TextType

from textual import events, on
from textual.app import App, ComposeResult, RenderResult
from textual.containers import Horizontal, Vertical
from textual.events import MouseScrollDown, MouseScrollUp
from textual.pad import HorizontalPad
from textual.widgets import Button, Input, Label

class CellButton( Button, can_focus=False ):

    def on_mouse_up(self, event):
        event.stop()
        if self.id == "sb_up":
            self.post_message( MouseScrollUp(self,
                                             event.x,
                                             event.y,
                                             event.delta_x,
                                             event.delta_y,
                                             1, 0, 0, 0) )
        elif self.id == "sb_dn":
            self.post_message( MouseScrollDown(self,
                                             event.x,
                                             event.y,
                                             event.delta_x,
                                             event.delta_y,
                                             1, 0, 0, 0) )

    def on_mouse_down(self, event):
        event.stop()

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

    draggable = False
    dragged = False
    def on_mouse_move(self, event):
        if self.draggable and event.delta_y < 0:
            self.dragged = True
            self.post_message( MouseScrollUp(self,
                                             event.x,
                                             event.y,
                                             event.delta_x,
                                             event.delta_y,
                                             1, 0, 0, 0) )
        elif self.draggable and event.delta_y > 0:
            self.dragged = True
            self.post_message( MouseScrollDown(self,
                                               event.x,
                                               event.y,
                                               event.delta_x,
                                               event.delta_y,
                                               1, 0, 0, 0) )

    def on_mouse_up(self, event):
        self.draggable = False
        if self.dragged:
            self.dragged = False
        self.release_mouse()

    def on_mouse_down(self, event):
        self.draggable = True
        self.capture_mouse()

    def on_mouse_scroll_up(self):
        self.delta_v( 1 )

    def on_mouse_scroll_down(self):
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
                yield Label("¦")
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
