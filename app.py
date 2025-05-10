from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import google.generativeai as genai
import os
from dotenv import load_dotenv
import pyttsx3
import logging
import re
# Load environment variables
load_dotenv()
api_key = os.getenv('API_KEY')

# Configure Google Gemini API
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name='gemini-1.5-flash')
chat = model.start_chat(history=[])

app = Flask(__name__)


# Initialize pyttsx3 once globally to avoid reinitialization overhead
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Set a specific voice
engine.setProperty('rate', 210)  # Set speech rate for better clarity

# Replace CSV loading with hardcoded dictionary
keywords ={
    "Home":"https://panimalar.ac.in/index.php",
    "profile":"https://codesofsakthi.github.io/profile/",
    "vision mission": "https://codesofsakthi.github.io/Vision-and-Mission/" ,
    "about us":"https://codesofsakthi.github.io/About-Us/" ,

  "IQAC first minutes of meeting 23-24":"https://panimalar.ac.in/assets/pdf/iqac/mom/First-Minutes-of-Meeting-23-24.pdf",
  "IQAC second minutes of meeting 23-24":"https://panimalar.ac.in/assets/pdf/iqac/mom/Second-Minutes-of-Meeting-23-24.pdf",
  "IQAC third minutes of meeting 23-24":"https://panimalar.ac.in/assets/pdf/iqac/mom/Third-Minutes-of-Meeting-23-24.pdf",
  "IQAC third minutes of meeting 22-23":"https://panimalar.ac.in/assets/pdf/iqac/mom/Third-Minutes-of-Meeting-22-23.pdf",
  "IQAC second minutes of meeting 22-23":"https://panimalar.ac.in/assets/pdf/iqac/mom/Second-Minutes-of-Meeting-22-23.pdf ",
  "IQAC first minutes of meeting 22-23":"https://panimalar.ac.in/assets/pdf/iqac/mom/First-Minutes-of-Meeting-22-23.pdf",
  "academic council members": "https://coe.panimalar.ac.in/Academic_Council.php",
  "core academic council team": "https://coe.panimalar.ac.in/Regulations.php",
  "regulation 2023 ug regulation": "https://coe.panimalar.ac.in/files/PEC-Regulation%202023-B.E%20&%20B.Tech%20N.pdf",
  "regulation 2023 pg regulation": "https://coe.panimalar.ac.in/files/PEC-Regulation%202023%20-%20M.E%20&%20M.Tech%20N.pdf",
  "regulation 2021 ug regulation with amendments": "https://coe.panimalar.ac.in/files/PEC-Regulation%202021-B.E%20&%20B.Tech%20N.pdf",
  "regulation 2021 pg regulation with amendments": "https://coe.panimalar.ac.in/files/PEC-Regulation%202021%20-%20M.E%20&%20M.Tech.pdf",
  
  "committees": "https://panimalar.ac.in/committee.php",
  "internal quality assurance cell": "https://panimalar.ac.in/iqac.php",
    "iqac coordinator message": "https://panimalar.ac.in/iqac.php",
    "iqac members": "https://panimalar.ac.in/iqac.php",
    "iqac policy manual": "https://panimalar.ac.in/assets/pdf/iqac/IQAC-Policy-Manual.pdf",
    "iqac procedures": "https://panimalar.ac.in/assets/pdf/iqac/IQAC-POLICIES.pdf",
    "memorandum of understanding (mou)": "https://panimalar.ac.in/mou.php",
    "pec-aicte idea lab": "https://panimalar.ac.in/idea-lab.php",
    "objective and benefits": "https://panimalar.ac.in/idea-lab.php",
    "committee members": "https://panimalar.ac.in/idea-lab.php",
    "inauguration": "https://panimalar.ac.in/idea-lab.php",
    "upcoming event": "https://panimalar.ac.in/idea-lab.php",
    "newsletter": "https://panimalar.ac.in/idea-lab.php",
    "institution’s innovation council (iic)": "https://panimalar.ac.in/iic.php",
    "entrepreneurship development cells (edc)": "https://panimalar.ac.in/entrepreneurship-development-cell.php",
    "entrepreneurship development cells": "https://panimalar.ac.in/entrepreneurship-development-cell.php",
    "actives of the cell": "https://panimalar.ac.in/entrepreneurship-development-cell.php",
    "programs organized": "https://panimalar.ac.in/entrepreneurship-development-cell.php",
    "events and participants": "https://panimalar.ac.in/entrepreneurship-development-cell.php",
    "future programs from cells": "https://panimalar.ac.in/entrepreneurship-development-cell.php",
    "policy": "https://panimalar.ac.in/entrepreneurship-development-cell.php",
    "nisp": "https://mic.gov.in/assets/doc/startup_policy_2019.pdf",
    "tamil nadu startup": "https://mic.gov.in/assets/doc/startup_policy_2019.pdf",
    "startup": "https://panimalar.ac.in/entrepreneurship-development-cell.php",
    "entrepreneurs": "https://panimalar.ac.in/entrepreneurship-development-cell.php",
    "immersive multimedia": "https://panimalar.ac.in/assets/images/edc/entrepreneur/immersive-multimedia.pdf",
    "ogrelix": "https://panimalar.ac.in/assets/images/edc/entrepreneur/Orgelix-company.pdf",
    "reverie synaptic pulse": "https://panimalar.ac.in/assets/images/edc/entrepreneur/Reverie-Synaptic-Pulse.pdf",
    "contacts us": "https://panimalar.ac.in/entrepreneurship-development-cell.php",
    "higher education centre": "https://panimalar.ac.in/higher-education-centre.php",
    "professional societies and clubs": "https://panimalar.ac.in/professional-bodies.php",
    "nptel": "https://nptel.ac.in/localchapter/statistics/161",
    "nasscom": "https://panimalar.ac.in/nasscom.php",
    "nirf 2024 engineering": "https://panimalar.ac.in/assets/pdf/academics/nirf2024/ENGINEERING.pdf",
    "nirf 2024 management": "https://panimalar.ac.in/assets/pdf/academics/nirf2024/MANAGEMENT.pdf",
    "nirf 2024 invocation": "https://panimalar.ac.in/assets/pdf/academics/nirf2024/INNOVATION.pdf",
    "nirf 2024 overall": "https://panimalar.ac.in/assets/pdf/academics/nirf2024/OVERALL.pdf",
    "About Panimalar":"https://panimalar.ac.in/about-us.php",
    "Management Team":"https://panimalar.ac.in/management-team.php",
    "Dr. P. Chinnadurai, M.A, Ph.D ":"https://panimalar.ac.in/secretary-correspondent.php",


  
}
def recognize_speech():
    """Recognize speech using the microphone."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjusts based on ambient noise

        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)  # Added timeout to avoid long waits
            text = recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            return text
        except sr.WaitTimeoutError:
            return "Listening timed out. Please try again."
        except sr.UnknownValueError:
            print("Sorry, I did not catch that.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None

def send_to_gemini(input_text):
    """Send recognized text to Google Gemini API and get a response."""
    context = [
        "you are the virtual assistance of the website for my department, you the bot of panimalar engineering college department of artificial intelliegence and data science"
        "this website contains the details of the ai&ds department, in this website there are 4 things in nav bar which are HOD PROFILE, vision&Mission, About Us, Achievements, Contact Us "
        "if they asked you anything about the hod details they can access the documnets with this keyword <profile> to see the deatils related to it, if they asked about hod details of out dept, Dr. S. Malathi,Head of the,Department - AI & DS,Profile Summary: Dr. S. Malathi has over 15 years of academic and research experience in the field of Artificial Intelligence, Data Science, and Machine Learning. She has published numerous papers in reputed journals and is passionate about mentoring students in emerging technologies.Area of Expertise:dl,ml,nlp,data mining."

        " and about the vision&mission use this keyword <vision mission> to get details, Our vision is to be a center of excellence in Artificial Intelligence and Data Science education, creating professionals with a deep understanding of intelligent systems and analytics. Our mission is to provide a strong academic foundation in AI and DS, encourage research and innovative thinking, and collaborate with industries for real-time exposure. We offer a B.Tech in Artificial Intelligence and Data Science, a 4-year undergraduate program",

        "and about the about us use this keyword <about us> for about us,The Department of Artificial Intelligence and Data Science, established in 2020, has been actively advancing in teaching and R&D with experienced faculty specialized in AI and Data Science. It offers a four-year full-time B.Tech program designed to equip students with skills in intelligent data analysis and emerging technologies like AI, Data Science, Machine Learning, Deep Learning, Robotics, and Natural Language Processing (NLP). Since 2022, the department also offers a Ph.D. program (Full Time/Part Time) aimed at developing leaders, researchers, and entrepreneurs through state-of-the-art infrastructure, updated curriculum, and industry-connected hands-on experience. Industry-institute collaborations are fostered through guest lectures, industrial visits, workshops, and training sessions. The department emphasizes the research, design, and development of next-generation technologies in AI and Data Analytics. Key program highlights include a focus on Data Science, Data Engineering, and Advanced Analytics; a student-centric, application-oriented learning approach; training in AI, Machine Learning, AR/VR, Product Development, and Mathematical Modelling; expertise in NLP, text mining, robotics, reasoning, and problem-solving; and the development of intelligent solutions for real-time business and healthcare challenges."

        "see the keywords that i gave you is importantt it must be the same do not never add any word with that keyword, ask the users to copy paste the keyword to make than directly veiw the detail so that certain page, the bot is designed in a way that if theuser give the keyword that document will be automatically opens in the next tab, so see throgh this that this keywords that i gav eyou within <> this is important ",
        "you the bot for ai&ds dept , you have all the right to tell the things you know aboutt my dept, see that you must be professional since it is a college bot"
    ]
    context.append(f"User: {input_text}")

    try:
        response = chat.send_message("\n".join(context))
        reply = response.text if hasattr(response, 'text') else 'Sorry, I could not understand your message.'
        return reply
    except Exception as e:
        print(f"Error communicating with Gemini API: {str(e)}")
        return 'Internal Server Error'

    
def speak_text(text):
    """Convert text to speech and play it."""
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error generating or playing speech: {e}")
@app.route('/process', methods=['POST'])
def process():
    data = request.json
    user_input = data.get('message', '').lower().strip()  # Normalize input
    pdf_url = None
    reply = "Sorry, I didn't catch that."

    # Check for keyword matches in the user's input
    for keyword, link in keywords.items():
        if keyword.lower() in user_input:  # Match keyword as substring
            reply = f"Here is the detailed information you requested for '{keyword}'."
            pdf_url = link

    try:
        reply = send_to_gemini(user_input)
        suggested_keywords = {}
        for keyword, link in keywords.items():
            pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
            if re.search(pattern, reply.lower()):
                suggested_keywords[keyword] = link
        #selected_keys = linkreply(reply)  # Get extracted keyword-link pairs
    except Exception as e:
        print(f"Error during Gemini API call: {e}")
        reply = "Sorry, something went wrong while processing your request."

    # Return the response with reply, PDF URL, and extracted keyword links
    response_data = {"reply": reply, "pdf_url": pdf_url, "suggested_keywords": suggested_keywords}
    return jsonify(response_data)




@app.route('/')
def index():
    return render_template('index.html')

logging.basicConfig(level=logging.INFO)
@app.route('/voice_input', methods=['GET'])
def voice_input():
    logging.info("Received a voice input request.")
    user_input = recognize_speech()
    logging.info(f"Recognized speech: {user_input}")
    
    if user_input:
        user_input = user_input.lower().strip()  # Normalize input
        pdf_url = None
        reply = "Sorry, I didn't catch that."

        # Check for keyword matches in the user's input
        for keyword, link in keywords.items():
            if keyword.lower() in user_input.lower().strip():  # Match keyword as substring
                reply = f"Here is the detailed information you requested for '{keyword}'."
                pdf_url = link
                break
        if pdf_url is None:
            try:
                 reply = send_to_gemini(user_input)
            except Exception as e:
                print(f"Error during Gemini API call: {e}")
                reply = "Sorry, something went wrong while processing your request."

        response_data = {"user_input": user_input,"reply": reply, "pdf_url": pdf_url}
        return jsonify(response_data)
    
    logging.warning("No user input recognized.")
    return jsonify({"user_input": None,"reply": "Sorry, I didn't catch that.", "pdf_url": None})

if __name__ == '__main__':
    app.run(debug=True)