# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 11:46:41 2023

@author: yrhourr
"""
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
        raise Exception("Error Fatal : trouve "+str(current_token.type_)+" ; in line "+current_token.nb_line)
    

"################################################# Analyse lexicale ##################################################################"
def isoperator(char):
    operators = "+-*!,/%=<>&|;[]()\{\}"
    return char in operators
nb_ligne = 1

def tokenizer(str):
    word = ""
    global tab_global 
    global tokens_global 
    global nb_ligne
    if(str[0] == " " or str[0]=="\t"):
        return str[1:]
    elif(str[0] == "\n"):
        nb_ligne = nb_ligne + 1
        return str[1:]
    elif(str == 'EOF'):
        tokens_global.append(token('EOF',None,nb_ligne))
    
    elif(str[0].isnumeric()):
        for i in str:
            if(i.isnumeric()):
                word += i
                str = str.replace(i, "", 1)
            else: break
        #print("CONSTANTE :" + str)
        tokens_global.append(token('const',int(word),nb_ligne))
        return str


    elif(str[0].isidentifier()):
        for i in str: 
            if(i.isidentifier()):
                word += i
                str = str.replace(i, "", 1)
            else: break
        tab_global.append(word)
        if(word in mots_cles):
            tokens_global.append(token(word,None,nb_ligne))
        else: 
            tokens_global.append(token("identificateur",word,nb_ligne))
        #print("IDENTIFIER :" + str)
        return str

    elif(isoperator(str[0])): 
        word = str[0]
        if(len(str)>1):
            if (isoperator(str[1])):
                 
                if( str[0:2] in mots_cles):
                    word = str[0:2]
                    str = str.replace(word, "", 1)
                    tokens_global.append(token(word,None,nb_ligne))
                    #print("OPERATOR :" + str)
                    return str
        
        if(str[0] in mots_cles):
            str = str.replace(str[0], "", 1)
            tokens_global.append(token(word,None,nb_ligne))
            #print("OPERATOR :" + str)
            return str
        
        else:
            raise Exception("Error in analyse lexicale with : " + str[0])
    
    else:
        raise Exception("Error in analyse lexicale with : " + str[0])
    
            
    

def init_analyse_lexicale(codesource):
    nb_ligne = 1
    file = open(codesource,"r")
    content = file.read()
    
    #print("printing the contents of the file : \n" + content)
    content.strip(' ')
    lines = content.split('\n') 
    for line in lines :
        while(line != None and len(line)!= 0):
            line = tokenizer(line)
        nb_ligne +=1

    tokens_global.append(token('EOF',None,nb_ligne))

    
    #for t in tokens_global:
    #    print(t)

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

"######################################################### Noeud S ####################################################################"
        
def noeudS():
    N = noeudA()
    if(check('(')):
        N = Noeud('appel',N.valeur,[N],last_token.nb_line)
        while(not check(')')):
            N.enfant.append(noeudE(0))
            if(check(')')):
                break
            else:
                accept(',')
    
    elif(check('[')):
        e = noeudE(0)
        accept(']')
        N = Noeud('indir',None,[e],last_token.nb_line)

    return N

 
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
    elif(check('*')):
        N = noeudP()
        return Noeud('indir',None,[N],last_token.nb_line)
    elif(check('&')):
        N = noeudP()
        return Noeud('addr',None,[N],last_token.nb_line)

    else:
        N = noeudS()
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
        return Noeud('EOF',None,[],current_token.nb_line)
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
    'bloc'  :'',
    'debug' :'dbg',
    'return':'ret'
        }
nb_label = 0
lbl_continue  = 0 
lbl_break = 0



def gencode(N):
    global nb_label
    global lbl_continue
    global lbl_break
  
    
    if(N.type_ == 'const'):
        print("push "+ str(N.valeur))
    
    elif(N.type_ == '-u'):
        print("push 0")
        print("push "+ str(N.enfant[0].valeur))
        print("sub")
    
    elif(N.type_ == 'decl'):
        "4 + 4"
        #print('')
    
    elif(N.type_ == 'seq'):
        for enf in N.enfant :
            gencode(enf)
        
    
    elif (N.type_ == 'decl'):
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
        if(N.enfant[0].type_ == 'indir'):
            gencode(N.enfant[0].enfant[0])
            print("write")
        elif(N.enfant[0].type_ != 'ref'):
            raise Exception("Error Fatal : in gencode 3")
        elif(N.enfant[0].symbole.type_ == 'var_loc'):
            print("set " + str(N.enfant[0].symbole.position))
        
        else:
            raise Exception("Error Fatal : in gencode 4")
    elif(N.type_ == 'target'):
        print(".l"+str(lbl_continue))
    
    elif(N.type_ == 'break'):
        print("jump l"+str(lbl_break))
        
        
    elif(N.type_ == 'continue'):
        print("jump l"+str(lbl_continue))
    
    elif (N.type_ == 'cond'):
        if(len(N.enfant) == 2):
            
            l1 = nb_label
            nb_label += 1
            gencode(N.enfant[0]) #condition a verifier
            print("jumpf l"+str(l1))
            gencode(N.enfant[1]) #instructions if 
            print(".l"+str(l1))
        else:
            
            l1 = nb_label
            nb_label += 1
            l2 = nb_label
            nb_label += 1
            gencode(N.enfant[0])        # condition a verifier
            print("jumpf l"+str(l1))   # pointeur label else
            gencode(N.enfant[1])        # instructions if
            print("jump l"+str(l2))    # pointeur label fin instructions else
            print(".l"+str(l1))         # label else
            gencode(N.enfant[2])        # instructions else
            print(".l"+str(l2))         # label fin else

    elif(N.type_ == 'loop'):
       
        lbl_debut = nb_label
        nb_label += 1
        
        save_lbl_continue = nb_label
        nb_label += 1
        lbl_continue = save_lbl_continue
        save_lbl_break = nb_label
        nb_label += 1
        lbl_break = save_lbl_break
        
        print(".l"+str(lbl_debut))
        for enf in N.enfant:
            gencode(enf)
        lbl_continue = save_lbl_continue
        lbl_break = save_lbl_break
        print("jump l"+str(lbl_debut))
        print(".l"+str(lbl_break))
    

    elif(N.type_ == 'appel'):
        if(N.enfant[0].type_ != 'ref' ):
            raise Exception("Undefined function : " + N.valeur )
        elif(N.enfant[0].symbole.type_ != 'fonc'):
            raise Exception(" Not a function : " + N.valeur )
        print( "prep " + str(N.valeur) )
        for i in range(1, len(N.enfant)):
            gencode(N.enfant[i])
        #N = N.enfant[0]
        print("call " + str(len(N.enfant)-1))
    
    elif(N.type_ == 'fonc'):
        print('.'+str(N.valeur))
        print("resn "+str(N.symbole.nbVar))
        gencode(N.enfant[ (len(N.enfant)-1) ] ) 
        print("push 0")
        print("ret")
    
    
    elif(N.type_ == 'indir'):
        gencode(N.enfant[0])
        print("read")
    
    elif(N.type_ == 'addr'):
        if(N.enfant[0].type_ != 'ref' and N.enfant[0].symbole.type_ != 'Var_loc' ):
            raise Exception ("Error Fatal : in gencode  56 " )
        else:
            print("prep start")
            print("swap")
            print("drop 1")
            print("push " + str(N.enfant[0].symbole.position + 1))
            print("sub")
            
    
    
                 
      
    else:
        for k in range(len(N.enfant)):
            #print("parent : "+ str(N.type_)) 
            gencode(N.enfant[k])
        if(dict_gencode[N.type_] != None):
            print(dict_gencode[N.type_])
        else:
            raise Exception("Error Fatal : in gencode 2 ")
            
"######################################################## Noeud I ######################################################################"

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
    elif(check('if')):
        accept('(')
        e = noeudE(0)
        accept (')')
        i1 = noeudI()
        i2 = None
        if(check('else')):
            i2 = noeudI()
        N = Noeud('cond',None,[e,i1],last_token.nb_line)
        if(i2 != None):
            N.enfant.append(i2)
        return N
    elif(check('while')):
        accept('(')
        e = noeudE(0)
        accept (')')
        i = noeudI()
        l = Noeud('loop',None,[],current_token.nb_line)
        t = Noeud('target',None,[],current_token.nb_line)
        c = Noeud('cond',None,[],current_token.nb_line)
        b = Noeud('break',None,[],current_token.nb_line)
        c.enfant = [e,i,b]
        l.enfant = [t, c]
        return l
    elif(check('break')):
        accept(';')
        return Noeud('break',None,[],last_token.nb_line)
    elif(check('continue')):
        accept(';')
        return Noeud('continue',None,[],last_token.nb_line)
    elif(check('for')):
        #print("enter here 45454545454545454")
        accept('(')
        e1 = noeudE(0)
        accept(';')
        e2 = noeudE(0)
        accept(';')
        e3 = noeudE(0)
        accept (')')
        l = Noeud('loop',None,[],last_token.nb_line)
        t = Noeud('target',None,[],last_token.nb_line)
        c = Noeud('cond',None,[],last_token.nb_line)
        b = Noeud('break',None,[],last_token.nb_line)
        d1 = Noeud('drop',None,[],last_token.nb_line)
        d2 = Noeud('drop',None,[],last_token.nb_line)        
        s1 = Noeud('seq',None,[],last_token.nb_line)
        s2 = Noeud('seq',None,[],last_token.nb_line)
        i = noeudI()
        d2.enfant.append(e3)
        s2.enfant = [i,t,d2]
        c.enfant = [e2,s2,b]
        d1.enfant.append(e1)
        l.enfant.append(c)
        s1.enfant = [d1,l]
        return s1  
    
    elif(check('return')):
        N = noeudE(0)
        accept(';')
        return Noeud('return',None,[N],last_token.nb_line)               
    
    else:
        N = noeudE(0)
        if( N.type_ == 'EOF'):
            print("End of file reached")
            return Noeud('EOF',None,[N],current_token.nb_line)
        else:
            accept(';')
            return Noeud('drop',None,[N],last_token.nb_line)


"######################################################## Noeud F ######################################################################"

def noeudF():
    global current_token
    global last_token
    accept('int')
    accept('identificateur')
    N = Noeud('fonc',str(last_token.valeur),[], last_token.nb_line)
    accept('(')
    
    while(check('int')):
        accept('identificateur')
        N.enfant.append(Noeud('decl',last_token.valeur,[], last_token.nb_line))
        if(check(',')):
            continue
        else:
            break
    accept(')')
    i = noeudI()
    N.enfant.append(i)
    return N
    

"######################################################## Analyse syntaxique ##########################################################"

def analyse_syntaxique():
    return(noeudF())
    

"######################################################## Gestion variable ############################################################"

class S:
    def __init__(self, nom):
        self.nom = nom 
        self.type_ = None
        self.position = None
        self.nbVar = 0
        
    
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
    #print("printing the last element : "+str(N.type_))
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
    elif(N.type_ == 'fonc'):
        nbVar = 0
        S = declarer(N.valeur)
        begin()
        for e in N.enfant :
            AnaSem(e)
        end()
        
        S.type_ = 'fonc'
        S.nbVar = nbVar #- (len(N.enfant) - 1)
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


def compile_fichier(filename):
    init_analyse_lexicale(filename)
    next()
    #print("\n \n")
    #print("******************************************************** Generation du code ***************************************************")
    #print("\n \n")
    
    
    while(current_token.type_ != 'EOF'):
        A = analyse_syntaxique()
        nbVar = 0
        AnaSem(A)
    #print('resn '+ str(nbVar))
        optimisation_const(A)
        gencode(A)
    #print('drop '+ str(nbVar))   
    
#print("\n \n")
    
def compile():

    lib_filename=input("Enter the name of the library file with the full path : ")
    lib_filename = lib_filename.replace('\\','\\\\',len(lib_filename))
    
    code_filename=input("Enter the name of the code file with the full path   : ")
    code_filename = code_filename.replace('\\','\\\\',len(code_filename))
    
    print("******************************************** DEBUT DE COMPILATION *********************************************")
    print("\n \n")

    compile_fichier(lib_filename)
    compile_fichier(code_filename)

    print(".start")
    print("prep main")
    print("call 0")
    print("dbg")
    print("halt")
    print("\n \n")
    print("********************************************* FIN DE COMPILATION **********************************************")

compile()
    
    
