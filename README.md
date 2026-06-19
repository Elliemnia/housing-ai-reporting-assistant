# Housing AI Reporting Assistant

An AI-powered reporting assistant that helps public-sector and nonprofit teams turn CSV datasets into stakeholder-friendly executive summaries.

## Project Purpose

Many public agencies, nonprofits, and community organizations work with important datasets but have limited time and technical resources to analyze them. This project demonstrates how AI can support reporting workflows by transforming structured data into clear, plain-English insights for non-technical stakeholders.

## Features

- Upload a CSV file
- Preview dataset structure
- Display row and column counts
- Identify numeric columns
- Generate basic statistics
- Generate an executive summary using Claude API
- Includes demo fallback mode when API credits are unavailable
- Translate technical findings into plain language for stakeholders

## Tech Stack

- Python
- Streamlit
- Pandas
- Claude API
- Anthropic Python SDK
- Python dotenv

## Example Use Case

A housing department, civic organization, or nonprofit can upload eviction, housing inventory, program, or service data and quickly generate a plain-language summary for internal teams, leadership, or community stakeholders.

## Demo Mode

This project supports a demo fallback mode. If a live Claude API response cannot be generated because of missing credits, billing limits, or API configuration, the app displays a sample executive summary instead of failing.

This makes the tool easier to test and demonstrates the intended user experience.

## How to Run Locally

1. Clone the repository

```bash
git clone https://github.com/Elliemnia/housing-ai-reporting-assistant.git
cd housing-ai-reporting-assistant
