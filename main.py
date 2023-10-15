import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
from graph import Graph, union, interseccion, complemento, reverso


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Graph")
        self.geometry("800x600")
        self.create_widgets()
        self.graph = nx.DiGraph()
        self.g1 = Graph()
        self.g2 = Graph()

    def show_automatas(self):
        self.graph.clear()
        # automata 1
        self.g1.add_node('A', True, False)
        self.g1.add_node('B', False, True)

        self.g1.add_edge('A', 'A', 'Y')
        self.g1.add_edge('A', 'B', 'X')
        self.g1.add_edge('B', 'B', 'X:Y')
        nc1 = self.g1.to_networkx(self.graph)

        # automata 2
        self.g2.add_node('C', True, False)
        self.g2.add_node('D', False, True)

        self.g2.add_edge('C', 'C', 'X')
        self.g2.add_edge('C', 'D', 'Y')
        self.g2.add_edge('D', 'D', 'X:Y')
        nc2 = self.g2.to_networkx(self.graph)

        nc1.update(nc2)

        self.draw_graph(nc1)
        pass

    def show_union(self):
        self.graph.clear()
        union_graph = union(self.g1, self.g2)
        nc = union_graph.to_networkx(self.graph)
        self.draw_graph(nc)

    def show_interseccion(self):
        self.graph.clear()
        interseccion_graph = interseccion(self.g1, self.g2)
        nc = interseccion_graph.to_networkx(self.graph)
        self.draw_graph(nc)

    def show_complemento(self):
        self.graph.clear()
        complemento_graph = complemento(self.g1)
        nc = complemento_graph.to_networkx(self.graph)
        self.draw_graph(nc)

    def show_reverso(self):
        self.graph.clear()
        inverso_graph = reverso(self.g1)
        nc = inverso_graph.to_networkx(self.graph)
        self.draw_graph(nc)

    def create_widgets(self):
        self.frame1 = tk.Frame(self)
        self.frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.frame2 = tk.Frame(self)
        self.frame2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.button1 = tk.Button(
            self.frame1, text="Mostrar automatas", command=self.show_automatas
        )
        self.button1.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.button2 = tk.Button(self.frame1, text="Union", command=self.show_union)
        self.button2.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.button3 = tk.Button(
            self.frame1, text="Interseccion", command=self.show_interseccion
        )
        self.button3.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.button4 = tk.Button(
            self.frame1, text="Complemento", command=self.show_complemento
        )
        self.button4.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.button5 = tk.Button(self.frame1, text="Reverso", command=self.show_reverso)
        self.button5.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.graph = nx.Graph()

        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.frame2)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.draw_graph({})

    def draw_graph(self, node_colors):
        self.ax.clear()

        # Define the positions of the nodes
        pos = nx.get_node_attributes(self.graph, 'pos')
        # pos = {"A": (0, 0), "B": (1, 0), "C": (0, 1), "D": (1, 1), "A:C": (2, 0)}

        # Draw the graph with the defined positions
        nx.draw_networkx(self.graph, pos=pos, with_labels=True, ax=self.ax, node_color=[node_colors[n] for n in self.graph.nodes])

        # Add edge labels
        edge_labels = nx.get_edge_attributes(self.graph, "label")
        for edge in self.graph.edges():
            if edge[0] == edge[1]:
                edge_labels[edge] = self.graph.edges[edge]["label"]
        label_pos = {
            k: (v[0], v[1] + 0.5) for k, v in pos.items()
        }  # move labels up by 0.1
        nx.draw_networkx_edge_labels(
            self.graph,
            label_pos,
            edge_labels=edge_labels,
            ax=self.ax,
        )

        self.canvas.draw()


app = App()
app.mainloop()