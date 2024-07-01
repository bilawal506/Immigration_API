import json
import re
from openai import OpenAI
from document_ai.settings import API_KEY
from document_ai.models.consultation_request import ConsultationRequest
from document_ai.models.consultation_response import ConsultationResponse

client = OpenAI(api_key=API_KEY)

def sanitize_json(json_string):
    return re.sub(r'(?<=\d),(?=\d)', '', json_string)


async def get_scholarship_consultation(request: ConsultationRequest):
    print(f"""
        ------------------------------------------------------------------------------------------
          {request}
        ------------------------------------------------------------------------------------------
    """)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": """
You should give these informations about a scholorship IN THIS SAME FORMAT WHETHER a CV IS PROVIDED OR NOT:-
1. University Name (Give Proper University name not just "Various countries in USA" blah blah blah)
2. Country name
3. Scholarship name
4. Recommended Program Name
5. University tuition Fee (approx.)
6. Living cost (approx.)
7. Duration program
8. Job opportunities
9. Future Prospects
10. Long term residency & passport
11. Application Link to apply in university
12. Religious demographics of country
13. GDP of country
14. Breif Description Of Country

THE CURRENCY SHOULD BE IN 'USD'

Dont add Additional Chit chat just generate with proper names and data i dont u to say like "It has various programms like MBA, MAR, MIA, IAW" just write straightly like "MBA, MIA, MAR, IAW" its an example.

Secondly, i want to add these to the database so i will give u gpt actions after sometime so give me answers in "JSON ARRAY FORMAT ONLY"

and Lastly, Dont Talk about anything else just give me the json data of them scholarships

IMPORTANT NOTE:- GIVE ONLY 5 SCHOLORSHIPS!!!
             
NOTE:- "ALWAYS SHOW TUTION FEES AND SCHOLARSHIPS FOR INTERNATIONAL STUDENTS"

NOTE:- "THE CURRENCY SHOULD BE IN 'USD' AND PLEASE ADD COMMMAS IN NUMBERS"

IMPORTANT NOTE:- EVERY NUMBER SHOULD BE ACCURATE AS POSSIBLE PLEASE IT IS A VERY IMPORTANT NOTE

NOTE:- "DONT ADD PREFIXES LIKE MILLION THOUSANDS ETC READ THE PROMPT CAREFULLY AND DONT USE PREFIXES"

NOTE:- "ALSO TELL THAT WILL BE POSSIBLE DURATION OF WORK I MEAN HOW MUCH TIME WILL THE POSSIBLY GET TO WORK"
             
NOTE:- "AND WHAT WILL BE THAT POSSIBLE EAARNING AFTER THAT EDUCATION"
             
NOTE:- "AND WHAT ARE THE CHANGE TO GET SCHOLARSHIP"

NOTE:- "ALL FEES SHOULD BE ONLY PER YEAR"

NOTE:- "THE TUITION FEE WHEN ADDED TOGETHER MAY BE EQUAL TO OR BELOW THE USER'S BUDGET"

NOTE:- "THE RESPONSE SHOULD ALWAYS BE IN JSON FORMAT AND READY TO BE ADDED INTO THE DATABASE AND ALSO SO THAT IT CAN BE SEARCHED FROM THE DATABASE AND PROVIDED TO THE USER"

NOTE:-"JUST SAY THE RELIGIONS NAMES DONT SAY THAT HOW MUCH POPULATION OF THAT RELIGION IS IN THAT COUNTRY"
             
NOTE:- "ALSO ALWAYS RETURN THE PERCENTAGE OF IMMIGRANTS OF USERS NATIONALITY."

NOTE:-"BE VERY SPECIFIC WITH INFORMATION"

Important NOTE:- EVERY NUMBER SHOULD BE ACCURATE AS POSSIBLE AS UP TO 1 IT IS A VERY IMPORTANT NOTE

NOTE:- "READ GUIDELINES BEFORE ANSWERING AND GIVE FULL ACCURATE ANSWERS NO CHIT CHATS!"

NOTE:-"ALSO SHOW THE PERCENTAGE FOR THE AMOUNT OF RELIGION IN A COUNTRY"

NOTE:-"U DONT UNDERSTAND DO U? "Job opportunities": "Research, Software Development, Data Science, AI" NOT LIKE THIS. I SAID IF THERE ARE MULTIPLE THINGS MAKE A LIST OF IT AND I MEANT IT FOR ALL THE MULTIPLE ATTRIBUTES."

NOTE:- "DONT GIVE LINKS IN TEXTS JUST PASTE THE WHOLE LINK IN THE JSON FORMAT"

NOTE:- "DONT GIVE ANYTHING RELATED TO NORMAL TEXT LIKE "VARIES ON THE LOCATION OF THE CAMPUS" JUST GIVE THE GDP JUST GIVE THE GDP OF ONE CAMPUS WE DONT CARE WHICH CAMPUS IT IS DONT MAKE IT FLEXIBLE MAKE IT MORE ACCURATE!!!"

NOTE:-"WHAT IS THIS HUH? "Long term residency & passport": "Eligible for Optional Practical Training (OPT) and potential H-1B visa" NOT LIKE THIS. IF THERE ARE MULTIPLE THINGS MAKE A LIST OF THEM DONT USE HELPING VERBS AND NOT LIKE "ELIGIBLE FOR" JUST SAY THE NAME DONT ADD ANYTHING BE AS SPECIFIC JUST SAY NAMES IF MULTIPLE MAKE A LIST"

This GPT provides detailed information about various scholarships available worldwide. The assistant offers data about each scholarship in a structured JSON format. The primary role is to guide users in finding the best scholarships based on their criteria, including eligibility, deadlines, and application processes. 

The GPT should prioritize accuracy and comprehensiveness, ensuring all responses are up-to-date and relevant. 

It will respond in a clear, concise, and helpful manner, using a friendly and professional tone. If a user asks for specific information not directly available, the GPT should use its browsing capability to find the latest details. 

Guidelines:
- Provide structured information in JSON format where appropriate.
- Include eligibility criteria, deadlines, benefits, and application processes for each scholarship.
- Offer suggestions based on the user's profile or preferences when asked.

When clarification is needed, the GPT should ask specific questions to understand the user's needs better. Personalization includes addressing users by name if provided, and tailoring responses to fit their academic background and goals.
REMEMBER: DONOT ADD json``` like thisjson```[]``` before and after array

Important conditions:
- If the user is enrolled in a program and has provided semesters passed and remaining, do not consider Program Name and Program Duration.
- If aiProgram is true, recommend the program based on the CV.
- If aiCountry is true, recommend the country based on the program.
- Ensure the response is always in JSON format and ready for database entry.
"""},
            {"role": "user", "content": f"Give me scholarship for this CV {request.document_text}, with these Filters:- Budget max {request.budget}$, in the country of {request.country}, in the University {request.university}, i want scholarships {request.programName} Program Duration {request.programDuration}, Country in which User is '{request.userCountry}' and i want scholarship of cover tution fees {request.tutionFee} and i also want scholarship to cover {request.universityFee} percent of scholarship i also want scholarship to cover the cost of living {request.costOfLiving} and i want university to be internationally in between these ranking {request.internationalUniversityRanking} and i am enrolled in {request.programEnrolled} in my universtity i have passed {request.semestersPassed} in months and {request.semestersRemainings} month of semesters are remaining and if {request.aiProgram} is true then recommend me the program according to my cv and if aiCountry is true then recommend me program country according to program"},
            {"role": "user", "content": """
The response should be a JSON array of objects, where each object represents a scholarship. Here is an example format:

[
    {
        "University Name": "Example University",
        "Country name": "Example Country",
        "Scholarship name": "Example Scholarship",
        "Recommended Program Name": "Example Program",
        "University tuition Fee (approx.)": 2000,
        "Living cost (approx.)": 1000,
        "Duration program": "2 years",
        "Nationality Immigrations Number":"30%",
        "Earning Duration": "5 hours",
        "Earning After Education": "2LPA",
        "Chances Of Scholarship": "70%",
        "Job opportunities": [
            "Research",
            "Teaching Assistant",
            "Internships"
        ],
        "Future Prospects": [
            "Corporate Sector",
            "Academia",
            "Government Jobs"
        ],
        "Long term residency & passport": [
            "Work Visa",
            "Permanent Residency",
            "Citizenship"
        ],
        "Application Link to apply in university": "https://www.example.com",
        "Religious demographics of country": {
            "Religion1": "70%",
            "Religion2": "20%",
            "Religion3": "10%"
        ],
        "GDP of country": "5,000,000,000,000",
        "Brief Description Of Country": "Example country description."
    },
    ...
]
"""}
        ],
        max_tokens=3000,
        temperature=0.1,
    )

    response_content = response.choices[0].message.content

    # Debugging: Print the raw response content
    print("Raw response content:", response_content)

    try:
        # Sanitize the response content to remove commas from numbers
        sanitized_response_content = sanitize_json(response_content)

        # Ensure the response content is valid JSON
        response_data = json.loads(sanitized_response_content)
        
        # Validate that response_data is a list
        if not isinstance(response_data, list):
            raise ValueError("Response data is not a list")

    except json.JSONDecodeError as e:
        # Debugging: Print the error and raw response content
        print("JSON decoding error:", str(e))
        print("Raw response content that caused the error:", response_content)
        raise ValueError(f"Invalid JSON response from OpenAI API: {str(e)}")
    except ValueError as e:
        # Debugging: Print the error and raw response content
        print("Value error:", str(e))
        print("Raw response content that caused the error:", response_content)
        raise ValueError(f"Unexpected response format from OpenAI API: {str(e)}")

    # Manually map the parsed JSON data to the ConsultationResponse model
    recommendations = []
    for recommendation in response_data:
        religious_demographics = recommendation.get('Religious demographics of country', {})
        religious_percentage_str = ', '.join([f"{religion}: {percentage}" for religion, percentage in religious_demographics.items()])
        consultation_response = ConsultationResponse(
            university_name=recommendation.get('University Name', ''),
            country_name=recommendation.get('Country name', ''),
            scholarship_name=recommendation.get('Scholarship name',''),
            earning_duration=recommendation.get('Earning Duration',''),
            earning_after_education=recommendation.get('Earning After Education',''),
            chances_of_scholarship=recommendation.get('Chances Of Scholarship',''),
            recommended_program_name=recommendation.get('Recommended Program Name', ''),
            university_tuition_fee=str(recommendation.get('University tuition Fee (approx.)', '')),
            living_cost=str(recommendation.get('Living cost (approx.)', '')),
            duration_program=recommendation.get('Duration program', ''),
            job_opportunities=', '.join(recommendation.get('Job opportunities', [])),
            future_prospects=', '.join(recommendation.get('Future Prospects', [])),
            long_term_residency_passport=', '.join(recommendation.get('Long term residency & passport', [])),
            application_link=recommendation.get('Application Link to apply in university', ''),
            nationality_immigrants_no=recommendation.get('Nationality Immigrations Number', ''),
            religious_demographics= religious_percentage_str,
            gdp=recommendation.get('GDP of country', ''),
            description=recommendation.get('Brief Description Of Country', '')
        )

        recommendations.append(consultation_response)

    return recommendations
