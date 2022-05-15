class TrieNode:

    def __init__(self, char):
        self.char = char
        self.children = {}
        self.is_end = False



class Trie(object):
    def __init__(self):
        self.root = TrieNode("")

    def insert(self, word):
        nood = self.root 

        for char in word:
            if char not in nood.children:
                nood.children[char] = TrieNode(char)
            nood = nood.children[char]
        nood.is_end = True     

    def search(self, x):
        node = self.root

        #if x empty
        if not len(x):
            return False

        for char in x:
            if char not in node.children:
                self.output = False
                return False

            #if Not
            node = node.children[char]

        self.output = True
        return True      


    def PartialSearch(self, x):
        node = self.root

        #if x empty
        if not len(x):
            return False

        for char in x:
            
            if char not in node.children:
                #skip till first char in word is found in trie
                if node == self.root:
                    continue
                return False
        
            #if Not
            node = node.children[char]

        return True

    def AhoCorasick(self, x):
        node = self.root
        self.output = []

        #if x empty
        if not len(x):
            return False

        for char in x:
            if char not in node.children:
                #skip till first char in word is found in trie
                if node == self.root:
                    continue
                return False
        
            #if Not
            node = node.children[char]

        self.output.append(node.char)
        return True

if __name__ == "__main__":
    tr = Trie()
    tr.insert("here")
    tr.insert("hear")
    tr.insert("he")
    tr.insert("hello")
    tr.insert("how ")
    tr.insert("her")
    # Search Function Returns True if the word is found in the trie
    print(tr.search("heres"))
    #you can also use the output variable to get the output which is True or False
    tr.search("he")
    print(tr.output)


    #Partial Search Function
    print(tr.PartialSearch("shge"))
    print(tr.PartialSearch("shgehe"))
    print(tr.PartialSearch("she"))
    print(tr.PartialSearch(""))
    print(tr.AhoCorasick("shgehe"))
    #my name is mohamed