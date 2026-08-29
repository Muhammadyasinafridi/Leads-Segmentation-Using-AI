BackEnd Url on render please click https://leads-segmentation-using-ai.onrender.com


To Access UI click here https://muhammadyasinafridi.github.io/Leads-Segmentation-Using-AI/

##Smart AI Based Leads Intent Segmentation System

An end-to-end unsupervised machine learning application that categorizes digital marketing leads based on behavioral patterns and 
engagement metrics. This project includes a complete data preprocessing pipeline, model selection benchmark, a **FastAPI** REST backend, 
and an interactive **HTML/CSS/JavaScript** frontend interface deployed on **Render**.

##Project Overview

Digital marketing platforms capture large volumes of unlabelled prospect data. This application automates lead qualification by:
- Processing raw marketing leads through a multi-stage feature engineering pipeline.
- Evaluating multiple unsupervised clustering techniques to select the optimal segmentation strategy.
- Serving real-time intent predictions and strategy playbooks via an interactive web interface.

## Tech Stack & Architecture

* **Frontend:** HTML5, CSS3, JavaScript (Fetch API / Async UI)
* **Backend API:** Python 3.10+, FastAPI, Uvicorn, Pydantic
* **Data Science & ML:** Pandas, NumPy, Scikit-Learn (StandardScaler, OneHotEncoder, PCA, Elbow Method, KMeans, AgglomerativeClustering)
* **Model Persistence:** Joblib
* **Deployment & Control:** Render,GitHub

## Feature Engineering & Model Selection

### 1. Data Preprocessing & Cleaning
* **Missing Value Handling:** Imputed numerical features using median values and filled categorical missing entries with modal values
* or dedicated unknown categories.
* **Outlier Handling:** Winsorized/clipped extreme values using IQR thresholds to prevent distortion in distance calculations.
* **Categorical Encoding:** Applied **One-Hot Encoding (OHE)** to convert nominal categorical variables into sparse binary features.
* **Feature Scaling:** Standardized features using `StandardScaler` ($\mu=0, \sigma=1$) to unify feature scales prior to distance-based
* modeling.

### 2. Dimensionality Reduction & Clustering Benchmark
* **PCA (Principal Component Analysis):** Applied PCA to reduce feature dimensionality while maintaining variance and removing
* multi-collinearity.
* **Model Comparison:** 
  * **Hierarchical (Agglomerative) Clustering:** Evaluated dendrogram structures and linkage metrics for baseline grouping.
  * **K-Means Clustering (Selected):** Evaluated cluster compactness using Elbow Method (WCSS) and Silhouette Scores.
  * **K-Means yielded tighter, better-separated clusters** and faster inference speeds compared to Hierarchical Clustering,
  * making it the final model chosen for production.

