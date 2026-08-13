from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll
from textual.widgets import Header, Footer, Input, Markdown, LoadingIndicator
from .llm import get_structured_prompt
import pyperclip

class Vibe2Prompt(App):
    CSS = """
    Screen {
        layout: vertical;
    }
    #output {
        height: 1fr;
        border: solid green;
    }
    #input {
        dock: bottom;
        height: 3;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield VerticalScroll(Markdown(id="output"))
        yield Input(placeholder="Type your informal prompt here...", id="input")
        yield Footer()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        if not event.value:
            return
        
        self.query_one("#output", Markdown).update("Generating prompt...")
        
        # In a real app, do this in a worker to keep UI responsive
        structured_prompt = get_structured_prompt(event.value)
        
        self.query_one("#output", Markdown).update(structured_prompt)
        pyperclip.copy(structured_prompt)
        self.notify("Prompt copied to clipboard!", title="Success")

def main():
    app = Vibe2Prompt()
    app.run()

if __name__ == "__main__":
    main()
