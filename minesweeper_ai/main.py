from value_iteration import train
from agent_statistics import get_statistics_random
from agent_statistics import get_statistics_rational

def main():
    print("Statistics random agent:")
    get_statistics_random()
    pi_star = train()
    print("Statistics rational agent:")
    get_statistics_rational(pi_star)

if __name__ == '__main__':
    main()

