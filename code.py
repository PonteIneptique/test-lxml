from lxml import etree
from lxml import objectify
import pickle

# To ensure things are all equal, we share the same Parser
from lxml.etree import XMLParser
X = XMLParser()

# We create two similar objects, one using etree, one using objectify
with open('./resources/phi1294.phi002.perseus-lat2.xml') as f:
    Tree1 = objectify.parse(f, X)
    # Note that parsing the same file twice results in  "Document is empty"
    # so we cannot do `Tree2 = etree.parse(f, parser=X)` here

with open('./resources/phi1294.phi002.perseus-lat2.xml') as f:
    Tree2 = etree.parse(f, parser=X)

# For the third tree, we pickle the Tree1 and reload it into Tree3
with open('./resources/pickled.pkl', "wb") as f:
    pickle.dump(Tree1, f)

with open('./resources/pickled.pkl', "rb") as f:
    Tree3 = pickle.load(f)

# We ensure things derive from the same parent object
trees = [Tree1, Tree2, Tree3]
assert [True, True, True] == [isinstance(tree, etree._ElementTree) for tree in trees]

# We recursively walk the tree through xpath, ensuring data are equal
def walking(xml, xpath):
    for node in xml.xpath(xpath):
        if isinstance(node, etree._Element):
            yield node


def compare(xml1, xml2, xml3, xpath="./node()", increment=1):
    # We apply the same
    nodes1 = list(walking(xml1, xpath))
    nodes2 = list(walking(xml2, xpath))
    nodes3 = list(walking(xml3, xpath))

    assert len(nodes2) == len(nodes3) == len(nodes1)
    for i in range(0, len(nodes1)):
        el1, el2, el3 = nodes1[i], nodes2[i], nodes3[i]
        if isinstance(el1, etree._Element):
            assert el1.tag == el2.tag == el3.tag, \
                "Failed at depth {} for {}".format(increment, str((el1, el2, el3)))
            compare(el1, el2, el3, xpath, increment=increment+1)

compare(Tree1, Tree2, Tree3)
