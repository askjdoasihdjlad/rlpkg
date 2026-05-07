from search import Problem, Node
from collections import deque


def convert_state_to_list(state_tuple):
    return [list(x) for x in state_tuple]


def convert_state_to_tuple(state_list):
    return tuple([tuple(x) for x in state_list])


def print_matrix(matrix):
    for i in range(len(matrix)):
        print(matrix(i))


class FourQueensProblem(Problem):
    def __init__(self):
        super().__init__(((0, 0, 0, 0),
                          (0, 0, 0, 0),
                          (0, 0, 0, 0),
                          (0, 0, 0, 0)))
        pass

    def actions(self, state):
        acts = []
        for i in range(4):
            for j in range(4):
                if state[i][j] == 0:
                    acts.append("o {} {}".format(i + 1, j + 1))
        return acts

    def result(self, state, action):
        # Return with the new state of the result of the action parameter used in the state parameter.
        # Tip: don't forget to convert state to list of lists and then convert the result back to tuple of tuples
        i, j = int(action.split(' ')[1]) - 1, int(action.split(' ')[2]) - 1
        new_state = convert_state_to_list(state)

        for l in range(4):
            for k in range(4):
                if l == i and k == j:
                    new_state[l][k] = 1
                elif l == i or k == j or abs(i - l) == abs(j - k):
                    new_state[l][k] = 2
        return convert_state_to_tuple(new_state)

    def goal_test(self, state):
        # For a given state parameter check if it is a goal state.
        # Tip 1: don't forget conversions; Tip 2: you can use any() or all() for easier implementation
        bool_state = convert_state_to_list(state)

        for i in range(4):
            for j in range(4):
                bool_state[i][j] = state[i][j] == 1
        return all([any(bool_state[i]) for i in range(4)])


def bfs_tree(problem):
    frontier = deque([Node(problem.initial)])  # queue FIFO
    while frontier:
        node = frontier.popleft()
        # goal test when node is removed (standard BFS)
        if problem.goal_test(node.state):
            return node
        # expand without any checks
        for child in node.expand(problem):
            frontier.append(child)
    return None


def bfs_graph(problem):
    frontier = deque([Node(problem.initial)])
    explored = set()
    while frontier:
        node = frontier.popleft()  # queue FIFO
        # for row in node.state:
        #     print(row)
        # for row in node.expand(problem):
        #     print(row)
        # print("\n")

        # this will try to put other queen every possible place from node
        explored.add(node.state)

        for child in node.expand(problem):
            if child.state not in explored and child.state not in frontier:  # if it existed it mean it failed to match
                # this check that once there's 4 queen and doesnt attach each other it pass the goal
                if problem.goal_test(child.state):
                    return child
                # append the failed case
                frontier.append(child)
    return None


# diff between tree and graph is tree is hierarchy -> no looped exploration
# while graph is arbitrary connected
def dfs_tree(problem):
    frontier = deque([Node(problem.initial)])  # stack
    while frontier:
        node = frontier.pop()  # LIFO
        if problem.goal_test(node.state):
            return node
        for child in node.expand(problem):
            frontier.append(child)  # no checks!
    return None


def dfs_graph(problem):
    frontier = deque([Node(problem.initial)])
    explored = set()
    while frontier:
        node = frontier.pop()  # stack LIFO instead of popleft()
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child.state not in frontier:
                if problem.goal_test(child.state):
                    return child
                frontier.append(child)  # push onto stack

    return None


def backtrack(problem):
    def btc(node):
        # check if node is the answer
        if problem.goal_test(node.state):
            return node

        # continue exploring
        for child in node.expand(problem):
            result = btc(child)
            if result is not None:
                return result

        return None

    return btc(Node(problem.initial))


def main():
    my_state = ((0, 0, 0, 0),
                (0, 0, 0, 0),
                (0, 0, 0, 0),
                (0, 0, 0, 0))
    fq = FourQueensProblem()

    # acts = fq.actions(my_state)
    # print(acts)
    # res = fq.result(my_state, 'o 1 4')
    # print(res)
    # goal_state = ((0, 1, 0, 0),
    #             (0, 0, 0, 1),
    #             (1, 0, 0, 0),
    #             (0, 0, 1, 0))
    # print(fq.goal_test(goal_state))
    #
    # print("BFS")
    print(bfs_tree(fq))
    print(bfs_graph(fq))
    print(dfs_tree(fq))
    print(dfs_graph(fq))
    print(backtrack(fq))


main()
