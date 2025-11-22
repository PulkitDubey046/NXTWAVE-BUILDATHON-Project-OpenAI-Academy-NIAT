import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Career Guide AI", page_icon="🎓", layout="centered")

# Load API Keys
gemini_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
openai_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")

# Initialize Gemini if key available
if gemini_key:
    import google.generativeai as genai
    genai.configure(api_key=gemini_key)

# Initialize OpenAI if key available
openai_client = None
if openai_key:
    from openai import OpenAI
    openai_client = OpenAI(api_key=openai_key)


# Reset function
def reset_app():
    st.session_state.clear()
    st.experimental_rerun()


# UI
st.title("🎓 AI Career Path Recommendation")
st.subheader("46Dubey will help you find Career Path that suits you. 🤝")
st.write("---")

name = st.text_input("👤 Your Name")
edu_level = st.selectbox("🎓 Current Education Level", ["Select", "10th", "12th", "Graduate", "Postgraduate"])

stream = ""
if edu_level == "12th":
    stream = st.selectbox("📘 Select Stream", ["Select", "Science", "Commerce", "Arts"])
elif edu_level in ["Graduate", "Postgraduate"]:
    stream = st.text_input("🎯 Specialization (B.Tech, B.Com, MBA...)")

interests = st.text_area("💡 Your Interests / Favorite Subjects", placeholder="coding, creativity, marketing, public service...")
goal = st.radio("🏁 Career Preference", ["Any", "Government Sector", "Private Sector", "Entrepreneurship"])

st.write("---")


# Submit button
if st.button("🚀 Generate My Career Roadmap"):

    if edu_level == "Select" or not name:
        st.warning("⚠ Please fill all required details!")
        st.stop()

    prompt = f"""
    Analyze this student and generate a career plan:

    Name: {name}
    Education: {edu_level}
    Stream: {stream}
    Interests: {interests}
    Career Preference: {goal}

    Provide:
    1️⃣ Personalized Career Summary
    2️⃣ Top 5 Suitable Career Paths
    3️⃣ Private sector job options
    4️⃣ Government job opportunities
    5️⃣ Best courses / certifications
    6️⃣ Step-by-step Career Roadmap
    """

    with st.spinner("✨ AI is preparing your personalized roadmap..."):

        final_text = ""

        try:
            # Try Gemini FIRST
            if gemini_key:
                model = genai.GenerativeModel("gemini-2.5-flash")
                gem_resp = model.generate_content(prompt)
                final_text = gem_resp.text
                st.success("✔ Generated using Gemini 🤖")

            # If Gemini fails → use OpenAI
            elif openai_client:
                openai_resp = openai_client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[{"role": "user", "content": prompt}]
                )
                final_text = openai_resp.choices[0].message.content
                st.success("✔ Generated using OpenAI 🎯")

            else:
                st.error("❌ No API keys found — Add GEMINI_KEY or OPENAI_KEY.")
                st.stop()

            # Bonus Motivation only if Gemini available
            if gemini_key:
                motivation_prompt = f"""
                Create a short emotional motivation message for this student:

                Name: {name}
                Education Level: {edu_level}
                Stream/Specialization: {stream}
                Interests: {interests}
                Career Preference: {goal}

                Motivation style requirements:
                - Positive, encouraging and uplifting
                - Include how their strengths and interests will help them succeed
                - 4 to 6 lines short paragraph
                - Add 2 motivational emoji relevant to career
                - Address the student directly by name
                """

            motivation = genai.GenerativeModel("gemini-2.5-flash") \
                            .generate_content(motivation_prompt).text
            final_text += f"\n\n---\n\n### 🌟 Motivation\n{motivation}"

            # Final message from your requirement
            final_text += "\n\n---\n\n💙 **Thank you for choosing Team 46Dubey for your career!** 💙"

            st.markdown("### 🧭 Your AI Career Guidance")
            st.markdown(final_text)

            st.write("---")
            st.button("🔄 Start Again", on_click=reset_app)

        except Exception as e:
            st.error(f"❌ Error: {e}")


st.write("---")
st.markdown("<p style='text-align:center;'>Made with ❤️ by <b>Pulkit Dubey</b></p>", unsafe_allow_html=True)
