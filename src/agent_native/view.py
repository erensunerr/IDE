from textual.app import App
from textual.widgets import Static, Input
from textual.containers import Vertical
from textual import events

class IDEApp(App):
    def __init__(self, ide):
        super().__init__()
        self.ide = ide

    def compose(self):
        self.buffer_display = Static("\n".join(self.ide.buffer))
        self.command_input = Input(placeholder="replace_line(2, 'foo')")
        yield Vertical(self.buffer_display, self.command_input)

    async def on_input_submitted(self, msg: Input.Submitted):
        try:
            cmd = msg.value
            fn_name = cmd.split('(')[0]
            args = eval(f"{cmd[cmd.find('('):]}")  # basic eval, replace with safer parser later
            if not isinstance(args, tuple):
                args = (args,)
            self.ide.tools[fn_name](*args)
        except Exception as e:
            self.buffer_display.update(f"Error: {e}")
        else:
            self.buffer_display.update("\n".join(self.ide.buffer))
    async def on_key(self, event: events.Key):
        if event.key == "ctrl+z":
            await self.action_quit()