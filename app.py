import streamlit as st
from openai import OpenAI

st.title("🔧 Prompt Enhancer App")
st.write("Enter Role, Context, and Task to generate a high-quality prompt that you can use with any AI system.")

# Input fields
api_key = st.text_input("🔑 Enter your OpenAI API Key", type="password")
role = st.text_input("🧑 Role", placeholder="e.g. You are a data analyst")
context = st.text_area("📘 Context", placeholder="e.g. Analyzing customer churn data...")
task = st.text_area("✅ Task", placeholder="e.g. Provide insights on churn patterns...")

if st.button("Enhance My Prompt"):
    if not api_key:
        st.error("Please enter your OpenAI API key.")
    elif not (role and context and task):
        st.warning("Please fill in all fields.")
    else:
        # Create a simple prompt from user inputs
        original_prompt = (
            f"{role}\n\n"
            f"Context: {context}\n\n"
            f"Task: {task}"
        )
        
        # Create the meta-prompt to ask GPT to enhance the user's prompt
        meta_prompt = (
            "You are a prompt engineering expert. Your task is to enhance and improve the following prompt "
            "to make it more effective, clear, and likely to generate high-quality responses from AI systems. "
            "Only provide the enhanced prompt itself without any explanations, introductions, or commentary. "
            "Here's the original prompt to enhance:\n\n" + original_prompt
        )
        
        # Display a loading spinner while waiting for the API response
        with st.spinner("🔄 Enhancing your prompt..."):
            try:
                # Create OpenAI client with API key
                client = OpenAI(api_key=api_key)
                
                # Call OpenAI API to enhance the prompt
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": meta_prompt}]
                )
                
                # Get the enhanced prompt from GPT
                enhanced_prompt = response.choices[0].message.content
                
                # Output
                st.subheader("✨ Enhanced Prompt")
                st.code(enhanced_prompt, language="markdown")
                
                # Add a copy button (Streamlit has this functionality built into code blocks)
                st.success("✅ Your prompt has been enhanced! You can copy it using the button in the top-right corner of the code block above.")
            
            except Exception as e:
                st.error(f"An error occurred: {e}")