import unittest

from textnode import TextNode, TextType


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






if __name__ == "__main__":
    unittest.main()