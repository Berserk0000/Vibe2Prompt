from typing import Optional

GLYPHS = {
    "v": ["#   #", "#   #", "#   #", " # # ", "  #  "],
    "i": ["  #  ", "  #  ", "  #  ", "  #  ", "  #  "],
    "b": ["#    ", "#    ", "#### ", "#   #", "#### "],
    "e": [" ### ", "#   #", "#####", "#    ", " ### "],
    "2": [" ### ", "#   #", "   # ", "  #  ", "#####"],
    "p": ["#### ", "#   #", "#### ", "#    ", "#    "],
    "r": ["#    ", "# ## ", "##   ", "#    ", "#    "],
    "o": [" ### ", "#   #", "#   #", "#   #", " ### "],
    "m": ["#   #", "## ##", "#   #", "#   #", "#   #"],
    "t": ["  #  ", "#####", "  #  ", "  #  ", "  #  "],
    " ": ["     ", "     ", "     ", "     ", "     "],
}

GRADIENT = [
    "#89B4FA",
    "#74C7EC",
    "#89DCEB",
    "#94E2D5",
    "#A6E3A1",
]

ROWS = 5
CELL = "█"


def render_banner(name: str, available_width: Optional[int] = None) -> str:
    name = name.lower()
    glyphs = [GLYPHS.get(ch, GLYPHS[" "]) for ch in name]
    needed = len(name) * (ROWS + 1) - 1
    if available_width is not None and available_width < needed:
        return f"[bold #89B4FA]⚡ {name}[/]"

    lines = [""] * ROWS
    for index, glyph in enumerate(glyphs):
        color = GRADIENT[index % len(GRADIENT)]
        for row in range(ROWS):
            cells = glyph[row].replace("#", CELL)
            lines[row] += f"[{color}]{cells}[/] "
    return "\n".join(lines).rstrip()
