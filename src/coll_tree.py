import xmmsclient.collections as coll

def _node_cmp_key(item):
    """Calculate the key used to sort nodes, ignores case"""
    key = item[0][0]

    if isinstance(key, basestring):
        return key.lower()
    else:
        return key

class CollectionTree:

    def __init__(self, xmms, steps, base=coll.Universe()):
        self.xmms = xmms
        self.base = base
        self.steps = steps

        self.requested = False
        self.childs = None

    def request(self):
        self.xmms.coll_query_infos(self.base, self.steps[0], cb=self._coll_cb).wait()
        self.requested = True

    def _build_child(self, item):
        """Turn a collection item into a node"""
        steps = self.steps

        # turn the dictionary into a list
        data = [item[attr] for attr in steps[0]]

        # create the new collection
        sub_coll = self.base
        for attr in steps[0]:
            value = item[attr]

            if value == None:
                # special case if the property doesn't exist
                sub_coll = coll.Complement(coll.Has(sub_coll, field=attr))
            else:
                # SRSLY? why do I have to care about encoding here????
                value = value.encode("utf-8")
                sub_coll = coll.Equals(sub_coll, field=attr, value=value)

        # actually create the node
        node = CollectionTree(self.xmms, steps[1:], sub_coll)

        # tuples are stored
        return (data, node)

    def _coll_cb(self, value):
        raw = value.value()

        # turn it into a sorted list
        self.childs = sorted((self._build_child(item) for item in raw),
                key=_node_cmp_key)


def test():
    global t, x
    from xmmsclient import XMMS
    x = XMMS()
    x.connect()
    t = CollectionTree(x, [['artist'], ['date', 'album'], ['tracknr', 'title']])
    t.request()
    return t

