from game import Game

class Environment:
    def __init__(self, n, m, bombs, reward_per_step, seed=None):
        self.__game = None
        if seed == None:
            self.__game = Game(n, m, bombs)
        else:
            self.__game = Game(n, m, bombs, seed)
        self.__actions = [(x, y) for x in range(m) for y in range(n)]
        self.__possibleStates = self.generateAllStates()
        self.__initial_state = []
        self.__state = self.__initial_state
        self.__reward_per_step = reward_per_step
        self.__states_id_map = dict(enumerate(self.__possibleStates))

    def getStatus(self):
        return self.__game.status

    def state_coords(self, state):
        temp = []
        for x in state:
            temp.append(state[0])
        return temp

    def __getReward(self, state, action=None):
        count = 0
        for x in state:
            if x[1] == 'B':
                return -1
            count += 1
        if count == ((len(self.__game.board) * len(self.__game.board[0])) - self.__game.bombsCount):
            return 10
        return self.__reward_per_step

    def generateAllStates(self):
        temp = []
        m = len(self.__game.board)
        n = len(self.__game.board[0])
        for x in self.__actions:
            newgame = Game(n, m, self.__game.bombsCount)
            board = newgame.getBoardConfig([x])
            states = self.__generatePossibleStates([(x, y) for x in range(m) for y in range(n)], [x])
            for s in states:
                newstate = []
                for e in s:
                    newstate.append((e, newgame.board[e[0]][e[1]]))
                temp.append(newstate)
        result = []
        for x in temp:
            if x not in result:
                result.append(x)
        return result

    def __combinations(self, iterable):
        if len(iterable) == 0:
            return [[]]
        combos = []
        for combo in self.__combinations(iterable[1:]):
            combos += [combo, combo + [iterable[0]]]
        return combos

    def __generatePossibleStates(self, iterable, bombs):
        temp = []
        for set_ in self.__combinations(iterable):
            if len(set(set_).intersection(set(bombs))) <= 1:
                temp.append(set_)
        return temp

    def __calculate_transition(self, action):
        self.__state.append((action, self.__game.board[action[0]][action[1]]))

    def getCurrentState(self):
        return self.__state

    def removeAction(self, action):
        self.__actions.remove(action)

    def getIdByState(self, state):
        for key, value in self.__states_id_map.items():
            if set(value) == set(state):
                return key

    def getStateById(self, _id):
        return self.__states_id_map[_id]

    def isGameOver(self):
        if self.__game.status == 1 or self.__game.status == -1:
            return True
        else:
            return False

    def isDone(self, state):
        count = 0
        for x in state:
            if x[1] == 'B':
                return True
            count += 1
        if count == ((len(self.__game.board) * len(self.__game.board[0])) - 1):
            return True
        return False

    def reset(self):
        self.__game = Game(len(self.__game.board[0]), len(self.__game.board), self.__game.bombsCount)
        self.__state = self.__initial_state
        return self.__state

    def step(self, action):
        # Open cell
        self.__game.openCell(action[0], action[1])
        # Step logic
        self.__calculate_transition(action)
        observation = self.__state
        done = self.isDone(self.__state)
        reward = self.__getReward(self.__state)
        info = self.__game
        return observation, done, reward, info

    def render(self, powerMode=False):
        for line in self.__game.board:
            print(line)
        print("State: ", self.__state)
        print("Status: ", self.__game.status)
        print("Bombs: ", self.__game.bombsCount)
        if powerMode:
            print("Bombs: ", self.__game.bombs)

    def get_possible_states(self):
        return self.__possibleStates

    def get_actions(self):
        return self.__actions

    def get_transition_prob(self, action, new_state, old_state=None):
        if self.isDone(old_state):
            return 0

            # Conditions
        length = (len(new_state) == len(old_state) + 1)
        intersection = set(new_state).intersection(set(old_state)) == set(old_state)
        diff = list(set(new_state) - set(old_state))
        same_action = [item[0] for item in diff] == [action]

        if not (length and intersection and same_action):
            return 0

        count = 0
        for x in self.__possibleStates:
            length = (len(x) == len(old_state) + 1)
            intersection = set(x).intersection(set(old_state)) == set(old_state)
            diff = list(set(x) - set(old_state))
            same_action = [item[0] for item in diff] == [action]
            if length and intersection and same_action:
                count += 1

        return 1 / count

    def getReward(self, state, action=None):
        return self.__getReward(state, action)
