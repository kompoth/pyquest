from bigtree import Node, shift_nodes
import requests


def add_node(line, order, prev_node, base_url):
    """Add next header node to Markdown tree."""
    level = 0
    while line[level] == '#':
        level += 1
    title = line[level + 1:]
    
    parent = prev_node
    if parent.level >= level:
        while parent.level != level - 1:
            parent = parent.parent
 
    node = Node.from_dict({
        'name': title,
        'level': level,
        'order': order,
        'url': base_url + '#' + title.replace(' ', '-'),
        'text': None,
        'done': False,
        'parent': parent
    })
    return node


def md_2_tree(raw_url, base_url, ignore=None):
    """Create Markdown tree from a string."""
    resp = requests.get(raw_url)
    md_str = resp.content.decode('utf-8')

    in_code = False
    root = Node.from_dict({
        'name': 'root',
        'level': 0,
        'order': 0,
        'url': base_url,
        'text': None,
        'done': False
    })
    node = root

    header_num = 0
    for line in md_str.split('\n'):
        if line and len(line) >= 3 and line[:3] == '```':
            in_code = not in_code
        elif line and line[0] == '#' and not in_code:
            header_num += 1
            node = add_node(line, header_num, node, base_url)
        elif node.text:
            node.text += '\n' + line
        else:
            node.text = line

    if ignore:
        for path in ignore:
            shift_nodes(root, [f'{path}'], [None], delete_children=True)
    return root            

def node_2_dict(node):
    return {
        'title': node.name,
        'order': node.order,
        'level': node.level,
        'url': node.url,
        'text': node.text,
        'kids': [node_2_dict(kid) for kid in node.children],
        'done': node.done
    }

def md_2_dict(raw_url, base_url, ignore=None):
    """Convert Markdown string to dictionary."""
    root = md_2_tree(raw_url, base_url, ignore=ignore)
    return node_2_dict(root)
