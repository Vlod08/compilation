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
        
    
    
        
class interface_lex_syn:
    def __init(self,actuel,last):
        self.actuel = actuel
        self.last = last
        
'#################################################Analyse lexicale##################################################################' 

file = open("codesource.c")
line = file.readline()
tab_global = []
tokens_global =[]
while( not (line == "")):
    tab_temp = line.rsplit(' ')
    for element in tab_temp:
        tab_global.append(element)
    line = file.readline();

for element in tab_global:
    for mot_cle in mots_cles:
        if mot_cle == element :
            tokens_global.append()
            
    

print(tab_global)
    
        

        
    
