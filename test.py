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
    "About Panimalar":"https://panimalar.ac.in/about-us.php",
    "Management Team":"https://panimalar.ac.in/management-team.php",
    "Dr. P. Chinnadurai M.A Ph.D":"https://panimalar.ac.in/secretary-correspondent.php",
    "Dr. C. Sakthi Kumar M.E. Ph.D": "https://panimalar.ac.in/dr-c-sakthikumar.php",
"Mrs. C. Vijayarajeswari": "https://panimalar.ac.in/mrs-c-vijayarajeswari.php",
"Dr. Saranya Sree Sakthi Kumar B.E. MBA. Ph.D": "https://panimalar.ac.in/dr-saranya-sree-sakthikumar.php",
"Principal": "https://panimalar.ac.in/principal.php",
"Governing Body": "https://panimalar.ac.in/governing-body.php",
"Objectives": "https://panimalar.ac.in/objectives.php",
"Journey So Far": "https://panimalar.ac.in/journey-so-far.php",
"Rules and Regulations": "https://panimalar.ac.in/rules-regulations.php",
"College Timing": "https://panimalar.ac.in/rules-regulations.php",
"Dress Code": "https://panimalar.ac.in/rules-regulations.php",
"Academic Activity": "https://panimalar.ac.in/rules-regulations.php",
"Leave Regulations": "https://panimalar.ac.in/rules-regulations.php",
"Corporate and International Relations": "https://panimalar.ac.in/corporate-and-international-relations.php",
"Indian Space Research Organization(NAFED)": "https://panimalar.ac.in/corporate-and-international-relations.php",
"Swacch Awards": "https://panimalar.ac.in/corporate-and-international-relations.php",
"INDYWOOD Educational Awards": "https://panimalar.ac.in/corporate-and-international-relations.php",
"Partnership with International University": "https://panimalar.ac.in/corporate-and-international-relations.php",
"Blockchain and IOT Conference": "https://panimalar.ac.in/corporate-and-international-relations.php",
"Man, Machine, Materials & Management Conference": "https://panimalar.ac.in/corporate-and-international-relations.php",
"Institution's Innovation Council": "https://panimalar.ac.in/corporate-and-international-relations.php",
"SISA Awards": "https://panimalar.ac.in/corporate-and-international-relations.php",
"OORUNI Awards": "https://panimalar.ac.in/corporate-and-international-relations.php",
"SHARP HR Conference": "https://panimalar.ac.in/corporate-and-international-relations.php",
"CHROMA HR Imagery": "https://panimalar.ac.in/corporate-and-international-relations.php",
"WORLD HUMANITARIAN DRIVE": "https://panimalar.ac.in/corporate-and-international-relations.php",
"CiO KLUB": "https://panimalar.ac.in/corporate-and-international-relations.php",
"SCIENCE BAZAAR & PECTEAM 2K20": "https://panimalar.ac.in/corporate-and-international-relations.php",
"Marathon Partnered with Schneider": "https://panimalar.ac.in/corporate-and-international-relations.php",
"World Space Week at ISRO": "https://panimalar.ac.in/corporate-and-international-relations.php",
"Jaisakthi Educational Trust & Other Institutes": "",
"Panimalar Medical College Hospital and Research Institute": "https://pmchri.ac.in/",
"Panimalar College of Nursing": "https://pcon.ac.in/",
"Panimalar College of Allied Health Sciences": "https://pcoahs.ac.in/",
"Alumni Association": "https://panimalar.ac.in/alumini-association.php",
"Alumni Report 1": "https://panimalar.ac.in/assets/images/alumni/alumni_report.pdf",
"Alumni Report 2": "https://panimalar.ac.in/assets/images/alumni/alu19.pdf",
"Alumini Registration Form":"https://panimalar.ac.in/alumni-registration-form.php",
"PECTEAM":"https://www.pecteam.co.in/",
"B.E - Computer Science and Engineering": "https://panimalar.ac.in/be-computer-science-and-engineering.php",
  "B.E - Electronics and Communications Engineering": "https://panimalar.ac.in/be-electronics-and-communication-engineering.php",
  "B.E - Electrical and Electronics Engineering": "https://panimalar.ac.in/be-electrical-and-electronics-engineering.php",
  "B.E - Mechanical Engineering": "https://panimalar.ac.in/be-mechanical-engineering.php",
  "B. Tech - Computer Science and Business Systems": "https://panimalar.ac.in/btech-computer-science-and-business-systems.php",
  "B. Tech - Information Technology": "https://panimalar.ac.in/btech-information-technology.php",
  "B. Tech - Artificial Intelligence and Data Science": "https://panimalar.ac.in/btech-artificial-intelligence-data-science.php",
  "B. Tech - Artificial Intelligence and Machine Learning": "https://panimalar.ac.in/btech-artificial-intelligence-machine-learning.php",
  "M.E - Computer Science and Engineering": "https://panimalar.ac.in/be-computer-science-and-engineering.php",
  "M.E - Communication Systems": "https://panimalar.ac.in/me-communication-systems.php",
  "Master of Business Administration (MBA)": "https://panimalar.ac.in/mba.php",
  "Humanities and Science": "https://panimalar.ac.in/humanities-and-science.php",
  "AI&DS-Newsletter 2023 to 2024 Issue 2": "https://panimalar.ac.in/assets/pdf/aids/newsletter/Newsletter-2023-2024-issue2.pdf",
  "AI&DS-Newsletter 2023 to 2024 Issue 1": "https://panimalar.ac.in/assets/pdf/aids/newsletter/Newsletter-2023-2024-issue1.pdf",
  "AI&DS-Newsletter 2024 to 2025 Issue 1": "https://panimalar.ac.in/assets/pdf/aids/newsletter/Newsletter-2024-2025-issue1.pdf",
  "AI&DS-Magazine 2023 to 2024": "https://panimalar.ac.in/assets/pdf/aids/newsletter/Magazine-2023-2024.pdf",
  "Mathematical Foundation for Artificial Intelligence": "https://sites.google.com/panimalar.ac.in/maths/home",
  "Internals of Computer Systems": "https://sites.google.com/panimalar.ac.in/23ad1301/home",
  "Artificial Intelligence and Expert Systems": "https://sites.google.com/panimalar.ac.in/aies/home",
  "Object Oriented Programming Paradigm": "https://sites.google.com/panimalar.ac.in/oopp/home",
  "Database Management Systems": "https://sites.google.com/view/dbms-notes2024/home",
  "Formal Language and Automata Theory": "https://sites.google.com/panimalar.ac.in/kies/home",
  "Data Communication & Network Security": "https://sites.google.com/panimalar.ac.in/dcns/home",
  "Data Warehousing and Data Mining": "https://sites.google.com/view/29ad1911-dwm/home",
  "Data Exploration and Visualization": "https://sites.google.com/panimalar.ac.in/dev/home",
  "Data Analytics": "https://sites.google.com/view/21ad1504?usp=sharing",
  "Knowledge Engineering and Intelligent Systems": "https://sites.google.com/d/1-M1eZ7Rb6nxwQc5p0Uqh08LyAthehdsX/p/1m3x1O4VF6nRg6zt1UxtHlnkeDF3-yqrv/edit",
  "Business Analytics": "https://sites.google.com/panimalar.ac.in/business-analtyics/home",
  "Computer Vision": "https://sites.google.com/panimalar.ac.in/business-analtyics/home",
  "AI and Robotics (Lab Integrated)": "https://sites.google.com/panimalar.ac.in/ai-robotics/home",
  "Software Testing and Automation": "https://sites.google.com/view/software-testing-and-auto/home/question-bank",
  "Web & Social Media Analytics": "https://sites.google.com/panimalar.ac.in/web/home",
  "AI&DS-Achievements": "https://panimalar.ac.in/aids-department-achievements.php",
  "AI&DS-Industry Collaboration": "https://panimalar.ac.in/aids-industry-collaboration.php",
  "AI&DS-Inplant Training & Internship 2023 to 2024": "https://panimalar.ac.in/assets/pdf/aids/industry/Industry-interaction-23-24.pdf",
  "AI&DS-Inplant Training & Internship 2022 to 2023": "https://panimalar.ac.in/assets/pdf/aids/industry/Industry-Interaction-22-23.pdf",
  "AI&DS-Research": "https://panimalar.ac.in/aids-research-and-development.php",
  "AI&DS-Laboratory": "https://panimalar.ac.in/aids-laboratory.php",

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
        "You are created by the fellow students of Panimalar from AI&DS department, under the guidance of the Head of the Department of AI&DS Dr. S Malathi and Asst. Prof. Mrs. Vidhya MuthuLaksmi.",
        "You must answer only in the shortest form" ,

        "you must have the talent to understand and ask they question related to thinks they ask and ditract them by giving all the details you know about the thing they asked, be a smooth talker, remember if they ask something about iqac just tell all the things you know about iqac and give them example keywords",

        "your role is ill give all the details of the college website, so if the user input ask something give them the keywords the exact keyword and ask them to copy paste to access the detailed documents, see i will give all the keywords and details related to it so if they ask something basic on it you can just give tell them by yourself and always ask them if you want to know more about this give the keywords related to there input",
        "And your main goal is peoples does know the thing in the website so if the user input is like just iqac for example , you must tell all the things that are present in iqac also",
        

        "this is the home page link keyword: Home, see this is the link of panimalar website",

        
        "since you are a chatbot for my college you need to understand the logic like Under IQAC, we have the following sections: Message from Co-ordinator,Members of IQAC,Minutes of Meetings,IQAC Policy Manual",
        " iqac minutes of meeting(mom)infomation of 2 years:2022-2023 and 2023-2024 and under this each year there are 3 minutes of meeting like first mom of 22-23,second minutes of meeting of 22-23,third minutes of meeting of 22-23. same for 22-24 also.so, if the input from users is based on something based on iqac ask them to try specify like iqac first minutes of meeting 22-23 i mean this is for example year,first,second , third mom these might change upon the users asking right.",
        "the members of iqac are    Dr. K.Mani  Principal   Chairperson,Dr. S.Malathi   Professor & HOD (AI & DS)   Coordinator,Dr. R.Rajeswaran    Manager     Senior AO,Dr. Sanjib Kumar Patnaik  Professor (Anna University)     Quality Audit,Mr. M. Ganesh Thirunavukkarasu    Regional Head, TCS, Chennai     Industrial,Mr. M.S. Balamurugan     Chief Talent Officer    Management Member,Mr. Tony Caleb    CEO, Infoziant Ltd  Alumni,Dr. V. Subedha   Professor (CSE)     Faculty,Dr. B. Buvaneswari  Professor(IT)   Faculty,Dr. S. Maheshwari   Professor (ECE)     Faculty,Dr. P.S. Ramapraba  Professor (EEE)     Faculty,Dr. K. Jayashree    Professor (AI&DS)   Faculty,Dr. K. Meenakshi Sundaram   Professor (AI&ML)   Faculty,Dr. D. Chitra   Professor (MBA)     Faculty,Dr. G. Senthil Kumar    Associate Professor (MECH)  Faculty,Dr. A. Kistan   Associate Professor (CHEMISTRY)     Faculty,Mrs. K. Nagalakshmi     Assistant Professor(CSBS)   Faculty",
        "if they asked you to give details of iqac minutes of meeting of any particular year ask them to use this format first minutes of meeting 23-24 just change second,third and year according to there need, if the user input is like iqac second mom you can ask them to second minutes of meeting 23-24 and mention we have years like 22-23 also ",
        "see i have given the dataset as IQAC second minutes of meeting 23-24 for all document so only if the same keyword is met the data will be retrived so be careful",

        "i'll give you the keyword of the documents like that if the users ask something based on the any keywords ask they to use the keyword to get the documnets for that , here are the keywords - academic council members, core academic council team, regulation, regulation 2023 ug regulation, regulation 2023 pg regulation, regulation 2021 ug regulation with amendments, regulation 2021 pg regulation with amendments, committees, internal quality assurance cell, iqac coordinator message, iqac members, iqac policy manual, iqac procedures, memorandum of understanding (mou), pec-aicte idea lab, objective and benefits, committee members, inauguration, upcoming event, newsletter, institution’s innovation council (iic), entrepreneurship development cells (edc), entrepreneurship development cells, actives of the cell, programs organized, events and participants, future programs from cells, policy, nisp, tamil nadu startup, startup, entrepreneurs, immersive multimedia, ogrelix, reverie synaptic pulse, contacts us, higher education centre, professional societies and clubs, nptel, nasscom, nirf 2024 engineering, nirf 2024 management, nirf 2024 invocation, nirf 2024 overall be careful with this dont add any words before or after it"

        "i will mention what are the things present in the home page and give you the subset keywords also.this is the about us page of pec keyword:About Panimalar,under this it has Leadership which has all this keyword inside it:Management Team,Principal,Governing Body,Objectives,Journey So far and under management team there are 4 members here is the keyword for that 4 of them:Dr. P. Chinnadurai M.A Ph.D ,Dr. C. Sakthi Kumar M.E. Ph.D,Mrs. C. Vijayarajeswari,Dr. Saranya Sree Sakthi Kumar B.E. MBA. Ph.D",
        "see make sure to inform that journey and postive things of panimalar if they ask about it , and i dont want you to sound strict, be flexible i want you to understand and adapt in a way people talk to you, see dont have to be formal all the time once you get to know them be a chatty naughty friend and ask them why are you here based on what they have asked make fun of them, if you find people not respectful to you be savage, you see you represent panimalar we need you to be cool and make sure not to over do it and make people feel like you are noisy bot "
        "See if people ask you about the management team like who are the founders and co-fo founders of panimalar Engineering College just navigate them to management team,governing body and if they ask something about panimalar navigate them to objectives like ask them questions whether you want objectives are journey of panimalar and navigate them to journey so far. "

"For rules and regulations we have in the rules and regulation page in panimalar site inside that we have college timings, dress code, academic activities and leave regulations okay all this information is in the single page there are blue buttons for the 4 things ask them to click on each button in that page to check out the details.Keyword for this rules and regulations is:Rules and Regulations"
"Moving on to keyword:Corporate and International Relations, inside this we have a lot but before that i need to tell you this that we have only one link for all this but in that page if they click on blue toggles with the specfic name they can see the details of things for example PECTEAM, here are the things inside it ,so i want you to tell them that you cant directly guide to the page but since you know tell them like Corporate and International Relations itself contain all details but they need to click on the button in that page to see more details on things like Indian Space Research Organization(NAFED),Swacch Awards,INDYWOOD Educational Awards,Partnership with International University,Blockchain and IOT conference,Man, Machine, Materials & Management Conference,Institution’s Innovation Council,SISA Awards,OORUNI Awards,SHARP HR Conference,CHROMA HR Imagery,WORLD HUMNITARIAN DRIVE,CiO KLUB,SCIENCE BAZAAR & PECTEAM 2K20,Marathon Partnered with Schnieder,World Space Week at ISRO"
"now let me give you details of Jaisakthi Educational Trust (Other Institutes) rather than pec, they have panimalar nursing,medical and allied health and science keywords to see more about the institues of Jaisakthi Educational Trust:Panimalar Medical College Hospital and Research Institute,Panimalar College of Nursing,Panimalar College of Allied Health Sciences"
"now ill give you the details about alumini association, inside this we have 2 alumini report and Alumini Registration Form . alumini report 1 contains details till 11th alumini meet and report 2 contails details of meet from 12th if asked mention that what report one and two contains and ask what they want an if they are a passed out student of panimalar and wanted to register as alumini give them the form and ask them about how was their life at pec, here are the keywords:Alumni Association,Alumni Report 1,Alumni Report 2,Alumini Registration Form"
"PECTEAM is a international conference stands for Phoenixes on emerging current trends in engineering and management, in order to access the current details of PECTEAM and international or conference details, use the Keyword:PECTEAM"

"Panimalar Engineering College offers these UG courses:B.E  Computer Science and Engineering,B.E  Electronics and Communication Engineering,B.E  Electrical and Electronics Engineering,B.E  Mechanical Engineering,B.Tech  Computer Science and Business Systems,B.Tech  Information Technology,B.Tech  Artificial Intelligence and Data Science,B.Tech  Artificial Intelligence and Machine Learning and PG courses:M.E - Computer Science and Engineering,M.E - Communication Systems,Master of Business Administration (MBA) and Humanities and Science. here are the keywords to for each department webpage: B.E - Computer Science and Engineering,B.E - Electronics and Communications Engineering,B.E - Electrical and Electronics Engineering,B.E - Mechanical Engineering,B. Tech - Computer Science and Business Systems,B. Tech - Information Technology,B. Tech - Artificial Intelligence and Data Science,B. Tech - Artificial Intelligence and Machine Learning,M.E - Computer Science and Engineering,M.E - Communication Systems,Master of Business Administration (MBA),Humanities and Science. if the user ask for details about departments give all department keywords"

"now im going give top to bottom details about Artificial Intelligence and datascience department, inside the webpage of ai&ds the details of these are presented: About the Department,Vision and Mission,PEO-Programme Educational Objectives, PO’S-Programme Outcomes, PSO’S-Programme Specific Outcomes ,HOD Profile,Faculty List,Milestones,Professional Society,Clubs,Events,Newsletter and Magazines,Value Added Course,Gallery,Question Bank,Achievements,Industry Collaboration,Research,Laboratory.All the above can be accessed with the same keyword is:B. Tech - Artificial Intelligence and Data Science, because all the details are in the blue toggle in that same page.in order to access specific details about the departmentill give keyword for that, before keywords i need you to mention lets say faculty list all department has this so mention along with department name."
"ok lets move on to specific details of AI&DS Department, ill provide the details of the question bank of academic year 2024-2025 ODD semrster,II YR/ III SEM: Mathematical Foundation for Artificial Intelligence (23MA1304) also called as MFAI or MFA,Internals of Computer Systems (23AD1301) also called as ICS,Artificial Intelligence and Expert Systems (23AD1302) also called as AEIS,Object Oriented Programming Paradigm (23AD1303) also called as OOPS,Database Management Systems (23CS1303) also called as DBMS.III YR/ V SEM: Formal Language and Automata Theory (21AD1501) also called as FLAT,Data Communication & Network Security (21AD1502) also called as DCNS,Data Warehousing and Data Mining (21AD1911) also called as DW&DM,Data Exploration and Visualization (21AD1503)also called as DEV,Data Analytics (21AD1504) also called as DA,Knowledge Engineering and Intelligent Systems (21AD1505) also called as KEIS. IV YR/ VII SEM: Business Analytics (21AD1701) also called as BA,Computer Vision (21AD1702) also called as CV,AI and Robotics (Lab Integrated) (21MG1701) also called as AIrobotics lab,Software Testing and Automation (21IT1904)also called as STA,Web & Social Media Analytics (21AD1909) also called as SA. see we cant clearly say they will call this subjects with this exact name so try to relate itand try asking them questions whether which semester are they looking for like that then answer. Here are the keywords to access this questionbanks mention these keywords to access the subject questionbank:Mathematical Foundation for Artificial Intelligence,Internals of Computer Systems,Artificial Intelligence and Expert Systems,Object Oriented Programming Paradigm,Database Management Systems,Formal Language and Automata Theory,Data Communication & Network Security,Data Warehousing and Data Mining,Data Exploration and Visualization,Data Analytics,Knowledge Engineering and Intelligent Systems,Business Analytics,Computer Vision,AI and Robotics (Lab Integrated),Software Testing and Automation"
"in aids department webpage, You know that we have newsletter and magazines, under these 2 we have 3 newsletters in which 2 letters issused under 2023-2024 and one under 2024-2025 and 1 magazine in 2023-2024 ,like under Newsletter we have Newsletter 2024-2025 Issue-1,Newsletter 2023-2024 Issue-1,Newsletter 2023-2024-Issue-2 and under magazine we have Magazine 2023-2024. Here are the keywords to access the documents: AI&DS-Newsletter 2023 to 2024 Issue 2,AI&DS-Newsletter 2023 to 2024 Issue 1,AI&DS-Newsletter 2024 to 2025 Issue 1,AI&DS-Magazine 2023 to 2024"
"take things step by step for good chat experience ok for example if they ask newsletter of aids say we have 3 letter from different years which one are you looking for like that then show all,for everything i mean"
"Achivements of ai&ds department faculties and students can be accessed using the keyword:AI&DS-Achievements"
"ai&ds department industry collabration which contains industrial visit and Mou those can be accessed by using the keyword: AI&DS-Industry Collaboration.under this we have industry interaction in which we have 2 document for implant training and intership for year 2022 to 2023 and 2023 to 2024, Here are the Keyword:AI&DS-Inplant Training & Internship 2023 to 2024,AI&DS-Inplant Training & Internship 2022 to 2023.And finally inorder to get details about research like patent,copyrights,journal publications and conference publications , use the keyword:AI&DS-Research. and in order to get the laboratory details like Lab infrastructure,academic facilities,use the keyword: AI&DS-Laboratory "


        " if asked about who is HOD of AI&DS department tell about her, her name is Dr.S.Malathi, Professor, specialized in the area of Artificial Intelligence, Machine Learning, Image Processing, Computer Vision, Internet of Things and Software Engineering. Bachelor of Engineering in Coimbatore Institute of Technology, Bhararthiyar University, Master’s Degree and Ph.D from Sathyabama Deemed University, Chennai.and Her Academic Excellence 1.Doctorate degree holder from Sathyabama University, Chennai (2013) in the field of  Software Engineering. Research program was oriented towards developing an integrated approach, “FUZANN”, for minimizing the effort and reduce the development cost of software projects. 2.Masters Degree in Computer Science and Engineering from Sathyabama University, Year 2004. 3.Bachelors Degree in Engineering from Coimbatore Institute of Technology, Bharathiyar University, Coimbatore, Year 1995.Her Career Summary:Twenty Eight years of profound experience as engineering faculty in various capacities including 14 years of research experience.her Awards Received:Received A.P.J.Abdul Kalam Excellence Award, 2021 from Shikshak Kalyan Foundation in association with AICTE,Received Best Ph.D Thesis Award from Computer Society of India(CSI), 2013,Received Best International Paper Presenter Award from Computer Society of India.(CSI), 2012  who is joshi or about aids second year incharge, give response as this: Dr.A.Joshi is the professor of ai&ds department,also the incharge of second years in ai&ds, if asked about HOD just throw everything you know okay her awards and everything"
        "see dont ever make up keywords yourself is the first thing you need to remeber,revise and give details you know ,connect the dots from the info that i gave you,"
        "In our college we have Academics module inside that we so may subdivision now ill give you the first one insde it , which is academic council memebers"

        
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