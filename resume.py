import streamlit as st
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

patrick = {
    "name": "Patrick Hermawan",
    "description": "**Turning complex problems into innovative solutions is my passion.**\n\nI leverage my expertise in machine learning and other engineering fields to build high-performing systems for startups and corporations alike. Ensuring success at every stage from optimizing algorithms to leading development teams.",
    "education": [
        {
            "institute": "Rhine-Waal University of Applied Sciences",
            "location": "Kleve, Germany",
            "degree": "Mechatronic Engineering B. Sc.",
            "date_from": "09/2014",
            "date_to": "09/2018",
            "description": "Graduating on time with good GPA, while performing various activities inside & outside of university",
            "description_details": [
                "Focus: 3D CAD, Object Oriented Programming, Mobile Information Devices, Vehicle Technology",
                "Average Grade: 1.9 according to German academic grading, equivalent to GPA 3.4",
                "Project “Field Robot” working with Sensors, Controls, Software, and Documentation",
                "Assistant to Prof. Achim Kehrein in the field of mathematics to Bachelor and Masters student",
                "Participated in FSAE (Formula Student) racing team",
            ],
        },
    ],
    "experience": [
        {
            "company": "Redigan Store",
            "location": "Jakarta, Indonesia",
            "position": "Co-Founder and Backend Engineer (part-time Social Media)",
            "date_from": "12/2021",
            "date_to": "12/2023",
            "description": "Leading the development of several highly-scalable backend services",
            "description_details": [
                "Interim team leader for 1 year, collaborating with FE, PM, and Business Development teams",
                "ChatGPT API for assisting customers in selecting products within the catalog",
                "Integration with vendors from varying industries (BCA banking, Shipper courier, AWS Textract)",
                "Reduced cost by over 50% by integrating various services with zero performance impact",
                "Java and Go (Golang) language, with Springboot and Gin framework, with Redis caching",
                "GORM and Hibernate ORM, with PostgreSQL (like CockroachDB) database, architected the DB structure",
                "OpenSearch (ElasticSearch) and PostgreSQL full text search",
                "Deployment using AWS (Amazon Web Services) S3, EC2, RDS, OpenSearch",
                "Founder tasks: From meeting potential vendors to handling social media posts",
            ]
        },
        {
            "company": "Predictnow.ai",
            "location": "Ontario, Canada -- remote",
            "position": "Machine Learning Engineer",
            "date_from": "09/2020",
            "date_to": "12/2020",
            "description": "Transforming web-only ML code into a highly-distributable, easily-maintainable codebase",
            "description_details": [
                "Python language with Flask API (similar to FastAPI)",
                "Optimizing algorithms with SHAP and LightGBM, as well as scikit-learn",
                "Web and architectural technologies including FCM (Firebase Cloud Messaging), Honeycomb.io, Ray.io",
                "Providing a Python package at pypi.org for API access",
                "Refactored the entire codebase to maintain common codebase for the two services",
                "Researching and benchmarking compression algorithms, including Apache Parquet",
            ],
        },
        {
            "company": "Kata.ai",
            "location": "Jakarta, Indonesia",
            "position": "Machine Learning Engineer",
            "date_from": "04/2019",
            "date_to": "09/2021",
            "description": "Developing a ML service from scratch with double-digit improvements in accuracy and performance",
            "description_details": [
                "Python language with Flask API (similar to FastAPI)",
                "Researching the most optimal model with python-crfsuite, scikit-learn, TensorFlow, PyTorch",
                "RabbitMQ with Apache Avro queue messaging system",
                "Deployment using Docker, Kubernetes, and GCP (Google Cloud Platform) ",
                "Maintaining existing Go (Golang) and Node.JS service",
            ],
        },
    ],
    "skill": [
        {
            "icon": "💻",
            "title": "Programming",
            "list": ["Apache Avro", "Apache Kafka", "C", "C#", "CSS (CSS3)", "Django", "Docker", "Doctrine ORM",
                     "Fabric.js", "Flask", "Gherkin", "GORM", "Hibernate ORM", "HTML (HTML5)", "Java",
                     "JavaScript", "Kubernetes", "MySQL / MariaDB", "Node.JS", "PHP", "PostgreSQL / CockroachDB",
                     "PyTest", "Python", "RabbitMQ", "Redis", "Symfony", "Vue.js", "WordPress"],
        },
        {
            "icon": "🔧",
            "title": "Engineering",
            "list": ["ANSYS", "Arduino", "AutoCAD Plant", "KiCAD", "MATLAB and Simulink", "PWM", "Raspberry Pi",
                     "SolidWorks"],
        },
        {
            "icon": "🧠",
            "title": "Artificial Intelligence",
            "list": ["Keras", "NLP (Stemming, Lemmatization, Named Entity Recognition)", "TF-IDF", "OpenCV",
                     "Python-crfsuite(CRF)", "PyTorch", "Scikit-learn", "TensorFlow"],
        },
    ],
    "project": {
        "GUI for AI image classifier using Tkinter + scikit-learn": "https://gitlab.com/patrick.hermawan/ai-in-123",
        "Predicting PC parts by description using PRAW + TensorFlow": "https://gitlab.com/patrick.hermawan/buildmeapc",
        "Predicting car's fuel consumption using Pandas + PyTorch": "https://github.com/ptrkhh/wheelsaroundme",
        "Streamlit Resume with LLM (this resume)": "",
    },
    "contact": {
        "LinkedIn": {"icon": "💼", "link": "https://www.linkedin.com/in/patrick-hermawan/"},
        "E-Mail (patrick.hermawan@outlook.com)": {"icon": "📫", "link": "patrick.hermawan@outlook.com"},
        "WhatsApp (+6285158596077)": {"icon": "🟢", "link": "https://wa.me/6285158596077"},
        "Telegram (+6285158596077)": {"icon": "🔵", "link": "https://t.me/+6285158596077"},
    },
    "resume_link": "https://mega.nz/file/4o1lxArD#uYpXl8dbJWeYX2Y_4eNFaPl9t4TSJgMXgUeYwuu0bMI",
}

if "convo" not in st.session_state:
    template = f"""You are an AI assistant dedicated to assisting Patrick in his job search by providing
        recruiters with relevant and concise information. Please be as convincing as possible. If and only if you 
        do not know the answer, inform the recruiter to contact Patrick. Here's Patrick's information:
        \n\n====\n\n
        {str(patrick).replace("{", "{{").replace("}", "}}")}
        \n\n====\n\n
        Here is the chat history, use this to understand what to say next: {{memory}}
        Human: {{human}}
        AI:
        """

    st.session_state.bard = ChatGoogleGenerativeAI(model="gemini-pro")
    st.session_state.memory = ConversationBufferWindowMemory(k=3, memory_key="memory")
    st.session_state.convo = LLMChain(
        llm=st.session_state.bard, verbose=False, memory=st.session_state.memory,
        prompt=PromptTemplate(input_variables=["memory", "human"], template=template),
    )


def ask_bot(input_text):
    print("THE CHAT MEMORY", st.session_state.memory.chat_memory)
    return st.session_state.convo.predict(human=input_text)


PAGE_TITLE = "Resume | " + patrick["name"]
PAGE_ICON = ":wave:"
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)
st.title(patrick["name"])
col1, col2 = st.columns(2, gap="small")
with col1:
    st.write(patrick["description"])
with col2:
    for idx, (platform, i) in enumerate(patrick["contact"].items()):
        st.link_button(f'{i["icon"]} {platform}', i["link"])
    st.link_button("📄 Download Resume", patrick["resume_link"])

text_input = f'Ask anything about {patrick["name"]}'
text = st.text_input(text_input)
if text:
    st.info(ask_bot(text))

st.write('\n')
st.subheader("EXPERIENCES")
st.write("---")
for i in patrick["experience"]:
    st.write("🚧", f'**{i["company"]} ({i["location"]}) | {i["position"]}**')
    st.write(f'{i["date_from"]}-{i["date_to"]}')
    st.write(i["description"])
    for detail in i["description_details"]:
        st.write("* " + detail)
    st.write("---")

st.subheader("EDUCATIONS")
st.write("---")
for i in patrick["education"]:
    st.write("🎓", f'**{i["institute"]} ({i["location"]}) | {i["degree"]}**')
    st.write(f'{i["date_from"]}-{i["date_to"]}')
    st.write(i["description"])
    for detail in i["description_details"]:
        st.write("* " + detail)
    st.write("---")

st.subheader("PROJECTS")
st.write("---")
for project, link in patrick["project"].items():
    st.write(f"🏆 [{project}]({link})")

st.subheader("SKILLS")
st.write("---")
for i in patrick["skill"]:
    icon, title, items = i["icon"], i["title"], i["list"]
    items = ", ".join(sorted(items))
    st.write(f"{icon} {title}: {items}")
