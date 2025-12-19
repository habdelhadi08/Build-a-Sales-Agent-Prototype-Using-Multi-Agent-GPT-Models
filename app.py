# app.py
import streamlit as st
from agents import run_sales_agent

st.set_page_config(
    page_title="AI Sales Assistant – Account Intelligence",
    layout="wide"
)

st.title("AI Sales Assistant – Account Intelligence")

# ----------------------------
# Helper: Normalize competitor URLs
# ----------------------------
def normalize_competitor_url(url: str) -> str:
    url = url.lower().strip()
    if "target.com" in url:
        return "https://corporate.target.com/about"
    if "amazon.com" in url:
        return "https://www.aboutamazon.com/about-us"
    if "walmart.com" in url:
        return "https://corporate.walmart.com/about"
    return url

# ----------------------------
# Input Fields
# ----------------------------
product_name = st.text_input("Product Name *")
company_url = st.text_input("Target Company URL *")
product_category = st.text_input("Product Category")
value_proposition = st.text_area("Value Proposition *")
target_customer = st.text_input("Target Customer")
competitor_urls = st.text_area(
    "Competitor URLs (one per line)",
    placeholder="https://www.target.com\nhttps://www.amazon.com"
)

pdf_file = st.file_uploader(
    "Optional: Upload Product Overview (PDF)",
    type=["pdf"]
)

# ----------------------------
# Generate Report
# ----------------------------
if st.button("Generate Account Intelligence"):
    if not product_name or not company_url or not value_proposition:
        st.error("Please fill out all required fields.")
    else:
        competitors_list = [
            normalize_competitor_url(c)
            for c in competitor_urls.splitlines()
            if c.strip()
        ]

        with st.spinner("Generating account intelligence report..."):
            report = run_sales_agent(
                product_name=product_name,
                company_url=company_url,
                category=product_category,
                value_prop=value_proposition,
                target=target_customer,
                competitors=competitors_list,
                pdf=pdf_file
            )

        st.markdown(report)




