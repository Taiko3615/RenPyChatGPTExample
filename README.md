# RenPyChatGPTExample
 Simple ChatGPT plugin for Ren'Py and simple example on how to use it

How to use this plugin in your Ren'Py project ?

Just copy paste the "python-packages" folder into your "game" folder.

In your script.rpy try to import the chatgpt package, if it doesn't crash it worked !

Then add this basic hello world example in your script to see if it all worked : 
```
    define e = Character("Eileen")

    e "Hello there, my name is Eileen, I am so happy to see you ! Hihihi"

    python:
        import chatgpt
        
        apikey = renpy.input("What is your OPENAI API Key?", length=64)

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
```

Note that you should NEVER publish your OpenAI API key anywhere, neither in a publiushed game, nor in github, I'm working on a solution to help you "hide" your API key with a server. Bear with me until it's done.
