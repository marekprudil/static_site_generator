import unittest

from htmlnode import HTMLNode


class TestHtmlNode(unittest.TestCase):
    def test_eq_html(self):
        node = HTMLNode("p", "some text")
        node2 = HTMLNode("p", "some text")

        self.assertEqual(node, node2)

    def test_eq_html_2(self):
        node = HTMLNode("p", "child1")
        node2 = HTMLNode("p", "child2")
        node3 = HTMLNode("p", "parentnode", [node, node2], {"prop1": "val1"})
        node4 = HTMLNode("p", "parentnode", [node, node2], {"prop1": "val1"})

        self.assertEqual(node3, node4)

    def test_eq_html_2_false(self):
        node = HTMLNode("p", "child1")
        node2 = HTMLNode("p", "child2")
        node3 = HTMLNode("p", "parentnode", [node, node2], {"prop1": "val1"})
        node4 = HTMLNode("p", "parentnode", [node, node2], {"prop1": "val4"})

        self.assertNotEqual(node3, node4)

    def test_repr_1(self):
        node = HTMLNode("tag", "value", "children", "props")
        repr_string = "HTMLNode(Tag=tag, Value=value, Children=children, Props=props)"
        self.assertEqual(repr(node), repr_string)

    def test_repr_2(self):
        node = HTMLNode("tag", "value", [], {"href": "boot.dev"})
        repr_string = "HTMLNode(Tag=tag, Value=value, Children=[], Props={'href': 'boot.dev'})"
        self.assertEqual(repr(node), repr_string)

    def test_props_to_html(self):
        node = HTMLNode("tag", "value", "children", {"prop1": "val1", "prop2": "val2"})
        html_string = 'prop1="val1", prop2="val2"'
        self.assertEqual(node.props_to_html(), html_string)

    def test_to_html_raises_error(self):
        node = HTMLNode("p", "Hello, world!")
        with self.assertRaises(NotImplementedError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()