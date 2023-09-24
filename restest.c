/* TEST DU FOR FONCTION AVEC VARIABLES ET CONDITOINNELLES*/
int f() {
    int i;
    int res;
    for (i = 0; i <10; i = i+1) {
        if (i <10) {
            res = res + i;
        }
    }
    return res;
}

int main() {
    int res;
    res = f();
    return res;
}
/****************************************************************************************/
/*TEST WHILE FONCTION AVEC VARIABLES ET CONDITIONNELES*/
int f() {
    int i;
    i = 0;
    int res;
    while (i < 10) {
        if (i < 10) {
            res = res + i;
        }
        i = i + 1;
    }
    return res;
}

int main() {
    int val;
    val = f();
    return val;
}
/*****************************************************/
/*test fonction avec parmetres boucle conditonnel*/
int f(int n) {
    int i;
    int res;
    while (i < n) {
        if (i < n) {
            res = res + i;
        }
        i = i + 1;
    }
    return res;
}

int main() {
    int val;
    val = f(10);
    return val;
}
/*test fonction recursive*/
int somme(int n) {
    if (n <= 0) {
        return 0;
    } else {
        return n + somme(n - 1);  
    }
}

int main() {
    int n ;
    n = 5;
    int resultat ;
    resultat = somme(n);
    return resultat;
}

/*test tableau*/
int main() {
    int tab;  
    tab[0] = 1;
    tab[1] = 2;
    tab[3] = 3;

    return tab[3];
}
int main() {
    int x ;
x = malloc(5);
int i; 
int a,b;
for(i=0;i<5;i=i+1){x[i] = i;}
return x[4];

}

int initTableau(int tab, int taille) {
    tab = malloc(taille);
    int i;
    for (i = 0; i < taille; i = i+1) {
        tab[i] = i;
    }
}
int main() {
    int taille;
    taille = 5;
    int x ;  

    initTableau(x, taille);

    return x[4];
    free(x);

}

/*POINTEUR TEST*/
int main() {
    int x ;
    x = 42;
    int ptr;
    ptr = &x;


    return *ptr;
}

int main() {
    int x ;
    x = 42;
    int ptr;
    ptr = &x;


    return &ptr;
}
