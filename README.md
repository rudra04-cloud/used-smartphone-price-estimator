# Used Smartphone Resell Price Estimator

End-to-end machine learning regression project and Streamlit web app for estimating secondary market resale values of used smartphones.

**Institution:** Bennett University | **Specialization:** B.Tech CSE (AI)

## Overview
- **Dataset:** `used_device_data.csv` (3,454 records)
- **Features (11):** `device_brand`, `os`, `5g`, `screen_size`, `rear_camera_mp`, `front_camera_mp`, `internal_memory`, `ram`, `battery`, `release_year`, and `normalized_new_price`
- **Best Model:** Random Forest Regressor (200 Trees, 80/20 train/test split, `random_state=42`)

## Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
