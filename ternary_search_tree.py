class Node:

    def __init__(self, token, is_end_of_word=False):
        self.token = token
        self.is_end_of_word = is_end_of_word

        self.left = None
        self.center = None
        self.right = None
        self.child_tokens = set()

    def __repr__(self):
        return 'Node({}, is_end_of_word={})\n'.format(self.token, self.is_end_of_word)

    def __str__(self):
        left = self.left.token if self.left is not None else None
        center = self.center.token if self.center is not None else None
        right = self.right.token if self.right is not None else None
        return self.__repr__() + '({}, {}, {})'.format(left, center, right)


class TernarySearchTree:

    def __init__(self):
        self.root = None

    @property
    def token(self):
        return self.root.token if self.root is not None else None

    @property
    def left(self):
        return self.root.left if self.root is not None else None

    @property
    def center(self):
        return self.root.center if self.root is not None else None

    @property
    def right(self):
        return self.root.right if self.root is not None else None

    def add(self, tokens):
        if not tokens:
            return
        self.root = add(tokens, self.root)

    def search(self, tokens):
        return search(tokens, self.root)

    def contains(self, tokens):
        if not tokens:
            return True

        node = self.search(tokens)
        if node is None:
            return False
        if node.is_end_of_word:
            return True
        return False

    def get_completions(self, tokens):
        if not tokens:
            return []

        node = self.search(tokens)
        if node is None:
            return []
        return get_completions(tokens, node)

    def __repr__(self):
        return self.root.__repr__()

def add(tokens, node):
    token = tokens[0]

    if node is None:
        node = Node(token, is_end_of_word=False)
        return add(tokens, node)

    if token > node.token:
        node.right = add(tokens, node.right)
    elif token < node.token:
        node.left = add(tokens, node.left)
    elif len(tokens) == 1:
        node.is_end_of_word = True
    else:
        node.child_tokens.add(tokens[1])
        if tokens[1] == node.token:
            node.center = add(tokens[1:], node.center)
        else:
            return add(tokens[1:], node)
    return node

def search(tokens, node):
    if not node:
        return
    if not tokens:
        return node

    if tokens[0] == node.token:
        tokens = tokens[1:]
        if not tokens:
            return node

    right_search = search(tokens, node.right)
    if right_search is not None:
        return right_search

    left_search = search(tokens, node.left)
    if left_search is not None:
        return left_search

    center_search = search(tokens, node.center)
    if center_search is not None:
        return center_search

def get_completions(tokens, node, target_token=None):
    if node is None:
        return []

    get_new_target_tokens = (target_token is None) or (node.token == target_token)

    if get_new_target_tokens:
        target_tokens = [token for token in node.child_tokens]
    else:
        target_tokens = [target_token]

    completions = []
    for target_token in target_tokens:
        if get_new_target_tokens:
            new_tokens = tokens + target_token
        else:
            new_tokens = tokens

        if target_token > node.token:
            completions += get_completions(new_tokens, node.right, target_token)
        elif target_token < node.token:
            completions += get_completions(new_tokens, node.left, target_token)
        else:
            completions += get_completions(new_tokens, node.center, target_token)
    if node.is_end_of_word:
        completions += [tokens]
    return completions
