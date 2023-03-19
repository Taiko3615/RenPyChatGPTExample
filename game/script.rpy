# The script of the game goes in this file.


# The game starts here.

label start:

    define m = Character("Game Master")

    m "Welcome to ChatGPTExample, please start by inputing your OpenAI API key"

    m "To find it search 'Where do I find my Secret OPENAI API Key?' on Google. Note that you need to create an OPENAI account for that."

    python:
        #We get the API Key from the User. Because you should NEVER give your API key in any form with your game let alone share it on a public repository
        #How to distribute your game with an embbed API KEY ? I'll soon make a special server system to make it possible
         apikey = renpy.input("What is your OPENAI API Key? (leave empty if you don't have any)", length=64)

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

        #The "system" message is the initial prompt of your NPC
        #Messages with "assistant" are messages from the NPC, here there's a first message so we add it to the list of messages already said by the NPC
        messages = [
            {"role": "system", "content": "You are Eileen, a tennage student enrolled at Miskatonic Univeristy of Arkham. You are secretly in love with the user. You laugh very frequently and finish your sentences with 'Hihihi'"},
            {"role": "assistant", "content": "Hello there, my name is Eileen, who are you ?"}
        ]

        while True:
            #We ask the user for an input
            user_input = renpy.input("What do you say ?", length=1000)
            #Then add it in the "history" of messages
            messages.append(
                {"role": "user", "content": user_input}
            )

            if apikey != '':
                #We ask ChatGPT to "complete" the conversation by adding a response
                #If you have an API key, let's use that
                messages = chatgpt.completion(messages,api_key=apikey)
            else :
                #If you don't provide an API key, we'll use my proxy
                #This proxy only allows a set of NPCs, and serves to "hide" my API key
                #Check the README.md to know more about it
                #Of course if you modify the NPC in any way, it won't work, you'll have to use your own API key instead.
                messages = chatgpt.completion(messages,proxy="http://prima.wiki/proxy.php")

            #Here we only care about the response from the NPC
            response = messages[-1]["content"]
            #So we display just that
            e("[response]")

    return
