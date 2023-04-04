import ujson

from pyquest.config import config


def load_json():
    root = {}
    with open(config.json_path, 'r') as fp:
        root = ujson.load(fp)
    return root

def dump_json(root):
    with open(config.json_path, 'w') as fp:
        json.dump(root, fp)

def find_node(node_path=None):
    root = load_json() 
    node_path_list = [] if not node_path else node_path.split('#')
    node = root

    for node_order in node_path_list:
        kids = node['kids']
        search = [kid for kid in kids if kid['order'] == int(node_order)]
        if not search:
            raise ValueError(f'Node doesn\'t exist: {node_path}')
        node = search[0]
    return node

def cat_node(node_path):
    node = find_node(node_path)
    return f"*{node['title']}*\n{node['text']}"

def toggle_node(node_path, with_kids=True):
    node = find_node(node_path)
    new_state = not node['done']
    if with_kids:
        for kid in node['kids']:
            kid['done'] = new_state
    node['done'] = new_state
    dump_json(root)
