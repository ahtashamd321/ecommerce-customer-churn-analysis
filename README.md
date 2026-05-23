# E-Commerce Customer Churn Analysis
### Identifying Revenue Risk and Building a Data-Driven Retention Strategy

---

## Project Overview

This project analyzes customer churn behavior across 5,000 e-commerce customers over a full year (Jan–Dec 2024). The goal was not simply to measure churn — but to identify **which customers are most financially dangerous to lose**, quantify the revenue impact, and deliver a prioritized retention strategy with specific actions for each business team.

The analysis moves from raw behavioral data through SQL-based segmentation, revenue risk quantification, and a four-tier customer risk framework — culminating in a five-page Power BI dashboard and a one-page business recommendation document.

---

## Business Problem

E-commerce companies spend ₹400–₹1,200 to acquire each new customer. When a customer churns, the business loses not just that customer — it loses the entire future revenue stream that customer would have generated, on top of the acquisition cost already spent.

**The core business questions this project answers:**

- Which customers are at highest risk of churning — and what is their financial value?
- At what stage of the customer lifecycle does churn hit hardest?
- Does complaint resolution behavior predict churn?
- How much annual revenue is currently at risk if no retention action is taken?
- Which specific actions should each business team take — and in what priority order?

---

## Dataset

The dataset was **custom-designed and generated** to reflect real e-commerce business logic — not sourced from a generic public repository. The schema was built around actual behavioral signals that drive churn in Indian e-commerce companies like Flipkart, Meesho, and Nykaa.

| Attribute | Details |
|-----------|---------|
| Total Records | 5,000 customers |
| Time Period | January 2024 – December 2024 |
| Total Columns | 33 |
| Churn Rate | 45.6% |
| Annual Revenue at Risk | ₹7.02 Crore |

**Key column categories:**

- **Identity** — CustomerID, Gender, Age, City Tier, Marital Status
- **Behavioral** — Orders Per Month, Days Since Last Order, App Logins, Wishlist Items, Return Rate
- **Experience** — Satisfaction Score, Complaints Raised, Complaint Resolution Status, Delivery Days
- **Financial** — Monthly Revenue, Total Spend, CLV Estimate, Cashback Received
- **Engineered** — Tenure Bucket, Value Segment, Recency Flag, Unresolved Complaint Flag, Risk Tier

---

## Tools & Technologies

| Tool | Purpose |
|------|---------|
| Python (Pandas, NumPy, Faker) | Dataset generation and data cleaning |
| MySQL | SQL-based business analysis and customer segmentation |
| Power BI | Interactive five-page dashboard |
| DAX | Custom KPI measures and calculated columns |

---

## Project Phases

### Phase 1 — Business Understanding
Defined the project objective, identified 10 core business questions, and established the analytical framework before touching any data. Business-first approach throughout.

### Phase 2 — Data Engineering
Generated a realistic 5,000-row dataset with business-logic-driven churn probabilities. Cleaned and enriched the data with five engineered columns:
- **TenureBucket** — lifecycle stage segmentation
- **ValueSegment** — revenue-based customer tiering
- **RecencyFlag** — engagement status (Active / Slipping / At Risk / Dormant)
- **UnresolvedComplaint** — binary flag for support failure
- **ReturnRate** — order return behavior ratio

### Phase 3 — SQL Analysis
Ran eight targeted business queries covering:
- Overall churn rate and annual revenue at risk
- Churn by tenure lifecycle stage
- Churn by complaint resolution status
- Revenue concentration by value segment
- Dormant customer revenue crisis
- The dangerous combination: High Value + Dormant + Unresolved Complaint
- Geographic churn by city tier
- Four-tier customer risk scoring framework (CRITICAL / HIGH / MEDIUM / LOW)

### Phase 4 — Power BI Dashboard
Built a five-page interactive dashboard:

| Page | Focus |
|------|-------|
| Executive Overview | Top-line KPIs and churn overview |
| Customer Segmentation | Behavioral and demographic churn drivers |
| Revenue Risk Analysis | Financial impact by segment and lifecycle |
| Retention Strategy | Risk tier breakdown and priority framework |
| Action Plan | Team-specific recommended actions with targets |

### Phase 5 — Recommendation Document
One-page business recommendation written in executive language — findings, implications, and actions by team with projected revenue recovery estimate.

---

## Key Findings

**Finding 1 — Scale of the crisis**
45.6% of customers churned in 2024, putting **₹7.02 crore in annual revenue at risk**. The industry average churn rate is approximately 20% — making this business's churn rate more than double the benchmark.

**Finding 2 — Early-stage customers are most vulnerable**
Customers in their first 3 months churn at **62%** — the highest rate across all lifecycle stages — contributing ₹1.57 crore in monthly revenue at risk. Onboarding experience is the single highest-ROI retention investment available.

**Finding 3 — Unresolved complaints are a silent revenue killer**
Customers with unresolved complaints churn at **56.4%** vs 37.8% for customers who never complained — an 18-percentage-point gap caused entirely by support team inaction. 721 customers currently have unresolved complaints representing ₹1.03 crore in monthly revenue at risk.

**Finding 4 — High Value customers carry disproportionate financial risk**
Although Low Value customers churn at the highest rate (52.7%), High Value customers represent **87% of total revenue at risk** despite having the lowest churn rate (39.4%). The business must prioritize quality of saves over quantity.

**Finding 5 — Dormant customers are the largest single revenue risk**
2,458 dormant customers (inactive 90+ days) churn at 58.3% and account for **₹3.7 crore in monthly revenue at risk** — 64% of total exposure. Re-engagement campaigns targeting this segment represent the highest ROI marketing action available.

**Finding 6 — The deadliest customer profile**
109 customers sit at the intersection of all three major risk factors: High Value + Dormant + Unresolved Complaint. This group churns at **65.1%** and carries ₹52 lakh in annual revenue at risk. Small enough to call personally. Dangerous enough to prioritize immediately.

---

## Risk Framework

A four-tier customer risk scoring framework was developed using value segment, recency behavior, and complaint resolution status:

| Risk Tier | Customers | Churn Rate | Annual Revenue at Risk | Recommended Action |
|-----------|-----------|------------|----------------------|-------------------|
| CRITICAL | 152 | 56.6% | ₹65.5L | Personal outreach within 7 days |
| HIGH | 2,044 | 47.4% | ₹425L | Automated re-engagement campaign |
| MEDIUM | 1,437 | 53.7% | ₹131.8L | Loyalty nudge campaigns |
| LOW | 1,367 | 33.1% | ₹79.6L | Standard engagement |

---

## Retention Recommendations

| Team | Priority Action | Target | Timeline |
|------|----------------|--------|---------|
| Retention | Personally call all 152 CRITICAL customers | Recover ₹20L annually | Week 1 |
| Marketing | Re-engagement campaign for 2,458 dormant customers | Reduce dormant churn 58%→45% | Week 2 |
| Customer Support | Resolve all 721 open complaints within 48 hours | Reduce unresolved churn 56%→42% | Immediate |
| Product | Fix onboarding for 0-3 month customers | Reduce early churn 62%→48% | Month 1 |

**Projected impact:** Implementing all four actions simultaneously could reduce overall churn from 45.6% to approximately 35% within 6 months — protecting an estimated **₹2.5 crore in annual revenue** currently at risk.

---

## Repository Structure

```
ecommerce-customer-churn-analysis/
│
├── data/
│   ├── ecommerce_churn_dataset.csv          # Raw generated dataset
│   └── ecommerce_churn_cleaned_v2.csv       # Cleaned and engineered dataset
│
├── scripts/
│   ├── generate_dataset.py                  # Dataset generation script
│   └── phase2_eda.py                        # Data cleaning and feature engineering
│
├── sql/
│   └── churn_analysis_queries.sql           # All 8 SQL analysis queries
│
├── dashboard/
│   └── ecommerce_churn_dashboard.pbix       # Power BI dashboard file
│
└── README.md
```

---

## How to Run

**1. Generate the dataset**
```bash
pip install pandas numpy faker
python scripts/generate_dataset.py
```

**2. Run data cleaning**
```bash
python scripts/phase2_eda.py
```

**3. Load into MySQL**
```bash
pip install sqlalchemy mysql-connector-python
python scripts/load_to_mysql.py
```

**4. Run SQL analysis**
Open `sql/churn_analysis_queries.sql` in MySQL Workbench and execute queries sequentially.

**5. Open dashboard**
Open `dashboard/ecommerce_churn_dashboard.pbix` in Power BI Desktop.

---

## About This Project

This project was built as a portfolio demonstration of end-to-end data analytics capability — from business problem definition through data engineering, SQL analysis, visualization, and business recommendation. Every analytical decision was made with a business outcome in mind, not just a technical output.

The dataset was intentionally custom-generated rather than sourced from a public repository to demonstrate schema design thinking and domain understanding of real e-commerce churn drivers.

---

*Built by Ahtasham Anjum | Data Analyst*
*Tools: Python · MySQL · Power BI · DAX*