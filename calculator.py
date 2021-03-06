"""

Infix Expression Evaluator

Comments, Schueller:  Tue Feb 17 20:53:17 PST 2015
    1)  Stack-based implementation:				1/1
    2)  Ignores extra spaces:					0.75/1
        - 2 + 3 fails
    3)  Catches syntax errors:					0.5/1
        - doesn't really
    4)  Implements unary negation:				0.75/1
        - trouble with -(2+3)
    5)  Uses prec table:					1/1
    6)  Evaluates infix expressions correctly:			0.75/1
        - problem with 8.0/(4-(3-7))
    7)  Loops for multiple expressions/doesn't crash:		1/1
    8)  Efficient/well-organized:				0.75/1
        - use named constants throughout
    9)  Above and beyond:					1/1


        GRADE:  7.5/9

Comments and modifications made by me in the body of the program are marked
by a // SCHUELAW.  You are encouraged to search through your graded program
for the "SCHUELAW" string for those comments/changes.

Other Comments:

"""
"""
@timmorris
This class contains the functions that format a user input into a list of tokens. The tokens are then interpreted
based on operator precedence and loaded into stacks representing the post fix form of the expression.
 A seperate function uses the organized postfix for to compute the answer from the expression. There is a
 while loop running to allow for continuous user input
A&B: I added an EXP operation! You can assign an exponent by using the '^' symbol rather than the '**' command
"""
#import Stack
class Stack:
     def __init__(self,L=[]):
         self.items = L

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)

     def clear(self):
         self.items = []

#operator codes, DLR is lowest precedence
ERR=-1; ADD=0; SUB=1; MLT=2; DIV=3; UNM=4; LPN=5; RPN=6; DLR=7; EXP=8; SIN=9;

#Token type codes
NUM = 0; OP = 1;

#Op dictionary
op_dict = {
    '+':ADD,
    '-':SUB,
    '*':MLT,
    '/':DIV,
    '(':LPN,
    ')':RPN,
    '^':EXP,
    'sin':SIN
}

#Global precedence const array
prec = [
  # ADD SUB MLT DIV UNM LPN RPN DLR EXP SIN #
   [0,   0,  0,  0,  0,  1,  0,  1,  0,  0],   #ADD#
   [0,   0,  0,  0,  0,  1,  0,  1,  0,  0],   #SUB#
   [1,   1,  0,  0,  0,  1,  0,  1,  0,  0],   #MLT#
   [1,   1,  0,  0,  0,  1,  0,  1,  0,  0],   #DIV#
   [1,   1,  1,  1,  1,  1,  0,  1,  1,  1],   #UNM#
   [1,   1,  1,  1,  1,  1,  0,  1,  1,  1],   #LPN#
   [0,   0,  0,  0,  0,  0,  0,  1,  0,  0],   #RPN#
   [0,   0,  0,  0,  0,  0,  0,  0,  0,  0],   #DLR#
   [1,   1,  1,  1,  0,  1,  0,  1,  1,  1],   #EXP#
   [1,   1,  1,  1,  0,  1,  0,  1,  1,  1],   #SIN#
]

#print op_dict[]
postStack = Stack([])
opStack = Stack([])

stringProcess = []
inputexp = str(raw_input("Please input your expression:"))

def process():
    global ADD, SUB, MLT, DIV, UNM, LPN, RPN, DLR, EXP, SIN, OP, NUM, ERR, op_dict
    global inputexp
    global stringProcess
    stringProcess = []
    start = 0
    while start< len(inputexp):
        numString=""
        if (inputexp[start] in '0123456789.-') == True:  #error check: if there is a "-" w/ no nums
            if inputexp[start] == '-' and len(inputexp)==1:
                print("error: no nums")
                break
            elif inputexp[start] == '-' and start == 0:
                numString+=inputexp[start]
                start+=1
            elif inputexp[start] == '-':
                if (inputexp[start-1] in '([*/+exp$)]') == True:
                    numString+=inputexp[start]
                    start+=1
                elif inputexp[start-1] == ' ': #checks to see if the the negative sign has a space above it that should be ignored
                    if (inputexp[start-2] in '([*/+^$)]') == True: #if the next previous is an operation
                        numString+=inputexp[start]                 #then the "-" should be treated as part of the num
                        start+=1
                    else:
                        stringProcess.append([op_dict['-'],OP])                #otherwise the "-" must indicate subtraction
                        start+=1
            #this next section operates under the assumption that there is no "-" involved for the rest of the float
            while start < len(inputexp):
                 if (inputexp[start] in '0123456789.') == True:
                    numString+=inputexp[start]
                    start+=1
                    if start==len(inputexp):
                        break
                 elif (inputexp[start] in '0123456789.') != True:
                    break
            stringProcess.append([float(numString),NUM])

        if start==len(inputexp): #ends the loop if the last digit of the string has been added to the token
            break
        #operation errors:
        if (inputexp[start] in '0123456789.)([]') != True and len(inputexp)-1==start: #checks if and operation is the last entry
            print("Error: No numbers to operate on.")
            break
        elif (inputexp[start] in '0123456789.[]()') != True and (inputexp[start+1] in '0123456789.()[]') != True:
            print("Error: Too many operations.")
            break

        elif (inputexp[start] in '0123456789.') != True:
            if inputexp[start] == "(":
                stringProcess.append([op_dict['('],OP])
            elif inputexp[start] == ")":
                stringProcess.append([op_dict[')'],OP])
            elif inputexp[start] == "+":
                stringProcess.append([op_dict['+'],OP])
            elif inputexp[start] == "-":
                stringProcess.append([op_dict['-'],OP])
            elif inputexp[start] == "*":
                stringProcess.append([op_dict['*'],OP])
            elif inputexp[start] == "/":
                stringProcess.append([op_dict['/'],OP])
            elif inputexp[start] == "^":
                stringProcess.append([op_dict['^'],OP])
            elif inputexp[start] == "sin":
                stringProcess.append([op_dict['sin'],OP])
            #elif inputexp[start] == "$":
                #stringProcess.append([OP,8])
            start+=1
    return stringProcess

#takes the tokens and then orders them appropriately in a postfix stack according to operator precedence
def operateStacks(tokens):
    index = 0
    while index<len(tokens) or opStack.isEmpty() != True:
        if index<len(tokens):
            if tokens[index][1] == 0:
                postStack.push(tokens[index])
                index+=1
            elif tokens[index][1] == 1:
                if opStack.size() == 0:
                    opStack.push(tokens[index])
                    index+=1
                elif prec[tokens[index][0]][opStack.peek()[0]] == 1:
                        opStack.push(tokens[index])
                        index+=1
                elif prec[tokens[index][0]][opStack.peek()[0]] == 0:
                    while prec[tokens[index][0]][opStack.peek()[0]] == 0:
                        operator = opStack.pop()
                        postStack.push(operator)
                        if opStack.isEmpty()==True:
                            break
                    opStack.push(tokens[index])
                    index+=1
        else:
            while opStack.isEmpty() != True:
                operator = opStack.pop()
                postStack.push(operator)
    return postStack
#uses the postFix stack to then operate on the expression as appropriate. Doesnt worry about precedence
#because that has already been established
def calculate(postFix):
    numStack = Stack([])
    reversePost = Stack([])
    answer = 0
    start = 0
    numLeft = 0
    numRight = 0
    opNum=0
    while postFix.isEmpty() != True:
        element = postFix.pop()
        reversePost.push(element)

    while reversePost.isEmpty() != True:
        if reversePost.peek()[1] == 0:
            temp = reversePost.pop()
            numStack.push(temp[0])
        elif reversePost.peek()[1] == 1:
            start+=1
            opNum+=1
            tokenOperator = reversePost.pop()

            if start == 1:
                a=numStack.pop()
                b=numStack.pop()
                if tokenOperator[0] == 0:
                    answer = b+a
                elif tokenOperator[0] == 1:
                    answer = b-a
                elif tokenOperator[0] == 2:
                    answer = b*a
                elif tokenOperator[0] == 3:
                    answer = b/a
                elif tokenOperator[0] == 4:
                    operator = 'unm'
                elif tokenOperator[0] == 5:
                    numLeft+=1
                elif tokenOperator[0] == 6:
                    numRight+=1
                elif tokenOperator[0] == 7:
                    operator = '$'
                elif tokenOperator[0] == 8:
                    answer = b**a
                elif tokenOperator[0] == 9:
                    operator = 'sin'
            else:
                if tokenOperator[0] == 0:
                    answer = answer+numStack.pop()
                elif tokenOperator[0] == 1:
                    answer = answer-numStack.pop()
                elif tokenOperator[0] == 2:
                    answer = answer*numStack.pop()
                elif tokenOperator[0] == 3:
                    answer = answer/numStack.pop()
                elif tokenOperator[0] == 4:
                    operator = 'unm'
                elif tokenOperator[0] == 5:
                    numLeft+=1
                elif tokenOperator[0] == 6:
                    numRight+=1
                elif tokenOperator[0] == 7:
                    operator = '$'
                elif tokenOperator[0] == 8:
                    answer = answer**numStack.pop()
                elif tokenOperator[0] == 9:
                    operator = 'sin'
    if opNum == 0:     #if there are no operators
        return "Error: No operators."
    elif numRight>numLeft:     #if there are too many right paren
        return "Error: Too many right parenthesis. Try again."
    elif numRight<numLeft:     #if there are too many left paren
        return "Error: Too many left parenthesis. Try again."
    elif numRight == numLeft:
        print ("Answer:")
        return  answer

while inputexp != "":
    print calculate(operateStacks(process()))
    print("")
    inputexp = str(raw_input("Please input your expression:"))
