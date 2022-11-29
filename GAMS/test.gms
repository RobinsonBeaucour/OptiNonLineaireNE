Sets
    t       temps           / t1*t5 /
    X       centrale type   / X1*X3 /;

Parameters
    demande(t)  demand at (t)
    / t1 17, t2 25, t3 30, t4 40, t5 29 /

    Nmax(X)     Nombre de centrales (X)
    / X1 12, X2 10, X3 5 /

    Pmax(X)     Puissance max centrale (X)
    / X1 2, X2 1.75, X3 2 /

    Pmin(X)     Puissance min centrale (X)
    / X1 0.8, X2 1, X3 1.1 /

    Cost(X)     Coût MWh centrales (X)
    / X1 1.5, X2 1.38, X3 2.8 /

    Duree(t)    Durée de la période (t)
    / t1 5, t2 3, t3 4, t4 4, t5 8 /;

Variables
    P(X,t)      "Puissance (X) à l'instant (t)"
    N(X,t)      "Nombre de centrale (X) allumées à l'instant (t)"
    Nstart(X,t) "Nombre de centrale (X) démarrant à (t)"
    z           "Coût total";

Positive variable P;
Integer variable N;

Equations
    obj                     Objectif
    Nsup(X,t)               Nombre max de centrale (X) à (t)
    Psup(X,t)               Borne sup de puissance
    Pinf(X,t)               Borne inf de puissance
    equ(t)                  Equilibre offre-demande
    demarrage(X,t)          Contrainte démarrage (X) à (t);

obj ..                          z                           =e= sum((X,t), P(X,t) * Cost(X) * Duree(t));
Psup(X,t) ..                    P(X,t)                      =l= Pmax(X) * N(X,t);
Pinf(X,t) ..                    P(X,t)                      =g= Pmin(X) * N(X,t);
equ(t) ..                       sum(X, P(X,t))              =e= demande(t);
Nsup(X,t) ..                    N(X,t)                      =l= Nmax(X);
demarrage(X,t) ..               N(X,t)                      =l= Nstart(X,t)+N(X,t-1);
model Optim_production / all /;

solve Optim_production using mip minimizing z;

display P.l, z.l, N.l, "Nombre max centrale (X)" Nmax;

