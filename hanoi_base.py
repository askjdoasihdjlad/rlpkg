import math
from search import Problem


class Hanoi(Problem):
    def __init__(self):
        super().__init__([{1, 2, 3}, set(), set()], [set(), set(), {1, 2, 3}])
        pass

    def actions(self, state):
        acts = []
        inf_set = {math.inf}
        for i in range(3) :
            for j in range(3) :
                if i != j :
                    for k in range(1, 4) :
                        if k == min(state[i].union(inf_set)) and k < min(state[j].union(inf_set)) :
                            acts.append("o {} {} {}".format(i + 1, j + 1, k))
        # Calculate possible actions here

        return acts

    def actions2(self, state):
        acts = []

        for i in range(3):
            if len(state[i]) == 0:
                continue

            top_disk = min(state[i])

            for j in range(3):
                if i == j:
                    continue

                if len(state[j]) == 0 or top_disk < min(state[j]):
                    # Output actions with 1-based indexing for user clarity
                    acts.append(f"o {i + 1} {j + 1} {top_disk}")

        return acts

    def result(self, state, action):
        i, j, k = action.split()[1 :]
        i, j, k = int(i), int(j), int(k)

        new_state = state

        for l in range(1, 4) :
            if l == j :
                new_state[l - 1] = state[l - 1].union({k})
            else :
                new_state[l - 1] = state[l - 1].difference({k})

        return new_state

    pass

    def result2(self, state, action):
        i, j, disk = action.split()[1: ]

        # Convert 1-based input to 0-based for internal indexing
        i = int(i) - 1
        j = int(j) - 1
        disk = int(disk)

        new_state = [set(peg) for peg in state]

        new_state[i].remove(disk)
        new_state[j].add(disk)

        return new_state


def main():
    h = Hanoi()

    # Test if actions works correctly
    print(h.actions([{1, 2, 3}, set(), set()]))
    print(h.actions([{1}, {2, 3}, set()]))

    # Test if result works correctly
    print(h.result(
        state=[{1}, {2, 3}, set()],
        action="o 2 3 2"
    ))


main()
