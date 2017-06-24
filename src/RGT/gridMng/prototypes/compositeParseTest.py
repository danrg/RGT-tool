import unittest

from compositeParse import CompositeParse


class FooTests(unittest.TestCase):

    def testFoo(self):
        self.failUnless(True)

    def testBasicString(self):
        compositeObject = CompositeParse("hello")
        self.failUnlessEqual(compositeObject.initialString, "hello")

    def testNumberOfItems(self):
        c = CompositeParse("A0&(B1|B2|B3)&C4&(D5|D6)")
        self.failUnlessEqual(c.getCountItems(), 4)
        c = CompositeParse("A0&B1&C2")
        self.failUnlessEqual(c.getCountItems(),3)

    def testNumberOfCompositions(self):
        c = CompositeParse("A0&B1&C2")
        self.failUnlessEqual(c.getNumberOfCompositions(), 1)
        c = CompositeParse("(A0)&(B1|B2|B3)&C4&(D5|D6)") #SHOULD ACCEPT ONE ELEMENT WITH PARATHESIS
        self.failUnlessEqual(c.getNumberOfCompositions(), 6)
        c = CompositeParse("A1")
        self.failUnlessEqual(c.getNumberOfCompositions(),1)
        c = CompositeParse("A1&B2")
        self.failUnlessEqual(c.getNumberOfCompositions(),1)
        c = CompositeParse("A1&(B2|B3)")
        self.failUnlessEqual(c.getNumberOfCompositions(),2)
        c = CompositeParse("A1&(B2|B3)&C4")
        self.failUnlessEqual(c.getNumberOfCompositions(),2)
