import pandas as pd
import numpy as np

df =pd.read_csv("C:/Users/ahtas/Downloads/ecommerce_churn_dataset.csv")

# first look
print(df.shape)
print(df.head())
print(df.dtypes)
print(df.isnull().sum())

# Fix ComplaintResolved — treat null as "No Complaint"
df['ComplaintResolved'] = df['ComplaintResolved'].fillna('No Complaint')
df['ComplaintResolved'] = df['ComplaintResolved'].astype(str).replace({
    '1.0' : 'Yes',
    '0.0' : 'No',
})

# Confirm
print(df['ComplaintResolved'].value_counts())

# Statistical summary of key numaric columns
cols = [
    'TenureMonths', 'OrdersPerMonth', 'AvgOrderValue', 'TotalOrders',
    'TotalSpend', 'MonthlyRevenue', 'DaysSinceLastOrder', 'WarehouseToDoorDays',
    'SatisfactionScore', 'ComplaintsRaised', 'CashbackReceived', 'ReturnedOrders', 
    'AppLoginsPerMonth'
]

print(df[cols].describe().round())

# Create business-ready derived columns
# 1. Return Rate — what % of orders were returned
df['ReturnRate'] = (df['ReturnedOrders'] / df['TotalOrders']).round(3)

# 2. Tenure Bucket — lifecycle stage
df['TenureBucket'] = pd.cut(
    df['TenureMonths'],
    bins=[0, 3, 6, 12, 24, 36],
    labels=['0-3 Months', '3-6 Months', '6-12 Months', '12-24 Months', '24+ Months']
)

# 3. Customer Value Segment based on MonthlyRevenue
df['ValueSegment'] = pd.qcut(
    df['MonthlyRevenue'],
    q=3,
    labels=['Low Value', 'Mid Value', 'High Value']
)

# 4. Risk Flag for unresolved complaints
df['UnresolvedComplaint'] = np.where(df['ComplaintResolved'] == 'No', 1, 0)

# 5. Recency Flag
df['RecencyFlag'] = pd.cut(
    df['DaysSinceLastOrder'],
    bins=[0, 30, 60, 90, 180],
    labels=['Active', 'Slipping', 'At Risk', 'Dormant']
)

# Confirm everything looks right
print(df[['CustomerID', 'ReturnRate', 'TenureBucket', 
          'ValueSegment', 'UnresolvedComplaint', 'RecencyFlag']].head(10))

print("\nValue Segment distribution:")
print(df['ValueSegment'].value_counts())

print("\nRecency Flag distribution:")
print(df['RecencyFlag'].value_counts())

print("\nTenure Bucket distribution:")
print(df['TenureBucket'].value_counts().sort_index())

# Save cleaned dataset for Phase 3 SQL Analysis
df.to_csv('ecommerce_churn_cleaned_v2.csv', index=False)

# Final confirmation
print("=" * 50)
print("PHASE 2 COMPLETE — CLEANED DATASET READY")
print("=" * 50)
print(f"Total Customers     : {len(df):,}")
print(f"Total Columns       : {len(df.columns)}")
print(f"Churned Customers   : {df['Churn'].sum():,} ({df['Churn'].mean()*100:.1f}%)")
print(f"Dormant Customers   : {(df['RecencyFlag'] == 'Dormant').sum():,}")
print(f"Unresolved Complaints: {df['UnresolvedComplaint'].sum():,}")
print(f"High Value Customers : {(df['ValueSegment'] == 'High Value').sum():,}")
print("=" * 50)
print("New columns added:")
new_cols = ['ReturnRate', 'TenureBucket', 'ValueSegment', 
            'UnresolvedComplaint', 'RecencyFlag']
for col in new_cols:
    print(f"  ✓ {col}")
print("\nFile saved → ecommerce_churn_cleaned.csv")


