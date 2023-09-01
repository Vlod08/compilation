# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 16:29:14 2023

@author: lvengad
"""


mots_cles = ['EOF','+','-','*','/','%','!','&','<',"<=",'>',">=","==","!=","&&","||",'(',')','[',']','{',
            '}',',',';','=','\n',"int","for","while","do","if","else","break","continue","return"]

tab_global = []
tokens_global= []


class token:
    def __init__(self,type_,valeur):
        self.type_ = type_
        self.valeur =valeur
    def __str__(self):
        if(self.valeur == None):
            return "type : "+self.type_
        else:
            return "type : "+self.type_+" ; valeur : "+str(self.valeur)
        
    
    
        
class interface_lex_syn:
    def __init(self,actuel,last):
        self.actuel = actuel
        self.last = last
        
"################################################# Next ##############################################################################"

currentind = -1
current_token = token("","")
last_token = token("","")
current_line = 0

def next():
    global currentind
    global tokens_global
    global current_token
    global last_token
    last_token.type_ = current_token.type_
    last_token.valeur = current_token.valeur
    currentind =  currentind + 1
    current_token.type_ = tokens_global[currentind].type_
    current_token.valeur = tokens_global[currentind].valeur

    
"################################################# Check ##############################################################################"

def check(T):
    global current_token
    global last_token
    if (current_token.type_ == T):
        next()
        return True
    else:
        return False
    
"################################################# Accept ############################################################################"

def accept(T):
    if(not check(T)):
        raise Exception("Error Fatal ! ")
    

"################################################# Analyse lexicale ##################################################################"
def init_analyse_lexicale(codesource):
    file = open(codesource,"r")
    content = file.read()
    global tab_global 
    global tokens_global 
    print("printing the contents of the file : \n" + content)
    content.strip(' ')
    lines = content.split('\n')
    for line in lines :
        elements = line.split(' ')
        for element in elements:
            if(element != ''):
                tab_global.append(element)
        tab_global.append('\n')

    tab_global.append('EOF')
    print("printing the elements in the tab : \n"+str(tab_global))
    
    for element in tab_global:
        m = False
        for mot_cle in mots_cles:
            if mot_cle == element :
                tokens_global.append(token(mot_cle,None))
                m = True
                break
        if(not m):
            if (element.isnumeric()):
                tokens_global.append(token('const',int(element)))
            elif(element.isidentifier()):
                tokens_global.append(token('identificateur',element))
            elif(element == '\n'):
                tokens_global.append(token('\n',None))
            else:
                raise Exception("Error :  " + str(element))


    for t in tokens_global:
        print(t)

"######################################################## Noeud ##############################################################"     


class Noeud:
    def __init__(self,type_ ,valeur, enfant):
        self.type_ = type_
        self.valeur = valeur
        self.enfant = enfant
    

    
    def __str__(self):
        out = "parent : "+str(self.type_)
        for i in range (0,len(self.enfant)):
            out = out +' enfant'+str(i)+': ' + str(self.enfant[i].type_)
        return out
            
        
            
    
        
"######################################################## Noeud A ############################################################"  

    
def noeudA():
    global current_token
    global current_line
    if(check("const")):
        return Noeud("const",last_token.valeur,[])
    elif(check("identificateur")):
        print("error")
    elif(check('(')):
        N = noeudE(0)
        accept(')')
        return N
    elif(check('\n')):
            print("entered here")
            current_line = current_line + 1
            return noeudA()
    else:
        print("error")

 
"######################################################### Noeud P ####################################################################"

def noeudP():
    if(check('-')):
        N = noeudP()
        return Noeud('-u',None,[N])
    elif(check('!')):
        N = noeudP()
        return Noeud('!',None,N)
    elif(check('+')):
        N = noeudP()
        print("printing from nouedP"+ str(N))
        return N
    else:
        N = noeudA()
        return N




"######################################################### Noeud E ####################################################################"
operateurs = {
    '=' : ['='  ,None ,1 ,1], 
    '||': ['||' ,None ,2 ,0],
    '&&': ['&&' ,None ,3 ,0],
    '==': ['==' ,None ,4 ,0],
    '!=': ['!=' ,None ,4 ,0],
    '<' : ['<'  ,None ,5 ,0],
    '<=': ['<=' ,None ,5 ,0],
    '>' : ['>'  ,None ,5 ,0],
    '>=': ['>=' ,None ,5 ,0],
    '+' : ['+'  ,None ,6 ,0],
    '-' : ['-'  ,None ,6 ,0],
    '*' : ['*'  ,None ,7 ,0],
    '/' : ['/'  ,None ,7 ,0],
    '%' : ['%'  ,None ,7 ,0],
}

def noeudE(prio_min):
    global current_token
    global current_line
    if(current_token.type_ == 'EOF'):
        print("end of file found")
        return None
    
    
    
    N = noeudP()
    while(operateurs.get(current_token.type_) != None):
        
        op = operateurs.get(current_token.type_)
        if(op[2] <= prio_min):
            break
        next()
        M = noeudE(op[2]-op[3])
        N = Noeud(op[0],op[1],[N,M])
    return N

"######################################################### Gencode ####################################################################"

dict_gencode = {
    '='     :'',
    '||'    :'or',
    '&&'    :'and',
    '=='    :'cmpeq',
    '!='    :'cmpne',
    '<'     :'cmplt',
    '<='    :'cmple',
    '>'     :'cmpgt',
    '>='    :'cmpge',
    '+'     :'add',
    '-'     :'sub',
    '*'     :'mul',
    '/'     :'div',
    '%'     :'mod',
    '!'     :'not'
        }

def gencode(N):
 
    if(N.type_ == 'const'):
        print("push "+ str(N.valeur))
    elif(N.type_ == '-u'):
        print("push 0")
        print("push "+ str(N.enfant[0].valeur))
        print("sub")
      
    else:
        for k in range(len(N.enfant)):
            gencode(N.enfant[k])
        if(dict_gencode[N.type_] != None):
            print(dict_gencode[N.type_])
        else:
            raise Exception("Error Fatal")


    
"######################################################## Main ########################################################################"       



init_analyse_lexicale("codesource.c")
next()
print("********************* Generation du code ***************************")
while(current_token.type_ != 'EOF'):
    print("\n")
    A = noeudE(0)
    #print(A)
    gencode(A)
    next()


        
