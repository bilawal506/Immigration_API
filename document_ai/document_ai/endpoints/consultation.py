from fastapi import APIRouter, UploadFile, File, HTTPException
from document_ai.services.document_processing import process_document
from document_ai.services.gpt_consultant import get_scholarship_consultation
from document_ai.models.consultation_request import ConsultationRequest
from document_ai.models.consultation_response import ConsultationResponse
from typing import List

router = APIRouter()

@router.get("/")
def home():
    return {"Message": "Welcome TO EDU Immigrates"}

@router.post("/consultation", response_model=List[ConsultationResponse])
async def consultation(userCountry: str, programName: str = "any", country: str = 'any', budget: str = 'any', university: str = 'any', programDuration: str = 'any', tutionFee: str = "any", internationalUniversityRanking: str = "any", programEnrolled: str = "any", semestersPassed: str = "any", semestersRemainings: str = "any", universityFee: str = "any", costOfLiving: str = "any", aiProgram: str = "any", aiCountry: str = "any", file: UploadFile = File(...)):
    try:
        print("Received request with the following parameters:")
        print(f"userCountry: {userCountry}, country: {country}, budget: {budget}, university: {university}, programDuration: {programDuration}, programName: {programName}, internationalUniversityRanking: {internationalUniversityRanking}, tutionFee: {tutionFee}, programEnrolled: {programEnrolled}, semestersPassed: {semestersPassed}, semestersRemaining: {semestersRemainings}, universityFee: {universityFee}, costOfLiving: {costOfLiving}, aiProgram: {aiProgram},aiCuntry: {aiCountry}")

        document_text = await process_document(file)
        print(f"Document processed: {document_text}")
        
        consultation_request = ConsultationRequest(
            document_text=document_text,
            budget=budget,
            country=country,
            university=university,
            programDuration=programDuration,
            tutionFee=tutionFee,
            aiCountry=aiCountry,
            universityFee=universityFee,
            aiProgram=aiProgram,
            costOfLiving=costOfLiving,
            semestersPassed=semestersPassed,
            semestersRemainings=semestersRemainings,
            programName=programName,
            programEnrolled=programEnrolled,
            internationalUniversityRanking=internationalUniversityRanking,
            userCountry=userCountry,
        )
        
        print("Consultation request created successfully.")
        
        response = await get_scholarship_consultation(consultation_request)
        print("Response generated successfully.")
        
        return response
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
