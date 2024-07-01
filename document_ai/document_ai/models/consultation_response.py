from pydantic import BaseModel

class ConsultationResponse(BaseModel):
    university_name: str
    country_name: str
    scholarship_name: str
    recommended_program_name: str
    university_tuition_fee: str
    living_cost: str
    duration_program: str
    job_opportunities: str
    future_prospects: str
    long_term_residency_passport: str
    application_link: str
    nationality_immigrants_no: str
    earning_duration: str
    earning_after_education: str
    chances_of_scholarship: str
    religious_demographics: str
    gdp: str
    description: str
