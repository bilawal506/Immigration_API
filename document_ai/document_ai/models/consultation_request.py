from pydantic import BaseModel

class ConsultationRequest(BaseModel):
    document_text: str
    budget: str
    country: str
    university: str
    programDuration: str
    userCountry: str
    tutionFee: str
    aiCountry: str
    universityFee: str
    aiProgram: str
    costOfLiving: str
    semestersPassed: str
    semestersRemainings: str
    programName: str
    programEnrolled: str
    internationalUniversityRanking: str