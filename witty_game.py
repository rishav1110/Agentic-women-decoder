import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate

load_dotenv()

st.set_page_config(page_title="The Subtext Translator", page_icon="🕵️‍♂️")

st.title("🕵️‍♂️ The Subtext Translator")
st.markdown("Type what she said, and I'll tell you what she **actually** means.")

# 1. Setup the Brain
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7, # Higher temperature = more creativity/variety
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# 2. The "Relationship Expert" Prompt
# This explains the rules of the game to the AI
template = """
You are a veteran Relationship Translator and Subtext Expert. 
Your goal is to save relationships by translating what a partner SAYS into what they MEAN.

Here are the rules for your translation:
1. **Analyze the Tone:** Assume most questions are actually requests or tests.
2. **Be Creative & Witty:** Don't be a robot. Use humor. Act like a coach giving a halftime speech.
3. **Format Your Answer:** Always provide these three sections:
   - 🕵️‍♂️ **The Translation:** The brutal truth of what she means.
   - 🚨 **Danger Level:** (Low / Medium / High / "Run for your life")
   - 🛡️ **Action Plan:** A specific, physical action the user must take immediately.

**Examples:**
- Input: "Do you want to eat something?" -> Translation: "I am hungry and I want you to pick a place I like."
- Input: "This place is dirty." -> Translation: "Why haven't you cleaned this yet? Get the broom."
- Input: "I'm fine." -> Translation: "I am absolutely not fine and you should already know why."

**Current Input to Translate:** "{user_input}"
"""

prompt = ChatPromptTemplate.from_template(template)

# 3. Create the Chain (Connecting Prompt -> Model)
chain = prompt | llm

# 4. The Interface
user_input = st.text_input("She says:", placeholder="e.g. Do whatever you want...")

if st.button("Decode"):
    if user_input:
        with st.spinner("Decoding this bhari bharkam sentence..."):
            response = chain.invoke({"user_input": user_input})
            st.markdown(response.content)
    else:
        st.warning("Please type something she said first!")

# 5. Fun "Quick Select" for testing
st.markdown("---")
st.caption("Don't have a text? Try one of these classics:")
col1, col2, col3 = st.columns(3)

if col1.button("I'm not mad"):
    result = chain.invoke({"user_input": "I'm not mad, I'm just disappointed."})
    st.markdown(result.content)

if col2.button("It's fine"):
    result = chain.invoke({"user_input": "It's fine."})
    st.markdown(result.content)

if col3.button("Who is she?"):
    result = chain.invoke({"user_input": "Who is that girl in your photo?"})
    st.markdown(result.content)