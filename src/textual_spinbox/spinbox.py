"""Widget definitions for SpinBox and a special 1 cell button child"""
from collections import deque
from rich.text import Text

from textual import events
from textual.app import ComposeResult, RenderResult
from textual.containers import Horizontal, Vertical
from textual.events import MouseScrollDown, MouseScrollUp
from textual.pad import HorizontalPad
from textual.widget import Widget
from textual.widgets import Button, Input, Label

class CellButton( Button, can_focus=False ):
    """A unit width Button based widget that issues scroll events
    instead of clicks, as an integral part of a spinbox
    it has no focus of its own"""

    def on_mouse_up(self, event):
        """Convert button up to suitable scrollevent"""
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
        """Handle button down as trigger to capture"""
        event.stop()

    def render(self) -> RenderResult:
        """Monkey patch the render for single cell button"""
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


class SpinBox(Widget):
    """Bundle up widgets and events to create a spinbox widget"""
    DEFAULT_CSS = """
    SpinBox {
        height: 3;
        min-height: 3;
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
            width: 100%;
        }
    }
    """

    def __init__( # pylint: disable=R0913
            self,
            iter_val = None,
            *,
            name: str | None = None,
            id: str | None = None,
            classes: str | None = None,
            disabled: bool = False,
        ) -> None:
        """Initialize a SpinBox.

        Args:
            iter_val: an iterator instance.
            name: The name of the widget.
            id: The ID of the widget in the DOM.
            classes: The CSS classes for the widget.
            disabled: Whether the widget is disabled or not.
        """
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.tooltip = "Scroll, Drag or Key Up/Down."
        if iter_val is not None:
            self.iter_ring = deque( iter_val )
            self.value = str( self.iter_ring[0] )
            self._sb_type = "text"
        else:
            self.iter_ring = iter_val
            self.value = str( 0 )
            self._sb_type = "integer"

    def on_key(self, event: events.Key)-> None:
        """Event handler for keyboard input"""
        if event.key == 'up':
            event.stop()
            self.delta_v( 1 )
        elif event.key == 'down':
            event.stop()
            self.delta_v( -1 )

    draging = False
    def on_mouse_move(self, event):
        """A change in y position will inc/dec value"""
        if self.draging and event.delta_y < 0:
            self.delta_v( 1 )
        elif self.draging and event.delta_y > 0:
            self.delta_v( -1 )

    def on_mouse_up(self):
        """clean up mouse handling"""
        self.draging = False
        self.release_mouse()

    def on_mouse_down(self):
        """While widget owns a mouse button down any move on the
        vertical will adjust the value up or down respectively."""
        self.draging = True
        self.capture_mouse()

    def on_mouse_scroll_up(self, event):
        """The driver event for increasing the widget value from child"""
        event.stop()
        self.delta_v( 1 )

    def on_mouse_scroll_down(self, event):
        """The driver event for decreasing the widget value from child"""
        event.stop()
        self.delta_v( -1 )

    def delta_v( self, dv ):
        """A handler to adjust the input widget value"""
        sb_input = self.query_one("#sb_input")
        if self.iter_ring is not None:
            self.iter_ring.rotate( -dv )
            self.value = str( self.iter_ring[0] )
        else:
            self.value = str( int( sb_input.value ) + dv )
        sb_input.value = self.value
        sb_input.action_home()
        if len( self.value ) > sb_input.size.width:
            self.query_one("#sb_overflow").update("…")
        else:
            self.query_one("#sb_overflow").update("¦")
        self.refresh(layout=True)

    def compose(self) -> ComposeResult:
        """Widget structure generator"""
        with Horizontal( id="sb_box" ):
            yield Input( self.value, type=self._sb_type, id="sb_input")
            with Vertical( id="sb_control" ):
                yield CellButton("▲", id="sb_up" )
                yield Label("¦", id="sb_overflow")
                yield CellButton("▼", id="sb_dn" )
