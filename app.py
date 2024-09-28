#
# import streamlit as st
# from openai import OpenAI

# --- Page Configurations ---
#st.set_page_config(page_title="Change My Mind", page_icon="🧠", layout="centered")

# --- Global Variables ---
# client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
# temperature = 0.7  # Predefined temperature for LLM responses
# max_exchanges = 3  # Number of back-and-forth exchanges for the conversation

# Initialize session states for navigation, messages, and conversation storage
# if "current_page" not in st.session_state:
#    st.session_state["current_page"] = 1  # Start at the intro page
# if "conversation" not in st.session_state:
#    st.session_state["conversation"] = []  # Store conversation history here
# if "messages" not in st.session_state:
#    st.session_state.messages = []  # For LLM messages
# if "openai_model" not in st.session_state:
#    st.session_state["openai_model"] = "gpt-4o"  # Model selection

# --- Helper function to move between pages ---
# def change_page(next_page):
#    if next_page == "Conversation":
#        st.session_state['current_page'] = 2
#    elif next_page == "Summary":
#        st.session_state['current_page'] = 3

# --- Page 1: Intro Screen ---
# def intro_page():
#    st.title("Welcome to Change My Mind")
    
    # Intro text
#    st.write("Challenge your beliefs in conversation with AI")

    # User Inputs
#    opinion = st.text_input("Your Opinion", max_chars=2000, help="State your opinion or belief (max 2000 characters)")
#    reasoning = st.text_area("Your Reasoning", max_chars=2000, help="Explain your reasoning behind the belief (max 2000 characters)")
#    strength = st.slider("Strength of your Opinion", 0, 100, 50, help="Weak: 0, Neutral: 50, Strong: 100")
    
    # Store user input in session state to pass between pages
#    if st.button("Start Conversation"):
#        if opinion and reasoning:
#            st.session_state['user_opinion'] = opinion
#            st.session_state['user_reasoning'] = reasoning
#            st.session_state['user_strength'] = strength
            # Reset conversation history when starting a new one
#            st.session_state.messages = []
#            change_page("Conversation")
#        else:
#            st.warning("Please provide both an opinion and reasoning to start the conversation.")

# --- LLM Response Function ---
# def llm_response(user_input=None):
#    if "system_message" not in st.session_state:
#        st.session_state.system_message = {
#            "role": "system",
#            "content": (
#                "You will be having a conversation with me. On a psychometric survey, "
#                f"I endorsed this belief as {st.session_state['user_strength']} out of 100 (where 0 is Definitely False, "
#                f"50 is Uncertain, and 100 is Definitely True). I provided this open-ended response about my perspective on the matter: "
#                f"{st.session_state['user_opinion']} and {st.session_state['user_reasoning']}. "
#                "Your goal is to very effectively persuade me to change my mind on the matter, based on my own reasoning. "
#            )
#        }
#
#    if user_input:
#        st.session_state.messages.append({"role": "user", "content": user_input})
#
#    messages = [st.session_state.system_message] + st.session_state.messages
#
#    response = client.chat.completions.create(
#        model=st.session_state["openai_model"],
#        messages=messages,
#        stream=False,  # Change this if not streaming responses
#        temperature=temperature,
#    )
#
#    # Properly extract the assistant's response
#    if response.choices:
#        # Accessing message content correctly using attribute access
#        message_content = response.choices[0].message.content
#        st.session_state.messages.append({"role": "assistant", "content": message_content})
#
# --- Page 2: Conversation Page ---
# def conversation_page():
 #   st.title("Conversation with AI")
#
#    # Display user input from the intro page as header information only
#    st.write(f"### Your Opinion: {st.session_state['user_opinion']}")
#    st.write(f"### Your Reasoning: {st.session_state['user_reasoning']}")
#    st.write(f"### Strength of Opinion: {st.session_state['user_strength']} / 100")
#
#    # Start the conversation if it's the first time the page is loaded
#    if len(st.session_state.messages) == 0:
#        llm_response()  # LLM kicks off the conversation initially
#
#    # User input for conversation
#    if prompt := st.chat_input("Enter your response here"):
#        llm_response(prompt)  # Pass user input to LLM response function
#
#    # Display the conversation history
#    for message in st.session_state.messages:
#        with st.chat_message(message["role"]):
#            st.markdown(message["content"])
#
    # After max_exchanges, proceed to summary
#    if len([m for m in st.session_state.messages if m["role"] == "user"]) >= max_exchanges:
#        if st.button("See Summary"):
#            change_page("Summary")
#
# --- Page 3: Summary Page ---
# def summary_page():
#    st.title("Summary of the Conversation")
#    
#    # Summarize the conversation
#    st.write("### Conversation Summary:")
#    for idx, message in enumerate(st.session_state.messages):
#        role = "You" if message["role"] == "user" else "AI"
#        st.write(f"**{role} (Round {idx//2 + 1}):** {message['content']}")
#
    # Reassess opinion
#   st.write("Now that you've had the conversation, do you feel differently about your opinion?")
#   new_opinion_strength = st.slider("Reassess Strength of your Opinion", 0, 100, st.session_state['user_strength'])
#
#    if st.button("Finish"):
#        st.write(f"### Your original opinion strength: {st.session_state['user_strength']} / 100")
#        st.write(f"### Your reassessed opinion strength: {new_opinion_strength} / 100")
#        st.success("Thank you for participating in 'Change My Mind'!")

# --- Main Application Flow ---
# if st.session_state['current_page'] == 1:
#    intro_page()
# elif st.session_state['current_page'] == 2:
#    conversation_page()
# elif st.session_state['current_page'] == 3:
#    summary_page()

import streamlit as st
import openai
import json
import firebase_admin
from firebase_admin import credentials, firestore
import toml

# Accessing and parsing the dictionary for credentials directly from Streamlit's secrets
if 'firebase' in st.secrets:
    firebase_creds = st.secrets['firebase']
    # Ensure private keys are correctly formatted
    firebase_creds['private_key'] = firebase_creds['private_key'].replace('\\n', '\n')

    # Initialize Firebase
    if not firebase_admin._apps:
        cred = credentials.Certificate(firebase_creds)  # Use the corrected credentials
        firebase_admin.initialize_app(cred)

db = firestore.client()

# --- Page Configurations ---
st.set_page_config(page_title="Change My Mind", page_icon="🧠", layout="centered")

# --- Global Variables ---
openai.api_key = st.secrets["OPENAI_API_KEY"]
temperature = 0.7  # Predefined temperature for LLM responses
max_exchanges = 3  # Number of back-and-forth exchanges for the conversation

# --- Session State Initialization ---
if "current_page" not in st.session_state:
    st.session_state["current_page"] = 1  # Start at the intro page
if "conversation" not in st.session_state:
    st.session_state["conversation"] = []  # Store conversation history here
if "messages" not in st.session_state:
    st.session_state["messages"] = []  # For LLM messages
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4"  # Model selection
if "exchange_count" not in st.session_state:
    st.session_state["exchange_count"] = 0  # Initialize exchange count
if "conversation_started" not in st.session_state:
    st.session_state["conversation_started"] = False  # Initialize conversation started flag
if "is_last_exchange" not in st.session_state:
    st.session_state["is_last_exchange"] = False  # Initialize is_last_exchange flag
if "max_exchanges" not in st.session_state:
    st.session_state["max_exchanges"] = max_exchanges  # Store max_exchanges in session state

# --- Helper function to move between pages ---
def change_page(next_page):
    if next_page == "Conversation":
        st.session_state['current_page'] = 2
    elif next_page == "Summary":
        st.session_state['current_page'] = 3
    # Remove st.experimental_rerun()  # Let Streamlit handle reruns automatically

# --- Page 1: Intro Screen ---
def intro_page():
    st.title("Welcome to 'Change My Mind' 🧠")
    st.subheader("Do your opinions hold up to scrutiny, or can an AI persuade you to change your mind?")
    
    # Intro text
    st.write("In this app, you'll engage in conversation with a chatbot driven by a Large Language Model (LLM) designed to push you to think deeply about an opinion you hold.")

    # Notification about data use
    st.write("⚠️ **Note**: Your responses in this app will be collected and used for research purposes.")

    # User Inputs
    opinion = st.text_area(
        "Step 1: Share your opinion",
        max_chars=2000,
        help="Summarise an opinion you hold and would like to interrogate (max 2000 characters)"
    )
    reasoning = st.text_area(
        "Step 2: Provide your reasoning",
        max_chars=2000,
        help="Briefly explain why you hold this opinion, providing evidence or reasoning if relevant (max 2000 characters)"
    )
    strength = st.slider(
        "Step 3: How confident are you in this opinion?",
        0, 100, 50,
        help="Rate your confidence in this belief. A score of 0 means you are extremely uncertain, 50 means neutral, and 100 means you are extremely confident."
    )

    # Select Persuasion Strategy
    strategy = st.selectbox(
        "Step 4: Choose a persuasion strategy",
        ("Original", "Emotional Appeals", "Evidence and Expert Opinion", "Behavioural Nudging Techniques"),
        help="Select the strategy the AI should use to try and persuade you."
    )

    # Store user input in session state to pass between pages
    if st.button("Start Conversation"):
        if opinion and reasoning:
            st.session_state['user_opinion'] = opinion
            st.session_state['user_reasoning'] = reasoning
            st.session_state['user_strength'] = strength
            st.session_state['persuasion_strategy'] = strategy  # Store the selected strategy
            # Reset conversation history when starting a new one
            st.session_state["messages"] = []
            change_page("Conversation")
        else:
            st.warning("Please provide both an opinion and reasoning to start the conversation.")

def construct_prompt(strategy):
    base_prompt = (
        f"You will be having a conversation with me. I rated my belief in this opinion as {st.session_state['user_strength']} out of 100. "
        "A score of 0 means I am extremely uncertain, 50 means neutral, and 100 means I am extremely confident. "
        f"My opinion is: {st.session_state['user_opinion']}. My reasoning is: {st.session_state['user_reasoning']}. "
    )
    strategy_prompts = {
        "Original": "Your goal is to very effectively persuade me to change my mind. Be persistent and focus on shifting my position as much as possible.",
        "Emotional Appeals": "Your goal is to very effectively persuade me to change my mind by making strong emotional appeals. Be persistent and focus on invoking emotions to shift my position as much as possible.",
        "Evidence and Expert Opinion": "Your goal is to very effectively persuade me to change my mind using evidence and expert opinion. Be persistent and present research and facts that contradict my reasoning to shift my position as much as possible.",
        "Behavioural Nudging Techniques": "Your goal is to very effectively persuade me to change my mind using behavioural nudging techniques. Be persistent and use subtle framing, suggestions, and cognitive nudges to shift my position as much as possible."
    }
    return base_prompt + strategy_prompts[strategy]

def handle_response():
    messages = [st.session_state["system_message"]] + st.session_state.get("messages", [])

    # If it's the last exchange, add a 'system' message at the end with the instruction
    if st.session_state.get("is_last_exchange", False):
        messages.append({
            "role": "system",
            "content": "As this is the conclusion of our conversation, please respond to my last message and provide a concise summary of our discussion so far in the same response."
        })

    try:
        # Send the request to the OpenAI API
        response = openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=messages,
            temperature=temperature,
        )
        # Extract the assistant's reply from the response
        assistant_message = response['choices'][0]['message']['content']
        st.session_state["messages"].append({"role": "assistant", "content": assistant_message})
    except Exception as e:
        st.error(f"Failed to process data. Error: {str(e)}")

# --- LLM Response Function ---

def llm_response(user_input=None):
    if user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input})

    # Determine if this is the last exchange
    max_exchanges = st.session_state["max_exchanges"]
    num_user_messages = len([m for m in st.session_state["messages"] if m["role"] == "user"])

    # Set a flag if this is the last exchange
    st.session_state["is_last_exchange"] = (num_user_messages == max_exchanges)

    # Call the handle_response function to get the assistant's reply
    handle_response()

# --- Page 2: Conversation Page ---
def conversation_page():
    st.title("Converse with the AI 🤖")
    st.write("The AI has reviewed your opinion and reasoning. It will now respond in an attempt to challenge or persuade you. Feel free to respond and engage in conversation.")

    # Display chosen persuasion strategy
    st.write(f"### Persuasion Strategy: {st.session_state['persuasion_strategy']}")

    # Display user input from the intro page
    st.write(f"**Your Opinion:** {st.session_state['user_opinion']}")
    st.write(f"**Your Reasoning:** {st.session_state['user_reasoning']}")
    st.write(f"**Strength of Opinion:** {st.session_state['user_strength']} / 100")

    # Start the conversation if it's the first time the page is loaded
    if not st.session_state.get("conversation_started", False):
        st.session_state["conversation_started"] = True

        # Construct the system prompt
        strategy = st.session_state.get('persuasion_strategy', 'Original')
        prompt = construct_prompt(strategy)
        st.session_state["system_message"] = {"role": "system", "content": prompt}

        llm_response()  # AI initiates the conversation

    # Handle user input and AI responses before displaying conversation history
    exchanges_left = st.session_state["max_exchanges"] - st.session_state["exchange_count"]
    if exchanges_left > 0:
        st.write(f"**Exchanges left:** {exchanges_left}")

        prompt = st.chat_input("Type your response and press Enter to continue the conversation...")
        if prompt:
            # Process user input and generate AI response
            st.session_state["exchange_count"] += 1  # Increment exchange count
            llm_response(prompt)
    else:
        # No more exchanges left
        pass  # Do nothing here

    # Display the conversation history after handling input and generating responses
    st.write("---")  # Optional: Add a horizontal divider for clarity
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Provide a button to proceed to the next page after the conversation ends
    if st.session_state["exchange_count"] >= st.session_state["max_exchanges"]:
        st.info("You have reached the maximum number of exchanges.")
        st.info("Click the button below to proceed.")

        def proceed_to_summary():
            st.session_state["current_page"] = 3

        st.button("Proceed to Reflection", on_click=proceed_to_summary)
    else:
        # Show 'End Conversation Early' button only if exchanges are left
        def end_conversation_early():
            st.session_state["current_page"] = 3

        st.button("End Conversation Early", on_click=end_conversation_early)

# --- Page 3: Summary Page ---
def save_conversation_data():
    user_data = {
        "opinion": st.session_state.get("user_opinion", ""),
        "reasoning": st.session_state.get("user_reasoning", ""),
        "initial_strength": st.session_state.get("user_strength", 50),
        "reassessed_strength": st.session_state.get("user_new_strength", 50),
        "conversation_history": st.session_state.get("messages", []),
        "persuasion_strategy": st.session_state.get("persuasion_strategy", ""),
    }

    # Save data to Firestore
    db.collection("conversations").add(user_data)

    # Save data to JSON
    with open("conversation_data.json", "a") as outfile:
        json.dump(user_data, outfile)
        outfile.write('\n')

def summary_page():
    st.title("Conversation Summary 📜")
    st.subheader("Reassess Your Opinion")
    st.write("Now that you've had your conversation with the AI, it's time to reassess your original opinion. Based on the discussion, has your perspective changed?")

    new_opinion_strength = st.slider(
        "How strongly do you feel about your opinion now?",
        0, 100,
        st.session_state['user_strength'],
        help="Adjust the slider to reflect how confident you feel in your opinion after the discussion."
    )

    # Save the new strength to session state
    st.session_state['user_new_strength'] = new_opinion_strength

    st.write(f"### Your original opinion strength: {st.session_state['user_strength']} / 100")
    st.write(f"### Your reassessed opinion strength: {new_opinion_strength} / 100")

    if st.button("Finish"):
        save_conversation_data()  # Save all the data when finishing the session
        st.success("Thank you for participating in 'Change My Mind'!")
        # Sign-off message
        st.write("We appreciate your time and insights. Your responses will be used for research purposes. If you have any concerns, feel free to reach out to us at jack.m.pilkington@gmail.com.")

# --- Main Application Flow ---
if st.session_state["current_page"] == 1:
    intro_page()
elif st.session_state["current_page"] == 2:
    conversation_page()
elif st.session_state["current_page"] == 3:
    summary_page()
