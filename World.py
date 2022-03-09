from Agent import Agent, Human

# Create an agent
agent = Human()

print(f"Generated random agent '{agent.firstName}' (M / {agent.age})")

while True:
    agent.listen()