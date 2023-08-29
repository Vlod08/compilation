# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 16:29:14 2023

@author: lvengad
"""


mots_cles = ['EOF','+','-','*','/','%','!','&','<',"<=",'>',">=","==","!=","&&","||",'(',')','[',']','{',
            '}',',',';','=',"int","for","while","do","if","else","break","continue","return"]



class token:
    def __init__(self,type_,valeur):
        self.type_ = type_
        self.valeur =valeur
    def __str__(self):
        if(self.valeur == None):
            return "type : "+self.type_
        else:
            return "type : "+self.type_+" ; valeur : "+self.valeur
        
    
    
        
class interface_lex_syn:
    def __init(self,actuel,last):
        self.actuel = actuel
        self.last = last
        
"################################################# Analyse lexicale ##################################################################"

file = open("C:/Users/lokes/OneDrive/Desktop/codesource.c","r")
line = file.readline()
tab_global = []
tokens_global =[]
while( not (line == "")):
    tab_temp = line.rsplit(' ')
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
            tokens_global.append(token("const",element))
        elif(element.isidentifier()):
            tokens_global.append(token("identificateur",element))
        elif(element== "\n"):
            continue
        else:
            print("Error")

#print(tab_global)

for t in tokens_global:
    print(t)
        

        
    
