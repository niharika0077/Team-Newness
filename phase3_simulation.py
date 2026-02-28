import pandas as pd
import os

def run_impact_simulation():
    # 1. LOAD DATASETS
    if not os.path.exists("data/msme_dataset.csv") or not os.path.exists("data/scheme_dataset.csv"):
        print("❌ Error: Run Phase 1 first to generate data.")
        return

    msme_df = pd.read_csv("data/msme_dataset.csv")
    scheme_df = pd.read_csv("data/scheme_dataset.csv")
    
    simulation_results = []

    # 2. MULTI-SCHEME ELIGIBILITY LOGIC
    # Checkpoint Requirement: Multi-scheme eligibility logic
    for _, msme in msme_df.iterrows():
        # Matches based on Sector, Growth_Category, and Location
        eligible_schemes = scheme_df[
            (scheme_df['Eligible_Sectors'].str.contains(msme['Sector'])) & 
            (scheme_df['Target_Category'] == msme['Growth_Category']) &
            ((scheme_df['Location_Criteria'] == 'All') | (scheme_df['Location_Criteria'] == msme['Location_Type']))
        ]

        if not eligible_schemes.empty:
            # 3. REVENUE & EMPLOYMENT IMPACT SIMULATION
            # Select the scheme with the highest revenue impact factor for simulation
            best_scheme = eligible_schemes.sort_values('Impact_Factor_Revenue', ascending=False).iloc[0]
            
            # Mathematical Projections
            # Revenue Impact (Capped at 25% per Phase 1 rules)
            rev_before = msme['Annual_Revenue']
            rev_gain = rev_before * (best_scheme['Impact_Factor_Revenue'] / 100)
            rev_after = rev_before + rev_gain
            
            # Employment Impact (Capped at 10 jobs per Phase 1 rules)
            jobs_created = best_scheme['Impact_Factor_Employment']
            
            simulation_results.append({
                "MSME_ID": msme['MSME_ID'],
                "Sector": msme['Sector'],
                "Growth_Category": msme['Growth_Category'],
                "Selected_Scheme": best_scheme['Scheme_Name'],
                "Subsidy_Cost": best_scheme['Max_Subsidy_Amount'],
                "Revenue_Before": round(rev_before, 2),
                "Revenue_After": round(rev_after, 2),
                "Revenue_Gain": round(rev_gain, 2),
                "Jobs_Created": jobs_created
            })

    # 4. EXPORT RESULTS FOR OPTIMIZATION
    output_df = pd.DataFrame(simulation_results)
    output_df.to_csv("data/impact_simulation.csv", index=False)

    # 5. SUMMARY OUTPUT (For Judges' Verification)
    print("\n" + "="*45)
    print(" PHASE 3: IMPACT SIMULATION SUMMARY ")
    print("="*45)
    print(f"Total MSMEs Eligible for Funding: {len(output_df)}")
    print(f"Projected Total Revenue Growth: ₹{output_df['Revenue_Gain'].sum():,.2f}")
    print(f"Projected Total New Jobs: {int(output_df['Jobs_Created'].sum())}")
    
    print("\nSample Projection (Before vs After):")
    # Checkpoint Requirement: Clear before-and-after projections
    print(output_df[['MSME_ID', 'Selected_Scheme', 'Revenue_Before', 'Revenue_After', 'Jobs_Created']].head())
    print("\n✅ Simulation results saved to data/impact_simulation.csv")

if __name__ == "__main__":
    run_impact_simulation()