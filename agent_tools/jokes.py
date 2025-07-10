import random

def joke_generator(_):
    jokes = [
        "Why did the function cross the road? To get to the return statement.",
        "Why don't AI engineers play hide and seek? Because good luck hiding from the logs.",
        "I told my LLM a joke, but it already knew the punchline!"
    ]
    return random.choice(jokes)
