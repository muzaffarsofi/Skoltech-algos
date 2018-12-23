class Node():
    
    def __init__(self, value=None, left=None, right=None, assoc_struct=None, *args, **kwargs):
        assert isinstance(left, Node) or (left is None), "wrong type of left Node"
        assert isinstance(right, Node) or (right is None), "wrong type of right Node"
        assert isinstance(value, tuple) or (value is None) or isinstance(value, list), "value type error"
        
        self.value = value
        self.left = left
        self.right = right
        self.assoc_struct = assoc_struct
        
    def set_value(self, value):
        assert isinstance(value, tuple) or (value is None) or isinstance(value, list), "value type error"
        self.value = value
    
    def set_left(self, left):
        assert isinstance(left, Node) or (left is None), "wrong type of left Node"
        self.left = left
    
    def set_right(self, right):
        assert isinstance(right, Node) or (right is None), "wrong type of right Node"
        self.right = right
        
    def set_assoc_struct(self, assoc_struct):
        assert isinstance(assoc_struct, Range1Dtree) or (assoc_struct is None), "assoc struct only Range1Dtree allowed or None"
        
        self.assoc_struct = assoc_struct

    @property
    def isLeaf(self):
        if (self.left is None) and (self.right is None):
            return True
        else:
            return False
        
class Range1Dtree():
    
    def _build1D(self, points):
        if len(points) <= 0:
            return None

        m_index = int(len(points)/2)
        node = Node()
        node.set_value(points[m_index])
        node.set_left(self._build1D(points[:m_index]))
        node.set_right(self._build1D(points[m_index+1:]))
        return node
        
    
    def __init__(self, points, which_dimension=0, *args, **kwargs):
        self.which_dimension = which_dimension
        sorted_p = sorted(points, key=lambda x: x[self.which_dimension])
        
        self.root_node  = self._build1D(sorted_p)
    
        
    def query(self, node, r):
        res = []
        if not node:
            return res
        
        if (r[0] <= node.value[self.which_dimension]):
            res += self.query(node.left, r)
            
        if (node.value[self.which_dimension] <= r[1]):
            res += self.query(node.right, r)
        
        if (r[0] <= node.value[self.which_dimension]) and (node.value[self.which_dimension] <= r[1]):
            res += [node.value]
        
        return res
        
        
class Range2Dtree():
    
    def _build2D(self, points):
        # Build a bb-search tree T_ay on the set P_in over y-coordinates. Store points in the leaves.
        bbTay = Range1Dtree(points, which_dimension=self.which_dimension+1)
        if len(points) == 1:
            return Node(points[0], assoc_struct=bbTay)
        else:
            sorted_p = sorted(points, key=lambda x: x[self.which_dimension])
            m_index = int(len(sorted_p)/2)
            left, right = sorted_p[:m_index], sorted_p[m_index:]
            
            node_v = Node()
            node_v.set_left(self._build2D(left))
            node_v.set_right(self._build2D(right))
            node_v.set_value(sorted_p[m_index])
            node_v.set_assoc_struct(bbTay)
            
            return node_v
        
    def __init__(self, points, which_dimension=0, *args, **kwargs):
        self.which_dimension = which_dimension
        self.root_node = self._build2D(points)
        

    def getRange(self, node):
        current_node = node
        res = []
        if current_node.isLeaf:
            res+= [current_node.value]
        if current_node.left:
            res+= self.getRange(current_node.left)
        if current_node.right:
            res+= self.getRange(current_node.right)
            
        return res
    
        
    def query(self, node, rx, ry):
        # rx, ry - range in x, range in y
        if node.isLeaf:
            p = node.value
            if ((p[self.which_dimension] >= rx[0]) and (p[self.which_dimension] <= rx[1])) and ((p[self.which_dimension+1] >= ry[0]) and (p[self.which_dimension+1] <= ry[1])):
                return [p]
            else:
                return []
        current_range_x = self.getRange(node)
        if ((current_range_x[0][self.which_dimension] >= rx[0]) and (current_range_x[-1][self.which_dimension] <= rx[1])):
            return node.assoc_struct.query(node.assoc_struct.root_node, ry)
        else:
            if (current_range_x[0][self.which_dimension] >= rx[0]) or (current_range_x[-1][self.which_dimension] <= rx[1]) or ((rx[1] <= current_range_x[-1][self.which_dimension]) and (rx[0] >= current_range_x[0][self.which_dimension])):
                return self.query(node.left, rx, ry) + self.query(node.right, rx, ry)

      
    
if __name__=="__main__":
    inp = open('input.txt', 'r')
    out = open('output.txt', 'w')

    min_num = int(inp.readline ())
    miners = []

    for i in range(min_num):
        miner = inp.readline()
        miner_list = [int(val) for val in miner.split()]
        miners.append(miner_list)


    tree = Range2Dtree(miners) 

    que_num = int(inp.readline())
    queries = []

    for i in range(que_num):
        rec_num = int(inp.readline())

        query = []

        for j in range(rec_num):
            rect = inp.readline()
            rect_list = [int(val) for val in rect.split()]
            query.append(rect_list)

        queries.append(query)

    with open('output.txt', 'w') as f:
        for query in queries:
            counted = set()
            summary = 0
            for rect in query:
                rx = [min(rect[0], rect[2]), max(rect[0], rect[2])]
                ry = [min(rect[1], rect[3]), max(rect[1], rect[3])]
                query_res = tree.query(tree.root_node, rx, ry)
                if query_res:
                    for elem in query_res:
                        elem_t = tuple(elem)
                        if elem_t not in counted:
                            counted.add(tuple(elem))
                            summary += elem[2]

            f.write(str(summary)+'\n')