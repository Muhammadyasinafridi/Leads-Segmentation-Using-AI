#import required libraries
from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib

#Create FastAPI Instance

app=FastAPI(
    title="AI Based Leads Intent Segmentation",
    description="This is an Unspervised Machine learning Model (KMeans Clustering) for Leads Segmentation",
    version="1.0.0"
)

#For FrontEnd and BackEnd Connectivity Enable CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


#Load ML Model, Scaler,PCA, and Features_names Files using joblib

kmeans=joblib.load("kmeans_model.joblib")  #KMeans_Clustering ML Model
scaler=joblib.load("scaler.joblib")        # Nuemrical Features Scaled File 
pca=joblib.load("pca.joblib")
feature_names=joblib.load("feature_names.joblib")
print("Joblib Files uploaded Successfully")


#Input Schema 

class LeadsFeature(BaseModel):
    TotalVisits:int
    TotalTimeSpent_sec:int
    PageViewsPer_visit:int 
    Lead_Origin:str
    Lead_Source:str
    Occupation:str

#Define Cluster Business Startegy

CLUSTER_MAPPING={

    0:{"lead_type": "Low Engagement Leads","conversion_rate": "15%"},
    1:{"lead_type": "Warm Engagement Leads","conversion_rate": "42%"},
    2:{"lead_type": "Hot High-Intent Leads","conversion_rate": "78%"},
    3:{"lead_type": "Casual Browsers Leads","conversion_rate": "20%"},
    4:{"lead_type": "Form Submitters Leads","conversion_rate": "55%"},
    5:{"lead_type": "Student Explorers Leads","conversion_rate": "10%"}


}


#API Endpoints/Routes

@app.get("/")
def rootroute():
    return{"message": "Welcome to the smart AI Based Leads intent segmentation"}

@app.post("/Segment_Lead")
def LeadSegmentor(features:LeadsFeature):
    try:

        #Create a DataFrame of all Columns initialized with 0
        input_dataFrame=pd.DataFrame(0,index=[0], columns=feature_names)

        #Set Numerical values

        input_dataFrame.at[0,"TotalVisits"]=int(features.TotalVisits)
        input_dataFrame.at[0, "Total Time Spent on Website"]=int(features.TotalTimeSpent_sec)
        input_dataFrame.at[0, "Page Views Per Visit"]=int(features.PageViewsPer_visit)


        #set Categorical Columns
        Categorical_input=[
            f"Lead Origin_{features.Lead_Origin}",
            f"Lead Source_{features.Lead_Source}",
            f"What is your current occupation_{features.Occupation}"

        ]

        for col in Categorical_input:
            if col in input_dataFrame:
                input_dataFrame.at[0,col]=1.0


        #Scale only numerical inputs

        numerical_inputs = ['TotalVisits', 'Total Time Spent on Website', 'Page Views Per Visit']
        input_dataFrame[numerical_inputs]=scaler.transform(input_dataFrame[numerical_inputs])

        #Apply PCA on all inputs
        #convert Dataframe to numpy array

        pca_tranformed=pca.transform(input_dataFrame.to_numpy())

        #Apply KMeans Clustering 
        #Convert predicted value to intiger values only

        Predicted_Cluster=int(kmeans.predict(pca_tranformed)[0])

        #Return response
        strategy = CLUSTER_MAPPING.get(Predicted_Cluster, {})
        return {
                    "cluster_id": Predicted_Cluster,
                    "prediction": strategy
                }





    


    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction Error: {str(e)}")


#To run 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("Main:app", host="127.0.0.1", port=8000, reload=True)
