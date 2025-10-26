# Data-Driven Global Student Recruitment
### Strategic Outreach Framework (WiDS)
Spark! October 25th Hackathon

---
## Overview 
Hi, welcome to our project! Our goal is to help Boston University expand its global recruitment opportunities by using data to make smarter outreach decisions. We researched and built a dataset that includes key indicators such as GDP per capita, number of international schools, student visa approval rates, and the size of a country’s upper-secondary (high school) student population. These factors help identify regions with strong potential for student engagement, allowing BU to reach students earlier in their academic journey and encourage them to apply. Ultimately, this approach supports BU’s mission of increasing global access and building a more diverse student body, because with greater diversity comes greater perspectives, innovation, and solutions.

## Objective 
Build a data-driven linear model that indetifies **where BU should recruit next** by analyzing: 
- International school availability  
- Visa approval feasibility  
- Youth population density  
- Financial accessibility
---

## Key Metrics & Weights

| Metric | Purpose | Weight | Insight |
|--------|---------|--------|---------|
| **International School Count** | Measures access to globally mobile students | **0.4** | Strong indicator of English proficiency and advising infrastructure |
| **Visa Approval Rate** | Measures feasibility of student mobility | **0.3** | Higher visa approval = stronger enrollment conversion |
| **Upper Secondary Population** | Measures future college-bound pipeline | **0.2** | Larger youth population = long-term growth |
| **GDP per Capita** | Proxy for financial ability | **0.1** | Higher affordability potential |

--- 

## Why These Weights?
The weights reflect **recruitment reality**—not just data importance.

- **International school access (0.4)** is the clearest pathway to meeting qualified students abroad.
- **Visa success (0.3)** directly impacts whether admitted students can enroll.
- **Youth population (0.2)** supports pipeline longevity by identifying countries with large and growing student populations.
- **GDP per capita (0.1)** matters, but aid programs can offset financial barriers.

Priority: **Access + Feasibility → Size → Affordability**

---
## Recruitment Opportunity Ranking
| Rank | Country | Score |
|------|---------|--------|
| 1 | China | 0.900 |
| 2 | India | 0.641 |
| 3 | **United Arab Emirates** | 0.390 |
| 4 | **Spain** | 0.252 |
| 5 | **Qatar** | 0.228 |
| 6 | **Thailand** | 0.216 |
| 7 | Singapore | 0.207 |
| 8 | Malaysia | 0.207 |
| 9 | Japan | 0.186 |
| 10 | Vietnam | 0.184 |
| 11 | Nigeria | 0.183 |
| 12 | Germany | 0.177 |
| 13 | Egypt | 0.163 |
| 14 | Canada | 0.159 |
| 15 | Saudi Arabia | 0.159 |

---
## What Is the Recruitment Opportunity Score?
The **Recruitment Opportunity Score** ranks countries by combining the metrics above using a weighted formula. Because each metric has a different scale (e.g. population in millions vs approval rates in percentages), we used **min–max normalization** to convert all data into values between 0 and 1.

This ensures fairness and prevents large values like population from overpowering visa or school data.

---

## Strategic Outreach Framework

### Core Principles
| Strategy | Description |
|----------|-------------|
| **Travel by Region** | Focus recruitment tours within the same region to increase visit efficiency |
| **Follow Urban Youth Density** | Prioritize large metro areas with high student populations |
| **Target International School Clusters** | Visit regions that have multiple schools per trip |
| **Ensure Regional Diversity** | Rotate outreach globally to prevent over-concentration |
| **Use Risk Filtering** | Take into account countries with low visa approval or high cost friction from the United States|

--- 
## Conclusion
This framework gives BU a **scalable, evidence-based approach** to global recruitment. It balances:

- Maintaining strong student pipelines in major countries (China, India)  
- Expanding into **high-opportunity emerging markets** (UAE, Spain, Thailand, Nigeria)  
- Improving **return on travel investment**  
- Strengthening **global access and diversity**  

---
## Repository Structure

| Folder | Description |
|--------|-------------|
| `Data/` | Contains raw and cleaned datasets used for analysis |
| `Notebooks/` | Jupyter notebooks for data exploration and model development |
| `deliverables/` | Project deliverables such as reports, slides, and documentation |
| `merging/` | Temporary working folder used for combining notebook and data files |
| `README.md` | Project overview and documentation |

## ✍️ Contributors

| Name | Role | Email |
|------|------|--------|
| Chloe Ling | Team Member |  |
| Diya Vora | Team Member |  |
| Cindy Frempong | Team Member |  |
| Primah Muwanga | Team Member |  |
| Arsheya Jaishiva | Team Member |  |


