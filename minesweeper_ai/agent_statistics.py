from statistics import mean, stdev
from environment import Environment
from random_agent import policy_random
from rational_agent import RationalAgentPlay

def run_one_episode_random(policy, pi_star):
    env = Environment(2,3,1,-0.04)

    total_reward = 0.0
    done = False
    while not done:
        next_action = policy(env)
        state, done, reward, info = env.step(next_action)
        total_reward += reward
    if env.getStatus() == 1:
      return 1
    return 0

def run_one_episode_rational(policy, pi_star):
    env = Environment(2,3,1,-0.04)
    if(RationalAgentPlay(env,pi_star) == 1):
      return 1
    return 0

def measure_performance(policy,pi_star, run_episode, nr_episodes=100):
    N = nr_episodes
    print('statistics over', N, 'episodes')
    all_rewards = []
    for _ in range(N):
        episode_reward = run_episode(policy, pi_star)
        all_rewards.append(episode_reward)

    print('mean: {:6.2f}, sigma: {:6.2f}'.format(mean(all_rewards), stdev(all_rewards)))
    for n, episode_reward in enumerate(all_rewards[:5], 1):
        print('ep: {:2d}, total reward: {:5.2f}'.format(n, episode_reward))
    print('......')
    for n, episode_reward in enumerate(all_rewards[-5:], len(all_rewards)-5):
        print('ep: {:2d}, total reward: {:5.2f}'.format(n, episode_reward))

def get_statistics_random(pi_star = None):
    measure_performance(policy_random,pi_star, run_one_episode_random)

def get_statistics_rational(pi_star):
    measure_performance(policy_random,pi_star,  run_one_episode_rational)

