from rich.text import Text, TextType

from textual import events, on
from textual.app import App, ComposeResult, RenderResult
from textual.containers import Horizontal, Vertical
from textual.events import MouseScrollDown, MouseScrollUp
from textual.pad import HorizontalPad
from textual.widgets import Button, Input, Label

"""A unit width Button based widget that issues scroll events
instead of clicks, as an integral part of a spinbox
it has no focus of its own"""
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

    DEFAULT_CSS = """
    SpinBox {
        height: 3;
        #sb_control {
            background: $background-lighten-1;
            height: 3;
            width: 1;
            position: relative;
            offset: -3 0;
            CellButton {
                color: $primary;
                background: $background-lighten-1;
                min-width: 1;
                width: 1;
                height: 1;
                border-top: none;
                border-bottom: none;
            }
        }
        #sb_input {
            width: 1fr;
        }
    }
    """
    draging = False
    """Any change in y position while draging will issue
    pseudo-scroll events"""
    def on_mouse_move(self, event):
        if self.draging and event.delta_y < 0:
            self.post_message( MouseScrollUp(self,
                                             event.x,
                                             event.y,
                                             event.delta_x,
                                             event.delta_y,
                                             1, 0, 0, 0) )
        elif self.draging and event.delta_y > 0:
            self.post_message( MouseScrollDown(self,
                                               event.x,
                                               event.y,
                                               event.delta_x,
                                               event.delta_y,
                                               1, 0, 0, 0) )

    def on_mouse_up(self, event):
        self.draging = False
        self.release_mouse()

    """While widget owns a mouse button down any move on the 
    vertical will generate scrollevents to adjust the 
    value up or down respectively."""
    def on_mouse_down(self, event):
        self.draging = True
        self.capture_mouse()

    """The driver event for increasing the widget value"""
    def on_mouse_scroll_up(self):
        self.delta_v( 1 )

    """The driver event for decreasing the widget value"""
    def on_mouse_scroll_down(self):
        self.delta_v( -1 )

    """A handler to adjust the input widget value"""
    def delta_v( self, dv ):
        sb_input = self.query_one("#sb_input")
        str_val = str( int( sb_input.value ) + dv )
        sb_input.value = str_val
        if len( str_val ) > sb_input.size.width:
            self.query_one("#sb_overflow").update("…")
        else:
            self.query_one("#sb_overflow").update("¦")
        self.refresh(layout=True)

    def compose(self) -> ComposeResult:
        with Horizontal( id="sb_box" ):
            yield Input("0", type="integer", id="sb_input")
            with Vertical( id="sb_control" ):
                yield CellButton("▲", id="sb_up" )
                yield Label("¦", id="sb_overflow")
                yield CellButton("▼", id="sb_dn" )

