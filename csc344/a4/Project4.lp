%Main Project: Social Distancing Simulator
% Facts 1
#const n1=24.
#const n2=24.
#const startX=13.
#const d=5. 
person(20, 4).
person(13, 7).
person(4, 19).

% Map
map(0..n1, 0..n2).
start(startX, 0).

% Check for path
distance(X1, Y1, X2, Y2, D) :-
   map(X1, Y1),
   map(X2, Y2),
   D = (X1 - X2) * (X1 - X2) + (Y1 - Y2) * (Y1 - Y2).

% Find if the cell is safe
safe(X,Y) :-
   map(X,Y),
   not unsafe(X,Y).

unsafe(X,Y) :-
   map(X,Y),
   person(X1,Y1),
   distance(X,Y,X1,Y1,D), D < (d*d).

{edge(X,Y,X,Y+1) :  start(X,Y), safe(X,Y), safe(X,Y+1)}.
{edge(X,Y,X+1,Y) :  start(X,Y), safe(X,Y), safe(X+1,Y)}.
{edge(X,Y,X-1,Y) :  start(X,Y), safe(X,Y), safe(X-1,Y)}.

% Path from start to goal
path(X1, Y1, X2, Y2) :-
   edge(X1, Y1, X2, Y2),
   safe(X1, Y1),
   safe(X2, Y2).
   
start(X,Y) :- path(_,_,X,Y).

:- not path(startX, 0, _, _).
:- not path(_, _, _, n2).
:- path(X1,Y1,X2,Y2), path(X2,Y2,X1,Y1).
:- path(X1,Y1,X2,Y2), path(X1,Y1,X3,Y3), X2 != X3, Y2 != Y3.


#show path/4.
