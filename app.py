import os
import streamlit as st
from dotenv import load_dotenv
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
import markdown2

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


# Reset App
def reset_app():
    st.session_state.clear()
    st.rerun()


# UI
st.title("🎓 AI Career Path Recommendation")
st.subheader("46Dubey will help you find Career Path that suits YOU 🤝")
st.write("---")

name = st.text_input("👤 Your Name")
edu_level = st.selectbox("🎓 Current Education Level", ["Select", "10th", "12th", "Graduate", "Postgraduate"])

stream = ""
if edu_level == "12th":
    stream = st.selectbox("📘 Select Stream", ["Select", "Science", "Commerce", "Arts"])
elif edu_level in ["Graduate", "Postgraduate"]:
    stream = st.text_input("🎯 Specialization (B.Tech, B.Com, MBA...)")

interests = st.text_area("💡 Your Interests / Favorite Subjects", placeholder="coding, creativity, marketing...")
goal = st.radio("🏁 Career Preference", ["Any", "Government Sector", "Private Sector", "Entrepreneurship"])

st.write("---")

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
            if gemini_key:
                model = genai.GenerativeModel("gemini-2.5-flash")
                gem_resp = model.generate_content(prompt)
                final_text = gem_resp.text
                st.success("✔ Generated using Gemini 🤖")

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

            # Motivation Add-on
            if gemini_key:
                motivation_prompt = f"""
                Write a short, uplifting motivational message for:
                Name: {name}
                Use 4–6 lines with emojis.
                """
                motivation = genai.GenerativeModel("gemini-2.5-flash") \
                    .generate_content(motivation_prompt).text
                final_text += f"\n\n### 🌟 Motivation\n{motivation}"

            final_text += "\n\n---\n\n💙 **Thank you for choosing Team 46Dubey for your career!** 💙"

            st.markdown("### 🧭 Your AI Career Guidance")
            st.markdown(final_text)

           # ---------------- PDF EXPORT ----------------
            pdf_buffer = BytesIO()

            # Register readable text font + Emoji font
            pdfmetrics.registerFont(TTFont("TextFont", "Roboto-Regular.ttf"))
            pdfmetrics.registerFont(TTFont("EmojiFont", "NotoColorEmoji.ttf"))

            styles = getSampleStyleSheet()

            # Paragraph style uses TextFont by default
            styles.add(ParagraphStyle(
                name="MainStyle",
                fontName="TextFont",
                fontSize=12,
                leading=16
            ))

            html_text = markdown2.markdown(final_text)

            doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
            story = []

            for line in html_text.split("\n"):
                story.append(Paragraph(line, styles["MainStyle"]))
                story.append(Spacer(1, 8))

            doc.build(story)
            pdf_buffer.seek(0)

            st.download_button(
                label="📄 Download My Career Roadmap (PDF)",
                data=pdf_buffer,
                file_name=f"{name}_Career_Roadmap.pdf",
                mime="application/pdf",
            )
            # -------------------------------------------------


            st.write("---")
            st.button("🔄 Start Again", on_click=reset_app)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


st.write("---")
st.markdown(
    "<p style='text-align:center;'>Made with ❤️ by "
    "<a href='https://pulkitdubey.netlify.app/' target='_blank'><b>Pulkit Dubey</b></a>"
    "</p>",
    unsafe_allow_html=True
)
