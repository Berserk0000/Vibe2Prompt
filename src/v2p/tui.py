from textual import work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, VerticalScroll
from textual.screen import Screen
from textual.widgets import Input, LoadingIndicator, Markdown, Static

from .banner import render_banner
from .llm import get_structured_prompt

import pyperclip


class ChatScreen(Screen):
    BINDINGS = [
        Binding("ctrl+c", "quit", "Exit"),
    ]


class Vibe2Prompt(App):
    TITLE = "⚡ vibe2prompt"
    SUB_TITLE = "Technical Spec Engine"
    ENABLE_COMMAND_PALETTE = False
    SCREENS = {"chat": ChatScreen}

    def get_default_screen(self) -> ChatScreen:
        return ChatScreen()

    CSS = """
    $markdown-h1-color: #89B4FA;
    $markdown-h1-background: transparent;
    $markdown-h1-text-style: bold;
    $markdown-h2-color: #94E2D5;
    $markdown-h2-text-style: bold;
    $markdown-h3-color: #C6A0F6;
    $markdown-h3-text-style: bold;
    $markdown-h4-color: #F5C2E7;
    $markdown-h5-color: #FAB387;
    $markdown-h6-color: #A6E3A1;

    Screen {
        background: #181825;
        layout: vertical;
    }

    #banner-section {
        background: #1E1E2E;
        border-bottom: tall #313244;
        padding: 1 2;
        height: auto;
    }
    #banner {
        width: 100%;
        height: auto;
        content-align: center middle;
        text-style: bold;
    }
    #banner-subtitle {
        width: 100%;
        content-align: center middle;
        color: #6C7086;
        margin-top: 1;
    }

    #output-scroll {
        background: #181825;
        overflow-y: scroll;
        scrollbar-color: #89B4FA;
        scrollbar-background: #313244;
    }
    #output-area {
        height: auto;
        padding: 1 2;
    }

    .user-wrap {
        height: auto;
        align: right top;
        margin-bottom: 1;
    }
    .user-card {
        width: 70%;
        background: #1E1E2E;
        color: #CDD6F4;
        border: round #89B4FA;
        padding: 1 2;
    }

    .loading {
        height: 3;
        margin-bottom: 1;
        background: #1E1E2E;
        border: round #89B4FA;
        color: #89B4FA;
        text-style: not reverse;
    }

    .error-box {
        background: #1E1E2E;
        color: #F38BA8;
        border: round #F38BA8;
        padding: 1 2;
        margin-bottom: 1;
    }

    .result-card {
        background: #1E1E2E;
        color: #CDD6F4;
        border: round #94E2D5;
        border-title-color: #94E2D5;
        border-title-style: bold;
        padding: 1 2;
        margin-bottom: 1;
    }
    .result-card MarkdownFence {
        background: #181825;
    }

    #input-section {
        dock: bottom;
        layout: horizontal;
        height: auto;
        padding: 1 2;
        background: #1E1E2E;
        border-top: tall #313244;
    }
    #input-prompt {
        content-align: center middle;
        height: 3;
        width: auto;
        margin-right: 1;
        color: #89B4FA;
    }
    #input {
        height: 3;
        padding: 0 1;
        background: #181825;
        color: #CDD6F4;
        border: round #585B70;
    }
    #input:focus {
        border: round #89B4FA;
    }

    #status-bar {
        dock: bottom;
        height: 1;
        background: #181825;
        color: #A6ADC8;
        padding: 0 2;
    }
    """

    BINDINGS = [
        ("ctrl+y", "copy_to_clipboard", "Copy Prompt"),
        ("up", "scroll_up", "Scroll Up"),
        ("down", "scroll_down", "Scroll Down"),
        ("pageup", "scroll_page_up", "Scroll Up"),
        ("pagedown", "scroll_page_down", "Scroll Down"),
    ]

    def compose(self) -> ComposeResult:
        with Container(id="banner-section"):
            yield Static("", id="banner")
            yield Static("Technical Spec Engine", id="banner-subtitle")
        yield VerticalScroll(
            Container(id="output-area"),
            can_focus=True,
            id="output-scroll",
        )
        with Container(id="input-section"):
            yield Static("❯", id="input-prompt")
            yield Input(
                placeholder="Type an informal prompt — e.g. 'make a button that increments a counter'…",
                id="input",
            )
        yield Static(
            "[bold #89B4FA]Ctrl+C[/] Exit   |   [bold #89B4FA]Ctrl+Y[/] Copy Prompt   |   [bold #89B4FA]PageUp/PageDown[/] Scroll",
            id="status-bar",
        )

    def on_mount(self) -> None:
        width = self.size.width
        self.query_one("#banner").update(render_banner("vibe2prompt", width))

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        if not event.value:
            return

        output_area = self.query_one("#output-area")
        output_area.mount(
            Container(Static(f"❯ {event.value}", classes="user-card"), classes="user-wrap")
        )

        loading = LoadingIndicator(classes="loading")
        output_area.mount(loading)
        self._scroll_to_end()

        prompt = event.value
        event.input.value = ""
        self._generate(prompt, loading)

    @work(thread=True)
    async def _generate(self, prompt: str, loading: LoadingIndicator) -> None:
        try:
            result = get_structured_prompt(prompt)
        except Exception as error:
            self.call_from_thread(self._show_error, str(error), loading)
        else:
            self.call_from_thread(self._show_result, result, loading)

    def _show_result(self, result: str, loading: LoadingIndicator) -> None:
        loading.remove()
        result_view = Markdown(result, classes="result-card")
        result_view.border_title = " Technical Spec "
        self.query_one("#output-area").mount(result_view)
        self.last_result = result
        self._scroll_to_end()

    def _show_error(self, message: str, loading: LoadingIndicator) -> None:
        loading.remove()
        self.query_one("#output-area").mount(
            Static(f"⚠ Error: {message}", classes="error-box")
        )
        self._scroll_to_end()

    def _scroll_to_end(self) -> None:
        self.query_one("#output-scroll").scroll_end(animate=True)

    def action_copy_to_clipboard(self) -> None:
        if hasattr(self, "last_result"):
            pyperclip.copy(self.last_result)
            self.notify("Prompt copied to clipboard!", title="Success")
        else:
            self.notify("Nothing to copy yet.", title="Info")

    def action_scroll_up(self) -> None:
        self.query_one("#output-scroll").scroll_up()

    def action_scroll_down(self) -> None:
        self.query_one("#output-scroll").scroll_down()

    def action_scroll_page_up(self) -> None:
        self.query_one("#output-scroll").scroll_page_up()

    def action_scroll_page_down(self) -> None:
        self.query_one("#output-scroll").scroll_page_down()


def main() -> None:
    Vibe2Prompt().run()


if __name__ == "__main__":
    main()
