Sets
    t       temps           / t1*t5 /
    X       centrale type   / X1*X3 /;

Parameters
    demande(t)  demand at (t)
    / t1 17, t2 25, t3 30, t4 40, t5 29 /

    Pmax(X)     puissance max centrales (X)
    / X1 24, X2 17.5, X3 10 /

    Cost(X)     Coût MWh centrales (X)
    / X1 1.5, X2 1.38, X3 2.8 /

    Duree(t)    Durée de la période (t)
    / t1 5, t2 3, t3 4, t4 4, t5 8 /;

Variables
    P(X,t)  "Puissance (X) à l'instant (t)"
    z       "Coût total";

Positive variable P;

Equations
    obj        Objectif
    Psup(X,t)   Borne sup de puissance
    equ(t)      Equilibre offre-demande;

obj ..         z               =e= sum((X,t), P(X,t) * Cost(X) * Duree(t));
Psup(X,t) ..    P(X,t)          =l= Pmax(X);
equ(t) ..       sum(X, P(X,t))  =e= demande(t);

model Optim_production / obj, Psup, equ /;

solve Optim_production using lp minimizing z;

display P.l, z.l;

