import pandas as pd
import numpy as np
import os

# Create directory structure
os.makedirs('data', exist_ok=True)

# 1. DEFINE DIVERSIFIED SECTORS
sectors = [
    "Manufacturing", "Services", "Retail", "Technology", 
    "Agri-Tech", "Pharmaceuticals", "Renewable Energy", "Textiles"
]

# --- 2. MSME DATASET GENERATION (400 Entries) ---
np.random.seed(42)
num_msmes = 400 

msme_data = {
    # Basic Information
    "MSME_ID": [f"MSME_{i+1:03d}" for i in range(num_msmes)],
    "Sector": np.random.choice(sectors, num_msmes),
    "Years_of_Operation": np.random.randint(1, 20, num_msmes),
    "Ownership_Type": np.random.choice(["Sole Proprietorship", "Partnership", "Pvt Ltd"], num_msmes),
    "Category": np.random.choice(["Micro", "Small", "Medium"], num_msmes),
    "Location_Type": np.random.choice(["Urban", "Semi-Urban", "Rural"], num_msmes),
    
    # Financial Indicators
    "Annual_Revenue": np.random.randint(10, 800, num_msmes), 
    "Revenue_Growth_Rate": np.random.uniform(2, 25, num_msmes),
    "Profit_Margin": np.random.uniform(5, 30, num_msmes),
    "Debt_Outstanding": np.random.randint(0, 200, num_msmes),
    "Loan_to_Revenue_Ratio": np.random.uniform(0.1, 0.8, num_msmes),
    
    # Operational Indicators
    "Number_of_Employees": np.random.randint(5, 150, num_msmes),
    "Capacity_Utilization": np.random.uniform(40, 95, num_msmes),
    "Export_Percentage": np.random.uniform(0, 90, num_msmes),
    "Technology_Level": np.random.randint(1, 6, num_msmes),
    
    # Compliance Indicators (Score 0-100)
    "GST_Compliance_Score": np.random.randint(40, 100, num_msmes),
    "Inspection_Score": np.random.randint(40, 100, num_msmes),
    "Documentation_Readiness_Score": np.random.randint(40, 100, num_msmes),
}

df_msme = pd.DataFrame(msme_data)

# --- ACCURACY BOOSTING LOGIC ---
# Mathematical correlation between Tech/Revenue and Growth_Category
correlation_score = (
    (df_msme['Technology_Level'] * 12) + 
    (df_msme['Revenue_Growth_Rate'] * 2.5) + 
    (df_msme['Profit_Margin'] * 1.8) +
    (df_msme['Export_Percentage'] * 0.4)
)

def determine_category(score):
    if score > 130: return "High"
    if score > 75: return "Moderate"
    return "Low"

df_msme['Growth_Category'] = correlation_score.apply(determine_category)
df_msme.to_csv("data/msme_dataset.csv", index=False)

# --- 3. SCHEME DATASET (Min 5 Schemes) ---
schemes = [
    {
        "Scheme_ID": 1, "Scheme_Name": "Green Tech Grant", 
        "Eligible_Sectors": "Renewable Energy, Manufacturing", "Max_Subsidy_Amount": 850000, 
        "Target_Category": "High", "Location_Criteria": "All",
        "Impact_Factor_Revenue": 22, # Within 5-25% rule
        "Impact_Factor_Employment": 9 # Within 1-10 jobs rule
    },
    {
        "Scheme_ID": 2, "Scheme_Name": "Rural Agri-Boost", 
        "Eligible_Sectors": "Agri-Tech, Retail", "Max_Subsidy_Amount": 400000, 
        "Target_Category": "Moderate", "Location_Criteria": "Rural",
        "Impact_Factor_Revenue": 15, "Impact_Factor_Employment": 6
    },
    {
        "Scheme_ID": 3, "Scheme_Name": "Pharma R&D Incentive", 
        "Eligible_Sectors": "Pharmaceuticals, Technology", "Max_Subsidy_Amount": 1000000, 
        "Target_Category": "High", "Location_Criteria": "Urban",
        "Impact_Factor_Revenue": 25, "Impact_Factor_Employment": 10
    },
    {
        "Scheme_ID": 4, "Scheme_Name": "Textile Modernization", 
        "Eligible_Sectors": "Textiles, Manufacturing", "Max_Subsidy_Amount": 550000, 
        "Target_Category": "Moderate", "Location_Criteria": "Semi-Urban",
        "Impact_Factor_Revenue": 12, "Impact_Factor_Employment": 7
    },
    {
        "Scheme_ID": 5, "Scheme_Name": "Digital Startup Fund", 
        "Eligible_Sectors": "Services, Technology", "Max_Subsidy_Amount": 300000, 
        "Target_Category": "Low", "Location_Criteria": "All",
        "Impact_Factor_Revenue": 10, "Impact_Factor_Employment": 4
    }
]

pd.DataFrame(schemes).to_csv("data/scheme_dataset.csv", index=False)
print("✅ Phase 1:  datasets generated.")