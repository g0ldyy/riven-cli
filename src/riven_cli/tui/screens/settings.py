from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.layout import Layout


class SettingsScreen:
    def __init__(self, app):
        self.app = app

    def render(self):
        header = Panel(
            Align.center(Text("Riven CLI - Settings", style="bold green")), style="blue"
        )

        body = Align.center(
            Text(
                "Settings are not yet implemented.\n\nEdit ~/.config/riven-cli/config.toml manually.",
                justify="center",
                style="yellow",
            )
        )

        footer = Panel(
            Align.center(Text("[Q] Back", style="bold red")), title="Navigation"
        )

        layout = Layout()
        layout.split(Layout(header, size=3), Layout(body), Layout(footer, size=3))
        return layout

    async def handle_input(self, key: str):
        if key.lower() == "q":
            self.app.switch_to("dashboard")
