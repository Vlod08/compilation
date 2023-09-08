# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 16:29:14 2023

@author: lvengad
"""
 

mots_cles = ['EOF','+','-','*','/','%','!','&','<',"<=",'>',">=","==","!=","&&","||",'(',')','[',']','{',
            '}',',',';','=','int',"for","while","do","if","else","break","continue","return"]




tab_global = []
tokens_global= []


class token:
    def __init__(self,type_,valeur,nb_ligne):
        self.type_ = type_
        self.valeur = valeur
        self.nb_line = None

    def __str__(self):
        if(self.valeur == None):
            return "type : "+self.type_
        else:
            return "type : "+self.type_+" ; valeur : "+str(self.valeur)
        
    

        
"################################################# Next ##############################################################################"

currentind = -1
current_token = token("","",None)
last_token = token("","",None)
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
        raise Exception("Error Fatal : trouve "+str(current_token.type_))
    

"################################################# Analyse lexicale ##################################################################"

"""

def init_analyse_lexicale(codesource):
    nb_ligne = 1
    file = open(codesource,"r")
    content = file.read()
    global tab_global 
    global tokens_global 
    #print("printing the contents of the file : \n" + content)
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
                tokens_global.append(token(mot_cle,None,nb_ligne))
                m = True
                break
        if(not m):
            if (element.isnumeric()):
                tokens_global.append(token('const',int(element),nb_ligne))
            elif(element.isidentifier()):
                tokens_global.append(token('identificateur',element,nb_ligne))
            elif(element == '\n'):
                nb_ligne = nb_ligne + 1
                continue
            else:
                raise Exception("Error : " + str(element))


    for t in tokens_global:
        print(t)


"""

import re

def init_analyse_lexicale(codesource):
    nb_ligne = 1
    file = open(codesource,"r")
    content = file.read()
    global tab_global 
    global tokens_global 
    #print("printing the contents of the file : \n" + content)
    content.strip(' ')
    
    #keyword_pattern = r"\b(?:if|else|while|for|const)\b"
    keyword_pattern = r"\b(?:EOF|\+|\-|\*|\/|%|!|&|<|<=|>|>=|==|!=|&&|\|\||\(|\)|\[|\]|\{|\}|,|;|=|int|for|while|do|if|else|break|continue|return)\b"

    identifier_pattern = r"\b[a-zA-Z_]\w*\b"
    numeric_pattern = r"\b\d+\b"
    newline_pattern = r"\n"
    whitespace_pattern = r"\s+"
    operator_pattern = r"[+\-*/=]"  
    
    combined_pattern = f"({keyword_pattern}|{identifier_pattern}|{numeric_pattern}|{newline_pattern}|{whitespace_pattern}|{operator_pattern})"
    
    tokens = re.findall(combined_pattern, content)
    
    for token_value in tokens:
        if re.match(keyword_pattern, token_value):
            tokens_global.append(token(token_value, None, nb_ligne))
        elif re.match(identifier_pattern, token_value):
            tokens_global.append(token('identificateur', token_value, nb_ligne))
        elif re.match(numeric_pattern, token_value):
            tokens_global.append(token('const', int(token_value), nb_ligne))
        elif re.match(newline_pattern, token_value):
            nb_ligne += 1
        elif re.match(whitespace_pattern, token_value):
            continue
        elif re.match(operator_pattern, token_value):
            tokens_global.append(token(token_value, None, nb_ligne))
        else:
            raise Exception("Error at line {}: Unknown token: {}".format(nb_ligne, token_value))

    for t in tokens_global:
        print(t)



"######################################################## Noeud ##############################################################"     


class Noeud:
    def __init__(self,type_ ,valeur, enfant,nb_ligne):
        self.type_ = type_
        self.valeur = valeur
        self.enfant = enfant
        self.symbole = None
        self.nb_ligne = nb_ligne
    

    
    def __str__(self):
        out = "parent : "+str(self.type_)
        for i in range (0,len(self.enfant)):
            out = out +' enfant'+str(i)+': ' + str(self.enfant[i].type_)
        return out
            
    
        
"######################################################## Noeud A ############################################################"  

    
def noeudA():
    global current_token
    global current_line
    global last_token
    if(check("const")):
        #print("found : "+str(current_token.valeur))
        return Noeud("const",last_token.valeur,[],last_token.nb_line)
    
    elif(check("identificateur")):
        return Noeud('ref', last_token.valeur,[],last_token.nb_line)
    
    elif(check('(')):
        N = noeudE(0)
        accept(')')
        return N
    
    elif(check('\n')):
            #print("entered here")
            current_line = current_line + 1
            return noeudA()
    
    elif(check('EOF')):
        return Noeud('EOF', None, [],last_token.nb_line)
    
    elif(current_token.type_ == ';'):
        return Noeud('vide', None, [], current_token.nb_line)
    
    else:
        raise Exception("atome inconnu : "+ str(current_token.type_))

 
"######################################################### Noeud P ####################################################################"

def noeudP():
    if(check('-')):
        N = noeudP()
        return Noeud('-u',None,[N],last_token.nb_line)
    elif(check('!')):
        N = noeudP()
        return Noeud('!',None,[N],last_token.nb_line)
    elif(check('+')):
        N = noeudP()
        #print("printing from nouedP"+ str(N))
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
    #print("printing N from nouedE: "+str(N))
    while(operateurs.get(current_token.type_) != None):
        
        op = operateurs.get(current_token.type_)
        temp_ligne = current_token.nb_line
        if(op[2] <= prio_min):
            break
        next()
        M = noeudE(op[2]-op[3])
        N = Noeud(op[0],op[1],[N,M],temp_ligne)
    return N

"######################################################### Gencode ####################################################################"

dict_gencode = {
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
    'EOF'   :'End of program !!!',
    'vide'  :'',
    'bloc'  :''
        }

def gencode(N):
 
    if(N.type_ == 'const'):
        print("push "+ str(N.valeur))
    
    elif(N.type_ == '-u'):
        print("push 0")
        print("push "+ str(N.enfant[0].valeur))
        print("sub")
    
    elif(N.type_ == 'decl'):
        "4 + 4"
        #print('')
    
    elif(N.type_ == 'seq' or N.type_ == 'decl'):
        "4 + 4"
        #print('')
    
    elif(N.type_ == 'ref'):
        if(N.symbole.type_ == 'var_loc'):
            print("get " + str(N.symbole.position))
        else:
            raise Exception("Error Fatal : in gencode 1 ")
        
    elif(N.type_ == '='):
        gencode(N.enfant[1])
        print("dup")
        if(N.enfant[0].type_ != 'ref'):
            raise Exception("Error Fatal : in gencode 3")
        elif(N.enfant[0].symbole.type_ == 'var_loc'):
            print("set " + str(N.enfant[0].symbole.position))
        else:
            raise Exception("Error Fatal : in gencode 4")
            
      
    else:
        for k in range(len(N.enfant)):
            #print("parent : "+ str(N.type_)) 
            gencode(N.enfant[k])
        if(dict_gencode[N.type_] != None):
            print(dict_gencode[N.type_])
        else:
            raise Exception("Error Fatal : in gencode 2 ")
            
"########################################################Noeud I ######################################################################"

def noeudI():

    if(check(";")):
        return Noeud('vide',None, [],last_token.nb_line)
    
    elif(check("{")):
        N = Noeud('bloc',None,[],last_token.nb_line)
        while(not check('}')):
            N.enfant.append(noeudI())
        return N
    
    elif(check('debug')):
        N = noeudE(0)
        accept(';')
        return Noeud('debug',None,[N],last_token.nb_line)
    
    elif(check('int')):
        N = Noeud('seq',None,[],last_token.nb_line)
        l = True
        while (l):
            accept('identificateur')
            N.enfant.append(Noeud('decl',last_token.valeur,[],last_token.nb_line))
            l = check(',')
        accept(';')
        return N
    
    else: 
        N = noeudE(0)
        if( N.type_ == 'EOF'):
            print("End of file reached")
            return Noeud('EOF',None,[N],current_token.nb_line)
        else:
            accept(';')
            return Noeud('drop',None,[N],last_token.nb_line)
        
"######################################################## Analyse syntaxique ##########################################################"

def analyse_syntaxique():
    return(noeudI())
    

"######################################################## Gestion variable ############################################################"

class S:
    def __init__(self, nom):
        self.nom = nom 
        self.type_ = None
        self.position = None
        
    
Vars = []
nbVar = 0

def declarer(nom):
    global Vars 
    for i in range (len(Vars) - 1, -1, -1):
        if(Vars[i].nom == nom):
            raise Exception("Declaration dupliquee de la variable : "+str(nom))
        elif(Vars[i].nom == "---"):
            break
    ns = S(nom)
    Vars.append(ns)
    #for i in range(len(Vars)):
    #   print(Vars[i].nom +" position : " + str(Vars[i].position))
    return Vars[len(Vars)-1]

def chercher(nom):
    global Vars
    #for i in range(len(Vars)):
    #   print(Vars[i].nom +" position : " + str(Vars[i].position))
    for i in range (len(Vars) -1, -1, -1):
        if(Vars[i].nom == nom):
            return Vars[i]
    raise Exception( "Variable non trouvee : " + str(nom) )


def begin():
    global Vars 
    Vars.append(S("---"))
    #for i in range(len(Vars)):
    #  print(Vars[i].nom +" position : " + str(Vars[i].position))

def end():
    global Vars
    while(Vars[(len(Vars) -1 )].nom != "---" and len(Vars)>0 ):
        Vars.pop()
    Vars.pop()
    #for i in range(len(Vars)):
    #  print(Vars[i].nom +" position : " + str(Vars[i].position))

"######################################################## Analyse Semantique #####################################################################"       
def AnaSem(N):
    global nbVar
    if(N.type_ == 'bloc'):
        begin()
        for i in N.enfant :
            AnaSem(i)
        end()
    elif(N.type_ == 'decl'):
        S = declarer(N.valeur)
        S.position = nbVar
        nbVar = nbVar + 1
        S.type_ = 'var_loc'
        N.symbole = S
    elif(N.type_ == 'ref'):
        S = chercher(N.valeur)
        N.symbole = S
    else:
        for i in N.enfant :
            AnaSem(i)
 

"######################################################### Optimisation Const ###############################################################"


def optimisation_const(N):
    
    if(len(N.enfant) == 0):
        return N
    
    else:
        G = optimisation_const(N.enfant[0]) 
        if( len(N.enfant) > 1 ):
            D = optimisation_const(N.enfant[1])
            if(G.type_ == 'const' and D.type_ == 'const'):
                exp = str(G.valeur) + str(N.type_) + str(D.valeur)
                return Noeud("const",eval(exp),[],None)
            else:
                N.enfant[1] = D
        elif(N.type_ == '+'):
            if(G.type_ == 'const'):
                exp = str(N.type_) + str(G.valeur)
                return Noeud("const",eval(exp),[],None)
        elif(N.type_ == '-u'):
            if(G.type_ == 'const'):
                return Noeud("const", -  int(G.valeur),[],None)        
        N.enfant[0] = G
        return N  


    
"################################################################### Main ##############################################################"       



init_analyse_lexicale("codesource.c")
next()
print("\n \n")
print("******************************************************** Generation du code ***************************************************")
print("\n \n")
while(current_token.type_ != 'EOF'):
    A = analyse_syntaxique()
    nbVar = 0
    AnaSem(A)
    print('resn '+ str(nbVar))
    optimisation_const(A)
    gencode(A)
    print('drop '+ str(nbVar))    
print("\n \n")
