# Comparative Analysis of Cause of Death Classification Among Individuals with IBD and their Matched Coutnerparts

This repository contains the analysis and code for comparing cause of death classification (for overall, premature, and non-premature mortality) among individuals with Inflammatory Bowel Disease (IBD) and their matched counterparts (i.e., individuals without IBD derived from the general population) using two different cause of death coding systems.

## Project Overview
In this analysis, we explore how the cause of death is classified for individuals with IBD, compared to those without IBD, using two different coding systems:
- **(1)** International Classification of Disease (ICD) Chapters
- **(2)** [Insert description of the second coding system]
The goal of the analysis is to understand the similarities and differences in how each system captures the primary cause of death and to assess potential implications for research and clinical practice in IBD populations. We assess each coding systems ability to capture overall mortality, premature mortality (<75 years), and non-premature mortality (>=75 years).

## Research Questions
- What are the top causes of death among those with IBD compared to matched controls?
- How consistent are the two coding systems in classifying the cause of death for individuals with IBD?
- Do causes of death differ for premature and non-premature mortality among those with and without IBD for both cause of death coding systems? 
- How might differences in classification impact our future study of mortality in the IBD population?

## Data Sources
The data used in this analysis comes from:
- **Source:*** Administrative health data of Ontarians (Canada) housed by ICES 
_ **Sample:** Individuals with a diagnosis of IBD (Crohn's Disease or Ulcerative Colitis) and their matched non-IBD counterparts (matched on year of birth, year of death, and sex)
- **Variables:** Includes demographic details, age of death (premature vs. non-premature), and cause of death classified by both coding systems.
- **General Methodology:** Cause of death codes are mapped across the two systems for each individual. Visual summaries of concordance was done with heatmaps

## Reproducing the Analysis
The descriptive code for the overall cohort as well as the code to compare cause of death are included in this repository. Data is confidential, with our cohort derived from ICES. The Dataset Creation Plan is available upon reasonable request. 
