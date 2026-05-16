import os
import json # gemini returns json, this converts to python dictionary so we can work with it
from pathlib import Path # for working with file paths, finds resume.md no matter what folder we're running this file from
from google import genai # Google's official Python SDK for Gemini
from dotenv import load_dotenv # makes the API key accessible anywhere in the project

load_dotenv() # actually runs the loading- imports alone don't trigger it

def load_resume() -> str:
    """Load resume.md and return its contents as a string.""" 
    resume_path = Path(__file__).parent / "data" / "resume.md" # build the path to resume.md relative to this file's location- works regardless of where we run from
    return resume_path.read_text(encoding="utf-8") # open the file and return all its text as a single string

# Define a function that takes a job description and returns a dictionary of analysis results
# Docstring serves three purposes:
# 1. Tells the ADK agent what this tool does and when to call it
# 2. Documents what input the function expects (job_description)
# 3. Describes the output format (dictionary with specific keys)
def analyze_job_fit(job_description: str) -> dict:
    """
    Analyze how well Gila's background fits a given job description.

    Use this tool when the user provides a job description and wants to understand fit, alignment, skill gaps, or how to position Gila's experience for the role.

    Args:
        job_description: The full text of the job description to analyze.

    Returns:
        A dictionary containing fit_score, aligned_skills, gap_skills, and suggested_framing.
    """
    resume = load_resume() # Load resume text from disk

    # Build the prompt- inject the resume and job description so Gemini has everything it needs
    prompt = f"""
You are an expert career advisor analyzing a candidate's fit for a job

CANDIDATE BACKGROUND:
{resume}

JOB DESCRIPTION:
{job_description}

Analyze the fit and respond with ONLY a JSON object in this exact format
(no extra text, no markdown, just the JSON):

{{
    "fit_score": <integer 0-100>,
    "aligned_skills": [<list of strings: skills/experiences that match>],
    "gap_skills": [<list of strings: skills the JD want that are missing or weak>],
    "suggested_framing": "<2-3 sentences on how Gila should position herself for this role>"
}}
"""

    # Send the prompt to Gemini and store the response
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    raw = response.text.strip()
    if not raw:
        return {"error": "Gemini returned an empty response"}
    # Remove markdown code fences if Gemini wrapped the JSON in them
    raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    result = json.loads(raw)  # Convert the cleaned JSON string into Python dictionary

    # Return the dictionary to whichever called this tool
    return result
