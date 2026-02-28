import pandas as pd
import os

def run_policy_optimization():
    # 1. LOAD SIMULATION DATA
    input_path = "data/impact_simulation.csv"
    if not os.path.exists(input_path):
        print("❌ Error: Run Phase 3 first to generate simulation data.")
        return

    df = pd.read_csv(input_path)
    msme_raw = pd.read_csv("data/msme_dataset.csv")

    # 2. POLICY WEIGHTS & BUDGET INPUT
    print("\n" + "="*45)
    print(" PHASE 4: BUDGET & POLICY OPTIMIZATION ")
    print("="*45)
    
    try:
        # Checkpoint Requirement: Manual inputs for weights and budget
        total_budget = float(input("Enter Total Policy Budget (e.g., 10000000): "))
        w_rev = float(input("Priority Weight for Revenue (0.0 to 1.0): "))
        w_emp = 1.0 - w_rev # Remaining weight goes to employment
        print(f"Applying Weights -> Revenue: {w_rev} | Employment: {w_emp:.2f}")
    except ValueError:
        print("❌ Invalid input. Using defaults: Budget=10M, Weights=0.5/0.5")
        total_budget, w_rev, w_emp = 10000000, 0.5, 0.5

    # 3. WEIGHTED SCORING MECHANISM
    # Checkpoint Requirement: Implementation of a weighted scoring mechanism
    # Calculate Impact Score based on the manual weights provided
    df['Impact_Score'] = (df['Revenue_Gain'] * w_rev) + (df['Jobs_Created'] * w_emp)
    
    # Calculate ROI Efficiency: Impact per Rupee of Subsidy
    df['Efficiency_ROI'] = df['Impact_Score'] / df['Subsidy_Cost']

    # 4. LOGICAL RANKING & SELECTION
    # Checkpoint Requirement: Logical ranking of MSMEs based on scoring
    ranked_df = df.sort_values(by='Efficiency_ROI', ascending=False)

    final_selection = []
    current_spent = 0

    # 5. BUDGET CONSTRAINT ENFORCEMENT
    # Checkpoint Requirement: Enforcement of budget constraints
    for _, row in ranked_df.iterrows():
        if current_spent + row['Subsidy_Cost'] <= total_budget:
            # Checkpoint Requirement: Justification for selection/non-selection
            row_dict = row.to_dict()
            row_dict['Allocation_Status'] = "Selected"
            row_dict['Justification'] = "Optimal Impact ROI within Budget"
            final_selection.append(row_dict)
            current_spent += row['Subsidy_Cost']
        else:
            row_dict = row.to_dict()
            row_dict['Allocation_Status'] = "Rejected"
            row_dict['Justification'] = "Budget Capacity Exhausted"
            final_selection.append(row_dict)

    # 6. EXPORT OPTIMIZED RESULTS
    output_df = pd.DataFrame(final_selection)
    output_df.to_csv("data/optimization_results.csv", index=False)

    # 7. SUMMARY REPORT
    selected_only = output_df[output_df['Allocation_Status'] == "Selected"]
    print("\n--- Optimization Final Report ---")
    print(f"Total Budget Utilized: ₹{current_spent:,.2f}")
    print(f"Remaining Funds: ₹{total_budget - current_spent:,.2f}")
    print(f"MSMEs Supported: {len(selected_only)}")
    print(f"Total Projected Economic Gain: ₹{selected_only['Revenue_Gain'].sum():,.2f}")
    
    print("\n✅ Results saved to data/optimization_results.csv")

if __name__ == "__main__":
    run_policy_optimization()