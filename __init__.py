import os
import importlib


NODE_CLASS_MAPPINGS = {}

 print("\033[38;5;229m Fictiverse nodes \033[0m")   
for node in os.listdir(os.path.dirname(__file__) + os.sep + 'nodes'):
    if node.startswith('FV_'):
        node = node.split('.')[0]
        node_import = importlib.import_module('custom_nodes.ComfyUI_Fictiverse.nodes.' + node)
        print("Imported : " + "\033[38;5;229m" + node + + "\033[0m")
        NODE_CLASS_MAPPINGS.update(node_import.NODE_CLASS_MAPPINGS)

#WEB_DIRECTORY = "./web"
