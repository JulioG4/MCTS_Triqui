class Tree:
    def __init__(self, root):
        root.id = 0
        self.nodes = [root]

    def get(self, id):
        return self.nodes[id]

    def insert(self, node, parent):
        node.id = len(self.nodes)
        node.parent_id = parent.id
        self.nodes.append(node)
        self.nodes[node.parent_id].children_id.append(node.id)

    def remove(self, node):
        removed_ids = self.remove_rec(node)
        self.nodes = [f for f in self.nodes if f is not None]

        for i in range(len(self.nodes)):
            removed_before_id = self.removed_before(self.nodes[i].id, removed_ids)
            self.nodes[i].id -= removed_before_id

            removed_before_parent_id = self.removed_before(self.nodes[i].parent_id, removed_ids)
            self.nodes[i].parent_id -= removed_before_parent_id

            for j in range(len(self.nodes[i].children_id)):
                removed_before_children_id = self.removed_before(self.nodes[i].children_id[j], removed_ids)
                self.nodes[i].children_id[j] -= removed_before_children_id

    def remove_rec(self, node):
        removed = []

        if node.is_root():
            return removed

        children = self.get_children(node)[:]
        for child in children:
            if child:
                removed.extend(self.remove_rec(child))

        parent_children = self.get_parent(node).children_id

        try:
            index_of_in_parent = parent_children.index(node.id)
            self.get_parent(node).children_id.pop(index_of_in_parent)
            self.nodes[node.id] = None
            removed.append(node.id)
        except ValueError:
            pass

        return removed

    def removed_before(self, id, removed_id):
        num = 0
        for removed in removed_id:
            if removed < id:
                num += 1
        return num

    def update(self, node, new_data):
        self.nodes[node.id].data = new_data

    def get_parent(self, node):
        return self.nodes[node.parent_id]

    def get_children(self, node):
        if not node:
            return []
        arr = []
        for child_id in node.children_id:
            arr.append(self.nodes[child_id])
        return arr

    def get_siblings(self, node):
        return self.get_children(self.get_parent(node))

    def get_root(self):
        return self.get(0)

    def copy(self):
        arr = []
        for node in self.nodes:
            arr.append(node.copy())
        new_tree = Tree(arr[0])
        new_tree.nodes = arr[:]
        return new_tree


class Node:
    def __init__(self, data, id=-1, children_id=None, parent_id=-1):
        self.data = data
        self.id = id
        self.children_id = children_id if children_id is not None else []
        self.parent_id = parent_id

    def copy(self):
        return Node(self.data.copy() if hasattr(self.data, 'copy') else self.data, 
                   self.id, self.children_id[:], self.parent_id)

    def has_n_children(self, n):
        return len(self.children_id) == n

    def is_leaf(self):
        return self.has_n_children(0)

    def is_root(self):
        return self.id == 0
