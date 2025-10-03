from backend.scraper import scrape_supreme_court
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from backend.database import SessionLocal, engine
import backend.models as models

app = FastAPI()

class CaseQuery(BaseModel):
    case_type: str
    case_number: int
    year: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/fetch-case")
def fetch_case(case_query: CaseQuery, db: Session = Depends(get_db)):
    db_query = models.Query(
        case_type = case_query.case_type,
        case_number = case_query.case_number,
        year = case_query.year
    )

    db.add(db_query)
    db.commit()
    db.refresh(db_query)

    scraper_result = scrape_supreme_court(case_query.case_type, case_query.case_number, case_query.year)

    raw_response = models.RawResponse(
        query_id = db_query.id,
        raw_html_or_json = str(scraper_result)
    )

    db.add(raw_response)
    db.commit()

    return{
        "query_id": db_query.id,
        "case_details": scraper_result
    }

@app.get("/case/{query_id}")
def get_case_details(query_id: int, db: Session = Depends(get_db)):
    db_query = db.query(models.Query).filter(models.Query.id == query_id).first()
    if not db_query:
        raise HTTPException(status_code=404, detail="Query not found")

    # Fetch associated raw responses and judgments
    raw_responses = db.query(models.RawResponse).filter(models.RawResponse.query_id == query_id).all()
    judgments = db.query(models.Judgment).filter(models.Judgment.query_id == query_id).all()

    return {
        "query": db_query,
        "raw_responses": raw_responses,
        "judgments": judgments
    }