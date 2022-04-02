# Multi-Agent-RL-simulating-collaboration-with-VDN-and-IQL

## Project description
The goal of the project was to simulate collaborative behaviour in a custom multi-agent reinforcement learning ([MARL](https://en.wikipedia.org/wiki/Multi-agent_reinforcement_learning)) environment. We look at two types of algorithms: **Independent Q-Learning (IQL)** and **Value Decomposition Network (VDN)**. The environment used is a Food Collector env detailed in the [environment description](#environment-description) section. The results are shown below. We can see clear collaborative behaviour from VDN, while the independent learning apprach leads to more indiviudalistic, greedy behaviour:


VDN             |  IQL
:-------------------------:|:-------------------------:
<a><img src="https://user-images.githubusercontent.com/74935134/161282878-4cc5a9cb-c68a-4e93-8a12-e50dfb491263.gif" align="middle" width="250" height="250"/>  |  <a><img src="https://user-images.githubusercontent.com/74935134/161281461-926ef432-d1c1-4a29-97be-c184871dce8b.gif" align="middle" width="250" height="250"/>

## Motivation
The motivation for this project comes mainly from two sources:
- [Simulating Green Beard Altruism](https://www.youtube.com/watch?v=goePYJ74Ydg), which explores the effects of natural selection on behaviour
- [Emergent Tool Use from Multi-Agent Interaction](https://arxiv.org/abs/1909.07528) by OpenAI, which explores complex collaborative behaviour in RL agents.
  
## Tags
Multi-Agent Reinforcement Learning, custom Gym enironment, Value Decompositon Network, Independent Q-Learning, Food Collector env

## Environment description
The environment is implemented as a grid world, with a basic 11x11 grid. Agents are colored red and oragne for better identification, the food is colored green, home is colored blue and walls are colored grey. The environment is based on and fully compatible with [OpenAI Gym](https://github.com/openai/gym).
 
### Game objective
The objective of the game is simple: one of the agents needs to eat the food and then they both need to return home. The game only ends if the food is eaten and both agents are in the home area. Moreover, the agents get bonus points if they are both next to the food when it is eaten. Therefore, the expected optimal behaviour is:
1. Both agents get close to the food (agent that is closer to food waits for the other agent)
2. One of them eats the food
3. They both return home straight after

On the contrary, a greedy behaviour would be for the agent closer to the food to immediately eat it.
  
### State Space
For simplicity and faster training, we use a feature vector for the state representation. The observable state space for each agent consists of a **7-element vector**:
- Two elements to describe the relative x and y distance to the food
- Two elements to describe the relative x and y distance to the home
- Two elements to describe the relative x and y distance to the other agent
- A binary element describing whether food has been eaten yet or not

### Action space
Each agent has 4 actions to chose: move up, down, left or right. If an illegal move is chosen, such as moving into a wall or colliding with another agent, the agents stay in place.

### Reward system
To observe collaborative behaviour we had to set the reward system so that it promotes collaboration. Therefore, we introduced bonus rewards for close proximity to the food when it is eaten.
 
  
<table>
<tr><th> Positive rewards </th><th> Negative rewards </th></tr>
<tr><td>

|                 Event                | Agent 1 | Agent 2 |
|:------------------------------------:|---------|---------|
| Food eaten by Agent 1                | +10     | +0      |
| Food eaten by Agent 2                | +0      | +10     |
| Home reached by both agents*         | +20     | +20     |
| Agent 1 eats food, agent 2 is nearby | +5      | +5      |
| Agent 2 eats food, agent 1 is nearby | +5      | +5      |

</td><td>

|       Event      | Agent |
|:----------------:|-------|
| Make step        | -0.1  |
| Hit wall         | -1    |
| Agents collide   | -5    |

</td></tr> </table>
  
*Reward given and game ends only if the food is eaten
  
  
## Brief description of the agents
The state and action spaces in our environment were simple enough that we could implement a tabular solution such as IQL. This method works by training each agent separately and including the other agent as part of the environment. In IQL each agent tries to maximize it’s own reward and is optimized using it’s own objective function.
  
At a lower level, VDN is similar to [IDQL](https://web.media.mit.edu/~cynthiab/Readings/tan-MAS-reinfLearn.pdf). There are multiple [DQL](https://arxiv.org/abs/1312.5602) agents, with their own networks and their own state representation inputs. The key difference is that the networks are optimized using a joint value function (Figure below). VDN backpropagates the total team reward signal back to each of the individual networks. As a result, the agents optimize their behaviour towards the benefit of all agents, promoting collaboration.

<p align="center">
  <img width="600" src="https://user-images.githubusercontent.com/74935134/161397892-060b5f3e-d0a6-40b8-9663-4a74282d0e74.png">
</p>
  

## Results

### Behaviours

### Training time

 
