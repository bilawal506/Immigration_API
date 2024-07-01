from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from document_ai.endpoints.consultation import router as consultation_router

app = FastAPI(description="Scholarship AI")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your frontend's URL if necessary
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(consultation_router)