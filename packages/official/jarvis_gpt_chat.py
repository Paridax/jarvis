import openai


def gpt_chat(dictionary, settings):
    # load api key
    openai.api_key = settings["openai_key"]

    # if the action is conversation then run the gpt chat
    if dictionary.get("action") == "conversation":
        chat = [{"role": "system", "content": "You are a helpful assistant who was created by DarkIndustries."}]
        print("Running gpt chat...")
        prompt = ""

        while prompt != "quit":
            prompt = input("You: ")
            # add the prompt to the chat
            chat.append({"role": "user", "content": prompt})

            result = openai.ChatCompletion.create(
                messages=chat,
                model="gpt-3.5-turbo",
                max_tokens=1000,
            )

            # add the response to the chat
            chat.append(
                {"role": "assistant", "content": result["choices"][0]["message"]["content"]}
            )
            print(f"""ChatGPT: {result["choices"][0]["message"]["content"]}""")
        return True
    return False
