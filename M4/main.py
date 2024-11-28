from fastapi import FastAPI, File, UploadFile
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
import glob
import aiofiles
import numpy as np
import pandas as pd
import sklearn as sk
from sklearn.model_selection import train_test_split
from lightgbm import LGBMClassifier
import os
import joblib
#import matplotlib.pyplot as plt

app = FastAPI()

glob_data=pd.DataFrame()
glob_model=joblib.load('./models/my_model.pkl')
glob_pedict=[]

@app.get("/")
async def root():
   return {"message": "Hello World"}



@app.post("/upload_csv_file/")
async def upload_csv_file(file: UploadFile = File(...)):
    file_location = f"./files/{file.filename}"
    if file.filename[-4:]==".csv":
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
        filesInDir=glob.glob(glob.escape("./files") + "/*.csv")
        return {"info": f"data storage:{[x[8:] for x in filesInDir]}"}
    return raises_error()

@app.get("/preprocess/")
async def prepocess_csv(filename:str):
    filesInDir=[x[8:] for x in glob.glob(glob.escape("./files") + "/*.csv")]
    if filename in filesInDir:
        try:
            preprocessing(filename)
            adress='./preprocess/'+filename[:-4]+".pkl"
            size=os.path.getsize(adress)
            return{"info": f"data preprocess:{filename} success!","size":f"{size} bit"}
        except:
            raises_error


@app.get("/loaded_csv/")
async def load_data():
    try:
        prerpocess_files=glob.glob(glob.escape("./files") + "/*.csv")
        return{"info": f"data csv:{[x[8:] for x in prerpocess_files]}"}
    except:
        return raises_error

@app.get("/ready_data")
async def ready_data():
    try:
        prerpocess_files=glob.glob(glob.escape("./preprocess") + "/*.pkl")
        return{f"{[x[13:] for x in prerpocess_files]}"}
    except:
        return raises_error


@app.get("/ready_models")
async def ready_models():
    try:
        prerpocess_files=glob.glob(glob.escape("./models") + "/*.pkl")
        return{f"{[x[9:] for x in prerpocess_files]}"}
    except:
        return raises_error


@app.get("/selcet_pickle")
async def selcet_pickle(filename: str):
    try:
        global glob_data
        print('./preprocess/'+filename)
        glob_data=pd.read_pickle('./preprocess/'+filename)
        return{"info":f"{filename}"}
    except:
        return raises_error
    
@app.get("/selcet_model")
async def selcet_model(filename: str):
    try:
        global glob_model
        pathhh='./models/'+ filename
        glob_model=joblib.load(pathhh)
        return{"info": f"select model success {filename}"}
    except:
        return raises_error


@app.get("/predict")
async def predict():
    try:
        global glob_model
        global glob_data
        data=glob_model.predict(glob_data).tolist()
        return{"predictions": data}
    except:
        return raises_error

@app.get("/draw")
async def predict(parametr: str):
    try:
        global glob_data
        global glob_pedict

    except:
        raises_error

@app.get("/info")
async def info():
    return "Разработка для системы классификации, для более подробной инофрмации перейдите в swagger-docs по адресу http://localhost:8000/docs"

def raises_error():
    raise HTTPException(400, detail='Bad request')

def preprocessing(path):
    df=pd.read_csv('./files/'+path)
    df=df.dropna()
    df.to_pickle('./preprocess/'+path[:-4]+".pkl")
    return