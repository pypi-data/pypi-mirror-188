# Textual: Terminal

A terminal widget for [Textual](https://github.com/Textualize/textual) using
[Pyte](https://github.com/selectel/pyte) as a linux terminal emulator.

<details><summary>Textual application example with two terminal widgets:</summary>

    
![textual_terminal_example](https://user-images.githubusercontent.com/922559/214794889-4d376da1-6aa9-4576-a01d-0beee2536e41.png)

</details>

## Usage

```python
from textual_terminal import Terminal

class TerminalApp(App):
    def compose(self) -> ComposeResult:
        yield Terminal(command="htop", id="terminal_htop")
        yield Terminal(command="bash", id="terminal_bash")

    def on_ready(self) -> None:
        terminal_htop: Terminal = self.query_one("#terminal_htop")
        terminal_htop.start()

        terminal_bash: Terminal = self.query_one("#terminal_bash")
        terminal_bash.start()
```

## Installation

```bash
pip install textual-terminal
```

## Features

* Colored output
* Automatic resize to widget dimensions
* Simple key handling (navigation, function keys)
* Simple mouse tracking (click, scroll)

## References

This library is based on the
[Textual pyte example](https://github.com/selectel/pyte/blob/master/examples/terminal_emulator.py)
by [David Brochart](https://github.com/davidbrochart).
