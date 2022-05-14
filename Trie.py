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

    def dfs(self, node, pre):
 
        if node.is_end:
            self.output.append((pre + node.char))
         
        for child in node.children.values():
            self.dfs(child, pre + node.char)
         
    def search(self, x):
        
        node = self.root
         
        for char in x:
            if char not in node.children:
                self.output = False
                return False
            #if Not
            node = node.children[char]

        self.output = True
        return True      


if __name__ == "__main__":
    tr = Trie()
    tr.insert("here")
    tr.insert("hear")
    tr.insert("he")
    tr.insert("hello")
    tr.insert("how ")
    tr.insert("her")

    tr.search("heres")
    print(tr.output)