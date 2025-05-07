import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq_different_type(self):
        node = TextNode("This is a different text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_link(self):    
        node = TextNode("This is a link node", TextType.LINK, "www.zelda.com")
        node2 = TextNode("This is a link node", TextType.LINK, "www.zelda.com")
        self.assertEqual(node, node2)

    def test_none_link(self):
        node = TextNode("This is a link node", TextType.LINK, "www.abc.def")
        node2 = TextNode("This is a link node", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_text_to_html(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_invalid_type(self):
        node = TextNode("asdf", None)      
        with self.assertRaises(Exception):
            html_node = text_node_to_html_node(node)

    def test_text_to_html_link(self):
        node = TextNode("This is a text node", TextType.LINK, "foo.bar")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.to_html(), '<a href="foo.bar">This is a text node</a>')

if __name__ == "__main__":
    unittest.main()