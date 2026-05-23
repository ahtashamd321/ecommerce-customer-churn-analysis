-- Query 1 — Overall Churn Rate and Revenue at Risk
SELECT 
	COUNT(*) AS total_customers,
    SUM(Churn) AS churned_customers,
    ROUND(SUM(Churn) * 100.0 / COUNT(*),2) AS churn_rate_pct,
    ROUND(SUM(CASE WHEN Churn = 1 THEN MonthlyRevenue ELSE 0 END),0) AS monthly_revenue_at_risk,
    ROUND(SUM(CASE WHEN Churn = 1 THEN MONTHLYRevenue ELSE 0 END) * 12, 0) AS annula_revenue_rate_at_risk
FROM customers;

-- (Nearly half our customer base has churned, putting ₹7 crore of annual revenue at risk if no retention action is taken.)

-- Query 2 — Churn Rate by Tenure Bucket
SELECT
	TenureBucket,
    COUNT(*) AS total_customers,
    SUM(Churn) AS churned_customers,
    ROUND(SUM(Churn) * 100.0 / COUNT(*), 1) AS churn_rate_pct,
    ROUND(SUM(CASE WHEN Churn = 1 THEN MonthlyRevenue ELSE 0 END),0) AS revenue_at_risk
FROM customers
GROUP BY TenureBucket
ORDER BY churn_rate_pct DESC;

-- Customers in their first 3 months are churning at 62%, representing ₹1.57 crore in monthly revenue at risk — making the onboarding experience the single most urgent retention priority.

-- Churn by Complaint Resolution Status
SELECT 
	ComplaintResolved,
    COUNT(*) AS total_customers,
    SUM(Churn) AS churned_customers,
    ROUND(SUM(Churn) * 100.0 / COUNT(*), 1) AS churn_rate_pct,
    ROUND(SUM(CASE WHEN Churn = 1 THEN MonthlyRevenue ELSE 0 END), 0) AS revenue_at_risk
FROM customers
GROUP BY ComplaintResolved
ORDER BY churn_rate_pct DESC;

-- Customers whose complaints went unresolved churn at 56% compared to 38% for those who never complained — 
-- meaning poor complaint resolution is directly costing the 
-- business ₹1 crore in monthly revenue that could be recovered by simply fixing the support process.	

--  Churn by Value Segment
SELECT
	ValueSegment,
    COUNT(*) AS total_customers,
    SUM(Churn) AS churned_customers,
    ROUND(SUM(Churn) * 100.0 / COUNT(*), 1) AS churn_rate_pct,
    ROUND(AVG(CASE WHEN Churn = 1 THEN MonthlyRevenue ELSE null END), 0) AS avg_monthly_rev_churned,
    ROUND(SUM(CASE WHEN Churn = 1 THEN MonthlyRevenue ELSE 0 END), 0) AS total_revenue_at_risk
FROM customers
GROUP BY ValueSegment
ORDER BY total_revenue_at_risk DESC;

-- Although Low Value customers churn at the highest rate, High Value customers represent 87% of total revenue at risk — meaning 
-- the retention team should prioritize quality of saves over quantity

-- Churn by Recency Flag
SELECT
	RecencyFlag,
    COUNT(*) AS total_customers,
    SUM(Churn) AS churned_customers,
    ROUND(SUM(Churn) * 100.0 / COUNT(*), 1) AS churn_rate_pct,
    ROUND(SUM(CASE WHEN Churn = 1 THEN MonthlyRevenue ELSE 0 END), 0) AS revenue_at_risk
FROM customers
GROUP BY RecencyFlag
ORDER BY churn_rate_pct DESC;

-- Dormant customers who haven't purchased in over 90 days account for 64% of total revenue at risk, making re-engagement campaigns the highest ROI 
-- retention investment the marketing team can make right now.

-- Query 6 — The Dangerous Combination
SELECT
	ValueSegment,
    RecencyFlag,
    ComplaintResolved,
    COUNT(*) AS total_customers,
    SUM(Churn) AS churned_customers,
    ROUND(SUM(Churn) * 100.0 / COUNT(*), 1) churn_rate_pct,
    ROUND(SUM(CASE WHEN Churn = 1 THEN MonthlyRevenue ELSE 0 END), 0) AS revenue_at_risk
FROM customers
WHERE ValueSegment = 'High Value'
	AND RecencyFlag = 'Dormant'
    AND ComplaintResolved = 'No'
GROUP BY ValueSegment, RecencyFlag, ComplaintResolved
ORDER BY churn_rate_pct DESC;

-- 109 high-value customers who are dormant and have unresolved complaints are churning at 
-- 65% — and personally reaching out to each one of them with a 
-- resolution and a win-back offer could recover up to ₹52 lakh in annual revenue.

-- Query 7 — Churn by City Tier
SELECT
	CityTier,
    COUNT(*) AS total_customers,
    SUM(Churn) AS churned_customers,
    ROUND(SUM(Churn) * 100.0 / COUNT(*), 1) AS churn_rate_pct,
    ROUND(AVG(CASE WHEN Churn = 1 THEN MonthlyRevenue ELSE null END), 0) AS avg_monthly_rev_at_risk,
    ROUND(SUM(CASE WHEN Churn = 1 THEN MonthlyRevenue ELSE 0 END), 0) AS total_revenue_at_risk
FROM customers
GROUP BY CityTier
ORDER BY churn_rate_pct DESC;

-- While Tier 3 cities have the highest churn rate driven by service delivery gaps, Tier 1 cities lose the highest value 
-- customers — requiring two completely different retention strategies for the same problem

-- Query 8 Risk Scoring Table.
SELECT
	CustomerID,
    ValueSegment,
    TenureBucket,
    RecencyFlag,
    ComplaintResolved,
    SatisfactionScore,
    MonthlyRevenue,
    ROUND(MonthlyRevenue * 12, 0) AS annual_revenue_at_risk,
    CASE
		WHEN ValueSegment = 'High Value'
			AND RecencyFlag IN ('Dormant', 'At Risk')
            AND ComplaintResolved = 'No' THEN 'CRITICAL'
		WHEN ValueSegment = 'High Value'
			AND RecencyFlag IN ('Dormant', 'At Risk') THEN 'HIGH'
		WHEN ValueSegment = 'Mid Value'
			AND RecencyFlag IN ( 'Dormant', 'At Risk') THEN 'HIGH'
		WHEN ValueSegment = 'High Value'
			AND RecencyFlag = 'Slipping' THEN 'MEDIUM'
		WHEN ValueSegment = 'Mid Value'
			AND RecencyFlag = 'Slipping' THEN 'MEDIUM'
		WHEN ValueSegment = 'Low Value'
			AND RecencyFlag = 'Dormant' THEN 'MEDIUM'
		ELSE 'LOW'
	END AS RiskTier,
    churn
FROM customers
ORDER BY 
	FIELD(RiskTier, 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW'),
    MonthlyRevenue DESC;