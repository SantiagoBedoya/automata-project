# generate a tkinter interface splited in 2 parts, in the first side put 5 buttons and in the second side put a networkx graph

import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Graph")
        self.geometry("800x600")
        self.create_widgets()
        self.graph = nx.DiGraph()

    def show_automatas(self):
        # automata 1
        self.graph.add_nodes_from(["A", "B"])
        self.graph.add_edges_from(
            [
                ("A", "A", {"label": "X"}),
                ("A", "B", {"label": "Y"}),
                ("B", "B", {"label": "X,Y"}),
            ]
        )

        # automata 2
        self.graph.add_nodes_from(["C", "D"])
        self.graph.add_edges_from(
            [
                ("C", "C", {"label": "Y"}),
                ("C", "D", {"label": "X"}),
                ("D", "D", {"label": "X,Y"}),
            ]
        )
        self.draw_graph()
        pass

    def show_union(self):
        pass

    def show_interseccion(self):
        pass

    def show_complemento(self):
        pass

    def show_inverso(self):
        pass

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

        self.button5 = tk.Button(self.frame1, text="Inverso", command=self.show_inverso)
        self.button5.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.graph = nx.Graph()

        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.frame2)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.draw_graph()

    def draw_graph(self):
        self.ax.clear()

        # Define the positions of the nodes
        pos = {"A": (0, 0), "B": (1, 0), "C": (0, 1), "D": (1, 1)}

        # Draw the graph with the defined positions
        nx.draw_networkx(self.graph, pos=pos, with_labels=True, ax=self.ax)

        # Add edge labels
        edge_labels = nx.get_edge_attributes(self.graph, "label")
        for edge in self.graph.edges():
            if edge[0] == edge[1]:
                edge_labels[edge] = self.graph.edges[edge]["label"]
        label_pos = {
            k: (v[0], v[1] + 0.05) for k, v in pos.items()
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
