from fastapi import FastAPI, APIRouter, HTTPException
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


@router.get("/week", tags=["semester"], summary="Возвращает номер текущей недели")
async def get_week_number():
    """
    Description:

        Возвращает номер текущей недели

    Response:

        - week - номер текущей недели

    Raises:

        - 404 - если семестр еще не начался
    """
    current_week = get_current_week_number()
    if current_week < 0:
        message = "Семестр еще не начался, до начала семестра осталось недель: " + str(-current_week)
        raise HTTPException(status_code=404, detail=message)

    return {
        "week": current_week
    }


@router.get("/semester", tags=["semester"], summary="Возвращает информацию о текущем семестре")
async def get_semester_info():
    """
    Description:

        Возвращает информацию о текущем семестре

    Response:

        - semester - номер текущего семестра
        - start_date - дата начала семестра
        - year_start - год начала семестра
        - year_end - год окончания семестра
    """
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
