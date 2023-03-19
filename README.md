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
# Important note about OpenAI API Keys !

While developing your game, it's ok to hardcode your OpenAI API key locally to do your tests.
But.
It's very important that you never actually publish your OpenAI API key anywhere. Neither inside your game assets or on your github repo (if it's a public repo).

Because if anyone has your API Key, they can send hundreds of thousands of requests using your API key and bankrupt you.

They can also release another game that uses your API key and the requests sent by your players will be billed to you.

And nobody wants that, right ?

So, how to still publish your game and allow your players to use your API key without seeing it ?

The easiest way is for you to create a kind of "proxy" that you control and that filters what requests are ok and which requests are not OK, and this proxy will inject your API key in your requests.

For example, you could make a list of "NPC prompts" that are in your game, those are allowed, but other unrelated requests aren't allowed.

Here's a sample code for a very basic proxy.php file you could use, just create this "proxy.php" file on your_server.com so that the url of this file is http://your_server.com/proxy.php : 
```
<?php
// proxy.php

// Replace this with your own OpenAI API Key
$openai_api_key = 'your_openai_api_key_here';

// Set the OpenAI API URL
$openai_api_url = 'https://api.openai.com/v1/chat/completions';

// Get the JSON payload from the incoming request
$json_data = file_get_contents('php://input');
$data = json_decode($json_data, true);

// Check if the messages list contains any of the Authorised NPCs, feel free to modify this list with only the NPCs allowed in your game.
$authorised_npcs = array(
    array(
        "role" => "system",
        "content" => "You are Eileen, a tennage student enrolled at Miskatonic Univeristy of Arkham. You are secretly in love with the user. You laugh very frequently and finish your sentences with 'Hihihi'"
    ),
    array(
        "role" => "system",
        "content" => "You are Brother Conrad, a crazy monk scribe at the Abbey of Neuberg, you are very nervous and scratch your arms intermitently."
    ),
    array(
        "role" => "system",
        "content" => "You are the Abbot of the Abbey of Neuberg, you like gardening."
    )
);

$contains_authorised_npc = false;
if (isset($data['messages']) && is_array($data['messages'])) {
    foreach ($data['messages'] as $message) {
        if (in_array($message, $authorised_npcs)) {
            $contains_authorised_npc = true;
            break;
        }
    }
}

if ($contains_authorised_npc) {
    // Forward the request to the OpenAI API with the API key
    $ch = curl_init($openai_api_url);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'POST');
    curl_setopt($ch, CURLOPT_POSTFIELDS, $json_data);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array(
        'Content-Type: application/json',
        'Authorization: Bearer ' . $openai_api_key,
        'Content-Length: ' . strlen($json_data))
    );

    // Get the response from the OpenAI API
    $response = curl_exec($ch);

    // Check for errors and send the response
    if (curl_errno($ch)) {
        $error_msg = curl_error($ch);
        http_response_code(500);
        echo json_encode(array('error' => $error_msg));
    } else {
        http_response_code(200);
        echo $response;
    }

    // Close the cURL session
    curl_close($ch);
} else {
    // Return an error message if none of the Authorised NPCs are present
    http_response_code(400);
    echo json_encode(array('error' => 'None of the Authorised NPCs were found in the request.'));
}

```

Now in your game instead of calling : chatgpt.completion(messages,api_key=apikey), call chatgpt.completion(messages,proxy="http://your_server.com/proxy.php")

And don't forget to modify your proxy.php file each time you add a new NPC in your game.

This is just a very simple proxy.php, you may want to consider adding some rate limitations or other securities.
