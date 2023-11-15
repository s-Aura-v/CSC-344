%Main Project: Social Distancing Simulator

% #const n1=24.
% #const n2=24.
% #const startX=13.
% #const d=2.  

#const n1=6.
#const n2=6.
#const startX=1.
#const d=2.  

%Add the people
% person(20, 4). 
% person(13, 7).
% person(4, 19).

person(0, 2).
% person(4, 4).

% Map
map(0..n1, 0..n2).

% Create the start and end
start(startX, 0).
goal(0..n1, n2).

% Check for path
distance(X1, Y1, X2, Y2, D) :-
    map(X1, Y1),
    map(X2, Y2),
    D = (X1 - X2) * (X1 - X2) + (Y1 - Y2) * (Y1 - Y2).

% Find if the cell is safe + unsafe
safe(X,Y) :- 
    map(X,Y), 
    not unsafe(X,Y).

unsafe(X,Y) :- 
    map(X,Y), 
    person(X1,Y1), 
    distance(X,Y,X1,Y1,D), D < (d*d).  

% {edge(X,Y,X,Y+1) : start(X,Y), safe(X,Y), safe(X,Y+1) }.
% {edge(X,Y,X+1,Y) : start(X,Y), safe(X,Y), safe(X+1,Y) }.
% {edge(X,Y,X-1,Y) : start(X,Y), safe(X,Y), safe(X-1,Y) }.

% % Path from start to goal
% path(X1, Y1, X2, Y2) :-
%     edge(X1, Y1, X2, Y2),
%     safe(X1, Y1),
%     safe(X2, Y2).

% :- not path(startX, 0, _, _).
% :- not path(_, _, _, n2). 


#show path/4.