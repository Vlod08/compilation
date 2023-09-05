# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 16:29:14 2023

@author: lvengad
"""


mots_cles = ['EOF','+','-','*','/','%','!','&','<',"<=",'>',">=","==","!=","&&","||",'(',')','[',']','{',
            '}',',',';','=',"int","for","while","do","if","else","break","continue","return"]

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
    if(currentind < len(tokens_global) - 1):
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
                continue
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
        print("found : "+str(current_token.valeur))
        return Noeud("const",last_token.valeur,[])
    elif(check("identificateur")):
        print("error")
    elif(check('(')):
        N = noeudE(0)
        accept(')')
        return N
    elif(check('\n')):
            #print("entered here")
            current_line = current_line + 1
            return noeudA()
    elif(check('EOF')):
        return Noeud('EOF', None, [])
    elif(current_token.type_ == ';'):
        return Noeud('vide', None, [])
    else:
        raise Exception("atome inconnu : "+ str(current_token.type_))

 
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
    print("printing N from nouedE: "+str(N))
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
    '!'     :'not',
    'drop'  :'drop 1',
    'EOF'   :'End of program !!'
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
            print("parent : "+ str(N.type_)) 
            gencode(N.enfant[k])
        if(dict_gencode[N.type_] != None):
            print(dict_gencode[N.type_])
        else:
            raise Exception("Error Fatal")
            
"########################################################Noeud I ######################################################################"

def noeudI():

    if(check(";")):
        return Noeud('vide',None, [])
    elif(check("{")):
        N = Noeud('bloc',None,[])
        while(not check('}')):
            N.enfant.append(noeudI())
        return N
    elif(check('debug')):
        N = noeudE(0)
        accept(';')
        return Noeud('debug',None,[N])
    else: 
        N = noeudE(0)
        if(not check('EOF')):
            print("End of file reached")
        return Noeud('EOF',None,[N])
        
"######################################################## Analyse syntaxique ##########################################################"

def analyse_syntaxique():
    return(noeudI())
    

"######################################################## Gestion variable ############################################################"

class S:
    def __init__(self,nom):
        self.nom = nom 
        
    
Vars = []

def declarer(nom):
    global Vars 
    for i in range (len(Vars) - 1, -1, -1):
        if(Vars[i].nom == nom):
            raise Exception("Declaration dupliquee de la variable : "+str(nom))
        elif(Vars[i].nom == ""):
            break
    ns = S(nom)
    Vars.append(ns)
    return Vars[len(Vars)-1]

def chercher(nom):
    global Vars
    for i in range (len(Vars) -1, -1, -1):
        if(Vars[i].nom == nom):
            return Vars[i]
    raise Exception("Variable non trouvee : "+str(nom))


def begin():
    global Vars 
    Vars.append(S(""))

def end():
    global Vars
    while(Vars[(len(Vars) -1 )].nom !="" ):
        Vars.pop()
    Vars.pop()





"#########################################################Optimisation Const##############################################################"


def optimisation_const(N):
    
    if(len(N.enfant) == 0):
        return N
    else:
        G = optimisation_const(N.enfant[0]) 
        if(len(N.enfant) >1):
            D = optimisation_const(N.enfant[1])
            if(G.type_ == 'const' and D.type_ == 'const'):
                exp = str(G.type_) + str(N.type_) + str(D.type_)
                return Noeud("const",eval(exp),[])
            else:
                N.enfant[1] = D
                
        N.enfant[0] = G
        return N  


    
"######################################################## Main ########################################################################"       



init_analyse_lexicale("C:/Users/lokes/OneDrive/Desktop/code.c")
next()
print("********************* Generation du code ***************************")
while(current_token.type_ != 'EOF'):
    print("\n")
    A = analyse_syntaxique()
    print("************************************************************************************************************")
    #print(A)
    gencode(A)
    
