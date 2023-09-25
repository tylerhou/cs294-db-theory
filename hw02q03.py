import itertools

X1 = "X1"
X2 = "X2"
X3 = "X3"
X4 = "X4"
X5 = "X5"

D = [X1, X2, X3, X4, X5]

CM1_A = set([
    (X1, X2),
    (X2, X3),
    (X3, X4),
    (X4, X5),
    (X5, X1),
])

CM1_Neq = set(itertools.product(D, D)) - set([
    (X1, X2),
    (X2, X1),
])

def Query1(x1, x2, x3, x4, x5, DB):
    A, Neq = DB
    return all([
        (x1, x2) in A,
        (x2, x3) in A,
        (x3, x4) in A,
        (x4, x5) in A,
        (x5, x1) in A,
        (x1, x2) not in Neq,
    ])

CM2_A = set([
    (X1, X2),
    (X2, X3),
    (X3, X4),
    (X4, X5),
    (X5, X1),
])

CM2_Neq = set(itertools.product(D, D)) - set([
    (X1, X3),
    (X3, X1),
])

def Query2(x1, x2, x3, x4, x5, DB):
    A, Neq = DB
    return all([
        (x1, x2) in A,
        (x2, x3) in A,
        (x3, x4) in A,
        (x4, x5) in A,
        (x5, x1) in A,
        (x1, x3) not in Neq,
    ])


def solve():
    for x1, x2, x3, x4, x5 in itertools.product(D, D, D, D, D):
        if Query1(x1, x2, x3, x4, x5, (CM2_A, CM2_Neq)):
            print("Q1", x1, x2, x3, x4, x5)

        if Query2(x1, x2, x3, x4, x5, (CM1_A, CM1_Neq)):
            print("Q2", x1, x2, x3, x4, x5)

if __name__ == "__main__":
    solve()

