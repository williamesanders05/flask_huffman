import os
import zipfile
from flask import Flask, flash, request, redirect, url_for, render_template, send_file

class TreeNode:
    def __init__(self, val, freq, left, right):
        self.val = val
        self.freq = freq
        self.left = left
        self.right = right
        
    def compareTo(self, other):
        return self.freq - other.freq
        
    def getVal(self):
        return self.val
        
    def getFreq(self):
        return self.freq
        
    def setFreq(self, freq):
        self.freq = freq
        
    def getRight(self):
        return self.right
        
    def getLeft(self):
        return self.left
        
    def isLeaf(self):
        return self.left == None and self.right == None
        
    def setLeft(self, left):
        self.left = left
        
    def setRight(self, right):
        self.right = right
        
    def printTree(self):
        if self.left != None:
            self.left.printTree()
        print(self.val)
        if self.right != None:
            self.right.printTree()

class PriorityQueue:
    def __init__(self):
        self.queue = []
        
    def getIndex(self, char):
        for i in range(len(self.queue)):
            if self.queue[i].getVal() == char:
                return i
        return -1
        
    def push(self, node):
        if len(self.queue) == 0:
            self.queue.append(node)
        else:
            index = self.getIndex(node.getVal())
            if index == -1:
                for i in range(len(self.queue)):
                    if node.compareTo(self.queue[i]) >= 0:
                        self.queue.insert(i, node)
                        break
            else:
                node.setFreq(self.queue[index].getFreq() + 1)
                del self.queue[index]
                self.push(node)
        
    def pop(self):
        return self.queue.pop(0)
        
    def size(self):
        return len(self.queue)
        
    def get(self, index):
        return self.queue[index]
        
    def dequeue(self):
        return self.queue.pop(0)
        
    def printQueue(self):
        for i in range(len(self.queue)):
            print(self.queue[i].getVal() + " " + str(self.queue[i].getFreq()))

ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if allowed_file(file.filename):
            text = ""
            for line in file:
                text = text + line.decode("utf-8").replace('\n', '')
            huffman(text)
            return send_file("files/compressed.zip", as_attachment=True)
    return render_template('encrypt.html')

@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'encrypted' not in request.files or 'key' not in request.files:
            flash('No file part')
            return redirect(request.url)
        encryptedFile = request.files['encrypted']
        keyFile = request.files['key']
        if allowed_file(encryptedFile.filename) and allowed_file(keyFile.filename):
            encrypted = ""
            for line in encryptedFile:
                encrypted = encrypted + line.decode("utf-8").replace('\n', '')
            key = ""
            for line in keyFile:
                key = key + line.decode("utf-8").replace('\n', '')
            keyList = list(key)
            newRoot = buildTree(keyList)
            result = huffmanDecode(encrypted, newRoot)
            with open("files/decoded.txt", "w") as file:
                file.write(result)
            return send_file("files/decoded.txt", as_attachment=True)
    return render_template('decrypt.html')


def huffman(text):
    print(text)
    bin = ""
    for x in text:
        bin = bin + format(ord(x), '08b')
    pq = PriorityQueue()
    while len(bin) > 0:
        value = bin[:8]
        bin = bin[8:]
        pq.push(TreeNode(value, 1, None, None))
    pq.printQueue()
    root = makeTree(pq)
    map = {}
    makeMap(root, "", map)
    encoded = rewrite(text, map)
    print(encoded)
    createEncodedFile(encoded)
    createKeyFile(root)
    compression = zipfile.ZIP_DEFLATED
    with zipfile.ZipFile("files/compressed.zip", mode='w') as z:
        z.write("files/encoded.txt", compress_type=compression)
        z.write("files/key.txt", compress_type=compression)

def makeTree(pq):
    while pq.size() > 1:
        left = pq.dequeue()
        right = pq.dequeue()
        parent = TreeNode(None, left.getFreq() + right.getFreq(), left, right)
        pq.push(parent)
    return pq.dequeue()

def makeMap(node, code, map):
    if node.getLeft() != None:
        makeMap(node.getLeft(), code + "0", map)
    if node.isLeaf():
        map[node.getVal()] = code
    if node.getRight() != None:
        makeMap(node.getRight(), code + "1", map)

def createEncodedFile(encoded):
    file = open("files/encoded.txt", "w")
    file.write(encoded)
    file.close()
    
def createKeyFile(root):
    result = str(preOrderTraversal(root, ""))
    file = open("files/key.txt", "w")
    file.write(result)
    file.close()

def rewrite(text, map):
    result = ""
    for x in text:
        binary = format(ord(x), '08b')
        result = result + map[binary]
    return result

def preOrderTraversal(node, result):
    if (node == None):
        return result
    if node.isLeaf() and node.getVal() != None:
        result = result + "1" + str(node.getVal())
        return result
    else:
        result = result + "0"
        result = str(preOrderTraversal(node.getLeft(), result))
        result = str(preOrderTraversal(node.getRight(), result))
        return result
    
def buildTree(key_list):
    if not key_list:
        return None
    bit = key_list.pop(0)
    if bit == "1":
        value = ''.join(key_list[:8])
        key_list[:8] = []
        return TreeNode(value, None, None, None)
    else:
        left = buildTree(key_list)
        right = buildTree(key_list)
        return TreeNode(None, None, left, right)
    
def huffmanDecode(encoded, root):
    result = ""
    node = root
    for x in encoded:
        if x == "0":
            node = node.getLeft()
        else:
            node = node.getRight()
        if node.isLeaf():
            result = result + chr(int(node.getVal(), 2))
            node = root
    return result