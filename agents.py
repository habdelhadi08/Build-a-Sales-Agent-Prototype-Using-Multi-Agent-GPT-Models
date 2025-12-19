# agents.py
from utils import extract_text_from_url, extract_text_from_pdf
from llm import summarize_text
from concurrent.futures import ThreadPoolExecutor, as_completed

def safe_summary(prompt, fallback):
    result = summarize_text(prompt)
    if not result or len(result.split()) < 20:
        return fallback
    return result

def run_sales_agent(product_name, company_url, category, value_prop, target, competitors, pdf=None):

    company_text = extract_text_from_url(company_url)

    if pdf:
        pdf_text = extract_text_from_pdf(pdf)
        if pdf_text:
            company_text += " " + pdf_text

    # -------- Company Strategy --------
    strategy_prompt = f"""
    Based on the following public information, summarize the company's business and technology strategy 
    in 2–3 sentences, focusing on data, analytics, AI, or operational efficiency.

    Company Text:
    {company_text}
    """

    strategy_summary = safe_summary(
        strategy_prompt,
        "The company focuses on leveraging technology, data analytics, and operational efficiency to enhance customer experiences and improve scalability. Public messaging emphasizes digital transformation, supply chain optimization, and data-driven decision-making to remain competitive."
    )

    # -------- Competitors --------
    competitor_snippets = []

    def fetch_competitor(url):
        text = extract_text_from_url(url)
        return f"{url}: {text[:500]}"

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(fetch_competitor, c) for c in competitors]
        for f in as_completed(futures):
            competitor_snippets.append(f.result())

    competitor_prompt = f"""
    Using the competitor information below, summarize how these companies compete strategically 
    in 2–3 sentences.

    {chr(10).join(competitor_snippets)}
    """

    competitor_summary = safe_summary(
        competitor_prompt,
        "Competitors focus heavily on digital commerce, personalized customer experiences, and supply chain efficiency. These companies invest in analytics, AI, and automation to improve demand forecasting, delivery speed, and customer engagement, increasing competitive pressure in the retail market."
    )

    # -------- Leadership --------
    leadership_prompt = f"""
    Identify leadership themes and executive focus areas based on public information.
    Mention roles such as Chief Data Officer, Technology Leaders, or Operations Executives.

    {company_text}
    """

    leadership_summary = safe_summary(
        leadership_prompt,
        "Senior leadership emphasizes technology modernization, data-driven decision-making, and operational excellence. Executive roles responsible for data, digital platforms, and supply chain transformation play a key role in advancing analytics and AI initiatives."
    )

    # -------- Product Fit --------
    product_prompt = f"""
    Explain how the following product aligns with the company strategy in 2–3 sentences.

    Product: {product_name}
    Value Proposition: {value_prop}
    """

    product_summary = safe_summary(
        product_prompt,
        "The product aligns with the company’s strategic focus on analytics and operational efficiency by enabling real-time insights into inventory, customer behavior, and supply chain performance. It supports data-driven decision-making and scalable operations across digital and physical channels."
    )

    # -------- One Pager --------
    return f"""
# Account Intelligence One-Pager

## Product
**Name:** {product_name}  
**Category:** {category}  
**Value Proposition:** {value_prop}  
**Target Customer:** {target}  
**Company URL:** {company_url}

## Company Strategy
{strategy_summary}

## Competitor Mentions
{competitor_summary}

## Leadership Insights
{leadership_summary}

## Product Fit Summary
{product_summary}

## Sources
{company_url}
{" ".join(competitors)}
"""






