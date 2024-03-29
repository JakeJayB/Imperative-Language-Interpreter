""" Jacob Bejarano,  Wesly Barayuga
    Project Phase 2.2 - Parser for Full Language
    03/25/23
"""
import Scanner

class Node():
    def __init__(self, value, type) -> None:
        self.value = value
        self.type = type
        self.left = None
        self.middle = None
        self.right = None      
        
    def MakeSubTree(root, left=None, middle=None, right=None):
        root = Node(root.value, root.type)
        root.left = left
        root.middle = middle
        root.right = right
        return root 
    
# Counter.val acts as our 'i' for accessing elements in token array
class Counter():
    def __init__(self) -> None:
        Counter.val = -1
        Counter.next_token = None
        
        
def printTree(node, output, whitespace=''):
    '''preorder traverse of tree'''
    
    if node == None: return
    output.write(whitespace + str(node.value) + " : " + str(Scanner.TokenType.toString(node.type)) + '\n')
    printTree(node.left, output, whitespace+'\t')
    printTree(node.middle, output, whitespace+'\t')
    printTree(node.right, output, whitespace+'\t')

def raiseError(token, output):
    '''when error occurs, raiseError() is called'''
    
    output.write(f"SyntaxError :: Parsing Exception => {token}")
    quit(0)
        

# Counter.val acts as our 'i' for accessing elements in token array
def consumeToken(tokens):
    Counter.val += 1
    if Counter.val+1 >= len(tokens): 
        Counter.next_token = None 
        return
    Counter.next_token = tokens[Counter.val+1]    
    

def parseStatement(tokens, output):
    tree = parseBaseStatement(tokens, output)
    while Counter.next_token != None and Counter.next_token.value == ';':
        temp = Counter.next_token
        consumeToken(tokens)
        tree = Node.MakeSubTree(temp, tree, None, parseBaseStatement(tokens, output))
    return tree

def parseBaseStatement(tokens, output):
    if Counter.next_token != None and Counter.next_token.value == "skip":
        temp = Counter.next_token
        consumeToken(tokens)
        return Node.MakeSubTree(temp, None, None, None)
    elif Counter.next_token != None and Counter.next_token.value == "if":
        return parseIfStatement(tokens, output)
    elif Counter.next_token != None and Counter.next_token.value == "while":
        return parseWhileStatement(tokens, output)
    elif Counter.next_token != None and Counter.next_token.type == Scanner.TokenType.INDENTIFIER:
        return parseAssignment(tokens, output)
    else:
        if Counter.next_token != None: raiseError(Counter.next_token.value, output)
        else: raiseError("EXPECTED STATEMENT AT END", output)

def parseAssignment(tokens, output):
    if Counter.next_token != None and Counter.next_token.type == Scanner.TokenType.INDENTIFIER:
        temp = Counter.next_token
        consumeToken(tokens)
        
        if Counter.next_token == None or Counter.next_token.value != ":=": raiseError("EXPECTING ':='", output)
        temp2 = Counter.next_token
        consumeToken(tokens)
        return Node.MakeSubTree(temp2, Node.MakeSubTree(temp, None, None, None), None, parseExpr(tokens, output))
            

def parseIfStatement(tokens, output):
        #  p V q
        # -p ^ -q
    if Counter.next_token != None and Counter.next_token.value == "if":
        temp = Counter.next_token
        consumeToken(tokens)
        tree_1 = parseExpr(tokens, output)

        if Counter.next_token == None or Counter.next_token.value != "then": raiseError("EXPECTED 'then'", output)
        consumeToken(tokens)
        tree_2 = parseStatement(tokens, output)

        if Counter.next_token == None or Counter.next_token.value != "else": raiseError("EXPECTED 'else'", output)
        consumeToken(tokens)
        tree_3 = parseStatement(tokens, output)

        if Counter.next_token == None or Counter.next_token.value != "endif": raiseError("EXPECTED 'endif'", output)
        consumeToken(tokens)
        return Node.MakeSubTree(temp, tree_1, tree_2, tree_3)
    else:
        raiseError("EXPECTED KEYWORD")         

def parseWhileStatement(tokens, output):
    if Counter.next_token != None and Counter.next_token.value == "while":
        temp = Counter.next_token
        consumeToken(tokens)
        tree_1 = parseExpr(tokens, output)

        if Counter.next_token == None or Counter.next_token.value != "do": raiseError("EXPECTED 'do'", output)
        consumeToken(tokens)
        tree_2 = parseStatement(tokens, output)

        if Counter.next_token == None or Counter.next_token.value != "endwhile": raiseError("EXPECTED 'endwhile'", output)
        consumeToken(tokens)
        return Node.MakeSubTree(temp, tree_1, None, tree_2)
            
    else:
        raiseError("EXPECTED KEYWORD")

def parseExpr(tokens, output):
    tree = parseTerm(tokens, output)
    while Counter.next_token != None and Counter.next_token.value == '+':
        temp = Counter.next_token
        consumeToken(tokens)
        tree = Node.MakeSubTree(temp, tree, None, parseTerm(tokens, output))
    return tree


def parseTerm(tokens, output):
    tree = parseFactor(tokens, output)
    while Counter.next_token != None and Counter.next_token.value == '-':
        temp = Counter.next_token
        consumeToken(tokens)
        tree = Node.MakeSubTree(temp, tree, None, parseFactor(tokens, output)) 

    return tree


def parseFactor(tokens, output):
    tree = parsePiece(tokens, output)
    while Counter.next_token != None and Counter.next_token.value == '/':
        temp = Counter.next_token
        consumeToken(tokens)
        tree = Node.MakeSubTree(temp, tree, None, parsePiece(tokens, output))

    return tree


def parsePiece(tokens, output):
    tree = parseElement(tokens, output)
    while Counter.next_token != None and Counter.next_token.value == '*': 
        temp = Counter.next_token
        consumeToken(tokens)
        tree = Node.MakeSubTree(temp, tree, None, parseElement(tokens, output))

    return tree

def parseElement(tokens, output):
    if Counter.next_token != None and Counter.next_token.value == '(':
        consumeToken(tokens)
        tree = parseExpr(tokens, output) 
        if Counter.next_token != None and Counter.next_token.value == ')':
            consumeToken(tokens)
            return tree
        else:
            raiseError("MISSING ')'", output)

    elif Counter.next_token != None and Counter.next_token.type == Scanner.TokenType.NUMBER:
        temp = Counter.next_token
        consumeToken(tokens)
                
        return Node.MakeSubTree(temp, None, None, None)
    elif Counter.next_token != None and Counter.next_token.type == Scanner.TokenType.INDENTIFIER:
        temp = Counter.next_token
        consumeToken(tokens)
        return Node.MakeSubTree(temp, None, None, None)
    elif Counter.next_token == None:
        raiseError("MISSING NUM OR IDENTIFIER AT END",output)
    else:
        raiseError(f"EXPECTED NUM OR IDENTIFIER, NOT '{Counter.next_token.value}'", output)

def checkASTValidity(tokens, output):
    # if Counter.val+1 < len(tokens): raiseError("INCOMPLETED TREE DUE TO INCONSISTENT SYNTAX STRUCTURE", output)
    if Counter.next_token != None: raiseError("INCOMPLETED TREE DUE TO INCONSISTENT SYNTAX STRUCTURE", output)

            
def getAST(input, output):
    '''
    For external and importing use
    '''
    tokens = []
    for line in input:
        temp = Scanner.getTokens(line,output)
        if temp == []: continue
        tokens = tokens + temp
    
    output.write("Tokens:\n")
    if tokens == []: 
        output.write("No Tokens...\n\n")
        return None
    
    for token in tokens:
        output.write(f"{token.value} : {Scanner.TokenType.toString(token.type)}\n")
    output.write("\n")
    
    # initializes Counter's 'val' attribute to 0, and 'next_token' to None
    Counter()
    Counter.next_token = tokens[0]
    
    # root = parseExpr(tokens, output)
    root = parseStatement(tokens, output)
    checkASTValidity(tokens, output)
    return root

    