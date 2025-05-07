import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "bnfgh")
        self.assertEqual(node.to_html(), "<b>bnfgh</b>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "anchor_text", {"href": "boot.dev"})
        self.assertEqual(node.to_html(), '<a href="boot.dev">anchor_text</a>')

    def test_leaf_to_html_moreprops(self):
        node = LeafNode("tag", "sometext", {"a": "b", "c": "d", "e": "f"})
        self.assertEqual(node.to_html(), '<tag a="b" c="d" e="f">sometext</tag>')

    def test_leaf_to_html_novalue(self):
        node = LeafNode("tag", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_plain(self):
        node = LeafNode(None, "oh yeah")
        self.assertEqual(node.to_html(), "oh yeah")

if __name__ == "__main__":
    unittest.main()