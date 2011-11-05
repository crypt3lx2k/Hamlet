import collections

class PrefixTree (object):
    """
    Prefix tree that behaves like a set for strings.
    """
    class Node (object):
        """
        Prefix tree node, contains a mapping from
        chars to nodes and a boolean value which
        indicates whether the node is a stored string.
        """
        def __init__ (self):
            """
            Initializes a new node.
            """
            self.children  = {}
            self.is_string = False

        def __contains__ (self, c):
            """
            Returns whether the char is a key in the mapping.
            """
            return c in self.children

        def __getitem__ (self, c):
            """
            Returns the node which the char maps
            to or None if it does not exist.
            """
            return self.children.get(c)

        def __setitem__ (self, c, n):
            """
            Maps char to node.
            """
            self.children[c] = n

        def __iter__ (self):
            """
            Iterator over the chars in mapping.
            """
            return iter(self.children)

        def get_by_prefix (self, prefix, list):
            """
            Adds strings to list if they exists,
            returns the same list.
            """
            if self.is_string:
                list.append (prefix)

            for c in self:
                self[c].get_by_prefix(prefix + c, list)

            return list

        def pop (self, c):
            """
            Removes specified char from mapping
            and returns the node.
            Raises KeyError if it doesn't exist.
            """
            return self.children.pop(c)

    def __init__ (self, iterable=None):
        """
        Returns a new instance, takes optional argument
        which must be a collection of strings.
        """
        self.root = PrefixTree.Node()

        if iterable is not None:
            [self.add(e) for e in iterable]

    @classmethod
    def __value_check (cls, v):
        """
        Raises TypeError if the value is not a string.
        """
        if not isinstance (v, str):
            raise TypeError ('argument must be string')

    def add (self, s):
        """
        Adds string to set.
        """
        PrefixTree.__value_check(s)

        current = self.root

        for c in s:
            if not c in current:
                current[c] = PrefixTree.Node()

            current = current[c]

        current.is_string = True

    def clear (self, s):
        """
        Removes all elements.
        """
        self.root = PrefixTree.Node()

    def contains (self, s):
        """
        Returns whether the string is in set.
        """
        try:
            PrefixTree.__value_check(s)
        except TypeError:
            return False

        current = self.root

        for c in s:
            if not c in current:
                return False

            current = current[c]

        return current.is_string

    def __contains__ (self, s):
        """
        Returns whether the string is in set.
        """
        return self.contains(s)

    def prefix (self, prefix):
        """
        Returns a list of strings that start
        with prefix.
        """
        PrefixTree.__value_check(prefix)

        current = self.root

        for c in prefix:
            if not c in current:
                return []

            current = current[c]

        return current.get_by_prefix(prefix, [])

    def remove (self, s):
        """
        Removes string from set, raises
        KeyError if it doesn't exist.
        """
        try:
            PrefixTree.__value_check(s)
        except TypeError:
            raise KeyError ('\'%s\'' % str(s))

        visited = collections.deque()
        current = self.root

        for c in s:
            if not c in current:
                raise KeyError ('\'%s\'' % s)

            visited.appendleft((c, current))
            current = current[c]

        if current.is_string:
            current.is_string = False
        else:
            raise KeyError ('\'%s\'' % s)

        for char, node in visited:
            if current.is_string or current.children:
                break

            node.pop (char)
            current = node

    def __repr__ (self):
        """
        Returns a string representation of the object.
        """
        return 'PrefixTree(%s)' % self.prefix('')

