import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import plotly.express as px

# --- 1. CONFIG & ASSET LOADING ---
st.set_page_config(page_title="AI MSME Pro", layout="wide")

def load_assets():
    if not os.path.exists('data/msme_dataset.csv'):
        st.error("❌ Data files not found. Ensure 'data/' folder contains the CSVs.")
        st.stop()
    msme = pd.read_csv("data/msme_dataset.csv")
    schemes = pd.read_csv("data/scheme_dataset.csv")
    with open('models/growth_model.pkl', 'rb') as f:
        ml = pickle.load(f)
    return msme, schemes, ml

msme_df, scheme_df, assets = load_assets()

# --- 2. MULTI-LAYER INTERFACE (TABS) ---
tab_dash, tab_reg = st.tabs(["🏛️ Strategic Authority Dashboard", "🔍 MSME Database Management"])

# --- LAYER 1: MSME SEARCH, INSIGHTS & REGISTRATION ---
with tab_reg:
    st.header("🔍 MSME Search & Registration Portal")
    
    search_id = st.text_input("Enter MSME ID to check database", placeholder="e.g., MSME_001").strip()
    
    if search_id:
        current_data = pd.read_csv("data/msme_dataset.csv")
        exists = current_data[current_data['MSME_ID'] == search_id]
        
        if not exists.empty:
            st.success(f"✅ Record Found for {search_id}")
            
            # --- SEARCH INSIGHTS ENGINE ---
            msme_data = exists.iloc[0]
            eligible_schemes = scheme_df[scheme_df['Target_Category'] == msme_data['Growth_Category']]
            
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.subheader("📋 Business Profile")
                st.write(f"**Sector:** {msme_data['Sector']}")
                st.write(f"**Annual Revenue:** ₹{msme_data['Annual_Revenue']} Lakhs")
                st.metric("Growth Classification", msme_data['Growth_Category'])

            with res_col2:
                st.subheader("💡 AI Suggested Scheme")
                if not eligible_schemes.empty:
                    best_match = eligible_schemes.sort_values('Impact_Factor_Revenue', ascending=False).iloc[0]
                    st.info(f"**Recommended:** {best_match['Scheme_Name']}")
                    r_impact = msme_data['Annual_Revenue'] * (best_match['Impact_Factor_Revenue'] / 100)
                    st.write(f"📈 **Projected Revenue Growth:** ₹{r_impact:.2f} Lakhs")
                else:
                    st.warning("No specific schemes found for this category.")
            st.divider()
            
        else:
            st.warning(f"⚠️ {search_id} not found. Please register below.")
            with st.form("full_registration_form"):
                st.subheader(f"New Profile Entry: {search_id}")
                c1, c2 = st.columns(2)
                with c1:
                    m_sector = st.selectbox("Industry Sector", assets['le_sector'].classes_)
                    m_rev = st.number_input("Annual Revenue (Lakhs)", value=150.0)
                    m_growth = st.number_input("Growth Rate (%)", value=12.0)
                    m_profit = st.number_input("Profit Margin (%)", value=18.0)
                    m_tech = st.slider("Technology Level", 1, 5, 3)
                with c2:
                    m_export = st.number_input("Export Intensity (%)", value=5.0)
                    m_emp = st.number_input("Employee Count", value=20)
                    m_gst = st.slider("GST Score", 0, 100, 85)
                    m_insp = st.slider("Inspection Score", 0, 100, 80)
                    m_cap = st.slider("Capacity Util %", 0, 100, 75)

                if st.form_submit_button("Save & Analyze"):
                    # 1. AI PREDICTION
                    input_row = pd.DataFrame([[m_rev, m_growth, m_profit, m_tech, m_export, m_emp, m_gst, m_insp, m_cap, assets['le_sector'].transform([m_sector])[0]]], columns=assets['features'])
                    predicted_cat = assets['model'].predict(input_row)[0]
                    
                    # 2. SAVE TO CSV
                    new_entry = {"MSME_ID": search_id, "Sector": m_sector, "Annual_Revenue": m_rev, "Revenue_Growth_Rate": m_growth, "Profit_Margin": m_profit, "Technology_Level": m_tech, "Export_Percentage": m_export, "Number_of_Employees": m_emp, "GST_Compliance_Score": m_gst, "Inspection_Score": m_insp, "Capacity_Utilization": m_cap, "Growth_Category": predicted_cat}
                    pd.DataFrame([new_entry]).to_csv("data/msme_dataset.csv", mode='a', header=False, index=False)
                    
                    # 3. SHOW IMMEDIATE RESULTS (The Solution for your issue)
                    st.success(f"🎉 {search_id} Registered Successfully!")
                    st.balloons()
                    
                    st.divider()
                    st.subheader("📊 Instant AI Growth Analysis")
                    ir_col1, ir_col2 = st.columns(2)
                    
                    # Display Classification
                    ir_col1.metric("Growth Classification", predicted_cat)
                    
                    # Match Scheme immediately for the new user
                    new_eligible = scheme_df[scheme_df['Target_Category'] == predicted_cat]
                    if not new_eligible.empty:
                        best_new_match = new_eligible.sort_values('Impact_Factor_Revenue', ascending=False).iloc[0]
                        ir_col2.info(f"**Suggested Scheme:** {best_new_match['Scheme_Name']}")
                        st.write(f"💡 *This business is eligible for up to ₹{best_new_match['Max_Subsidy_Amount']:,} in support.*")
                    else:
                        ir_col2.warning("No immediate scheme match found.")

# --- LAYER 2: STRATEGIC AUTHORITY DASHBOARD ---
with tab_dash:
    st.header("🏛️ Strategic Policy & Impact Dashboard")
    
    col_cfg, col_met = st.columns([1, 2])
    with col_cfg:
        st.subheader("Policy Configuration")
        total_budget = st.number_input("Total Subsidy Budget (INR)", value=5000000, step=500000)
        w_rev = st.slider("Revenue Priority Weight", 0.0, 1.0, 0.5)
        w_emp = 1.0 - w_rev

    # Optimization Engine
    dynamic_results = []
    current_msme_data = pd.read_csv("data/msme_dataset.csv") 
    
    for _, msme in current_msme_data.iterrows():
        eligible = scheme_df[scheme_df['Target_Category'] == msme['Growth_Category']]
        if not eligible.empty:
            eligible = eligible.copy()
            eligible['Temp_Score'] = (eligible['Impact_Factor_Revenue'] * w_rev) + (eligible['Impact_Factor_Employment'] * w_emp)
            best_s = eligible.sort_values('Temp_Score', ascending=False).iloc[0]
            
            r_gain = msme['Annual_Revenue'] * (best_s['Impact_Factor_Revenue'] / 100)
            jobs = best_s['Impact_Factor_Employment']
            eff = ((r_gain * w_rev) + (jobs * w_emp)) / best_s['Max_Subsidy_Amount']
            
            dynamic_results.append({
                **msme.to_dict(), 
                "Selected_Scheme": best_s['Scheme_Name'], 
                "Subsidy_Cost": best_s['Max_Subsidy_Amount'], 
                "Revenue_Gain": r_gain, 
                "Jobs_Created": jobs, 
                "Efficiency": eff
            })

    ranked_df = pd.DataFrame(dynamic_results).sort_values('Efficiency', ascending=False)
    final_rows, spent = [], 0
    for _, row in ranked_df.iterrows():
        r = row.to_dict()
        if spent + r['Subsidy_Cost'] <= total_budget:
            r['Status'], r['Reason'] = "✅ Selected", "Optimal Impact ROI"
            spent += r['Subsidy_Cost']
        else:
            r['Status'], r['Reason'] = "❌ Rejected", "Budget Capacity Exhausted"
        final_rows.append(r)

    full_res_df = pd.DataFrame(final_rows)
    selected_only = full_res_df[full_res_df['Status'] == "✅ Selected"]
    rejected_only = full_res_df[full_res_df['Status'] == "❌ Rejected"]

    # Metrics
    with col_met:
        st.subheader("Simulated Economic Impact")
        m1, m2, m3 = st.columns(3)
        m1.metric("Budget Utilization", f"₹{spent:,}")
        m2.metric("Total Jobs Created", int(selected_only['Jobs_Created'].sum()) if not selected_only.empty else 0)
        m3.metric("Total Revenue Gain", f"₹{selected_only['Revenue_Gain'].sum():,.1f}" if not selected_only.empty else "0")

    # Visuals
    st.divider()
    
    c1, c2 = st.columns(2)
    with c1:
        if not selected_only.empty:
            fig_pie = px.pie(selected_only, values='Revenue_Gain', names='Sector', title="Revenue Gain Division by Sector", hole=0.4)
            st.plotly_chart(fig_pie, use_container_width=True)
    with c2:
        if not selected_only.empty:
            fig_freq = px.bar(selected_only.groupby('Selected_Scheme')['MSME_ID'].count().reset_index(), x='Selected_Scheme', y='MSME_ID', title="Scheme Adoption Frequency", color='MSME_ID')
            st.plotly_chart(fig_freq, use_container_width=True)

    # Tables
    st.divider()
    st.subheader("📋 Policy Allocation Audit Log")
    sel_tab, rej_tab = st.tabs(["✅ Funded MSMEs", "❌ Rejected Candidates"])
    with sel_tab:
        st.dataframe(selected_only[['MSME_ID', 'Sector', 'Selected_Scheme', 'Efficiency', 'Revenue_Gain', 'Jobs_Created']], use_container_width=True)
    with rej_tab:
        st.dataframe(rejected_only[['MSME_ID', 'Sector', 'Selected_Scheme', 'Efficiency', 'Reason']], use_container_width=True)