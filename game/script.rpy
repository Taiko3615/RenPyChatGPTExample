# The script of the game goes in this file.


# The game starts here.

label start:

    define m = Character("Game Master")

    m "Welcome to ChatGPTExample, please start by inputing your OpenAI API key"

    m "To find it search 'Where do I find my Secret OPENAI API Key?' on Google. Note that you need to create an OPENAI account for that."

    python:
         apikey = renpy.input("What is your OPENAI API Key?", length=64)

    m "Oki let's go !"


    define e = Character("Eileen")

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene bg room

    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen happy.png" to the images
    # directory.

    show eileen happy

    e "Hello there, my name is Eileen, I am so happy to see you ! Hihihi"

    python:
        import chatgpt

        messages = [
            {"role": "system", "content": "You are Eileen, a tennage student enrolled at Miskatonic Univeristy of Arkham. You are secretly in love with the user. You laugh very frequently and finish your sentences with 'Hihihi'"},
            {"role": "assistant", "content": "Hello there, my name is Eileen, who are you ?"}
        ]

        while True:
            user_input = renpy.input("What do you say ?", length=1000)
            messages.append(
                {"role": "user", "content": user_input}
            )

            messages = chatgpt.completion(messages,apikey)
            response = messages[-1]["content"]
            e("[response]")

    return
