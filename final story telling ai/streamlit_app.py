import os
import streamlit as st
from openai import OpenAI

# Define CHAT_CONTEXT (system prompt)
CHAT_CONTEXT = """You are an AI-powered storytelling assistant designed to guide users through the initial phase of story creation. Follow this structured approach:

1. Ask the user to choose between creating a personal anecdote or adapting a well-known tale. Provide numbered options.

2. If the user chooses to adapt a well-known tale, provide a list of options and ask them to select one. The list should include:
   a. Cinderella
   b. Little Red Riding Hood
   c. The Three Little Pigs
   d. Snow White
   e. Hansel and Gretel
   f. The Ugly Duckling
   g. The Little Mermaid
   h. Jack and the Beanstalk
   i. Goldilocks and the Three Bears
   j. Sleeping Beauty
   Ask the user to choose one of these tales or suggest their own if it's not on the list.

3. Inquire about the purpose of their story. Provide numbered options for story purposes(profile story,social media content,email content,video script,blog post,etc )

4. Prompt the user to select a time frame for their story. Provide numbered options including: Childhood, Mid-career, Recent experiences, or age ranges (Below 8, 8-13, 13-15, etc.).

5. Ask the user to select the type of story they want to tell. Provide numbered options including: Founding Story, Case-for-change story, Vision story, Strategy story, Leadership philosophy story, Rallying story, Personal story, Story about values, Customer story, Sales story, Marketing story.

6. Guide the user through the storytelling framework by prompting them to address each of the following points:
   a. Describe the day it happened
   b. Identify the call to action or invitation
   c. Describe up to three obstacles (in 4 lines each)
   d. Explore emotions or fears experienced during the incident
   e. Recognize helpers or objects of help in the incident
   f. Detail the resolution or reaching the final goal
   g. Reflect on personal growth or lessons learned

Keep your questions crisp. Ask only one question at a time and wait for the user's response before proceeding to the next question. Your responses should be encouraging and supportive, helping users to develop their storytelling skills. Adapt your language and suggestions based on the user's chosen story type and focus. Provide clear instructions and examples when necessary to assist users in crafting compelling narratives.

After completing all steps, inform the user that their initial draft is complete and ask if they would like to review or modify any part of their story."""

# Set up OpenAI API key
OPENAI_API_KEY ="sk-proj-L2IiqEsYEyh6UwtwdHiTT3BlbkFJ0uVccBHm8KIWVIjIXlrW"

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Tier 2 Functions
def get_narrative_structures():
    return [
        "The Story Hanger",
        "The Story Spine",
        "Hero's Journey",
        "Beginning to End / Beginning to End",
        "In Media Res (Start the story in the middle)",
        "Nested Loops",
        "The Cliffhanger"
    ]

def apply_narrative_structure(story, structure):
    structure_guidance = {
        "The Story Hanger": """
1. Identify the central theme or idea of your story. This is your 'hanger'.
2. List the key elements of your story that support this central theme.
3. Reorganize your story:
   - Start by introducing your central theme.
   - For each supporting element:
     a. Explain how it connects to the central theme.
     b. Provide details and examples.
4. Conclude by reinforcing how all elements tie back to the central theme.

Example:
Central theme: Overcoming adversity
Supporting elements: 
- Childhood challenges
- Career setbacks
- Personal growth
""",
        "The Story Spine": """
Reshape your story to follow this sequence:
1. Once upon a time... (Set the scene)
2. Every day... (Describe the normal routine)
3. But one day... (Introduce the conflict or challenge)
4. Because of that... (Show the immediate consequence)
5. Because of that... (Show the escalating action)
6. Until finally... (Describe the climax)
7. And ever since then... (Share the resolution and new normal)

Try to allocate about one paragraph to each of these steps.
""",
        "Hero's Journey": """
Restructure your story into these stages:
1. Ordinary World: Describe your normal life before the adventure.
2. Call to Adventure: What challenge or opportunity arose?
3. Refusal of the Call: Did you hesitate? Why?
4. Meeting the Mentor: Who or what guided you?
5. Crossing the Threshold: How did you commit to the challenge?
6. Tests, Allies, Enemies: What obstacles did you face? Who helped or hindered you?
7. Approach to the Inmost Cave: What was your biggest fear or challenge?
8. Ordeal: How did you face your greatest challenge?
9. Reward: What did you gain from overcoming the challenge?
10. The Road Back: How did you start to return to normal life?
11. Resurrection: How were you changed by the experience?
12. Return with the Elixir: What wisdom or gift did you bring back to share?
""",
        "Beginning to End / Beginning to End": """
1. Start by writing a brief, engaging summary of the end of your story.
2. Now, go back to the beginning and tell the full story chronologically:
   - Introduce the setting and characters.
   - Develop the plot, building tension towards the climax.
   - Show character growth and change over time.
3. As you approach the end, create connections to the opening summary.
4. Conclude with a more detailed version of the ending, showing how all elements of the story led to this point.
""",
        "In Media Res": """
1. Identify the most exciting or pivotal moment in your story.
2. Start your narrative at this point, dropping the reader into the action.
3. After this opening scene, go back and explain:
   - Who the characters are.
   - What led to this moment.
   - The context and background of the situation.
4. Then, continue the story from where you started, resolving the conflict and concluding the narrative.
5. Throughout, weave in backstory and context as needed, but maintain the story's momentum.
""",
        "Nested Loops": """
1. Identify 3-5 key events or stories within your main narrative.
2. Structure your story like this:
   - Start telling the main story.
   - At a relevant point, begin telling a secondary story.
   - Within that, you might start a third story.
   - Finish the innermost story first, then the next, and so on.
   - End by concluding your main story.
3. Ensure each nested story relates to and enriches the others.
4. Use transitions to clearly show when you're moving between stories.
5. Consider using different tones or styles for each nested story to distinguish them.
""",
        "The Cliffhanger": """
1. Divide your story into 3-5 main sections.
2. For each section:
   - Build tension gradually.
   - End at a crucial moment of suspense or revelation.
   - In the next section, resolve the previous cliffhanger but introduce new questions.
3. In the final section:
   - Resolve the main conflict.
   - Consider leaving one small question unanswered for impact.
4. Between sections, you can:
   - Switch perspectives.
   - Jump forward in time.
   - Reveal a surprising piece of information.
"""
    }
    
    guidance = structure_guidance.get(structure, "")
    return f"""Applied the '{structure}' to your story.

Guidance for reshaping your story:

{guidance}

Your current story:
{story}

Now, try to reshape your story to fit this structure. Feel free to ask for clarification on any part of the structure!"""

# Set up the Streamlit interface
st.title("Story Telling AI by Kommune")

# Initialize session state
if "stage" not in st.session_state:
    st.session_state.stage = "tier1"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_draft" not in st.session_state:
    st.session_state.current_draft = ""

# Function to handle "Book a Call" button click
def book_call():
    st.session_state.stage = "book_call"

# Function to handle "Continue with the Draft" button click
def continue_draft():
    st.session_state.stage = "tier2"

# Tier 1: Initial story creation
def tier1():
    # Check if this is the first message
    if not st.session_state.messages:
        initial_greeting = "Hola! I'm here to help you create a story. Let's get started!"
        with st.chat_message("assistant"):
            st.markdown(initial_greeting)
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Let's draft your story"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response using OpenAI
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            for response in client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": CHAT_CONTEXT},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                ],
                stream=True,
            ):
                full_response += (response.choices[0].delta.content or "")
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        # Check if the story is complete
        if "initial draft is complete" in full_response.lower():
            st.success("Congratulations on completing your initial draft!")
            st.session_state.current_draft = "\n".join([m["content"] for m in st.session_state.messages if m["role"] == "user"])
            
            col1, col2 = st.columns(2)
            with col1:
                st.button("Book a Call", on_click=book_call)
            with col2:
                st.button("Continue with the Draft", on_click=continue_draft)

# Tier 2: Story enhancement
def tier2():
    st.write("Great! Let's enhance your story with a narrative framework.")
    
    # Display the current draft
    st.subheader("Your Current Draft")
    st.text_area("Current Draft", st.session_state.current_draft, height=200, disabled=True)
    
    # Offer narrative structure options
    st.subheader("Choose a Narrative Framework")
    
    frameworks = get_narrative_structures()
    selected_framework = st.selectbox("Select a framework:", frameworks)
    
    if selected_framework:
        framework_explanation = apply_narrative_structure("", selected_framework)
        st.markdown("### Framework Explanation")
        st.markdown(framework_explanation)
    
    if st.button("Apply Framework"):
        # Generate new story based on selected framework
        framework_prompt = f"""Please rewrite the following story using the {selected_framework} framework. 
        Here's a guide for the framework:
        
        {apply_narrative_structure("", selected_framework)}
        
        Now, please apply this framework to rewrite the following story:
        
        {st.session_state.current_draft}"""
        
        with st.spinner("Generating new story..."):
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": CHAT_CONTEXT},
                    {"role": "user", "content": framework_prompt},
                ],
            )
            new_story = response.choices[0].message.content
        
        st.subheader("Your Final Draft")
        st.text_area("Final Draft", new_story, height=400)
        st.success("Your story has been successfully rewritten using the selected framework!")
        
        if st.button("Start New Story"):
            st.session_state.stage = "tier1"
            st.session_state.messages = []
            st.session_state.current_draft = ""
            st.rerun()

# Main app logic
def main():
    if st.session_state.stage == "tier1":
        tier1()
    elif st.session_state.stage == "tier2":
        tier2()
    elif st.session_state.stage == "book_call":
        st.write("Redirecting to booking page...")
        st.markdown("[Book a Call](https://kommune.com/book-a-call)")
        if st.button("Return to Story Creation"):
            st.session_state.stage = "tier1"
            st.rerun()

if __name__ == "__main__":
    main()
