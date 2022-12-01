$TITLE Pump scheduling smallest 
$ontext
version: 2.0
author of this version: sofdem@gmail.com
characteristics: 9-period model for free GAMS version
$offtext

*$offlisting
* stops the echo print of the input file
*$offsymxref
* stops the print of a complete cros-reference list of symbols
*option limcol = 0;
* stops the print of the column listing
*option limrow = 0;
* stops the print of the equation listing
*option solprint = off;
* stop report solution

Sets 
     n          nodes      / s, j1, j2, r1, r2, r3, r4 /
     j(n)       junctions  / j1, j2 /
     r(n)       reservoirs / r1, r2, r3, r4 /
     l(n,n)     pipes      / s.j1, j1.j2, j1.r1, j1.r4, j2.r2, j2.r3 /
     t          1-hour periods / t1*t9 /
     night(t)   night periods  / t1*t4 /      
     c          pump class   / small /
     d          pump number  / p1*p3 /
     k(c,d)     pump type    / small.p1*p3 /
     degree     polynomial degrees / 0*2 /
     

     alias (n,np)          
     alias (k,kp)
     alias (d,dp);

Scalar
     height0      reference height at the source (m)      / 0 /
     tariffnight  electricity hourly tariff at night (euro.kWh^-1)  / 0.02916 /
     tariffday    electricity hourly tariff at day (euro.kWh^-1)    / 0.04609 /
     Qmin         minimal debit for pumps    / 1 /
     Qmax         maximal debit for pumps    / 300 /;

Parameter tariff(t)   electricity tariff;
    tariff(t)        = tariffday;
    tariff(night(t)) = tariffnight;

Parameters
    height(n)   elevation at each node relative to s (m)
                / s 0, j1 30, j2 30, r1 50, r2 50, r3 45, r4 35 /

    surface(r)  mean surface of each reservoir (m^2)
                / r1 80, r2 80, r3 80, r4 80 /

    vmin(r)     minimal volume of each reservoir (m^3)
                / r1 100, r2 100, r3 100, r4 100 /

    vmax(r)     maximal volume of each reservoir (m^3)
                / r1 300, r2 300, r3 300, r4 300 /

Parameter vinit(r) initial volume of each reservoir;
    vinit(r) = vmin(r);

* a polynomial is represented as the list of coefficients for each term degree
Table psi(c,degree) quadratic fit of the service pressure (m) on the flow (m^3.h^-1) for each class of pumps
                  0              1            2
      small       63.0796        0            -0.0064085;

Table gamma(c,degree) linear fit of the electrical power (kW) on the flow (m^3.h^-1) for each class of pumps
                  0              1
      small       3.81101     0.09627;

Table demand(r,t) demand in water at each reservoir each hour (m^3)
     t1     t2    t3    t4     t5     t6    t7      t8      t9
r1   9.83   5.0   3.67  6.5    5.67   7.5   3.0     3.0     2.0
r2   44.83  18.0  0.0   0.0    0.0    0.0   0.0     45.0    51.67
r3   14.0   13.33 25.5  11.0   10.0   10.0  11.0    10.33   30.17
r4   1.0    1.0   8.5   9.5    4.0    2.33  0.0     1.0     0.83;

Table phi(n,n,degree) quadratic fit of the pressure loss (m) on the flow (m^3.h^-1) for each pipe
                2               1
     s.j1       0.00005425      0.00038190  
     j1.j2      0.00027996      0.00149576
     j1.r1      0.00089535      0.00340436
     j1.r4      0.00044768      0.00170218  
     j2.r2      0.00223839      0.00851091
     j2.r3      0.00134303      0.00510655;

Variables
     Charge(n,t)         Niveau de charge au noeud (n) à (t)
     Qpompe(c,d,t)       Débit de la pompe (k) à (t)
     Qreserve(n,t)       Débit entrant au réservoir (r) à (t)
     Gpompe(c,d,t)       Gain de charge de la pompe (k) à (t) en (m)
     Ppompe(c,d,t)       Puissance électrique de la pompe (k) à (t) en (kW)
     v(n,t)              Volume au réservoir (r) en (t)
     Son(c,d,t)          Statut de la pompe (k) fonctionne à (t)
     z                   Coût exploitation final;

v.up(r,t)      =    vmax(r);
v.lo(r,t)      =    vmin(r);
v.fx(r,'t1')   =    vinit(r);

Positive variables Qpompe, Qreserve, Ppompe, Charge;
Binary variable Son;

Equations
     obj                           Objectif
     Charge_s(n,t)                 Niveau de charge à la source à (t)
     Charge_j(n,t)                 Niveau de charge aux jonctions (j) à (t)
     Charge_r(n,t)                 Niveau de charge au réservoir (r) à (t)
     Noeud(t)                      Contrainte débit noeud à (t)
     Satisfaction_demande(r,t)     Satisfaction de la demande en (r) à (t)
     Gain_charge_pompe(c,d,t)      Gain de charge de la pompe (k) à (t)
     Elec_pompe(c,d,t)             Consommation électrique de la pompe (k) à (t)
     Qpompe_inf(c,d,t)             Borne inférieur pompe (k) à (t)
     Qpompe_sup(c,d,t)             Borne supérieur pompe (k) à (t)
     Perte_charge(n,n,t)           Perte charge (n,n) à (t);    

Noeud(t) ..                   sum(k, Qpompe(k,t)) =e=  sum(r, Qreserve(r,t));
Satisfaction_demande(r,t) ..  v(r,t) - v(r,t-1)   =e=  1 * (Qreserve(r,t)-demand(r,t));
Elec_pompe(k,t) ..            Ppompe(k,t)         =g=  gamma("small","0") * Son(k,t) + gamma("small","1")*Qpompe(k,t);
Gain_charge_pompe(k,t) ..     Gpompe(k,t)         =l=  psi("small","0") * Son(k,t) + psi("small","2")*Qpompe(k,t)**2;
Qpompe_inf(k,t) ..            Qpompe(k,t)         =g=  Son(k,t)*Qmin;
Qpompe_sup(k,t) ..            Qpompe(k,t)         =l=  Son(k,t)*Qmax;
obj ..                        z                   =e=  sum((k,t), Ppompe(k,t)*tariff(t));
Charge_s("s",t) ..            Charge("s",t)       =e=  sum(k, Gpompe(k,t));
Charge_j(j,t) ..              Charge(j,t)         =g=  height(j);
Charge_(r,t) ..               Charge(r,t)         =g=  height(r) + v(r)/surface(r);


model Optim_production / all /;

solve Optim_production using minlp minimizing z;

display Ppompe.l, v.l, z.l;

File volumes / volume.txt /;
volumes.pc = 5;
put volumes;
put "Volume" /;
loop((n,t),
  put n.tl, t.tl, v.l(n,t) /
);
putclose;

File Conso / Conso.txt /;
Conso.pc = 5;
put Conso;
put "Consommation électrique des pompes" /;
loop((c,d,t),
  put c.tl, d.tl, t.tl, Ppompe.l(c,d,t) /
);
putclose;

File Dpompe / Dpompe.txt /;
Dpompe.pc = 5;
put Dpompe;
put "Débit des pompes" /;
loop((c,d,t),
  put c.tl, d.tl, t.tl, Qpompe.l(c,d,t), Ppompe.l(c,d,t), Son.l(c,d,t) /
);
putclose;








