# chapter_11_api.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from kadai_functions import fit_trendline, country_trendline, generate_image
from fastapi.responses import FileResponse
import os

app = FastAPI()

@app.get("/say_hi/")
def say_hi():   
    return {"Hi": "There"}


@app.get("/say_hello/{name}")
def say_hello(name):
    return {"Hello": name}


class TrendlineInput(BaseModel):
    timestamps: List[int]
    data: List[float]


@app.post(
    "/fit_trendline/",
    summary="Fit a trendline to any data",
    description="Provide a list of integer timestamps and a list of floats",
)
def calculate_trendline(trendline_input: TrendlineInput):
    slope, r_squared = fit_trendline(trendline_input.timestamps, trendline_input.data)
    return {"slope": slope, "r_squared": r_squared}


@app.get("/country_trendline/{country}")
def calculate_country_trendline(country: str):
    slope, r_squared,intercept = country_trendline(country)
    return {"slope": slope, "r_squared": r_squared}


@app.get("/country_image/{country}")
def generate_country_image(country: str):
    IMAGE_PATH = generate_image(country)
    #IMAGE_PATH = country+".png"
    print(IMAGE_PATH)
    if os.path.exists(IMAGE_PATH):
        return FileResponse(IMAGE_PATH, media_type="image/png")
    else:
        return {"error": "画像生成に失敗しました"}
