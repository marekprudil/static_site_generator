import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
        new_nodes = []
        for old_node in old_nodes:
            if old_node.text_type != TextType.TEXT:
                new_nodes.append(old_node)
                continue
            
            split_nodes = []
            split_text = old_node.text.split(delimiter)
            if len(split_text) % 2 == 0:
                raise ValueError("markdown section not closed")
            
            for i, section in enumerate(split_text):
                if section == "":
                    continue
                if i % 2 == 0:
                    split_nodes.append(TextNode(section, TextType.TEXT))
                else:
                    split_nodes.append(TextNode(section, text_type))
            new_nodes.extend(split_nodes)
        return new_nodes
        
def extract_markdown_images(text):
     matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
     return list(matches)

def extract_markdown_links(text):
     matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
     return list(matches)

def split_nodes_image(old_nodes):
        new_nodes = []
        for old_node in old_nodes:
            if old_node.text_type != TextType.TEXT:
                new_nodes.append(old_node)
                continue
            
            split_nodes = []
            remaining_text = old_node.text
            images = extract_markdown_images(old_node.text)
            
            if images == []:
                 new_nodes.append(old_node)
                 continue

            for img_tuple in images:
                img_alt = img_tuple[0]
                img_link = img_tuple[1]

                sections = remaining_text.split(f"![{img_alt}]({img_link})", 1)
                
                if sections[0] != "":                 
                    split_nodes.append(TextNode(sections[0], TextType.TEXT))
                
                split_nodes.append(TextNode(img_alt, TextType.IMAGE, img_link))

                remaining_text = sections[1]
            
            if remaining_text != "":
                split_nodes.append(TextNode(remaining_text, TextType.TEXT))
            new_nodes.extend(split_nodes)

        return new_nodes
                     
                

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        split_nodes = []
        remaining_text = old_node.text
        links = extract_markdown_links(old_node.text)
        
        if links == []:
                new_nodes.append(old_node)
                continue

        for link_tuple in links:
            link_alt = link_tuple[0]
            link_url = link_tuple[1]

            sections = remaining_text.split(f"[{link_alt}]({link_url})", 1)
            
            if sections[0] != "":                 
                split_nodes.append(TextNode(sections[0], TextType.TEXT))
            
            split_nodes.append(TextNode(link_alt, TextType.LINK, link_url))

            remaining_text = sections[1]
        
        if remaining_text != "":
            split_nodes.append(TextNode(remaining_text, TextType.TEXT))
        new_nodes.extend(split_nodes)

    return new_nodes

def text_to_textnodes(text):
    text_node = TextNode(text, TextType.TEXT)
    img_split = split_nodes_image([text_node])
    link_split = split_nodes_link(img_split)
    bold_split = split_nodes_delimiter(link_split,"**", TextType.BOLD)
    italic_split = split_nodes_delimiter(bold_split, "_", TextType.ITALIC)
    return split_nodes_delimiter(italic_split, "`", TextType.CODE)


