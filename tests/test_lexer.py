import unittest
import turboterm

class TestLexer(unittest.TestCase):

    def test_basic_styles(self):
        self.assertEqual(turboterm.apply_styles("[b]Hello[/b]"), "\x1b[1mHello\x1b[0m")
        self.assertEqual(turboterm.apply_styles("[red]World[/red]"), "\x1b[31mWorld\x1b[0m")
        self.assertEqual(turboterm.apply_styles("[u]Test[/u]"), "\x1b[4mTest\x1b[0m")

    def test_nested_styles(self):
        # Expected output for nested styles: bold then underline, then reset underline, then reset bold.
        # The current implementation correctly applies styles and resets them in order.
        self.assertEqual(turboterm.apply_styles("[b]bold [u]underline[/u][/b]"), "\x1b[1mbold \x1b[4munderline\x1b[0m\x1b[1m\x1b[0m")

    def test_mixed_styles(self):
        self.assertEqual(turboterm.apply_styles("[b]Hello [red]colorful[/red] World[/b]"), "\x1b[1mHello \x1b[31mcolorful\x1b[0m\x1b[1m World\x1b[0m")

    def test_unclosed_styles(self):
        self.assertEqual(turboterm.apply_styles("[b]Hello"), "\x1b[1mHello\x1b[0m")
        self.assertEqual(turboterm.apply_styles("Hello [b]World"), "Hello \x1b[1mWorld\x1b[0m")

    def test_plain_text(self):
        self.assertEqual(turboterm.apply_styles("Just plain text"), "Just plain text")

    def test_empty_string(self):
        self.assertEqual(turboterm.apply_styles(""), "")

    def test_unrecognized_tag(self):
        self.assertEqual(turboterm.apply_styles("[xyz]Unknown[/xyz]"), "[xyz]Unknown[/xyz]")
        self.assertEqual(turboterm.apply_styles("Hello [xyz]World[/xyz]"), "Hello [xyz]World[/xyz]")

    def test_tag_like_text(self):
        self.assertEqual(turboterm.apply_styles("This is [not] a tag."), "This is [not] a tag.")
        self.assertEqual(turboterm.apply_styles("An [b]example[/b] with [brackets]."), "An \x1b[1mexample\x1b[0m with [brackets].")

if __name__ == '__main__':
    unittest.main()
