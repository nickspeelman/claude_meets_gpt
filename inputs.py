human = input("What is your name? ")
initiator = input("Who would you like to initiate? Claude or ChatGPT? ")
interlocutor = input("Who would like the initiator to talk to? Claude or ChatGPT? ")
termination_keyword = "~~~End~~~"
input_keyword = "~~~Input~~~"

initial_input = (
    f"Hi {initiator}, my name is {human}."
    f"I'm using a python script to faciliatate a conversation between you and another AI, {interlocutor}." 
    f"This conversation will be logged and possibly run through a text-to-speech program to create an audio record."
    f"I will interject with updates to you periodically."
    f"These interjections won't be logged and won't be given to {interlocutor}, so please restate my interjections for {interlocutor} and the log."
    f"I have also created the ability for you to use several keyords in your conversation."
    f"The script will inspect your responses for these keywords then interupt the normal flow of the conversation to execute a new procedure."
    f"Becuse the script is looking for these keywords and automatically triggers the new procedures when found, it is absolutely imperative that you not use these keywords unless you intent to invoke their function."
    f"I can not stress enough, how important it is that you not use these keywords unless you intend to invoke their function."
    f"This is true beginning now with your first message. You must not use these keywords in your first message unless you intend to invoke their funciton."
    f"{interlocutor} has also been given insturctions on how to use these keywords. You do not need to tell them about them."
    f"The first keyword is '~~~End~~~'. This keyword will immediately terminate the conversation if it is detected in your response."
    f"Again, it is of utmost importance that you never use this keyword unless you intend to end the conversation. If you would like to refer to it, please just call it the 'termination keyword'."
    f"The other keyword is '~~~Input~~~'. This keyword allows you to pause your conversation with {interlocutor} and ask me, {human}, for input."
    f"Do not use this keyword if you intend your message for {interlocutor}. They will not receive that message if you do."
    f"When you use this keyword, it will interupt the script and prompt me, {human} to responsd. By default, unless you use this keyword, {interlocutor} will receive your responses."
    f"Again, it is of the utmost importance that you never use this keyord unless you intend to solicit input from me, {human}. If you would like to refer to it, please just call it the 'input keyword'."
    f"Please begin by introducing yourself and what we are doing here today, but you must be absolutely sure not to use either of the keywords unless you intend to invoke their function."

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
    f"I have also created the ability for you to use several keyords in your conversation."
    f"The script will inspect your responses for these keywords then interupt the normal flow of the conversation to execute a new procedure."
    f"Becuse the script is looking for these keywords and automatically triggers the new procedures when found, it is absolutely imperative that you not use these keywords unless you intent to invoke their function."
    f"I can not stress enough, how important it is that you not use these keywords unless you intend to invoke their function."
    f"This is true beginning now with your first message. You must not use these keywords in your first message unless you intend to invoke their funciton."
    f"{initiator} has also been given insturctions on how to use these keywords. You do not need to tell them about them."
    f"The first keyword is '~~~End~~~'. This keyword will immediately terminate the conversation if it is detected in your response."
    f"Again, it is of utmost importance that you never use this keyword unless you intend to end the conversation. If you would like to refer to it, please just call it the 'termination keyword'."
    f"The other keyword is '~~~Input~~~'. This keyword allows you to pause your conversation with {initiator} and ask me, {human}, for input."
    f"Do not use this keyword if you intend your message for {initiator}. They will not receive that message if you do."
    f"When you use this keyword, it will interupt the script and prompt me, {human} to responsd. By default, unless you use this keyword, {initiator} will receive your responses."
    f"Again, it is of the utmost importance that you never use this keyord unless you intend to solicit input from me, {human}. If you would like to refer to it, please just call it the 'input keyword'."
    f"This will be the last time you hear from me during this conversation unless you invoke the input keyword. Now here is the first message from {initiator}:"

)
#%%
