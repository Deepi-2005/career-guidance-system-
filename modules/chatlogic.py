from bs4 import BeautifulSoup
import requests
def scrape_jobs(role):
    params = {
        "engine": "google_jobs",
        "q": f"{role} jobs in India",
        "location": "India",
        "api_key": "389eb6d2b4445aa24858084f4b5bc30f838722d1355355563d43a820306e6cfd"
    }
    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()
    jobs = []

    for job in data.get("jobs_results", []):
        title = job.get("title", "No title")
        company = job.get("company_name", "")
        location = job.get("location", "")
        link = job.get("via", "")  # This is usually the source site
        apply_link = job.get("job_apply_link") or f"https://www.google.com/search?q={title.replace(' ', '+')}+{company.replace(' ', '+')}"
        
        jobs.append(f"**{title}** at *{company}* ({location})\n🔗 [Apply Here]({apply_link})")

    return jobs if jobs else ["No jobs found."]

def scrape_skills(role):
    predefined = {
        "web developer": ["HTML", "CSS", "JavaScript", "React", "Node.js"],
        "data scientist": ["Python", "Pandas", "Scikit-learn", "TensorFlow", "SQL"],
        "android developer": ["Java", "Kotlin", "Android Studio", "Firebase"],
        "ai engineer": ["Python", "TensorFlow", "NLP", "PyTorch", "ML Algorithms"],
        "communication": [
            "Active Listening",
            "Public Speaking",
            "Non-verbal Communication",
            "Email Etiquette",
            "Empathy",
            "Presentation Skills",
            "Writing Skills",
            "Conflict Resolution"
        ]
    }

    # If user enters a general query like "communication", offer advice too
    if role.lower() in ["communication", "communication skills"]:
        tips = [
            "**Career Advice for Improving Communication:**",
            "- Join public speaking clubs like Toastmasters.",
            "- Practice mock interviews and presentations.",
            "- Watch TED Talks and analyze speaker techniques.",
            "- Enroll in online courses (Coursera, LinkedIn Learning).",
            "- Take feedback from peers to improve clarity and tone."
        ]
        skills = predefined["communication"]
        return skills + ["\n"] + tips

    return predefined.get(role.lower(), ["Critical Thinking", "Teamwork", "Problem Solving"])

def get_internships(role):
    params = {
        "engine": "google_jobs",
        "q": f"{role} internships in India",
        "location": "India",
        "api_key": "389eb6d2b4445aa24858084f4b5bc30f838722d1355355563d43a820306e6cfd"
    }
    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()
    internships = []

    for job in data.get("jobs_results", []):
        title = job.get("title", "No title")
        company = job.get("company_name", "")
        location = job.get("location", "")
        apply_link = job.get("job_apply_link") or f"https://www.google.com/search?q={title.replace(' ', '+')}+{company.replace(' ', '+')}"

        internships.append(f"**{title}** at *{company}* ({location})\n🔗 [Apply Here]({apply_link})")

    return internships if internships else ["No internships found."]


def get_courses(role):
    params = {
        "engine": "google",
        "q": f"{role} courses site:coursera.org",
        "api_key": "389eb6d2b4445aa24858084f4b5bc30f838722d1355355563d43a820306e6cfd"
    }
    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()
    courses = []

    for result in data.get("organic_results", []):
        title = result.get("title", "No title")
        link = result.get("link", "#")
        courses.append(f"**{title}**\n🔗 [Go to Course]({link})")

    return courses if courses else ["No courses found."]

def get_bot_response(user_input):
    user_input = user_input.lower()

    # Handle job-related queries
    if any(keyword in user_input for keyword in ["job", "jobs", "become", "career in", "how to be", "how to become"]):
        role = user_input.replace("jobs for", "").replace("career in", "").replace("how to become", "").replace("how to be", "").replace("become", "").strip()
        results = scrape_jobs(role)
        return f"Here are some job opportunities or career roles related to **{role.title()}**:\n\n" + "\n\n".join(results)

    # Handle internship-related queries
    elif any(keyword in user_input for keyword in ["internship", "internships", "intern"]):
        role = user_input.replace("internships in", "").replace("internship for", "").replace("internship", "").replace("intern", "").strip()
        results = get_internships(role)
        return f"Here are some internships related to **{role.title()}**:\n\n" + "\n\n".join(results)

    # Handle skill-related queries
    elif any(keyword in user_input for keyword in ["skill", "skills", "improve", "needed", "what to learn", "how to improve"]):
        role = user_input.replace("skills for", "").replace("suggest skills for", "").replace("what to learn for", "").replace("how to improve", "").replace("needed for", "").replace("what are the skills", "").strip()
        results = scrape_skills(role)
        return f"Here are suggested skills for **{role.title()}**:\n- " + "\n- ".join(results)

    # Handle course/learning queries
    elif any(keyword in user_input for keyword in ["course", "courses", "learn", "study", "learning", "where to learn", "how to learn"]):
        role = user_input.replace("courses for", "").replace("learn", "").replace("study", "").replace("learning", "").replace("how to learn", "").strip()
        results = get_courses(role)
        return f"Here are some courses to learn **{role.title()}**:\n\n" + "\n\n".join(results)

    # Default help message
    else:
        return (
            "Hi! I can help you with:\n"
            "- 🔍 `How to become a data analyst`\n"
            "- 🧠 `What skills do I need for web development?`\n"
            "- 🎓 `Courses to learn AI`\n"
            "- 💼 `Internships in frontend`\n"
            "- 💬 `How to improve communication skills`\n"
            "- And many more! Just ask away 😊"
        )
