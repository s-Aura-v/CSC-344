%Microproject 4: Find the 2-cell neighbors of node (1,2) in a 4x4 grid

% The grid size
node(0..3, 0..3).

% Fact 
node(1, 2).

% Find the distance using pythagorean theorem
distance(X1, Y1, X2, Y2, D) :-
    node(X1, Y1),
    node(X2, Y2),
    D = (X1 - X2) * (X1 - X2) + (Y1 - Y2) * (Y1 - Y2).

% Find what cells are within a 2 cell distance using (1,2)
reachable(X, Y) :-  
    node(X, Y),
    distance(1, 2, X, Y, D),
    D <= 2.

% Show the central cell (1,2) and the reachable cells
#show reachable/2.