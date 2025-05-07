import unittest

from htmlnode import ParentNode, LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_no_child(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_to_html_missing_tag(self):
        parent_node = ParentNode(None, [])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_missing_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()
    
    def test_to_html_multiple_children(self):
        child1 = LeafNode("p", "text 1 is a paragraph")
        child2 = LeafNode("a", "text 2 is a link", {"href": "some.where"})
        parent = ParentNode("div", [child1, child2], {"prop1": "value1"})
        self.assertEqual(parent.to_html(), '<div prop1="value1"><p>text 1 is a paragraph</p><a href="some.where">text 2 is a link</a></div>')

    def test_to_html_more_layers(self):
        node0 = LeafNode("b", "boldleaf")
        node1 = LeafNode("i", "italicleaf")
        node2 = ParentNode("span", [node0, node1])
        node3 = ParentNode("div", [node2])
        node4 = ParentNode("div", [node3])
        self.assertEqual(node4.to_html(), "<div><div><span><b>boldleaf</b><i>italicleaf</i></span></div></div>")

    def test_to_html_more_layers_2(self):
        node0 = LeafNode("b", "boldleaf")
        node1 = LeafNode("i", "italicleaf")
        node2 = LeafNode("p", "paragraph")
        node3 = ParentNode("span", [node0, node1])
        node4 = ParentNode("div", [node2])
        node5 = ParentNode("div", [node3, node4])
        self.assertEqual(node5.to_html(), "<div><span><b>boldleaf</b><i>italicleaf</i></span><div><p>paragraph</p></div></div>")

if __name__ == "__main__":
    unittest.main()