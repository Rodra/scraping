# Senior Automation & Scraping Engineer Assessment

## Project Overview
This repository contains a base project structure for the Senior Automation & Scraping Engineer assessment. The goal is to build a resilient web scraper for a fictional retailer's portal that extracts product inventory data.

## Project Structure
```
.
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── scraper/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── parser.py
│   │   └── utils.py
│   └── data/
│       ├── __init__.py
│       └── models.py
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   └── test_parser.py
└── docs/
    └── system_design.md
```

## Assessment Requirements

### Part 1: System Design Document
Create a system design document (2-3 pages) that describes:
1. Cloud-based data pipeline integration using GCP
2. Monitoring and maintenance approach
3. Scaling strategy for multiple portals
4. Data security and compliance strategies

### Part 2: Web Scraper Implementation
Build a Python-based web scraper that:
1. Authenticates to https://quotes.toscrape.com/
2. Extracts data from multiple pages
3. Handles common scraping challenges:
   - Session management
   - Rate limiting
   - Error recovery
   - Data validation

## Evaluation Criteria
1. **Code Quality (25%)**
   - Clean, readable, and well-organized code
   - Appropriate error handling and logging
   - Efficient resource usage

2. **Resilience & Reliability (25%)**
   - Authentication handling
   - Failure recovery
   - Anti-blocking strategies

3. **System Design (25%)**
   - Cloud architecture
   - Scalability
   - Monitoring and maintenance

4. **Data Processing (15%)**
   - Data validation
   - Structured output
   - Edge case handling

5. **Documentation & Communication (10%)**
   - Clear explanations
   - Design decisions
   - Running instructions

## Getting Started

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Submission Instructions
1. Implement your solution
2. Push your code to a new private repository
3. Share access with our GitHub user: qualitara-technical-vetting
4. Submit your system design document via email (if not included in the repository) to technical.vetting@qualitara.com, CCing your recruiter

## Notes
- Use any Python libraries you're comfortable with
- Include a section on "what you would do with more time"
- Ask questions if anything is unclear

Good luck!
