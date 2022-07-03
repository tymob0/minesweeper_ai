import random

def RationalAgentPlay(env,pi_star, render = False):
  random.seed(None)
  cell = random.choice(env.get_actions())
  env.step(cell)
  if render: env.render(True)
  while not env.isGameOver():
    state = env.getCurrentState()
    next_move = pi_star[env.getIdByState(state)]
    env.step(next_move)
    if render: env.render(True)
  return env.getStatus()