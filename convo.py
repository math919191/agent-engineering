import streamlit as st
import asyncio

from completion import Completion

def get_file_contents(file_name):
    with open(file_name, "r") as file:
        content = file.read()
    return content

async def main(agent1, agent2, agent1_name, agent2_name, rounds, eval_agent):


    rounds_complete = 0
    while rounds_complete < rounds:
        agent1_response = await agent1.get_completion(st.session_state.messages)

        st.chat_message(agent1_name).markdown(agent1_response)
        st.session_state.messages.append({"role": agent1_name, "content": agent1_response})

        agent2_response = await agent2.get_completion(st.session_state.messages)

        st.chat_message(agent2_name).markdown(agent2_response)
        st.session_state.messages.append({"role": agent2_name, "content": agent2_response})

        rounds_complete += 1

    eval_response = await eval_agent.get_completion(st.session_state.messages)
    st.chat_message("eval").markdown(eval_response)

st.title("Echo Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

teacher = Completion(get_file_contents("prompts/student.md"), "gpt-4")
student = Completion(get_file_contents("prompts/tutor.md"),"gpt-4")

# eval = Completion(get_file_contents("prompts/eval.md") + "every message has an emoji","gpt-4")
eval = Completion(get_file_contents("prompts/eval.md") + "the tutor effectively responds to the student messages","gpt-4")

asyncio.run(main(teacher, student, "teacher", "student", 4, eval))
