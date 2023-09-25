import itertools

X = "x"
Y = "y"
Z = "z"
U = "u"

D = [X, Y, Z, U]

CM1_R = set([
    (X, Y),
    (Z, Y),
    (X, U),
])


def Query1(x, y, z, u, DB):
    (A,) = DB
    return all([
        (x, y) in A,
        (z, y) in A,
        (x, u) in A,
    ])


CM2_R = set([
    (X, Y),
    (Y, Z),
    (Z, U),
])


def Query2(x, y, z, u, DB):
    (A,) = DB
    return all([
        (x, y) in A,
        (y, z) in A,
        (z, u) in A,
    ])


CM3_R = set([
    (X, Y),
    (Y, Z),
    (Z, X),
])


def Query3(x, y, z, u, DB):
    (A,) = DB
    return all([
        (x, y) in A,
        (y, z) in A,
        (z, x) in A,
    ])


CM4_R = set([
    (X, Y),
])


def Query4(x, y, z, u, DB):
    (A,) = DB
    return all(
        [
            (x, y) in A,
        ]
    )


def solve():
    subset = set()
    for x, y, z, u in itertools.product(*[D for _ in range(4)]):
        for combo in itertools.combinations(
            [
                (Query1, (CM1_R,)),
                (Query2, (CM2_R,)),
                (Query3, (CM3_R,)),
                (Query4, (CM4_R,)),
            ],
            r=2,
        ):
            ((query_a, db_a), (query_b, db_b)) = combo

            if query_a(x, y, z, u, db_b):
                subset.add((query_b.__name__, query_a.__name__))
                print(f"{query_a.__name__}(DB_{query_b.__name__}) = true")
                print(f"\t(x, y, z, u) -> ({x}, {y}, {z}, {u})")

            if query_b(x, y, z, u, db_a):
                subset.add((query_a.__name__, query_b.__name__))
                print(f"{query_b.__name__}(DB_{query_a.__name__}) = true")
                print(f"\t(x, y, z, u) -> ({x}, {y}, {z}, {u})")

    equiv = set()
    subset_but_not_eq = set()
    for a, b in subset:
        tup = tuple((a, b))
        if (b, a) in subset:
            if a <= b:
                equiv.add(tup)
        else:
            subset_but_not_eq.add(tup)

    for a, b in sorted(equiv):
        print(f"{a} ≡ {b}")

    for a, b in sorted(subset_but_not_eq):
        print(f"{a} ⊆ {b}")


if __name__ == "__main__":
    solve()
