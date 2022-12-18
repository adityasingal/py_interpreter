from re import A

# the following function checks whether a is present in list L
def inlist(a,L):
    count=0
    for i in range(len(L)):
        if str(a)!=str(L[i]):
            count+=1
    if count==len(L):
        return False
    else:
        return True

# the following function checks whether a is present as first element of any tuple in list L
def exist(a,L):
    count=0
    for l in L:
        if (type(l) is tuple) and str(l[0])==str(a):
            return True
        else:
            count+=1
    if count==len(L):
        return False

# the following function finds tuples in list L and returns the index of the tuple with first value a
def ind(a,L):
    i=0
    while i<len(L):
        if type(L[i])==tuple and str(a)==str(L[i][0]):
            return i
        else:
            i+=1

#the following function returns the second value of the tuple.
def find(a,L):
    for l in L:
        if (type(l) is tuple):
            if l[0]==a:
                return L[l[1]]

# the following function returns the index of a in list L
def tellindex(a,L):
    found=False
    i=0
    while i<len(L) and found==False:
        if str(a)==str(L[i]):
            found=True
        else:
            i+=1
    return i

# this function returns the index of the list in instruction list with first element
# BLE OR BLT OR BE
def index1(L):
    for l in L:
        if type(l)==list:
            if l[0]=='BLE' or l[0]=='BLT' or l[0]=='BE':
                return L.index(l)

# this function returns the index of the list in instruction list with first element
# branch
def index2(L):
    for l in L:
        if type(l)==list:
            if l[0]=='branch':
                return L.index(l)

lines = [] # initalise to empty list
with open("C:/Users/adity/Desktop/IIT Delhi/1st Year/Sem 1/COL100/Learning Python/input_file.txt") as f:
    lines = f.readlines() # read all lines into a list of strings
L=[]
inst_list=[]
tabs_list=[]
for statement in lines: # each statement is on a separate line
    
    tabs = 0
    while statement[tabs] == '\t':
        tabs += 1
    tabs_list.append(tabs)
    token_list = statement.split() # split a statement into a list of tokens
    L.append(token_list)
n=len(L)
DATA=[]
for i in range(n):
    n1=len(L[i])

    if L[i][0]!='while':
        # the following function returns True if the input has syntax error and returns False if the
        # input doesn't have any syntax error
        def synerror():
            counter=0
            for z in range(n1):
                if len(L[i][z])>1 and not((L[i][z]).isdigit()) and not((L[i][z]).isalpha()) and L[i][z]!='==' and L[i][z]!='!='and L[i][z]!='<='and L[i][z]!='>='and L[i][z]=='while':
                    counter+=1
            if counter>0:
                return True
            else:
                return False

        count=0
        if synerror():                    # code for syntax error
            print('Syntax Error')
            count+=1

        if len(L[i])>2:                    # code for undefined variable error
            if (L[i][2]).isalpha():
                if not(exist(L[i][2],DATA)):
                    if len(L[i][2])==1:
                        print("Variable", L[i][2], "is not defined")
                        count+=1

        if len(L[i])>4:                    # code for undefined variable error
            if (L[i][4]).isalpha():
                if not(exist(L[i][4],DATA)):
                    if len(L[i][4])==1:
                        print("Variable", L[i][4], "is not defined")
                        count+=1

        if n1>1:                    # code for division by zero error
            if L[i][-2]=='/' and L[i][-1]=='0':
                print("Zero Division Error")
                count+=1

        if count==0:
            for j in range(n1):
                if (L[i][j]).isdigit():     # checks if the string at L[i][j] has only digits
                    if not(int(L[i][j]) in DATA):  # checks if L[i][j] is present in DATA list. If not,
                        DATA.append(int(L[i][j]))  # appends integer value of L[i][j] to DATA list
            
            for D in DATA:
                if type(D)==tuple:          # assigns variable to string
                    locals()[str(D[0])]=DATA[D[1]]
            
            value=(eval(lines[i][4:]))      # evaluates the expression in string and stores it in value
            
            if type(value)==float:          # checks if the number store in value is floating point or not
                value=int(value)            # converts floating point to intger value Eg 1.0 -> 1
            
            if not(inlist(value,DATA)):     # checks if the number stored in value is in DATA list. If not,
                DATA.append(value)          # appends number stored in value to DATA list
            
            if exist(L[i][0],DATA):         # checks if variable L[i][0] has any value assigned in DATA
                index=tellindex(value,DATA) # returns the index of the value assigned to the variable
                DATA[ind(L[i][0],DATA)]=(L[i][0],index) # changes element at ith index to (L[i][0],index)
            
            else:
                DATA.append((lines[i][:1],tellindex(value,DATA)))
            if tabs_list[i]<tabs_list[i-1] and i>0:
                inst_list.append(['branch',index1(inst_list)])
            inst_list.append(lines[i].strip('\n').strip('\t'))
        else:
            break      # this line is used to terminate the program if even one error is produced
    else:              # add code for while statements here
        if L[i][2]=='>':
            inst_list.append(['BLE',L[i][1],L[i][3][0]])
        elif L[i][2]=='<':
            inst_list.append(['BLE',L[i][3][0],L[i][1]])
        elif L[i][2]=='<=':
            inst_list.append(['BLT',L[i][3][0],L[i][1]])
        elif L[i][2]=='>=':
            inst_list.append(['BLT',L[i][1],L[i][3][0]])
        elif L[i][2]=='!=':
            inst_list.append(['BE',L[i][1],L[i][3][0]])
if len(inst_list[index1(inst_list)])<4:
    (inst_list[index1(inst_list)]).append(index2(inst_list)+1)

print(inst_list)

intDATA=[]
for d in DATA:
    if type(d)==int:                 # appending integer value in DATA to intDATA as we are only
        intDATA.append(d)            # interested in integer values in our garbage list
for d in DATA:                  # the following lines of code is used to print the garbage list.
    if type(d)==tuple:
        if inlist(DATA[d[1]],intDATA):
            intDATA.remove(DATA[d[1]])
GARBAGE=intDATA
#print('Garbage = ',GARBAGE)