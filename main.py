from openai import OpenAI

MY_API_KEY = ""
# openai.my_api_key = YOUR_API_KEY

client = OpenAI(api_key=MY_API_KEY)
# client.

messages = [ {"role": "system", "content": "You are a intelligent assistant."} ]


message = input("User : ")
if message:
    messages.append(
        {"role": "user", "content": message},
    )
completion = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=messages
    )
reply = completion.choices[0].message.content
print(f"ChatGPT: {reply}")
# messages.append({"role": "assistant", "content": reply})