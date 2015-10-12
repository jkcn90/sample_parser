from collections import defaultdict
from six import string_types

class Node:

    def __init__(self, token):
        self.token = token
        self.left = None
        self.right = None

        self.child_tokens_dict = defaultdict(set)
        self.metadata = set()

    def __repr__(self):
        return 'Node({})'.format(self.token)

    def __str__(self):
        left = self.left.token if self.left is not None else None
        right = self.right.token if self.right is not None else None
        return self.__repr__() + ': ({}, {})'.format(left, right)


class TernarySearchTree:

    def __init__(self):
        self.root_map = defaultdict(lambda: None)

    def add(self, tokens, metadata=None):
        if not tokens:
            return
        key = tokens[0]
        self.root_map[key] = add(tokens, self.root_map[key], metadata)

    def search(self, tokens, flexible=True):
        key = tokens[0]
        node, repeated_count = search(tokens, self.root_map[key], flexible)
        return (node, repeated_count)

    def contains(self, tokens):
        if not tokens:
            return True

        (node, count) = self.search(tokens, flexible=False)
        if node is None:
            return False

        last_token_count = 0
        for token in reversed(tokens):
            if token == tokens[-1]:
                last_token_count += 1
            else:
                break
        return count == last_token_count

    def get_completions(self, tokens):
        if not tokens:
            return []

        (node, count) = self.search(tokens)

        if node is None:
            return []
        return get_completions(tokens, node, starting_count=count-1)

    def __repr__(self):
        return self.root_map.keys().__repr__()

def add(tokens, node, metadata=None):
    token = tokens[0]
    if node is None:
        node = Node(token)
        node.metadata.add(metadata)

    if token > node.token:
        node.right = add(tokens, node.right)
        return node
    elif token < node.token:
        node.left = add(tokens, node.left)
        return node

    for i, token in enumerate(tokens):
        if token != node.token:
            node.child_tokens_dict[i].add(token)
            node.metadata.add(metadata)
            return add(tokens[i:], node)
    node.child_tokens_dict[len(tokens)].add('')
    node.metadata.add(metadata)
    return node

def search(tokens, node, flexible=True):
    if node is None:
        return (None, 0)

    this_token_count = 0
    for token in tokens:
        if token == node.token:
            this_token_count += 1
        else:
            break

    reduction = 0
    for token_count in node.child_tokens_dict:
        if flexible and (reduction < token_count) and (this_token_count <= token_count):
            reduction = token_count
        if (not flexible) and (this_token_count == token_count):
            reduction = this_token_count

    if flexible:
        reduction = min(reduction, this_token_count)
    tokens = tokens[reduction:]

    if not tokens:
        return (node, reduction)

    right_search, repeated_count = search(tokens, node.right, flexible)
    if right_search is not None:
        return (right_search, repeated_count)

    left_search, repeated_count = search(tokens, node.left, flexible)
    if left_search is not None:
        return (left_search, repeated_count)
    return (None, 0)

def get_completions(tokens, node, target_token=None, starting_count=0):
    if node is None:
        return []

    get_new_target_tokens = (target_token is None) or (node.token == target_token)

    if get_new_target_tokens:
        target_token_counts = [(count, value)
                               for count, value_set
                               in node.child_tokens_dict.items()
                               for value in list(value_set)]
    else:
        target_token_counts = [(0, target_token)]

    completions = []
    for count, target_token in target_token_counts:
        if starting_count:
            count -= starting_count
        count = max(count - 1, 0)

        if get_new_target_tokens:
            if isinstance(tokens, string_types):
                new_tokens = tokens + count * node.token + target_token
            else:
                new_tokens = tokens + count * [node.token] + [target_token]
        else:
            new_tokens = tokens

        if target_token > node.token:
            completions += get_completions(new_tokens, node.right, target_token)
        if target_token < node.token:
            completions += get_completions(new_tokens, node.left, target_token)
        if target_token == '':
            completions += [new_tokens]
    if completions and isinstance(completions[0], list):
        return completions
    else:
        return list(set(completions))
