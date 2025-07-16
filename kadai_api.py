# chapter_11_api.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from kadai_functions import fit_trendline, country_trendline, generate_image, process_sdg_data
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
    print(IMAGE_PATH)#デバック用のプリントコマンド
    if os.path.exists(IMAGE_PATH):
        return FileResponse(IMAGE_PATH, media_type="image/png")#
    else:
        return {"error": "画像生成に失敗しました"}

_cached_df = None

def load_data():
    global _cached_df
    _cached_df = process_sdg_data()

def get_cached_df():
    global _cached_df
    if _cached_df is None:
        load_data()
    return _cached_df

@app.on_event("startup")
def startup_event():
    load_data()

@app.get("/available_countries", summary="利用可能な国名リストを取得")
def get_countries():
    df = get_cached_df()
    countries = list(df.columns)
    return {"countries": countries}

