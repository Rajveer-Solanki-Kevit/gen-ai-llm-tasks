import streamlit as st
from codegen.generator import generate_code
from codegen.tester import test_code, clean_code

st.set_page_config(page_title="AI Code Generator", layout="wide")

st.title("Minimal AI Code Project Generator")
st.markdown(
    "Enter a description of a coding task.")

prompt = st.text_area(
    "Enter your task description:",
    height=100,
    placeholder="e.g., Write a Python function that checks if a number is prime."
)

if st.button("Generate Code"):
    if not prompt.strip():
        st.warning("Please enter a valid prompt.")
    else:
        feedback_placeholder = st.empty()
        code_placeholder = st.empty()
        result_placeholder = st.empty()

        base_prompt = f"""
        You are an expert Python developer.
        Write a Python function for the following task:
        {prompt}

        The code must define a valid function name.
        Only output valid Python code, no explanations.
        """

        code = None
        passed = False
        feedback = ""
        max_attempts = 3

        for attempt in range(1, max_attempts + 1):
            feedback_placeholder.info(f"Attempt {attempt} of {max_attempts}: Generating code...")

            try:
                raw_code = generate_code(
                    base_prompt if attempt == 1 else base_prompt + f"\nFix the following issue: {feedback}")
            except Exception as e:
                st.error(f"Error while generating code: {e}")
                break

            code = clean_code(raw_code)
            if not code:
                st.error("No code returned by the generator.")
                break
            code_placeholder.code(code, language="python")

            try:
                passed, feedback = test_code(code)
            except Exception as e:
                st.error(f"Error while testing code: {e}")
                break

            result_placeholder.write(f"**Test Result:** {feedback}")

            if passed:
                st.success("Code passed all tests!")
                break
            else:
                feedback_placeholder.warning(f"Regenerating : {feedback}")

        else:
            st.error("Failed after 3 attempts.")
