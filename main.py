import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI

template = """
    Below is a draft text that may be poorly worded
    - Properly redact the draft text
    - Convert the draft text to a specified tone
    - Convert the draft text to a specified dialect

    Here are some examples different Tones:
    - Formal: Greetings! OpenAI has announced that Sam Altman is rejoining the company as its Chief Executive Officer. After a period of five days of conversations, discussions, and deliberations, the decision to bring back Altman, who had been previously dismissed, has been made. We are delighted to welcome Sam back to OpenAI.
    - Informal: Hey everyone, it's been a wild week! We've got some exciting news to share - Sam Altman is back at OpenAI, taking up the role of chief executive. After a bunch of intense talks, debates, and convincing, Altman is making his triumphant return to the AI startup he co-founded.  

    Here are some examples of words in different dialects:
    - American: French Fries, cotton candy, apartment, garbage, \
        cookie, green thumb, parking lot, pants, windshield
    - British: chips, candyfloss, flag, rubbish, biscuit, green fingers, \
        car park, trousers, windscreen

    -Turkish: patates kızartması,pamuk şeker,bayrak, çöp , bisküvi, yeşil parmaklar, \
        otopark,pantolon , ön cam

    Example Sentences from each dialect:
    - American: Greetings! OpenAI has announced that Sam Altman is rejoining the company as its Chief Executive Officer. After a period of five days of conversations, discussions, and deliberations, the decision to bring back Altman, who had been previously dismissed, has been made. We are delighted to welcome Sam back to OpenAI.
    - British: On Wednesday, OpenAI, the esteemed artificial intelligence start-up, announced that Sam Altman would be returning as its Chief Executive Officer. This decisive move follows five days of deliberation, discourse and persuasion, after Altman's abrupt departure from the company which he had co-established.
    -Turkish:Saygın yapay zeka girişimi OpenAI, Çarşamba günü Sam Altman'ın İcra Kurulu Başkanı olarak geri döneceğini duyurdu. Bu belirleyici hareket, Altman'ın birlikte kurduğu şirketten ani bir şekilde ayrılmasının ardından beş günlük müzakere, söylem ve ikna sürecinin ardından geldi.


    Below is the draft text, tone, and dialect:
    DRAFT: {draft}
    TONE: {tone}
    DIALECT: {dialect}

    YOUR {dialect} RESPONSE:

"""

prompt = PromptTemplate(
    input_variables=["tone", "draft", "dialect"],
    template=template,
)


# llm and key loading function
def load_LLM(openai_api_key):
    """logic for loading the chain you want to use should go here"""
    llm = OpenAI(temperature=0.7, api_key=openai_api_key)  # creativity
    return llm


# page title
st.set_page_config(page_title="Re-write your text")
st.header("Re-write your text")

# Intro: instructions
col1, col2 = st.columns(2)

with col1:
    st.markdown("Re-write your text in different styles.")

with col2:
    st.write("Contact with [AI Accelera](https://aiaccelera.com) to build your AI Projects")

# API_KEY
st.markdown("##Enter Your OpenAI API Key")


def get_openai_api_key():
    input_text = st.text_input(label="OpenAI API Key",
                               placeholder="Ex: sk-2twmA8tfCb8un4...",
                               key="openai_api_key_input",
                               type="password")
    return input_text


openai_api_key = get_openai_api_key()

# Input
st.markdown("Enter the text you want to re-write")


def get_draft():
    draft_text = st.text_area(label="Text", label_visibility='collapsed', placeholder="Your Text...", key="draft_input")
    return draft_text


draft_input = get_draft()

if len(draft_input.split(" ")) > 50:
    st.write("Please enter a shorter text. The maximum length is 50 words.")
    st.stop()

# prompt template tunning options
col1, col2 = st.columns(2)
with col1:
    option_tone = st.selectbox(
        'Which tone would you like your redaction to have?',
        ('Formal', 'Informal'))

with col2:
    option_dialect = st.selectbox(
        "Which Dialecet would you like to use?",
        ("Turkish", "American", "British")
    )

# Output
st.markdown("### Your Re-written text:")

if draft_input:
    if not openai_api_key:
        st.warning('Please insert OpenAI API Key. \
            Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)',
                   icon="⚠️⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_draft = prompt.format(
        tone=option_tone,
        dialect=option_dialect,
        draft=draft_input,
    )
    improved_redaction = llm(prompt=prompt_with_draft)
    st.write(improved_redaction)
