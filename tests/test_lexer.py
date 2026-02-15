import unittest

import turboterm


class TestLexer(unittest.TestCase):
    def test_basic_styles(self):
        self.assertEqual(turboterm.apply_styles("[b]Hello[/b]"), "\x1b[1mHello\x1b[0m")
        self.assertEqual(
            turboterm.apply_styles("[red]World[/red]"), "\x1b[31mWorld\x1b[0m"
        )
        self.assertEqual(turboterm.apply_styles("[u]Test[/u]"), "\x1b[4mTest\x1b[0m")

    def test_nested_styles(self):
        self.assertEqual(
            turboterm.apply_styles("[b]bold [u]underline[/u][/b]"),
            "\x1b[1mbold \x1b[4munderline\x1b[0m\x1b[1m\x1b[0m",
        )

    def test_mixed_styles(self):
        self.assertEqual(
            turboterm.apply_styles("[b]Hello [red]colorful[/red] World[/b]"),
            "\x1b[1mHello \x1b[31mcolorful\x1b[0m\x1b[1m World\x1b[0m",
        )

    def test_unclosed_styles(self):
        self.assertEqual(turboterm.apply_styles("[b]Hello"), "\x1b[1mHello\x1b[0m")
        self.assertEqual(
            turboterm.apply_styles("Hello [b]World"), "Hello \x1b[1mWorld\x1b[0m"
        )

    def test_plain_text(self):
        self.assertEqual(turboterm.apply_styles("Just plain text"), "Just plain text")

    def test_empty_string(self):
        self.assertEqual(turboterm.apply_styles(""), "")

    def test_unrecognized_tag(self):
        self.assertEqual(
            turboterm.apply_styles("[xyz]Unknown[/xyz]"), "[xyz]Unknown[/xyz]"
        )
        self.assertEqual(
            turboterm.apply_styles("Hello [xyz]World[/xyz]"), "Hello [xyz]World[/xyz]"
        )

    def test_tag_like_text(self):
        self.assertEqual(
            turboterm.apply_styles("This is [not] a tag."), "This is [not] a tag."
        )
        self.assertEqual(
            turboterm.apply_styles("An [b]example[/b] with [brackets]."),
            "An \x1b[1mexample\x1b[0m with [brackets].",
        )

    # --- Text attributes ---

    def test_bold_aliases(self):
        self.assertEqual(
            turboterm.apply_styles("[bold]text[/bold]"), "\x1b[1mtext\x1b[0m"
        )
        self.assertEqual(turboterm.apply_styles("[b]text[/b]"), "\x1b[1mtext\x1b[0m")

    def test_dim(self):
        self.assertEqual(
            turboterm.apply_styles("[dim]text[/dim]"), "\x1b[2mtext\x1b[0m"
        )

    def test_italic_aliases(self):
        self.assertEqual(
            turboterm.apply_styles("[italic]text[/italic]"), "\x1b[3mtext\x1b[0m"
        )
        self.assertEqual(turboterm.apply_styles("[i]text[/i]"), "\x1b[3mtext\x1b[0m")

    def test_underline_aliases(self):
        self.assertEqual(
            turboterm.apply_styles("[underline]text[/underline]"), "\x1b[4mtext\x1b[0m"
        )
        self.assertEqual(turboterm.apply_styles("[u]text[/u]"), "\x1b[4mtext\x1b[0m")

    def test_blink(self):
        self.assertEqual(
            turboterm.apply_styles("[blink]text[/blink]"), "\x1b[5mtext\x1b[0m"
        )

    def test_inverse_aliases(self):
        self.assertEqual(
            turboterm.apply_styles("[inverse]text[/inverse]"), "\x1b[7mtext\x1b[0m"
        )
        self.assertEqual(
            turboterm.apply_styles("[reverse]text[/reverse]"), "\x1b[7mtext\x1b[0m"
        )

    def test_hidden(self):
        self.assertEqual(
            turboterm.apply_styles("[hidden]text[/hidden]"), "\x1b[8mtext\x1b[0m"
        )

    def test_strike_aliases(self):
        self.assertEqual(turboterm.apply_styles("[s]text[/s]"), "\x1b[9mtext\x1b[0m")
        self.assertEqual(
            turboterm.apply_styles("[strike]text[/strike]"), "\x1b[9mtext\x1b[0m"
        )
        self.assertEqual(
            turboterm.apply_styles("[strikethrough]text[/strikethrough]"),
            "\x1b[9mtext\x1b[0m",
        )

    def test_overline(self):
        self.assertEqual(
            turboterm.apply_styles("[overline]text[/overline]"), "\x1b[53mtext\x1b[0m"
        )

    # --- Standard foreground colors ---

    def test_foreground_colors(self):
        colors = {
            "black": 30,
            "red": 31,
            "green": 32,
            "yellow": 33,
            "blue": 34,
            "magenta": 35,
            "cyan": 36,
            "white": 37,
        }
        for name, code in colors.items():
            self.assertEqual(
                turboterm.apply_styles(f"[{name}]x[/{name}]"),
                f"\x1b[{code}mx\x1b[0m",
                f"Failed for foreground color: {name}",
            )

    # --- Bright foreground colors ---

    def test_bright_foreground_colors(self):
        colors = {
            "bright_black": 90,
            "bright_red": 91,
            "bright_green": 92,
            "bright_yellow": 93,
            "bright_blue": 94,
            "bright_magenta": 95,
            "bright_cyan": 96,
            "bright_white": 97,
        }
        for name, code in colors.items():
            self.assertEqual(
                turboterm.apply_styles(f"[{name}]x[/{name}]"),
                f"\x1b[{code}mx\x1b[0m",
                f"Failed for bright fg color: {name}",
            )

    def test_grey_gray_aliases(self):
        expected = "\x1b[90mx\x1b[0m"
        self.assertEqual(turboterm.apply_styles("[grey]x[/grey]"), expected)
        self.assertEqual(turboterm.apply_styles("[gray]x[/gray]"), expected)
        self.assertEqual(
            turboterm.apply_styles("[bright_black]x[/bright_black]"), expected
        )

    # --- Standard background colors ---

    def test_background_colors(self):
        colors = {
            "on_black": 40,
            "on_red": 41,
            "on_green": 42,
            "on_yellow": 43,
            "on_blue": 44,
            "on_magenta": 45,
            "on_cyan": 46,
            "on_white": 47,
        }
        for name, code in colors.items():
            self.assertEqual(
                turboterm.apply_styles(f"[{name}]x[/{name}]"),
                f"\x1b[{code}mx\x1b[0m",
                f"Failed for background color: {name}",
            )

    # --- Bright background colors ---

    def test_bright_background_colors(self):
        colors = {
            "on_bright_black": 100,
            "on_bright_red": 101,
            "on_bright_green": 102,
            "on_bright_yellow": 103,
            "on_bright_blue": 104,
            "on_bright_magenta": 105,
            "on_bright_cyan": 106,
            "on_bright_white": 107,
        }
        for name, code in colors.items():
            self.assertEqual(
                turboterm.apply_styles(f"[{name}]x[/{name}]"),
                f"\x1b[{code}mx\x1b[0m",
                f"Failed for bright bg color: {name}",
            )

    def test_on_grey_on_gray_aliases(self):
        expected = "\x1b[100mx\x1b[0m"
        self.assertEqual(turboterm.apply_styles("[on_grey]x[/on_grey]"), expected)
        self.assertEqual(turboterm.apply_styles("[on_gray]x[/on_gray]"), expected)

    # --- Compound tags ---

    def test_compound_two_tokens(self):
        result = turboterm.apply_styles("[bold red]text[/bold red]")
        self.assertEqual(result, "\x1b[1m\x1b[31mtext\x1b[0m")

    def test_compound_three_tokens(self):
        result = turboterm.apply_styles("[italic red on_blue]text[/italic red on_blue]")
        self.assertEqual(result, "\x1b[3m\x1b[31m\x1b[44mtext\x1b[0m")

    def test_compound_with_aliases(self):
        result = turboterm.apply_styles("[b u]text[/b u]")
        self.assertEqual(result, "\x1b[1m\x1b[4mtext\x1b[0m")

    def test_compound_nested_under_simple(self):
        result = turboterm.apply_styles(
            "[b]hello [red on_white]world[/red on_white][/b]"
        )
        self.assertEqual(
            result, "\x1b[1mhello \x1b[31m\x1b[47mworld\x1b[0m\x1b[1m\x1b[0m"
        )

    def test_compound_invalid_token_literal(self):
        # If any token in a compound tag is unrecognized, treat whole tag as literal
        result = turboterm.apply_styles("[bold xyz]text[/bold xyz]")
        self.assertEqual(result, "[bold xyz]text[/bold xyz]")

    # --- 256-color ---

    def test_color_256_foreground(self):
        result = turboterm.apply_styles("[color(208)]text[/color(208)]")
        self.assertEqual(result, "\x1b[38;5;208mtext\x1b[0m")

    def test_color_256_background(self):
        result = turboterm.apply_styles("[on_color(52)]text[/on_color(52)]")
        self.assertEqual(result, "\x1b[48;5;52mtext\x1b[0m")

    def test_color_256_boundary_values(self):
        self.assertEqual(
            turboterm.apply_styles("[color(0)]x[/color(0)]"), "\x1b[38;5;0mx\x1b[0m"
        )
        self.assertEqual(
            turboterm.apply_styles("[color(255)]x[/color(255)]"),
            "\x1b[38;5;255mx\x1b[0m",
        )

    # --- Truecolor rgb() ---

    def test_rgb_foreground(self):
        result = turboterm.apply_styles("[rgb(255,128,0)]text[/rgb(255,128,0)]")
        self.assertEqual(result, "\x1b[38;2;255;128;0mtext\x1b[0m")

    def test_rgb_background(self):
        result = turboterm.apply_styles("[on_rgb(0,0,64)]text[/on_rgb(0,0,64)]")
        self.assertEqual(result, "\x1b[48;2;0;0;64mtext\x1b[0m")

    # --- Hex colors ---

    def test_hex_foreground(self):
        result = turboterm.apply_styles("[#ff8000]text[/#ff8000]")
        self.assertEqual(result, "\x1b[38;2;255;128;0mtext\x1b[0m")

    def test_hex_background(self):
        result = turboterm.apply_styles("[on_#000040]text[/on_#000040]")
        self.assertEqual(result, "\x1b[48;2;0;0;64mtext\x1b[0m")

    def test_hex_uppercase(self):
        result = turboterm.apply_styles("[#FF8000]text[/#FF8000]")
        self.assertEqual(result, "\x1b[38;2;255;128;0mtext\x1b[0m")

    # --- Compound with dynamic tokens ---

    def test_compound_with_hex(self):
        result = turboterm.apply_styles("[bold #ff0000]text[/bold #ff0000]")
        self.assertEqual(result, "\x1b[1m\x1b[38;2;255;0;0mtext\x1b[0m")

    def test_compound_with_rgb(self):
        result = turboterm.apply_styles(
            "[italic rgb(100,200,50)]text[/italic rgb(100,200,50)]"
        )
        self.assertEqual(result, "\x1b[3m\x1b[38;2;100;200;50mtext\x1b[0m")

    def test_compound_with_256_color(self):
        result = turboterm.apply_styles("[bold color(196)]text[/bold color(196)]")
        self.assertEqual(result, "\x1b[1m\x1b[38;5;196mtext\x1b[0m")


if __name__ == "__main__":
    unittest.main()
