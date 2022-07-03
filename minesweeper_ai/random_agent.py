import random
from environment import Environment


def policy_random(env):
    # action is random choice from all actions in Action Space
    random.seed(None)
    cell = random.choice(env.get_actions())
    return cell


def play_random(env):
    total_reward = 0.0
    done = False
    nr_steps = 0

    while not done:
        next_cell = policy_random(env)
        state, done, reward, info = env.step(next_cell)
        total_reward += reward
        nr_steps += 1
        print('cell: {}, reward: {:5.2f}'
              .format(next_cell, reward))
        for row in info.board:
            print(*row, sep="\t")
        print(info.bombs)
    print('Episode done after {} steps. total reward: {:6.2f}. Result: {}'.format(nr_steps, total_reward, info.status))