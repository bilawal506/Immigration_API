# Immigration API (Scholarship AI)

A FastAPI backend that recommends scholarships to international students. A user uploads their CV (PDF, DOCX or image) together with optional filters such as budget, target country, program and university ranking. The API extracts the CV text, sends it with the filters to OpenAI's `gpt-4o`, and returns five structured scholarship recommendations as JSON.

## Features

- **CV parsing** for PDF, Word (`.docx`) and image files (OCR via Tesseract)
- **Personalised scholarship recommendations** (5 per request) based on the CV and the filters supplied
- **Rich results** per scholarship: university, country, program, tuition and living costs, duration, job opportunities, future prospects, residency and passport pathways, application link, chances of getting the scholarship, expected earnings, religious demographics, GDP and a short country description
- **AI-assisted choices**: can recommend the program from the CV (`aiProgram`) and the country from the program (`aiCountry`)
- **Interactive docs** at `/docs` (Swagger UI) and `/redoc`, provided by FastAPI
- **CORS enabled** for all origins by default

## Tech stack

| Area | Tools |
| --- | --- |
| Framework | FastAPI, Uvicorn |
| AI | OpenAI API (`gpt-4o`) |
| Document parsing | pdfplumber, python-docx, Pillow, pytesseract |
| Validation | Pydantic v2 |
| Packaging | Poetry, Python 3.12+ |

## Project structure

```
Immigration_API/
└── document_ai/
    ├── pyproject.toml
    ├── poetry.lock
    ├── .env                      # CHAT_GPT_API_KEY (see Configuration)
    ├── document_ai/
    │   ├── main.py               # FastAPI app, CORS, router registration
    │   ├── settings.py           # Loads CHAT_GPT_API_KEY from .env / environment
    │   ├── endpoints/
    │   │   └── consultation.py   # GET / and POST /consultation
    │   ├── services/
    │   │   ├── document_processing.py  # PDF / DOCX / image text extraction
    │   │   └── gpt_consultant.py       # Prompt, OpenAI call, JSON parsing
    │   └── models/
    │       ├── consultation_request.py
    │       └── consultation_response.py
    └── tests/
```

## Getting started

### Prerequisites

- Python 3.12 or newer
- [Poetry](https://python-poetry.org/docs/#installation)
- [Tesseract OCR](https://tesseract-ocr.github.io/tessdoc/Installation.html) installed on your system (needed only for image uploads)
  - Ubuntu/Debian: `sudo apt install tesseract-ocr`
  - macOS: `brew install tesseract`
- An [OpenAI API key](https://platform.openai.com/api-keys) with access to `gpt-4o`

### Installation

```bash
git clone https://github.com/bilawal506/Immigration_API.git
cd Immigration_API/document_ai
poetry install
```

### Configuration

Create a `.env` file in the `document_ai/` directory (the same folder as `pyproject.toml`):

```env
CHAT_GPT_API_KEY=your-openai-api-key
```

The key can also be provided as a regular environment variable. Keep this file private and never commit it to version control.

### Run the server

Run from the `document_ai/` directory (the app reads `.env` from the current working directory):

```bash
poetry run uvicorn document_ai.main:app --reload
```

The API is now available at `http://127.0.0.1:8000`, and the interactive docs at `http://127.0.0.1:8000/docs`.

## API reference

### `GET /`

Health check / welcome message.

```json
{ "Message": "Welcome TO EDU Immigrates" }
```

### `POST /consultation`

Generates scholarship recommendations from an uploaded CV and filters.

- **Request body:** `multipart/form-data` with a single `file` field (the CV)
- **Filters:** sent as **query parameters**
- **Supported file types:** PDF, DOCX, and images (`image/*`)

#### Query parameters

| Parameter | Required | Default | Description |
| --- | --- | --- | --- |
| `userCountry` | yes | | Applicant's country (nationality) |
| `programName` | no | `any` | Desired program |
| `country` | no | `any` | Target study country |
| `budget` | no | `any` | Maximum budget in USD |
| `university` | no | `any` | Target university |
| `programDuration` | no | `any` | Desired program duration |
| `tutionFee` | no | `any` | Tuition coverage wanted from the scholarship |
| `universityFee` | no | `any` | Percentage of university fees the scholarship should cover |
| `costOfLiving` | no | `any` | Cost-of-living coverage wanted |
| `internationalUniversityRanking` | no | `any` | Acceptable international ranking range |
| `programEnrolled` | no | `any` | Program the applicant is currently enrolled in |
| `semestersPassed` | no | `any` | Months of study already completed |
| `semestersRemainings` | no | `any` | Months of study remaining |
| `aiProgram` | no | `any` | Pass `true` to let the AI recommend a program from the CV |
| `aiCountry` | no | `any` | Pass `true` to let the AI recommend a country based on the program |

> The spellings `tutionFee` and `semestersRemainings` are intentional: they match the parameter names in the code.

If the applicant is already enrolled and both `semestersPassed` and `semestersRemainings` are given, program name and duration are ignored.

#### Example request

```bash
curl -X POST "http://127.0.0.1:8000/consultation?userCountry=Pakistan&country=Germany&budget=15000&aiProgram=true" \
  -F "file=@/path/to/cv.pdf"
```

#### Response

`200 OK` returns a JSON array of five scholarship objects. Every field is a string; list-like fields (job opportunities, future prospects, residency options, religious demographics) are comma-separated.

| Field | Description |
| --- | --- |
| `university_name` | University offering the scholarship |
| `country_name` | Country of the university |
| `scholarship_name` | Name of the scholarship |
| `recommended_program_name` | Suggested program |
| `university_tuition_fee` | Approximate yearly tuition (USD) |
| `living_cost` | Approximate yearly living cost (USD) |
| `duration_program` | Program length |
| `job_opportunities` | Likely job paths |
| `future_prospects` | Longer-term career prospects |
| `long_term_residency_passport` | Residency / citizenship pathways |
| `application_link` | Link to apply |
| `nationality_immigrants_no` | Share of immigrants from the applicant's nationality |
| `earning_duration` | Expected working time per period |
| `earning_after_education` | Expected earnings after graduating |
| `chances_of_scholarship` | Estimated chance of receiving the scholarship |
| `religious_demographics` | Religions in the country with percentages |
| `gdp` | GDP of the country |
| `description` | Short country description |

Illustrative shape (values are placeholders, not real data):

```json
[
  {
    "university_name": "Example University",
    "country_name": "Example Country",
    "scholarship_name": "Example Scholarship",
    "recommended_program_name": "Example Program",
    "university_tuition_fee": "2000",
    "living_cost": "1000",
    "duration_program": "2 years",
    "job_opportunities": "Research, Teaching Assistant, Internships",
    "future_prospects": "Corporate Sector, Academia, Government Jobs",
    "long_term_residency_passport": "Work Visa, Permanent Residency, Citizenship",
    "application_link": "https://www.example.com",
    "nationality_immigrants_no": "30%",
    "earning_duration": "5 hours",
    "earning_after_education": "2LPA",
    "chances_of_scholarship": "70%",
    "religious_demographics": "Religion1: 70%, Religion2: 20%, Religion3: 10%",
    "gdp": "5,000,000,000,000",
    "description": "Example country description."
  }
]
```

#### Errors

Any failure (unsupported file type, unreadable document, invalid JSON from the model, OpenAI errors) returns `500 Internal Server Error` with the message in `detail`.

## How it works

1. The uploaded CV is converted to plain text based on its content type (`pdfplumber`, `python-docx`, or `pytesseract` OCR for images).
2. The text and filters are combined into a prompt and sent to `gpt-4o` (`temperature=0.1`, `max_tokens=3000`), which is instructed to answer with a JSON array of exactly five scholarships.
3. The reply is parsed as JSON, mapped to the `ConsultationResponse` model, and returned to the client.

## Notes

- Recommendations are generated by a language model. Verify tuition figures, deadlines and application links with the university before applying.
- Restrict `allow_origins` in `document_ai/main.py` to your frontend's URL before deploying to production.
