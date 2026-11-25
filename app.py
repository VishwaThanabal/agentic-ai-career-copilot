
import streamlit as st
from pypdf import PdfReader
from google import genai
from google.genai import types


# ----------------------------------
# FUNCTION 1: Extract text from PDF
# ----------------------------------

def extract_resume_text(uploaded_file):

    reader = PdfReader(uploaded_file)

    resume_text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            resume_text += page_text + "\n"

    return resume_text


# ----------------------------------
# FUNCTION 2: Analyze resume skills
# ----------------------------------

def analyze_skills(resume_text, job_description):

    skills = [
        "Python",
        "SQL",
        "Machine Learning",
        "Pandas",
        "NumPy",
        "Power BI",
        "Excel",
        "AWS",
        "Deep Learning",
        "Data Visualization"
    ]

    resume_text = resume_text.lower()
    job_description = job_description.lower()

    resume_skills = []

    for skill in skills:

        if skill.lower() in resume_text:
            resume_skills.append(skill)

    required_skills = []

    for skill in skills:

        if skill.lower() in job_description:
            required_skills.append(skill)

    matched_skills = []

    for skill in required_skills:

        if skill in resume_skills:
            matched_skills.append(skill)

    missing_skills = []

    for skill in required_skills:

        if skill not in resume_skills:
            missing_skills.append(skill)

    if len(required_skills) > 0:

        match_percentage = (
            len(matched_skills) / len(required_skills)
        ) * 100

    else:
        match_percentage = 0

    return (
        resume_skills,
        required_skills,
        matched_skills,
        missing_skills,
        match_percentage
    )

# ----------------------------------
# FUNCTION 3: Gemini AI Analysis
# ----------------------------------

def analyze_with_gemini(resume_text, job_description):

    client = genai.Client(
        api_key=st.secrets["GOOGLE_API_KEY"]
    )

    prompt = f"""
    You are an expert AI career assistant.

    Analyze the candidate's resume against the job description.

    RESUME:
    {resume_text[:12000]}

    JOB DESCRIPTION:
    {job_description[:8000]}

    Give your analysis under these headings:

    1. JOB FIT SUMMARY
    2. MATCHED SKILLS
    3. MISSING OR WEAK SKILLS
    4. LEARNING ROADMAP
    5. RESUME IMPROVEMENT

    Do not invent experience or qualifications.
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text

# ----------------------------------
# TOOL 1: CREATE PERSONALIZED LEARNING PLAN
# ----------------------------------

def create_learning_plan(missing_skills):

    learning_plan = []

    for skill in missing_skills:

        if skill == "Python":

            topic = "Python basics, functions, loops and data structures"

        elif skill == "SQL":

            topic = "SQL queries, joins, grouping and subqueries"

        elif skill == "Machine Learning":

            topic = "Supervised learning, regression and classification"

        elif skill == "Pandas":

            topic = "DataFrames, data cleaning and data manipulation"

        elif skill == "NumPy":

            topic = "Arrays, indexing and numerical operations"

        elif skill == "Power BI":

            topic = "Data visualization, dashboards and DAX basics"

        elif skill == "Excel":

            topic = "Formulas, pivot tables and data analysis"

        elif skill == "AWS":

            topic = "Cloud fundamentals, S3 and basic AWS services"

        elif skill == "Deep Learning":

            topic = "Neural networks and deep learning fundamentals"

        elif skill == "Data Visualization":

            topic = "Charts, graphs and data storytelling"

        else:

            topic = "Learn the fundamentals and practise practical projects"

        learning_plan.append({
            "skill": skill,
            "topic": topic
        })

    return learning_plan

  
# ----------------------------------
# FUNCTION 4: GEMINI AGENT WITH TOOL CALLING
# ----------------------------------

def generate_ai_learning_plan(missing_skills):

    # Step 1: Connect to Gemini
    client = genai.Client(
        api_key=st.secrets["GOOGLE_API_KEY"]
    )

    # Step 2: Define the Python tool for Gemini
    learning_tool = {
        "name": "create_learning_plan",
        "description": "Creates learning topics for the candidate's missing skills.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "missing_skills": {
                    "type": "ARRAY",
                    "items": {
                        "type": "STRING"
                    },
                    "description": "List of skills the candidate needs to learn."
                }
            },
            "required": ["missing_skills"]
        }
    }

    # Step 3: Allow Gemini to use the Python tool
    config = types.GenerateContentConfig(
        tools=[{
            "function_declarations": [learning_tool]
        }]
    )

    # Step 4: Ask Gemini to create a learning plan
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=f"""
        Create a personalized learning plan for these missing skills:

        {missing_skills}

        Use the create_learning_plan tool to get the learning topics.
        """,
        config=config
    )

    # Step 5: Check whether Gemini requested the tool
    
    for part in response.candidates[0].content.parts:

        if part.function_call:

            function_name = part.function_call.name
            arguments = part.function_call.args

            if function_name == "create_learning_plan":

                tool_result = create_learning_plan(
                    arguments["missing_skills"]
                )

                # Send the Python tool result back to Gemini
                function_response_part = types.Part.from_function_response(
                    name=function_name,
                    response={"result": tool_result}
                )

                final_response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=[
                        f"""
    Create a detailed learning plan for these missing skills: {missing_skills}.

    Use the Python tool result provided below.
    For every skill, clearly display:
    1. Skill name
    2. Topics to learn
    3. A short explanation of what to study.

    Do not give a generic confirmation.
    Display the actual learning topics from the tool result.
    """,
                        response.candidates[0].content,
                        types.Content(
                            role="user",
                            parts=[function_response_part]
                        )
                    ],
                    config=config
                )

                return tool_result

    return []

  







# ----------------------------------
# STREAMLIT APPLICATION
# ----------------------------------

st.set_page_config(
    page_title="Career Copilot",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Agentic AI Career Copilot")

st.write(
    "Your personal AI assistant for placement preparation."
)

st.subheader("1. Upload your resume")

resume = st.file_uploader(
    "Choose your resume in PDF format",
    type=["pdf"]
)

st.subheader("2. Enter your job description")

job_description = st.text_area(
    "Paste the job description here",
    placeholder="Enter the skills required for your target job..."
)

if st.button("Analyze my career readiness"):

    if resume is None:

        st.warning("Please upload your resume.")

    elif not job_description.strip():

        st.warning("Please enter a job description.")

    else:

        try:

            # Extract resume text
            resume_text = extract_resume_text(resume)

            if not resume_text.strip():

                st.error("No readable text found in this PDF.")

            else:

                # Analyze skills
                (
                    resume_skills,
                    required_skills,
                    matched_skills,
                    missing_skills,
                    match_percentage
                ) = analyze_skills(
                    resume_text,
                    job_description
                )

                st.subheader("3. Resume Analysis Results")

                st.write("Skills found in your resume:")
                st.write(resume_skills)

                st.write("Skills required by the job:")
                st.write(required_skills)

                st.subheader("4. Skill Matching")

                st.success(f"Matched Skills: {matched_skills}")

                st.warning(f"Missing Skills: {missing_skills}")

                st.metric(
                    "Skill Coverage",
                    f"{match_percentage:.1f}%"
                )

         
                # ----------------------------------
                # GEMINI AI CAREER ANALYSIS
                # ----------------------------------

                st.subheader("5. AI Career Analysis")

                with st.spinner("Gemini is analyzing your resume..."):

                    gemini_analysis = analyze_with_gemini(
                        resume_text,
                        job_description
                    )

                if gemini_analysis:

                    st.markdown(gemini_analysis)

                else:

                    st.warning("Gemini did not return an analysis.")
                
                # ----------------------------------
                # PERSONALIZED LEARNING PLAN
                # ----------------------------------

                st.subheader("6. Personalized Learning Plan")

                if missing_skills:

                    with st.spinner("Creating your personalized learning plan..."):

                        learning_plan = generate_ai_learning_plan(
                            missing_skills
                        )

                    if learning_plan:

                        for item in learning_plan:

                            st.markdown(f"**{item['skill']}**")

                            st.write(item["topic"])

                    else:
                        st.warning("No learning plan was generated.")

                else:
                    st.success("Congratulations! No missing skills found.")


        except Exception as error:

            st.error(f"An error occurred: {error}")
