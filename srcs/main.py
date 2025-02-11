from Agent import Agent


def main():
    agent = Agent()
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        agent.ask(user_input)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
