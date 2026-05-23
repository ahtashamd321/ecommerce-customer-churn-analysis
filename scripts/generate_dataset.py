import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker('en_IN')
np.random.seed(42)
random.seed(42)

N = 5000  # customers
START_DATE = datetime(2024, 1, 1)
END_DATE   = datetime(2024, 12, 31)

# ── helpers ──────────────────────────────────────────────────────────────────
def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

def clamp(val, lo, hi):
    return max(lo, min(hi, val))

# ── base customer attributes ──────────────────────────────────────────────────
customer_ids   = [f"CUST{str(i).zfill(5)}" for i in range(1, N+1)]
genders        = np.random.choice(['Male', 'Female'], N, p=[0.54, 0.46])
age            = np.random.randint(18, 65, N)
city_tiers     = np.random.choice(['Tier 1', 'Tier 2', 'Tier 3'], N, p=[0.35, 0.40, 0.25])
preferred_device = np.random.choice(['Mobile', 'Desktop', 'Tablet'], N, p=[0.65, 0.28, 0.07])
preferred_payment = np.random.choice(
    ['UPI', 'Credit Card', 'Debit Card', 'COD', 'Net Banking', 'Wallet'],
    N, p=[0.32, 0.20, 0.18, 0.15, 0.08, 0.07]
)
preferred_category = np.random.choice(
    ['Fashion', 'Electronics', 'Grocery', 'Beauty', 'Home & Kitchen', 'Sports'],
    N, p=[0.28, 0.22, 0.18, 0.14, 0.12, 0.06]
)
marital_status = np.random.choice(['Single', 'Married'], N, p=[0.45, 0.55])

# ── tenure & registration ─────────────────────────────────────────────────────
tenure_months = np.random.choice(
    [1,2,3,4,5,6,7,8,9,10,11,12,18,24,30,36],
    N,
    p=[0.07,0.06,0.06,0.05,0.05,0.05,0.04,0.04,0.04,0.04,0.04,0.04,
       0.10,0.10,0.10,0.12]
)
registration_date = [END_DATE - timedelta(days=int(t*30.5)) for t in tenure_months]

# ── behavioural signals ───────────────────────────────────────────────────────
orders_per_month   = np.round(np.random.exponential(2.5, N), 1).clip(0.5, 15)
avg_order_value    = np.round(np.random.lognormal(6.8, 0.7, N), 2).clip(150, 12000)
total_orders       = np.round(orders_per_month * tenure_months).astype(int).clip(1, 500)
total_spend        = np.round(avg_order_value * total_orders, 2)

warehouse_to_door  = np.round(np.random.normal(4.5, 1.8, N), 1).clip(1, 12)  # days
days_since_last_order = np.random.choice(
    list(range(1, 180)),
    N,
    p=[1/179]*179
)

satisfaction_score = np.random.choice([1,2,3,4,5], N, p=[0.08,0.12,0.25,0.35,0.20])
complaints_raised  = np.random.choice([0,1,2,3,4,5], N, p=[0.48,0.25,0.13,0.07,0.04,0.03])
complaint_resolved = np.where(
    complaints_raised > 0,
    np.random.choice([0,1], N, p=[0.28, 0.72]),
    np.nan
)

cashback_received  = np.round(np.random.exponential(180, N), 2).clip(0, 2500)
coupon_used_count  = np.random.poisson(3, N).clip(0, 20)
returned_orders    = np.round(total_orders * np.random.beta(1.2, 8, N)).astype(int)
app_logins_per_month = np.round(np.random.exponential(8, N), 0).clip(1, 60).astype(int)
wishlist_items     = np.random.poisson(4, N).clip(0, 30)

# ── churn logic (business-realistic) ─────────────────────────────────────────
# Start with a base churn probability and adjust with real-world drivers
churn_prob = np.full(N, 0.18)  # base ~18% industry churn

# Tenure: new customers churn more
churn_prob += np.where(tenure_months <= 3,  0.22, 0)
churn_prob += np.where((tenure_months > 3) & (tenure_months <= 6), 0.10, 0)
churn_prob += np.where(tenure_months > 24, -0.08, 0)

# Satisfaction: strong signal
churn_prob += np.where(satisfaction_score == 1,  0.30, 0)
churn_prob += np.where(satisfaction_score == 2,  0.18, 0)
churn_prob += np.where(satisfaction_score == 3,  0.05, 0)
churn_prob += np.where(satisfaction_score >= 4, -0.10, 0)

# Complaints: unresolved ones hurt more
churn_prob += complaints_raised * 0.06
churn_prob += np.where(
    (complaints_raised > 0) & (complaint_resolved == 0), 0.12, 0
)

# Recency: not ordering recently is a red flag
churn_prob += np.where(days_since_last_order > 90,  0.18, 0)
churn_prob += np.where(days_since_last_order > 120, 0.10, 0)
churn_prob += np.where(days_since_last_order < 30, -0.08, 0)

# Order frequency: low engagement
churn_prob += np.where(orders_per_month < 1,   0.12, 0)
churn_prob += np.where(orders_per_month > 4,  -0.08, 0)

# COD customers churn slightly more (lower digital commitment)
churn_prob += np.where(preferred_payment == 'COD', 0.06, 0)

# High return rate: dissatisfied signal
return_rate = returned_orders / total_orders.clip(1)
churn_prob  += np.where(return_rate > 0.3, 0.10, 0)

# Delivery speed: slow delivery hurts
churn_prob += np.where(warehouse_to_door > 7, 0.08, 0)
churn_prob += np.where(warehouse_to_door < 3, -0.05, 0)

# City tier: Tier 3 slightly higher churn (service quality gaps)
churn_prob += np.where(city_tiers == 'Tier 3', 0.05, 0)

# Clamp to valid probability range
churn_prob = churn_prob.clip(0.03, 0.95)

# Final churn flag
churn = (np.random.rand(N) < churn_prob).astype(int)

# ── churn date (only for churned customers) ───────────────────────────────────
churn_date = [
    random_date(registration_date[i], END_DATE).strftime('%Y-%m-%d')
    if churn[i] == 1 else None
    for i in range(N)
]

# ── monthly revenue (key business metric) ────────────────────────────────────
monthly_revenue = np.round(avg_order_value * orders_per_month, 2)

# ── CLV estimate (simple: monthly revenue × expected remaining tenure) ────────
avg_remaining_tenure = np.where(churn == 0, 24, 0)  # 24-month forward look for active
clv_estimate = np.round(monthly_revenue * avg_remaining_tenure, 2)

# ── build dataframe ───────────────────────────────────────────────────────────
df = pd.DataFrame({
    'CustomerID'            : customer_ids,
    'Gender'                : genders,
    'Age'                   : age,
    'MaritalStatus'         : marital_status,
    'CityTier'              : city_tiers,
    'PreferredDevice'       : preferred_device,
    'PreferredPaymentMode'  : preferred_payment,
    'PreferredCategory'     : preferred_category,
    'RegistrationDate'      : [d.strftime('%Y-%m-%d') for d in registration_date],
    'TenureMonths'          : tenure_months,
    'OrdersPerMonth'        : orders_per_month,
    'AvgOrderValue'         : avg_order_value,
    'TotalOrders'           : total_orders,
    'TotalSpend'            : total_spend,
    'MonthlyRevenue'        : monthly_revenue,
    'CLV_Estimate'          : clv_estimate,
    'DaysSinceLastOrder'    : days_since_last_order,
    'WarehouseToDoorDays'   : warehouse_to_door,
    'SatisfactionScore'     : satisfaction_score,
    'ComplaintsRaised'      : complaints_raised,
    'ComplaintResolved'     : complaint_resolved,
    'CashbackReceived'      : cashback_received,
    'CouponUsedCount'       : coupon_used_count,
    'ReturnedOrders'        : returned_orders,
    'AppLoginsPerMonth'     : app_logins_per_month,
    'WishlistItems'         : wishlist_items,
    'Churn'                 : churn,
    'ChurnDate'             : churn_date,
})

# ── quick sanity checks ───────────────────────────────────────────────────────
print("=" * 55)
print("   DATASET GENERATION COMPLETE")
print("=" * 55)
print(f"  Total customers     : {len(df):,}")
print(f"  Churned customers   : {churn.sum():,}  ({churn.mean()*100:.1f}%)")
print(f"  Active customers    : {(1-churn).sum():,}")
print(f"  Date range          : {START_DATE.date()} → {END_DATE.date()}")
print(f"  Columns             : {len(df.columns)}")
print()
print("  Churn by Tenure bucket:")
df['TenureBucket'] = pd.cut(df['TenureMonths'],
    bins=[0,3,6,12,24,99],
    labels=['0-3m','3-6m','6-12m','12-24m','24m+'])
print(df.groupby('TenureBucket', observed=True)['Churn'].mean().apply(lambda x: f"  {x*100:.1f}%"))
print()
print("  Churn by Satisfaction Score:")
print(df.groupby('SatisfactionScore')['Churn'].mean().apply(lambda x: f"  {x*100:.1f}%"))
print()
print("  Churn by City Tier:")
print(df.groupby('CityTier')['Churn'].mean().apply(lambda x: f"  {x*100:.1f}%"))
print()

monthly_rev_at_risk = df[df['Churn']==1]['MonthlyRevenue'].sum()
print(f"  Monthly Revenue at Risk : ₹{monthly_rev_at_risk:,.0f}")
print(f"  Annual Revenue at Risk  : ₹{monthly_rev_at_risk*12:,.0f}")
print("=" * 55)

# ── export ────────────────────────────────────────────────────────────────────
df.drop(columns=['TenureBucket']).to_csv('/home/claude/ecommerce_churn_dataset.csv', index=False)
print("\n  ✓ Saved → ecommerce_churn_dataset.csv")