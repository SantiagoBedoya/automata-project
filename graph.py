class Node:
    def __init__(self, node: str, is_initial: bool, is_acceptable: bool):
        self.id: str = node
        self.is_initial: bool = is_initial
        self.is_acceptable: bool = is_acceptable
        self.adjacent: dict[Node, str] = {}

    def __str__(self):
        return f'[{self.id}] = [is_initial: {self.is_initial}, is_acceptable: {self.is_acceptable}]'

    def add_neighbor(self, neighbor, weight: str):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()
    
    def get_weights(self):
        return self.adjacent.values()
    
    def is_connected_with_himself(self):
        for conn in self.adjacent.items():
            node = conn[0]
            weight = conn[1]
            if self.id == node.id:
                return (True, weight)
        return (False, '')

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

class Graph:
    def __init__(self):
        self.node_dict: dict[str, Node] = {}
        self.num_nodes = 0

    def __iter__(self):
        return iter(self.node_dict.values())

    def add_node(self, node: str, is_initial: bool, is_acceptable: bool):
        self.num_nodes = self.num_nodes + 1
        new_node = Node(node, is_initial, is_acceptable)
        self.node_dict[node] = new_node
        return new_node

    def get_node(self, n):
        if n in self.node_dict:
            return self.node_dict[n]
        else:
            return None

    def add_edge(self, frm: str, to: str, cost: str):
        if frm not in self.node_dict:
            self.add_node(frm)
        if to not in self.node_dict:
            self.add_node(to)

        self.node_dict[frm].add_neighbor(self.node_dict[to], cost)
        self.node_dict[to].add_neighbor(self.node_dict[frm], cost)

    def get_nodes(self):
        return self.node_dict.keys()
    
    def union(self, graph: 'Graph'):
        result = Graph()

        # Generate nodes
        for g1_node in self.get_nodes:
            n1 = self.get_node(g1_node)

            for g2_node in graph:
                n2 = graph.get_node(g2_node)
                is_initial = False
                is_acceptable = False

                if n1.is_initial and n2.is_initial:
                    is_initial = True

                if n1.is_acceptable or n2.is_acceptable:
                    is_acceptable = True
                
                key = f'{g1_node}:{g2_node}'
                result.add_node(key, is_initial, is_acceptable)

        return result