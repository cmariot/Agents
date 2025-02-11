# Unit 1 : Introduction to agents

## What is an agent?

An agent is an AI model capable of reasoning, planning, and interacting with its environment.

An Agent is a system that uses an AI Model (typically a LLM) as its core reasoning engine, to:

- Understand natural language: Interpret and respond to human instructions in a meaningful way.
- Reason and plan: Analyze information, make decisions, and devise strategies to solve problems.
- Interact with its environment: Gather information, take actions, and observe the results of those actions.

An AI agent is a system that perceives its environment, processes information, and takes actions to achieve a goal.


## Agent planning and reasoning

In artificial intelligence (AI) and autonomous systems, planning is a crucial function that enables an agent to decide on a sequence of actions to achieve its goal efficiently. It allows the agent to think ahead rather than simply reacting to immediate inputs.

Agents can decide on the sequence of actions and select the best tools to achieve their goals. They can also adapt their strategies based on the results of their actions and the feedback they receive from the environment.


## Tools are agents capabilities

In AI tools play a crucial role in enhancing an agent’s capabilities by improving its ability to perceive, reason, plan, and act effectively. These tools provide external resources, computational power, and real-world connectivity that extend what an agent can achieve.

Tools can help an agent in several ways:
- Expanding Knowledge → Access to external data sources (APIs, databases, or web search).
- Improving Decision-Making → Using algorithms, planners, or machine learning models.
- Enhancing Efficiency → Automating tasks that would otherwise take too much time.
- Enabling Execution → Allowing the agent to interact with external systems (robotics, blockchain, web applications).


## Understanding AI Agents through the Thought-Action-Observation Cycle

The Thought-Action-Observation (TAO) cycle is a conceptual framework that describes how an AI agent interacts with its environment. It consists of three main stages:

- **Thought**: The agent processes information, reasons about it, and decides on a course of action.
- **Action**: The agent executes the chosen action in the environment.
- **Observation**: The agent observes the results of its action and updates its internal state based on the feedback received.

This cycle repeats continuously, allowing the agent to learn from its interactions and improve its decision-making over time.

In the TAO cycle, the agent's goal is to maximize its utility by selecting the best actions based on its current state and the information available to it. By following this cycle, the agent can adapt to changing conditions and achieve its objectives more effectively.

The rules and guidelines can be embedded directly into the system_prompt. 

```python

system_prompt = """
You are an AI agent tasked with helping a user find a restaurant in a new city.

You have access to the following tools:
- Tool name : 'Restaurant API'
  Description: 'Accesses a database of restaurants in the city.'
  Arguments: 'city_name, cuisine_type'
- Tool name : 'Map API'
  Description: 'Provides a map of the city with restaurant locations.'
  Arguments: 'city_name, restaurant_name'
- Tool name : 'Review API'
  Description: 'Accesses user reviews and ratings for restaurants.'
  Arguments: 'restaurant_name'

You should think step by step in order to fulfill the objective with a reasoning divided in
Thought/Action/Observation that can repeat multiple times if needed. You should first reflect with 'Thought: {your_thoughts}' on the current situation, then (if necessary), call a tool with the proper JSON formatting 'Action: {JSON_BLOB}', or print
your final answer starting with the prefix 'Final Answer: {your_answer}'.

"""

```

