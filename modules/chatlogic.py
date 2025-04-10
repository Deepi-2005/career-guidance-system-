from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string

questions = [
    "How to improve my resume?",
    "What skills are required for software engineer?",
    "Suggest skills for data analyst",
    "What are trending tech skills?",
    "How to prepare for interviews?",
    "Hi",
    "Hello",
    "Hey there",
    "Tell me about you",
    "I have Python skill, what should I do?",
    "I want to get into AI",
    "What should I learn for DevOps?",
    "Give me skills for UI/UX",
    "How to become a backend developer?",
    "Suggest courses for cloud computing",
    "I’m interested in data science, where should I start?",
    "I want a remote job. What should I learn?",
    "What’s the roadmap for cybersecurity?",
    "Skills needed for game development",
    "Give me a roadmap for full stack development",
    "I want to learn frontend. What’s the plan?",
    "I have JavaScript experience, what can I do with it?",
    "Which skills are needed for machine learning?",
    "What should I learn to become a mobile app developer?",
    "I want to work in blockchain, help me out",
    "Where do I start with ethical hacking?",
    "Tell me about cloud certifications",
    "Give me design tools for UI/UX",
    "I want to get into game development",
    "Suggest free resources for data science",
    "How do I start freelancing in tech?",
    "I want to work in web development",
    "Web dev path please",
    "Tell me about frontend and backend",
    "Explain MERN stack",
    "Skills needed for AR/VR",
    "How to become a product manager?",
    "Guide me on software testing",
    "I want to learn embedded systems",
    "How to become a data engineer?",
    "What is the career path for robotics?"
]

responses = [
    "Make sure your resume is clear, concise, and tailored to the job you're applying for.",
    "You should be good at DSA, system design, and have strong coding and communication skills.",
    "You’ll need Excel, SQL, Python, and a data visualization tool like Power BI.",
    "AI, ML, cloud, and cybersecurity are trending right now.",
    "Start with common HR questions, then move on to technical questions for your domain.",
    "Hello! How can I help you with your career today? 😊",
    "Hey there! I’m your SkillSync bot, here to guide you in your career journey.",
    "Hi! Ask me anything about skills, jobs, or learning paths.",
    "I’m SkillSync, your intelligent career guide 🤖 Here to help you upskill!",
    "Nice! With Python, you can explore data analysis, automation, backend development, or even AI.",
    "🧠 Start with Python, math basics, and linear algebra. Then move into ML with scikit-learn, followed by deep learning using TensorFlow or PyTorch.",
    "🔧 Start with Linux, networking, and shell scripting. Learn tools like Docker, Kubernetes, Jenkins, Terraform. Try freeCodeCamp or KodeKloud.",
    "🎨 Learn tools like Figma, Adobe XD. Study design principles, user psychology, and accessibility. Platforms: Coursera, UX Crash Course (by The Hipper Element).",
    "🛠 Learn DSA, databases (SQL), backend frameworks like Node.js or Django, and APIs. Deploy projects on Heroku or Render.",
    "☁️ Basics: Linux, Networking. Platforms: AWS (start with Cloud Practitioner), GCP, Azure. Tools: Docker, Kubernetes. Try AWS Skill Builder, KodeKloud, Coursera.",
    "📊 Learn Python, statistics, data wrangling (Pandas), visualization (Matplotlib, Seaborn), ML, and tools like Jupyter, Git. Courses: IBM Data Science on Coursera.",
    "🌍 For remote tech jobs, focus on web dev, freelancing platforms, and GitHub portfolio. Learn React, Node.js, Git. Build solid projects and learn async communication tools.",
    "🔐 Cybersecurity Roadmap: Start with Networking, Linux, and Python. Learn about firewalls, ethical hacking, and tools like Wireshark, Metasploit. Try Hack The Box and TryHackMe.",
    "🎮 Game Dev Skills: Learn C# with Unity or C++ with Unreal. Understand game physics, animation, and 3D modeling. Explore Brackeys YouTube channel and GameDev.tv.",
    "🌐 Full Stack Dev: Learn HTML, CSS, JS, React (frontend), Node.js, Express, MongoDB (backend). Projects, GitHub portfolio, and Netlify deployment help a lot.",
    "🖥 Frontend Learning Path: Start with HTML, CSS, JS → move to React or Angular → Learn responsive design, accessibility, and animation libraries.",
    "🔥 With JavaScript, dive into frontend (React, Vue), backend (Node.js), or even mobile (React Native). Lots of job options!",
    "📘 Core ML Skills: Python, statistics, data wrangling, model building, and deployment using Flask/FastAPI. Learn from fast.ai, Kaggle, and Coursera.",
    "📱 Mobile Dev Path: Learn Java/Kotlin for Android or Swift for iOS. Cross-platform? Go with Flutter or React Native. Try Udacity, Codecademy, or YouTube playlists.",
    "⛓ Blockchain: Start with basics of decentralization, learn Solidity (Ethereum), understand smart contracts. Follow tutorials on buildspace.so or LearnWeb3.",
    "💻 Ethical Hacking: Networking, Linux, Python → then move into OWASP Top 10, Kali Linux, and hands-on labs on TryHackMe, Hack The Box.",
    "📜 Start with AWS Cloud Practitioner. Move up to Solutions Architect Associate. Azure and GCP offer similar tracks too!",
    "🎨 Top Tools: Figma, Sketch, Adobe XD, Canva (for simple design). Learn them with free YouTube series and Coursera UI/UX courses.",
    "🎮 You’ll love it! Start with Unity or Unreal tutorials, game design principles, and build mini projects. Showcase on Itch.io.",
    "📚 Try freeCodeCamp, Kaggle Learn, and Coursera’s free tracks for data science. Tons of hands-on notebooks there!",
    "💼 Learn web dev or design, make profiles on Fiverr/Upwork, build portfolio sites. Learn how to pitch and manage clients.",
    "🌐 Web Dev: Start with HTML, CSS, JS → choose frameworks (React/Angular/Vue). Backend: Node/Django. Tools: Git, GitHub, Netlify.",
    "🧭 Web Dev Roadmap: Frontend → HTML, CSS, JS, frameworks. Backend → DBs, APIs. DevOps → CI/CD basics. Build and deploy projects.",
    "🧑‍💻 Frontend = UI/UX + JS + frameworks. Backend = DB + server-side logic. Together = Full Stack!",
    "💻 MERN = MongoDB, Express, React, Node.js. Great for full stack apps. Learn each with projects.",
    "🕶 AR/VR: Learn Unity, C#, Blender, 3D math, and device SDKs like Oculus SDK. Try XR Bootcamps.",
    "📋 Product Manager: Learn agile, user stories, wireframing, basic tech understanding, data-driven decision making. Read Inspired by Marty Cagan.",
    "🧪 Testing: Learn manual testing, test case design, automation with Selenium, frameworks like Jest/Mocha. Try Test Automation University.",
    "📟 Embedded Systems: Learn C/C++, microcontrollers (Arduino, STM32), basic electronics, RTOS. Try Neso Academy and Coursera.",
    "🧱 Data Engineer Path: Learn Python, SQL, ETL, Airflow, Spark, DBs like PostgreSQL and data warehousing. Try DataCamp or Data Engineering Zoomcamp.",
    "🤖 Robotics: Learn Python/C++, sensors, actuators, ROS, embedded systems. Courses: Coursera Robotics Specialization or edX Robotics."
]

def preprocess(text):
    text = text.lower()
    return text.translate(str.maketrans('', '', string.punctuation))

def get_bot_response(user_input):
    processed_questions = [preprocess(q) for q in questions]
    processed_input = preprocess(user_input)
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(processed_questions + [processed_input])
    similarity = cosine_similarity(vectors[-1], vectors[:-1])
    idx = similarity.argmax()

    if similarity[0][idx] < 0.3:
        return "Hmm, I'm not sure about that. Could you rephrase your question?"

    return responses[idx]