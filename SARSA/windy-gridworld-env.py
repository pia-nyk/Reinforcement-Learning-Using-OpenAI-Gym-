from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt

'''
    epsilon greedy policy, chooses randomly with probability
    eps or else chooses greedily
'''
def policy(env, st, eps, Q):
    if np.random.rand() > eps:
        return get_action_with_max_val([Q[st,a] for a in env.act_space])
    else:
        return np.random.choice(env.act_space)

def get_action_with_max_val(action_vals):
    return np.random.choice(np.flatnonzero(action_vals == np.max(action_vals)))

'''
    Windy grid world env in accordance to the rules given in
    Sutton-Barto book.
'''
class WindyGridWorld:
    def __init__(self):
        self.act_space = [0,1,2,3]
        self.reset()

    def reset(self):
        self.x = 0
        self.y = 3
        return (0,3) #start state

    def step(self, action):
        self.x, self.y = self.transition(action)
        if self.x == 7 and self.y == 3: #end state
            return (self.x, self.y), 0, True
        return (self.x, self.y), -1, False

    def transition(self, action):
        x = self.x
        y = self.y
        if self.x in [3,4,5,8]: y-=1 #for these x values, wind will take the agent diagonally up by 1 step
        elif self.x in [6,7]: y-=2 #for these x values, wind will take the agent diagonally up by 2 steps

        if action == 0: x-=1 #left
        elif action == 1: x+=1 #right
        elif action == 2: y-=1 #up
        elif action == 3: y+=1 #down
        if x >= 0 and x <= 9: #horizontal boundaries
            self.x = x
        if y >=0 and y <= 6: #vertical boundaries
            self.y = y
        return self.x, self.y


def sarsa(env, ep, alpha, n_episodes, max_steps, gamma=1.0):
    hist_ep = [] #list to keep a track of how many iterations per episode
    Q = defaultdict(float)
    for _ in range(n_episodes):
        if(_%500 == 0):
            print(_)
        S = env.reset()
        A = policy(env, S, ep, Q)
        while True:
            S_, reward, done = env.step(A)
            A_ = policy(env, S_, ep, Q)
            Q[S,A] = Q[S,A] + alpha * (reward + gamma*Q[S_,A_] - Q[S,A]) #sarsa update
            S = S_
            A = A_

            hist_ep.append(_)
            if max_steps is not None:
                if len(hist_ep) >= max_steps: #if the max steps required to plot progress have to be bound
                    return Q, hist_ep
            if done:
                break
    return Q, hist_ep

env = WindyGridWorld()
Q, hist_ep = sarsa(env, 0.1, 0.5, 1000, 8000)


fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(hist_ep, color='red')
ax.set_xlabel('Time Steps')
ax.set_ylabel('Episodes')
plt.tight_layout()
plt.show()
