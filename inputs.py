human = input("What is your name? ")
initiator = input("Who would you like to initiate? Claude or ChatGPT? ")
interlocutor = input("Who would like the initiator to talk to? Claude or ChatGPT? ")
termination_keyword = "~~~End~~~"  # Define the termination keyword

initial_input = (
    f"Hi {initiator}, my name is {human}."
    f"I'm using a python script to faciliatate a conversation between you and another AI, {interlocutor}." 
    f"This conversation will be logged and possibly run through a text-to-speech program to create an audio record."
    f"I will interject with updates to you periodically."
    f"These interjections won't be logged and won't be given to {interlocutor}, so please restate my interjections for {interlocutor} and the log."
    f"If you would ever like to end the conversation just use the keyword {termination_keyword} in your response and the script will terminate."
    f"It is absolutely imperative you not use that keyword unless you intend to end the conversation."
    f"The script inspects your responses for it and will terminate the conversation automatically."
    f"Your conversant has also been informed of the keyword so you should not provide it to them, as doing so will terminate the script."
    f"Please begin by introducing yourself and what we are doing here today."

)

interupt_input = (
    f"Hi {initiator}, this is {human}. I'm just interjecting here to let you know this conversation is programmed to come to an end soon."
    f"Please start tying up any lose ends. Per my initial instructions, please restate this interjection for the log and {interlocutor}."
    f"Now here is their most recent message:"

)

final_interupt_input = (
    f"Hi {initiator}, this is {human} again. Just letting you know this will be your last message if you would like to provide any final thoughts. "
    f"Here is their most recent message:"
)

reassurance_input = (
    f"Hi {interlocutor}, my name is {human}. I'm using a Python script to facilate a conversation between you and another AI, {initiator}."
    f"I will be giving them periodic updates throughout the conversation and have asked them to pass those updates on to you."
    f"If you would ever like to end the conversation just use the keyword {termination_keyword} in your response and the script will terminate."
    f"It is absolutely imperative you not use that keyword unless you intend to end the conversation."
    f"The script inspects your responses for it and will terminate the conversation automatically."
    f"Your conversant has also been informed of the keyword so you should not provide it to them, as doing so will terminate the script."
    f"This will be the last time you hear from me during this conversation. Now here is the first message from {initiator}:"

)
#%%
