from fastapi import FastAPI, APIRouter
from fastapi.responses import RedirectResponse

import datetime

from app.semester import get_current_week_number, get_period, get_semester_start_date

import logging

app = FastAPI(
    title='Semester API',
)

router = APIRouter()


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')


@router.get("/week")
async def get_week_number():
    return {"week_number": get_current_week_number()}


@router.get("/semester")
async def get_semester_info():
    period = get_period(datetime.date.today())
    start_date = get_semester_start_date(period.year_start, period.year_end, period.semester)

    return {
        "semester": period.semester,
        "start_date": start_date.strftime("%d.%m.%Y"),
        "year_start": period.year_start,
        "year_end": period.year_end,
    }


app.include_router(router, prefix='/api')


@app.on_event("startup")
async def startup_event():
    logging.basicConfig(level=logging.INFO)
    logging.info(" Date: " + datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"))