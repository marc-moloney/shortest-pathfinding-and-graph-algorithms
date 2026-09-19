class Vertex:
    """ A Vertex in a graph. """
    
    def __init__(self, element, cost):
        """ Create a vertex, with data element and cost. """
        self._element = element
        self._cost = cost

    def __str__(self):
        """ Return a string representation of the vertex. """
        return str(self._element) + " " + str(self._cost)

    def element(self):
        """ Return the data for the vertex. """
        return self._element
    
    def cost(self):
        """Return the cost for the vertex."""
        return self._cost
    
    def __lt__(self, v):
        """ Return true if this object is less than v.
       
        Args:
            v -- a vertex object
        """
        return self._element < v.element()

class Edge:
    """ An edge in a graph.

    Implemented with an order, so can be used for directed or undirected
    graphs. Methods are provided for both. It is the job of the Graph class
    to handle them as directed or undirected.
    """
    
    def __init__(self, v, w, element):
        """ Create an edge between vertices v and w, with label element.

        Args:
            v -- a Vertex object
            w -- a Vertex object
            element -- the label, can be an arbitrarily complex structure.
        """
        self._vertices = (v,w)
        self._element = element

    def __str__(self):
        """ Return a string representation of this edge. """
        return ('(' + str(self._vertices[0]) + '--'
                   + str(self._vertices[1]) + ' : '
                   + str(self._element) + ')')

    def vertices(self):
        """ Return an ordered pair of the vertices of this edge."""
        return self._vertices

    def opposite(self, v):
        """ Return the opposite vertex to v in this edge, or None if this edge not incident on v.  
        
        Args:
            v - a Vertex object
        """
        if self._vertices[0] == v:
            return self._vertices[1]
        elif self._vertices[1] == v:
            return self._vertices[0]
        else:
            return None

    def element(self):
        """ Return the data element for this edge. """
        return self._element

    def start(self):
        """ Return the first vertex in the ordered pair. """
        return self._vertices[0]

    def end(self):
        """ Return the second vertex in the ordered. pair. """
        return self._vertices[1]


class Graph:
    """ Represent a simple graph.

        This version maintains only undirected graphs, and assumes no
        self edges (i.e. no edge from a vertex v to v).
    """

    #Implement as a Python dictionary
    #  - the keys are the vertices
    #  - the values are the edge sets for that vertex
    #         Each edge set is also maintained as a dictionary,
    #         with opposite vertex as the key and the edge object as the value
    #         Suppose v and w are vertices in the graph, with an edge e between v and w
    #         self._structure[v] is a dictionary of edges
    #         self._structure[v][w] is the edge e
    
    def __init__(self):
        """ Create an initial empty graph. """
        self._structure = dict()

    def __str__(self):
        """ Return a string representation of the graph. """
        hstr = ('|V| = ' + str(self.num_vertices())
                + '; |E| = ' + str(self.num_edges()))
        vstr = '\nVertices: '
        for v in self._structure:
            vstr += str(v) + ' '
        edges = self.edges()
        estr = '\nEdges: '
        for e in edges:
            estr += str(e) + ' '
        return hstr + vstr + estr

    #--------------------------------------------------#
    #ADT methods to query the graph
    
    def num_vertices(self):
        """ Return the number of vertices in the graph. """
        return len(self._structure)

    def num_edges(self):
        """ Return the number of edges in the graph. """
        num = 0
        for v in self._structure:
            num += len(self._structure[v])    #the dict of edges for v
        return num //2     #divide by 2, since each edge appears in the
                           #vertex list for both of its vertices

    def vertices(self):
        """ Return a list of all vertices in the graph. """
        return [key for key in self._structure]

    def get_vertex_by_label(self, element):
        """ get the first vertex that matches element. 
        
        BEWARE! - this method is inefficient, and will be really slow
        if used repeatedly on large graphs.
        """
        for v in self._structure:
            if v.element() == element:
                return v
        return None

    def edges(self):
        """ Return a list of all edges in the graph. """
        edgelist = []
        for v in self._structure:
            for w in self._structure[v]:
                #to avoid duplicates, only return if v is the first vertex
                if self._structure[v][w].start() == v:
                    edgelist.append(self._structure[v][w])
        return edgelist

    def get_edges(self, v):
        """ Return a list of all edges incident on v.

        Args:
            v -- a vertex object
        """
        if v in self._structure:
            edgelist = []
            for w in self._structure[v]:
                edgelist.append(self._structure[v][w])
            return edgelist
        return None

    def get_edge(self, v, w):
        """ Return the edge between v and w, or None, if there is no edge.

        Args:
            v -- a Vertex object
            w -- a Vertex object
        """
        if (self._structure != None
                         and v in self._structure
                         and w in self._structure[v]):
            return self._structure[v][w]
        return None

    def degree(self, v):
        """ Return the degree of vertex v. 

        Args:
            v -- a Vertex object
        """
        return len(self._structure[v])

    #--------------------------------------------------#
    #ADT methods to modify the graph
    
    def add_vertex(self, element, cost):
        """ Add and return a new vertex with data element.

        Note -- if there is already a vertex with the same data element,
        this will create another vertex instance with the same element.
        If the client using this ADT implementation does not want  
        duplicate elements, it is their responsibility not to add them.
        """
        v = Vertex(element, cost)
        self._structure[v] = dict()  # create an empty dict, ready for edges
        return v

    def add_vertex_if_new(self, element, cost):
        """ Add and return a vertex with element and cost, if not already in graph.

        Checks for equality between the elements. If there is special
        meaning to parts of the element (e.g. element is a tuple, with an
        'id' in cell 0), then this method may create multiple vertices with
        the same 'id' if any other parts of element are different.

        To ensure vertices are unique for individual parts of element,
        separate methods need to be written.

        BEWARE! -- this uses linear search and will be inefficient for large graphs.
        """
        for v in self._structure:
            if v.element() == element:
                #print('Already in graph')
                return v
        return self.add_vertex(element, cost)

    def add_edge(self, v, w, element):
        """ Add and return an edge, with element, between two vertices v and w.

        If either v or w are not vertices in the graph, does not add, and
        returns None.
            
        If an edge already exists between v and w, this will
        replace the previous edge.

        Args:
            v -- a Vertex object
            w -- a Vertex object
            element -- arbitrary complex structure with info for the edge
        """
        if not v in self._structure or not w in self._structure:
            return None
        e = Edge(v, w, element)
        # self._structure[v] is the dictionary of v's edges
        # so need to insert an entry for key w, with value e
        # A clearer way of expressing it would be
        # v_edges = self._structure[v]
        # v_edges[w] = e
        # etc.
        self._structure[v][w] = e  
        self._structure[w][v] = e
        return e

    def add_edge_pairs(self, elist):
        """ Add all vertex pairs in elist as edges with empty elements. """
        for (v,w) in elist:
            self.add_edge(v,w,None)

    #--------------------------------------------------#
    # Methods related to Dijkstra's algorithm.

    def a_star(self, v, finish):
        """Find the shortest path from v to all other vertices.
        
        Args:
            source (Vertex): The starting vertex for the shortest path computation.

        Returns:
            dict: A dictionary mapping each reachable vertex to a tuple.
        """

        # Initialize open adaptable priority queue for storing vertices with
        # shortest known path cost.
        open = AdaptablePriorityQueue()

        # Initialize closed to store final info about shortest path.
        closed = {}

        # Initialize preds to store predecessor for each vertex in open.
        preds = {v: None}

        # Counter for removed and added items.
        removed_count = 0
        added_count = 0

        # Compute total cost for start.
        start_incurred = 0
        start_total = start_incurred + abs(v.element()[0]-finish.element()[0]) + abs(v.element()[1]-finish.element()[1])
        open.add((start_total, start_incurred), v)
        added_count += 1

        # While open is not empty.
        while not open.is_empty():
            (start_total, start_incurred), current = open.remove_min()
            removed_count += 1
            closed[current] = (start_incurred, preds.get(current))
            preds.pop(current)

            if current == finish:
                break

            # Explore all neighbours of vertex.
            for edge in self.get_edges(current):
                opp = edge.opposite(current)
                # Skip if shortest path is finalized.
                if opp not in closed:
                    edge_weight = edge.element()
                    incurred = start_incurred + edge_weight + opp.cost()
                    total = incurred + abs(opp.element()[0]-finish.element()[0]) + abs(opp.element()[1]-finish.element()[1])
                    
                    # Add to open if newly discovered.
                    if opp not in preds:
                        preds[opp] = current
                        open.add((total, incurred), opp)
                        added_count += 1
                    # If shorter path is found update the cost.
                    elif incurred < open.get_key(opp)[1]:
                        preds[opp] = current
                        open.update_key(opp, (total, incurred))
                        added_count += 1

        print("A* removed items:", removed_count)
        print("A* vertices added to open APQ:", added_count)

        # Return dictionary with shortest path and predecessors.
        return closed
    
    def dijkstra(self, start):
        """Find the shortest path from start to all other vertices using the APQ.

        Args:
            start (Vertex): The starting vertex for the shortest path computation.

        Returns:
            dict: A dictionary mapping each reachable vertex to a tuple of (cost, predecessor).
        """

        # Initialize open adaptable priority queue for storing vertices with shortest known path cost.
        open = AdaptablePriorityQueue()

        # Initialize closed to store final info about shortest path.
        closed = {}

        # Initialize preds to store predecessor for each vertex in open.
        preds = {start: None}

        # Counter for removed and added items.
        removed_count = 0
        added_count = 0

        # Add source vertex with cost 0.
        open.add((0, 0), start)
        added_count += 1

        # While open is not empty.
        while not open.is_empty():

            # Remove the vertex with minimum cost so far.
            (total_cost, incurred_cost), current = open.remove_min()

            removed_count += 1

            # Pop predecessor
            pred = preds.pop(current)

            # Save finalized cost and predecessor
            closed[current] = (incurred_cost, pred)

            # Explore all neighbours of vertex
            for edge in self.get_edges(current):
                opp = edge.opposite(current)
                # Skip if shortest path is finalized
                if opp not in closed:
                    edge_weight = edge.element()
                    new_incurred = incurred_cost + edge_weight + opp.cost()

                    # Add to open if newly discovered
                    if opp not in preds:
                        preds[opp] = current
                        open.add((new_incurred, new_incurred), opp)  # key = (total_cost, incurred_cost)
                        added_count += 1
                    # If shorter path is found update the cost
                    elif new_incurred < open.get_key(opp)[1]:
                        preds[opp] = current
                        open.update_key(opp, (new_incurred, new_incurred))
                        added_count += 1

        print("Dijkstra's algorithm removed items:", removed_count)
        print("Dijkstra's algorithm vertices added to open APQ:", added_count)

        # Return dictionary with shortest path and predecessors
        return closed
    
    def extract_path(self, closed, dest):
        """Use closed from Dijkstra's algorithm to get shortest path."""

        # Find the destination vertex.
        end_v = None
        for v in closed:
            if v.element() == dest:
                end_v = v

        # If theres no destination return None, None.
        if end_v is None:
            return None, None
        
        # Create path list.
        path = []

        n = end_v

        # Add to the path list, going from destination to start following predecessors.
        while n:
            path.append(n.element())
            n = closed[n][1]

        # Reverse the path to correct the order.
        path.reverse()
        # Get the total cost of the path.
        cost = closed[end_v][0]

        # Return the path and cost.
        return path, cost
    
    def create_from_grid(self, grid):
        rows = len(grid)
        columns = len(grid[0])
        for row in range(rows):
            for column in range(columns):
                cell = grid[row][column]
                if cell != "X":
                    if cell == "F" or cell == "S":
                        cost = 0
                    else:
                        cost = int(cell)
                    self.add_vertex((row, column), cost)

        for row in range(rows):
            for column in range(columns):
                if grid[row][column] != "X":
                    vertex = self.get_vertex_by_label((row,column))
                    if row+1 < rows and grid[row+1][column] != "X":
                        other = self.get_vertex_by_label(((row+1,column)))
                        self.add_edge(vertex,other,1)
                    if column+1 < columns and grid[row][column+1] != "X":
                        other = self.get_vertex_by_label((row,column+1))
                        self.add_edge(vertex,other,1)
    
    #--------------------------------------------------#
    #Additional methods to explore the graph
        
    def highestdegreevertex(self):
        """ Return the vertex with highest degree. """
        hd = -1
        hdv = None
        for v in self._structure:
            if self.degree(v) > hd:
                hd = self.degree(v)
                hdv = v
        return hdv            


class Element:
    """ A key, value and index. """
    def __init__(self, total, incurred, v, i):
        self._key = (total, incurred)
        self._value = v
        self._index = i

    def __eq__(self, other):
        return self._key == other._key
        
    def __lt__(self, other):
        return self._key < other._key
        
    def _wipe(self):
        self._key = None
        self._value = None
        self._index = None


class AdaptablePriorityQueue:
    """Represents adaptable priority queue."""
    def __init__(self):
        """Initializes binary heap."""
        self._heap = []
        self._item_finder = {}

    # Helpers

    def _left(self, posn):
        """ Return the index of the left child of elt at index posn. """
        return 1 + 2*posn

    def _right(self, posn):
        """ Return the index of the right child of elt at index posn. """
        return 2 + 2*posn

    def _parent(self, posn):
        """ Return the index of the parent of elt at index posn. """
        return (posn - 1)//2
    
    def _upheap(self, posn):
        """ Bubble the item in posn in the heap up to its correct place. """
        if posn > 0 and self._upswap(posn, self._parent(posn)):
            self._upheap(self._parent(posn))

    def _upswap(self, posn, parent):
        """ If heap elt at posn has lower key than parent, swap. """
        if self._heap[posn] < self._heap[parent]:
            self._heap[posn], self._heap[parent] = self._heap[parent], self._heap[posn]
            self._heap[posn]._index = posn
            self._heap[parent]._index = parent
            return True
        return False

    def _downheap(self, posn):
        """ Bubble the item in posn in the heap down to its correct place. """
        #find minchild position
        #if minchild is in the heap
        #    if downswap with minchild is true
        #        downheap minchild
        minchild = self._left(posn)
        if minchild < len(self._heap):
            if (minchild + 1 < len(self._heap) and
                self._heap[minchild]._key > self._heap[minchild + 1]._key):
                minchild +=1
            if self._downswap(posn, minchild):
                self._downheap(minchild)

    def _downswap(self, posn, child):
        """ If healp elt at posn has lower key than child, swap; else return False. """
        #Note: this could be merged with _upswap to provide a general
        #heapswap(first, second) method, which swaps if the element
        #first has lower key than the element second
        if self._heap[posn]._key > self._heap[child]._key:
            self._heap[posn], self._heap[child] = self._heap[child], self._heap[posn]
            self._heap[posn]._index = posn
            self._heap[child]._index = child
            return True
        return False

    # Public methods

    def add(self, key, item):
        """Add new item into priority queue with priority key."""
        total, incurred = key
        # Create new element object.
        element = Element(total, incurred, item, len(self._heap))
        # Add element to the heap.
        self._heap.append(element)
        # Add element to item finder dictionary.
        self._item_finder[item] = element
        # Bubble up as needed.
        self._upheap(element._index)

    def min(self):
        """Return the key and value with the minimum key."""
        if not self._heap:
            return None, None
        # Retrieve the root of the heap for min element.
        return self._heap[0]._key, self._heap[0]._value

    def remove_min(self):
        """Remove and return the item with the minimum key."""
        if not self._heap:
            return None, None
        
        # Save the min element.
        min = self._heap[0]
        # Remove last element from the heap.
        last = self._heap.pop()

        if self._heap:
            # Move last element to root.
            self._heap[0] = last
            # Correct new first element's index.
            self._heap[0]._index = 0
            # Bubble down as needed.
            self._downheap(0)

        # Remove the element from item finder dictionary.
        del self._item_finder[min._value]

        return min._key, min._value

    def update_key(self, item, newkey):
        """Update the key in item’s element to be newkey, and rebalance the APQ."""
        # Save the old key.
        oldkey = self._item_finder[item]._key

        # Update key to the new value.
        self._item_finder[item]._key = newkey

        # Bubble or or bubble down depending on new key is greater or less than old one.
        if newkey < oldkey:
            self._upheap(self._item_finder[item]._index)
        
        if newkey > oldkey:
            self._downheap(self._item_finder[item]._index)

    def get_key(self, item):
        """Return the current key for item"""
        return self._item_finder[item]._key

    def remove(self, item):
        """Remove and return they (key, value) pair for this item, and rebalance the APQ."""
        # Find element and its current index.
        el = self._item_finder[item]
        index = el._index

        # Replace element with last element in the heap.
        last = self._heap[-1]
        self._heap[index] = last
        last._index = index

        # Remove the last element from heap and item finder.
        self._heap.pop()
        del self._item_finder[item]

        # Bubble up or bubble down as needed.
        if index < len(self._heap):
            if last._key < el._key:
                self._upheap(index)
            else:
                self._downheap(index)
        return el._key, el._value
    
    def is_empty(self):
        """Checks if the heap is empty"""
        return len(self._heap) == 0

#--------------------------------------------------#
# Functions related to Dijkstra's algorithm.

def graphreader(filename):
    """ Read and return the route map in filename. """
    graph = Graph()
    file = open(filename, 'r')
    entry = file.readline() #either 'Node' or 'Edge'
    num = 0
    while entry == 'Node\n':
        num += 1
        nodeid = int(file.readline().split()[1])
        vertex = graph.add_vertex(nodeid)
        entry = file.readline() #either 'Node' or 'Edge'
    print('Read', num, 'vertices and added into the graph')
    num = 0
    while entry == 'Edge\n':
        num += 1
        source = int(file.readline().split()[1])
        sv = graph.get_vertex_by_label(source)
        target = int(file.readline().split()[1])
        tv = graph.get_vertex_by_label(target)
        length = float(file.readline().split()[1])
        edge = graph.add_edge(sv, tv, length)
        file.readline() #read the one-way data
        entry = file.readline() #either 'Node' or 'Edge'
    print('Read', num, 'edges and added into the graph')
    print(graph)
    return graph

def dijkstra_result(result):
        """Prints Dijkstra's algorithm results in readable format."""
        for v in result:
            cost, pred = result[v]
            # Get predecessor's name if it exists.
            if pred is None:
                pred_name = None
            else:
                pred_name = pred.element()
            # Print vertex information.
            print("Vertex", str(v.element()) + ":",  "Cost:", cost, "Predecessor:", pred_name)