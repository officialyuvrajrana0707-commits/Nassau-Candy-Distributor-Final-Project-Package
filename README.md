# Nassau-Candy-Distributor-Final-Project-Package
Files:
1. Nassau_Candy_Final_Analysis.xlsx – cleaned/derived data and all KPI tables.
2. Nassau_Candy_Shipping_Route_Final_Report.pdf – executive/research-style report.
3. app.py – Streamlit dashboard source. Keep it in the same folder as the Excel workbook and run: streamlit run app.py

Important data-quality finding:
Order dates are 2024–2025 while ship dates are 2026–2030. Therefore calculated lead times are 904–1,642 days and 100% exceed 365 days. The analysis intentionally preserves the supplied dates rather than inventing corrected dates.
