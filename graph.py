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
        if neighbor not in self.adjacent.keys():
            return None
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
        # self.node_dict[to].add_neighbor(self.node_dict[frm], cost)

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
    
def print_graph(g: Graph):
    for node in g.get_nodes():
        n = g.get_node(node)
        print(n)
        for conn in n.get_connections():
            print(f'\t{n.get_weight(conn)} => {conn}')

def complemento(g1: Graph):
    result = Graph()

    for node in g1.get_nodes():
        n = g1.get_node(node)
        result.add_node(n.id, not n.is_initial, not n.is_acceptable)

    for node in g1.get_nodes():
        n = g1.get_node(node)
        for conn in n.get_connections():
            result.add_edge(n.id, conn.id, n.get_weight(conn))

    return result


def union(g1: Graph, g2: Graph):
    g1_nodes = g1.get_nodes()
    g2_nodes = g2.get_nodes()

    result = Graph()

    # Generate nodes
    for g1_node in g1_nodes:
        n1 = g1.get_node(g1_node)

        for g2_node in g2_nodes:
            n2 = g2.get_node(g2_node)
            is_initial = False
            is_acceptable = False

            if n1.is_initial and n2.is_initial:
                is_initial = True

            if n1.is_acceptable or n2.is_acceptable:
                is_acceptable = True
            
            key = f'{g1_node}:{g2_node}'
            result.add_node(key, is_initial, is_acceptable)

    # Generate edges
    ready = []
    for node in result.get_nodes():
        ready.append(node)
        [n1, n2] = node.split(':')
        node_1 = g1.get_node(n1)
        node_2 = g2.get_node(n2)

        # revisamos las conexiones del nodo_1
        for conn in node_1.get_connections():
            # si la conexion es hacia ella misma
            if node_1.id == conn.id:
                # buscamos otro nodo que contenga a node_1
                different_nodes = find_different_nodes(result, node_1.id, node)
                # si la encuentra
                for different_node in different_nodes:
                    if different_node is not None and different_node not in ready:
                        # obtenemos los nodos de r
                        [p1, p2] = different_node.split(':')
                        node_p1 = g1.get_node(p1)
                        node_p2 = g2.get_node(p2)

                        # si node_2 se connecta al node_p2
                        way1 = node_1.get_weight(node_p1)
                        way2 = node_2.get_weight(node_p2)
                        if way1 is not None and way2 is not None:
                            if way2 == way1:
                                result.add_edge(node, different_node, way2)
                            else:
                                done_conn = []
                                if way2 in way1:
                                    result.add_edge(node, different_node, way2)
                                    done_conn.append(way2)
                                if way1 in way2:
                                    result.add_edge(node, different_node, way1)
                                    done_conn.append(way1)

                                longest = longest_word(way1, way2)
                                for way in longest.split(':'):
                                    if way not in done_conn:
                                        result.add_edge(node, node, way)
                        
                    else:
                        result.add_edge(node, node, node_1.get_weight(conn))

            # si la conexion es hacia otro nodo
            else:
                # buscamos otro nodo que contega el nodo al que se conecta
                different_nodes = find_different_nodes(result, conn.id, node)
                # si encuentra otro nodo
                for different_node in different_nodes:
                    if different_node is not None:
                        [p1, p2] = different_node.split(':')
                        node_p1 = g1.get_node(p1)
                        node_p2 = g2.get_node(p2)

                        # si existe conexion entre el node_1 y node_p1
                        way1 = node_1.get_weight(node_p1)
                        way2 = node_2.get_weight(node_p2)
                        if way1 is not None and way2 is not None and way1 in way2:
                            result.add_edge(node, different_node, node_1.get_weight(node_p1))

    return result

def longest_word(w1: str, w2: str):
    if len(w1) > len(w2):
        return w1
    return w2

def find_different_nodes(g: Graph, key: str, current_node: str):
    results = []
    for node in g.get_nodes():
        if key in node and current_node != node:
            results.append(node)
        
    return results
    

if __name__ == '__main__':
    g1 = Graph()
    g1.add_node('a', True, False)
    g1.add_node('b', False, True)

    g1.add_edge('a', 'a', 'Y')
    g1.add_edge('a', 'b', 'X')
    g1.add_edge('b', 'b', 'X:Y')

    print('\n-----AUTOMATA 1-----')
    print_graph(g1)

    g2 = Graph()
    g2.add_node('c', True, False)
    g2.add_node('d', False, True)

    g2.add_edge('c', 'c', 'X')
    g2.add_edge('c', 'd', 'Y')
    g2.add_edge('d', 'd', 'X:Y')

    print('\n-----AUTOMATA 2-----')
    print_graph(g2)

    print("\n----UNION----")
    print_graph(union(g1, g2))

    print("\n----COMPLEMENTO----")
    print_graph(complemento(g1))