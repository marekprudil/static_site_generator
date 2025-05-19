import unittest

from textnode import TextNode, TextType
from inline import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

class TestInline(unittest.TestCase):
    def test_codeblock(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
                                        TextNode("This is text with a ", TextType.TEXT),
                                        TextNode("code block", TextType.CODE),
                                        TextNode(" word", TextType.TEXT),
                                    ])
    
    def test_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
                                        TextNode("This is text with a ", TextType.TEXT),
                                        TextNode("bold", TextType.BOLD),
                                        TextNode(" word", TextType.TEXT),
                                    ])
        
    def test_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
                                        TextNode("This is text with an ", TextType.TEXT),
                                        TextNode("italic", TextType.ITALIC),
                                        TextNode(" word", TextType.TEXT),
                                    ])

    def test_multiple_nodes(self):
        node_1 = TextNode("This is text with a **bold** word", TextType.TEXT)
        node_2 = TextNode("This is text with another **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node_1, node_2], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
                                        TextNode("This is text with a ", TextType.TEXT),
                                        TextNode("bold", TextType.BOLD),
                                        TextNode(" word", TextType.TEXT),
                                        TextNode("This is text with another ", TextType.TEXT),
                                        TextNode("bold", TextType.BOLD),
                                        TextNode(" word", TextType.TEXT),
                                    ])
        
    def test_nontext_node(self):
        node = TextNode("This is a node that's not a TEXT type", TextType.ITALIC)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual([node], new_nodes)
    
    def test_invalid(self):
        node = TextNode("This is text with a **bold** word and an unclosed **bold section", TextType.TEXT)
        
        with self.assertRaises(ValueError):
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_extract_markdown_images_1(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_images_2(self):
        matches = extract_markdown_images("This is text with a ![picture](link.to.picture1) and ![another one](right@here)")
        self.assertListEqual([("picture", "link.to.picture1"),("another one", "right@here")], matches)
    
    def test_extract_md_img_none(self):
        matches = extract_markdown_images("This is a text without an image")
        self.assertListEqual([],matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_md_link_none(self):
        matches = extract_markdown_links("This is a text without any link")
        self.assertListEqual([],matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and some text at the end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" and some text at the end", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_no_image(self):
        node = TextNode(
            "This is text without an image",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [node],
            new_nodes,
        )

    def test_split_ends_with_image(self):
        node = TextNode(
            "This is text that ends with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text that ends with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes,
        )

    def test_split_starts_with_image(self):
        node = TextNode(
            "![This](https://i.imgur.com/zjjcJKZ.png) is text that starts with an image",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" is text that starts with an image", TextType.TEXT)
            ],
            new_nodes,
        )
    
    def test_split_images_next(self):
        node = TextNode(
            "This test has ![two](https://i.imgur.com/zjjcJKZ.png)![images](https://i.imgur.com/3elNhQu.png) right next to each other",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This test has ", TextType.TEXT),
                TextNode("two", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("images", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" right next to each other", TextType.TEXT)
            ],
            new_nodes,
        )
        
    def test_split_images_multiple_nodes(self):
        node1 = TextNode(
            "This is text that ends with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This is text without an image",
            TextType.TEXT,
        )
        node3 = TextNode(
            "This test has ![two](https://i.imgur.com/zjjcJKZ.png)![images](https://i.imgur.com/3elNhQu.png) right next to each other",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node1, node2, node3])
        self.assertListEqual(
            [
                TextNode("This is text that ends with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("This is text without an image", TextType.TEXT),
                TextNode("This test has ", TextType.TEXT),
                TextNode("two", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("images", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" right next to each other", TextType.TEXT)
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.google.com) and another [second link](https://www.boot.dev) and some text at the end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and some text at the end", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_no_link(self):
        node = TextNode(
            "This is text without a link",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [node],
            new_nodes,
        )

    def test_split_ends_with_link(self):
        node = TextNode(
            "This is text that ends with a [link](https://www.google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text that ends with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com")
            ],
            new_nodes,
        )

    def test_split_starts_with_link(self):
        node = TextNode(
            "[This](https://www.google.com) is text that starts with a link",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This", TextType.LINK, "https://www.google.com"),
                TextNode(" is text that starts with a link", TextType.TEXT)
            ],
            new_nodes,
        )
    
    def test_split_links_next(self):
        node = TextNode(
            "This test has [two](https://i.imgur.com/zjjcJKZ.png)[links](https://i.imgur.com/3elNhQu.png) right next to each other",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This test has ", TextType.TEXT),
                TextNode("two", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("links", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" right next to each other", TextType.TEXT)
            ],
            new_nodes,
        )
        
    def test_split_links_multiple_nodes(self):
        node1 = TextNode(
            "This is text that ends with a [link](https://www.google.com)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This is text without a link",
            TextType.TEXT,
        )
        node3 = TextNode(
            "This test has [two](https://i.imgur.com/zjjcJKZ.png)[links](https://i.imgur.com/3elNhQu.png) right next to each other",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node1, node2, node3])
        self.assertListEqual(
            [
                TextNode("This is text that ends with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode("This is text without a link", TextType.TEXT),
                TextNode("This test has ", TextType.TEXT),
                TextNode("two", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("links", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" right next to each other", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_text_to_nodes1(self):
        text =  "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )
    
    def test_text_to_nodes_boldlink(self):  # we don't support nesting yet, so this should just be a link with the bold delimiters shown as text
        text =  "Here is a [**bold link**](https://example.com)"
        new_nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("Here is a ", TextType.TEXT),
                TextNode("**bold link**", TextType.LINK, "https://example.com")
            ],
            new_nodes
        )