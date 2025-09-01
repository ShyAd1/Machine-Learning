# Script para convertir el árbol 20Q en JSON a formato DOT para Graphviz
# Uso: python jsonToPNGTree.py > arbol.dot && dot -Tpng arbol.dot -o arbol.png

import json

# Cargar el árbol desde el archivo JSON
with open("arbol_20q.json", "r", encoding="utf-8") as f:
    data = json.load(f)

edges = []
node_id = 0


def get_edges(nodo, parent_id=None):
    global node_id
    my_id = node_id
    node_id += 1
    label = nodo["q"].replace('"', '"')
    this_node = f"node{my_id}"
    nodes[this_node] = label
    if parent_id is not None:
        edges.append((f"node{parent_id}", this_node))
    # Recorrer ramas "si" y "no" si existen
    for branch in ["si", "no"]:
        if branch in nodo:
            get_edges(nodo[branch], my_id)


# Diccionario para guardar los labels de los nodos
nodes = {}
get_edges(data)

# Imprimir en formato DOT
print("digraph tree {")
for node, label in nodes.items():
    print(f'    {node} [label="{label}"]')
for src, dst in edges:
    print(f"    {src} -> {dst};")
print("}")
