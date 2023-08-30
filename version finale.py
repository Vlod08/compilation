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

def next():
    global currentind
    global tokens_global
    global current_token
    global last_token
    last_token.type_ = current_token.type_
    last_token.valeur = current_token.valeur
    currentind =  currentind + 1
    current_token.type_ = tokens_global[ currentind].type_
    current_token.valeur = tokens_global[ currentind].valeur

    
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
    line = file.readline()
    global tab_global 
    global tokens_global 
    while( not (line == "")):
        line= line.strip('\n')
        line= line.strip(' ')
        tab_temp = line.rsplit(' ')
        if(line != ''):
            for element in tab_temp:
                tab_global.append(element)
        line = file.readline()

    for element in tab_global:
        m = False
        for mot_cle in mots_cles:
            if mot_cle == element :
                tokens_global.append(token(mot_cle,None))
                #print("found the token : "+ mot_cle)
                m = True
                break
        if(not m):
            if (element.isnumeric()):
                tokens_global.append(token("const",int(element)))
            elif(element.isidentifier()):
                tokens_global.append(token("identificateur",element))
            elif(element== "\n"):
                continue
            else:
                print("Error")

    print(tab_global)

    for t in tokens_global:
        print(t)
 
"######################################################### Noeud P ####################################################################"

def noeudP():
    if(check('-')):
        N = noeudP()
        return Noeud('-',N)
    elif(check('!')):
        N = noeudP()
        return Noeud('!',N)
    elif(check('+')):
        N = noeudP()
        return N
    else:
        N = noeudA()
        return N

"######################################################### Noeud E ####################################################################"

def noeudE():
    return noeudP()
    
    
"######################################################## Main ########################################################################"       



init_analyse_lexicale("codesource.c")
next()
print(current_token.type_)
print(current_token.valeur)

print(last_token.type_)
print(last_token.valeur)

next()
print(current_token.type_)
print(current_token.valeur)

print(last_token.type_)
print(last_token.valeur)


        

######################################################## Analyse Sntaxique ########################################################################       

class Noeud:
    def __init__(self,type_,valeur,enfant):
        self.type_ = type_
        self.valeur =valeur
        self.enfant=enfant

    
def noeudA():
    if(check("const")):
        return Noeud("const",last_token.valeur)
    elif(check("identificateur")):
        print("error")
    elif(check('(')):
        N = noeudE()
        accept(')')
        return N
    else:
        print("error")


