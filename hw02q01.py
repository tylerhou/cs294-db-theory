import collections
import dataclasses
import random
import enum
import functools
import itertools

bools = (False, True)

def get_fields(v):
    if dataclasses.is_dataclass(v):
        return [f.name for f in dataclasses.fields(v)]
    else:
        return v._fields
    assert False

def make_table(v):
    fields = sorted(get_fields(v))

    def f():
        for tup in itertools.product(*[bools for _ in fields]):
            if random.choice([0, 1]) == 0:
                continue

            kws = {f: t for f, t in zip(fields, tup)}
            yield v.__class__(**kws)

    table = []
    while not table:
        table = sorted(f())
    return table

def match(l, r, intersection):
    for field in intersection:
        if getattr(l, field) != getattr(r, field):
            return False
    return True


def semijoin(left, right):
    if not left or not right:
        return []

    left_fields = {f for f in get_fields(left[0])}
    right_fields = {f for f in get_fields(right[0])}
    intersection = left_fields & right_fields

    def f():
        for l, r in itertools.product(left, right):
            if match(l, r, intersection):
                yield l

    return sorted(set(f()))

@functools.cache
def make_join_nt(left, left_fields, right, right_fields):
    union = sorted(set(left_fields) | set(right_fields))
    nt = collections.namedtuple(type(left).__name__ + "_" + type(right).__name__, union)
    return nt

def join(left, right):
    if not left or not right:
        return []

    left_fields = {f for f in get_fields(left[0])}
    right_fields = {f for f in get_fields(right[0])}
    intersection = left_fields & right_fields
    nt = make_join_nt(left[0], tuple(left_fields), right[0], tuple(right_fields))

    def f():
        for l, r in itertools.product(left, right):
            if match(l, r, intersection):
                result = {}
                result.update(l._asdict())
                result.update(r._asdict())
                yield nt(**result)

    return sorted(set(f()))

def print_table(table):
    if not table:
        print('empty')
        return

    fields = get_fields(table[0])
    for field in fields:
        print(field, end="\t")
    print()

    print('--------' * len(fields))

    for row in table:
        for field in fields:
            v = getattr(row, field);
            print('1' if v else '0', end="\t")
        print()

class Vars(enum.Enum):
    A = "A"
    B = "B"
    Q = "Q"
    AB = "AB"
    AQ = "AQ"
    BQ = "BQ"
    ABQ = "ABQ"


def powerset(iterable):
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))


A_VARS = {Vars.A, Vars.AB, Vars.AQ, Vars.ABQ}
B_VARS = {Vars.B, Vars.AB, Vars.BQ, Vars.ABQ}
Q_VARS = {Vars.Q, Vars.AQ, Vars.BQ, Vars.ABQ}

def combos():
    for combo in powerset(Vars):
        combo = set(combo)
        a_vars = combo & A_VARS
        b_vars = combo & B_VARS
        q_vars = combo & Q_VARS

        if not (a_vars and b_vars and q_vars):
            continue

        yield a_vars, b_vars, q_vars

def print_cols(cols):
    for var in Vars:
        if var in cols:
            print(var.value, end="")
        print("\t", end="")
    print()

def solve():
    for a_vars, b_vars, q_vars in combos():
        for _ in range(1_000 * 10):
            # if _ % 1000 == 0:
            #     print('-', end="", flush=True)
            nt_a = collections.namedtuple('A', sorted(e.value for e in a_vars))
            nt_b = collections.namedtuple('B', sorted(e.value for e in b_vars))
            nt_q = collections.namedtuple('Q', sorted(e.value for e in q_vars))


            a_table = make_table(nt_a(*[False for _ in a_vars]))
            b_table = make_table(nt_b(*[False for _ in b_vars]))
            q_table = make_table(nt_q(*[False for _ in q_vars]))

            a_join_b = join(a_table, b_table)
            lhs = semijoin(a_join_b, q_table)

            a_semijoin_q = semijoin(a_table, q_table)
            b_semijoin_q = semijoin(b_table, q_table)
            rhs = join(a_semijoin_q, b_semijoin_q)

            if len(lhs) != len(rhs) or set(lhs) != set(rhs):
                # print("A")
                # print_table(a_table)
                # print()

                # print("B")
                # print_table(b_table)
                # print()

                # print("Q")
                # print_table(q_table)
                # print()

                # print("A <> B")
                # print_table(a_join_b)
                # print()

                # print("A <| Q")
                # print_table(a_semijoin_q)
                # print()

                # print("B <| Q")
                # print_table(b_semijoin_q)
                # print()

                # print("LHS")
                # print_table(lhs)
                # print()

                # print("RHS")
                # print_table(rhs)
                # print()

                # print()
                # print_cols(a_vars | b_vars | q_vars)
                # break
                pass

        else:
            pass
            print_cols(a_vars | b_vars | q_vars)




    # print("rhs")
    # print_table(join(semijoin(TableA, TableQ), semijoin(TableB, TableQ)))


if __name__ == "__main__":
    print_cols(set(Vars))
    print("--------" * len(Vars))
    solve()
