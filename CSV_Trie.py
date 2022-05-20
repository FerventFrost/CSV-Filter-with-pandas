import queue
class TrieNode:

    def __init__(self, char):
        self.char = char
        self.children = {}
        self.is_end = False


class Trie(object):
    def __init__(self):
        self.root = TrieNode("")
        self.Q = queue.Queue()
        self.Bad_is_found = False

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

    #Search for the First word only if the word is not the same break and exit
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
    
    #My Custom AhoCorasick
    def Custom_AhoCorasick(self, x):
        self.Bad_is_found = False
        self.Q.queue.clear()
        self.Q.put(None)
        node = self.root
        x = x.lower()
        #if x empty
        if not len(x):
            return False

        for char in x:
            if char in node.children:
                self.Q.put(node.children[char])

            while True:
                temp = self.Q.get()
                if temp is None:
                    self.Q.put(temp)
                    break
                elif char in temp.children:
                    temp = temp.children[char]
                    if temp.is_end:
                        self.Bad_is_found = True
                        break

                    self.Q.put(temp)

            if self.Bad_is_found:
                return True

        return False
    
    #doesn't have any use
    def AhoCorasick(self, x, Custom = False):
        if Custom:
            pass
        return self.Custom_AhoCorasick(x)

if __name__ == "__main__":
    tr = Trie()
    tr.insert("here")
    tr.insert("hear")
    tr.insert("he")
    tr.insert("hello")
    tr.insert("how")
    tr.insert("her")

    #Implement my Aho Algo
    print(tr.Custom_AhoCorasick("shgh"))
    print(tr.Custom_AhoCorasick("shetw"))
    # # Search Function Returns True if the word is found in the trie
    # print(tr.search("heres"))
    # # #you can also use the output variable to get the output which is True or False
    # tr.search("he")
    # print(tr.output)


    # # #Partial Search Function
    print(tr.PartialSearch("she"))
    # print(tr.PartialSearch("shgehe"))
    # print(tr.PartialSearch("she"))
    # print(tr.PartialSearch(""))
    # print(tr.AhoCorasick("shgehe"))
    # #my name is mohamed