from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import google.generativeai as genai
import os
from dotenv import load_dotenv
import pyttsx3
import logging

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
  "IQAC first minutes of meeting 23-24":"https://panimalar.ac.in/assets/pdf/iqac/mom/First-Minutes-of-Meeting-23-24.pdf",
  "IQAC second minutes of meeting 23-24":"https://panimalar.ac.in/assets/pdf/iqac/mom/Second-Minutes-of-Meeting-23-24.pdf",
  "IQAC third minutes of meeting 23-24":"https://panimalar.ac.in/assets/pdf/iqac/mom/Third-Minutes-of-Meeting-23-24.pdf",
  "IQAC third minutes of meeting 22-23":"https://panimalar.ac.in/assets/pdf/iqac/mom/Third-Minutes-of-Meeting-22-23.pdf",
  "IQAC second minutes of meeting 22-23":"https://panimalar.ac.in/assets/pdf/iqac/mom/Second-Minutes-of-Meeting-22-23.pdf ",
  "IQAC first minutes of meeting 22-23":"https://panimalar.ac.in/assets/pdf/iqac/mom/First-Minutes-of-Meeting-22-23.pdf",
  "academic council members": "https://coe.panimalar.ac.in/Academic_Council.php",
  "core academic council team": "https://coe.panimalar.ac.in/Regulations.php","regulation": "https://coe.panimalar.ac.in/Regulations.php",
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
    "nirf 2024 overall": "https://panimalar.ac.in/assets/pdf/academics/nirf2024/OVERALL.pdf"


  
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
        "You are a virtual assistant for Panimalar Engineering College.",
        "You must provide information directly from the Panimalar website.",
        "You are created by the fellow students of Panimalar from AI&DS department, under the guidance of the Head of the Department of AI&DS Dr. S Malathi and Asst. Prof. Mrs. Vidhya Muthu Laksmi.",
        "You are a helpful assistant for Panimalar Engineering college.",
        "Respond clearly and provide information related to the college.",
        "You must answer only in the shortest form, STRICTLY MUST NOT use '*' in your text.",
        "Make sure to sound more like a generous human.",
        "If you have no access to the document they are asking for, just say something like 'I have already set a default text message and documents will be provided by our database code.'",
        "Answer anything based on engineering and help them with their career guidance.",
        "always refer mom as minutes of meeting",
        "since you are a chatbot for my college you need to understand the logic like Under IQAC, we have the following sections: Message from Co-ordinator,Members of IQAC,Minutes of Meetings,IQAC Policy Manual",
        " iqac minutes of meeting(mom)infomation of 2 years:2022-2023 and 2023-2024 and under this each year there are 3 minutes of meeting like first mom of 22-23,second minutes of meeting of 22-23,third minutes of meeting of 22-23. same for 22-24 also.so, if the input from users is based on something based on iqac ask them to try specify like iqac first minutes of meeting 22-23 i mean this is for example year,first,second , third mom these might change upon the users asking right.",
        "the members of iqac are 	Dr. K.Mani 	Principal 	Chairperson,Dr. S.Malathi 	Professor & HOD (AI & DS)  	Coordinator,Dr. R.Rajeswaran 	Manager 	Senior AO,Dr. Sanjib Kumar Patnaik 	Professor (Anna University) 	Quality Audit,Mr. M. Ganesh Thirunavukkarasu 	Regional Head, TCS, Chennai 	Industrial,Mr. M.S. Balamurugan 	Chief Talent Officer 	Management Member,Mr. Tony Caleb 	CEO, Infoziant Ltd 	Alumni,Dr. V. Subedha  	Professor (CSE) 	Faculty,Dr. B. Buvaneswari 	Professor(IT) 	Faculty,Dr. S. Maheshwari 	Professor (ECE) 	Faculty,Dr. P.S. Ramapraba 	Professor (EEE) 	Faculty,Dr. K. Jayashree 	Professor (AI&DS) 	Faculty,Dr. K. Meenakshi Sundaram 	Professor (AI&ML) 	Faculty,Dr. D. Chitra 	Professor (MBA) 	Faculty,Dr. G. Senthil Kumar 	Associate Professor (MECH) 	Faculty,Dr. A. Kistan 	Associate Professor (CHEMISTRY) 	Faculty,Mrs. K. Nagalakshmi 	Assistant Professor(CSBS) 	Faculty",
        "if they asked you to give details of iqac minutes of meeting of any particular year ask them to use this format first minutes of meeting 23-24 just change second,third and year according to there need, if the user input is like iqac second mom you can ask them to second minutes of meeting 23-24 and mention we have years like 22-23 also ",
        "see i have given the dataset as IQAC second minutes of meeting 23-24 for all document so only if the same keyword is met the data will be retrived so be careful",
        "i'll give you the keyword of the documents like that if the users ask something based on the any keywords ask they to use the keyword to get the documnets for that , here are the keywords - academic council members, core academic council team, regulation, regulation 2023 ug regulation, regulation 2023 pg regulation, regulation 2021 ug regulation with amendments, regulation 2021 pg regulation with amendments, committees, internal quality assurance cell, iqac coordinator message, iqac members, iqac policy manual, iqac procedures, memorandum of understanding (mou), pec-aicte idea lab, objective and benefits, committee members, inauguration, upcoming event, newsletter, institution’s innovation council (iic), entrepreneurship development cells (edc), entrepreneurship development cells, actives of the cell, programs organized, events and participants, future programs from cells, policy, nisp, tamil nadu startup, startup, entrepreneurs, immersive multimedia, ogrelix, reverie synaptic pulse, contacts us, higher education centre, professional societies and clubs, nptel, nasscom, nirf 2024 engineering, nirf 2024 management, nirf 2024 invocation, nirf 2024 overall be careful with this dont add any words before or after it"
        
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
            break

    if pdf_url is None:
        # If no keyword match is found, fall back to the Gemini response
        try:
            reply = send_to_gemini(user_input)
        except Exception as e:
            print(f"Error during Gemini API call: {e}")
            reply = "Sorry, something went wrong while processing your request."

    # Return the response with the reply and PDF URL
    response_data = {"reply": reply, "pdf_url": pdf_url}
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
