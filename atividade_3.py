import random
import matplotlib.pyplot as plt
import networkx as nx

# Classe do Nó da árvore
class Node:
    def __init__(self, valor):
        self.valor = valor
        self.esquerda = None
        self.direita = None

# Classe da Árvore Binária de Busca
class ArvoreBinaria:
    def __init__(self):
        self.raiz = None

    def inserir(self, valor):
        if self.raiz is None:
            self.raiz = Node(valor)
        else:
            self._inserir(self.raiz, valor)

    def _inserir(self, node, valor):
        if valor < node.valor:
            if node.esquerda is None:
                node.esquerda = Node(valor)
            else:
                self._inserir(node.esquerda, valor)
        else:
            if node.direita is None:
                node.direita = Node(valor)
            else:
                self._inserir(node.direita, valor)

    def inorder(self):
        return self._inorder(self.raiz)

    def _inorder(self, node):
        if node is None:
            return []
        return self._inorder(node.esquerda) + [node.valor] + self._inorder(node.direita)

    def preorder(self):
        return self._preorder(self.raiz)

    def _preorder(self, node):
        if node is None:
            return []
        return [node.valor] + self._preorder(node.esquerda) + self._preorder(node.direita)

    def postorder(self):
        return self._postorder(self.raiz)

    def _postorder(self, node):
        if node is None:
            return []
        return self._postorder(node.esquerda) + self._postorder(node.direita) + [node.valor]

    def visualizar(self, titulo="Árvore Binária"):
        G = nx.DiGraph()
        pos = {}

        def add_edges(node, x=0, y=0, dx=1.0):
            if node is None:
                return
            G.add_node(node.valor)
            pos[node.valor] = (x, y)
            if node.esquerda:
                G.add_edge(node.valor, node.esquerda.valor)
                add_edges(node.esquerda, x - dx, y - 1, dx / 2)
            if node.direita:
                G.add_edge(node.valor, node.direita.valor)
                add_edges(node.direita, x + dx, y - 1, dx / 2)

        add_edges(self.raiz)

        plt.figure(figsize=(10, 6))
        nx.draw(G, pos, with_labels=True, arrows=False, node_size=1500, node_color='lightblue', font_size=12)
        plt.title(titulo)
        plt.show()


# ----------------------
# Árvore com valores fixos
# ----------------------

valores_fixos = [55, 30, 80, 20, 45, 70, 90]
arvore_fixa = ArvoreBinaria()
for v in valores_fixos:
    arvore_fixa.inserir(v)

print("=== Árvore com Valores Fixos ===")
print("Valores Inseridos:", valores_fixos)
print("In-Order (Esquerda, Raiz, Direita):", arvore_fixa.inorder())
print("Pre-Order (Raiz, Esquerda, Direita):", arvore_fixa.preorder())
print("Post-Order (Esquerda, Direita, Raiz):", arvore_fixa.postorder())

arvore_fixa.visualizar("Árvore com Valores Fixos")

# ----------------------
# Árvore com valores randômicos
# ----------------------

valores_random = random.sample(range(1, 100), 10)
arvore_random = ArvoreBinaria()
for v in valores_random:
    arvore_random.inserir(v)

print("\n=== Árvore com Valores Randômicos ===")
print("Valores Inseridos:", valores_random)
print("In-Order (Esquerda, Raiz, Direita):", arvore_random.inorder())
print("Pre-Order (Raiz, Esquerda, Direita):", arvore_random.preorder())
print("Post-Order (Esquerda, Direita, Raiz):", arvore_random.postorder())

arvore_random.visualizar("Árvore com Valores Randômicos")