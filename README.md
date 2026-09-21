# ResumeMatch

ResumeMatch is a web application I built to practice Python and web development. It allows users to upload a resume, paste a job description, and see how well their technical skills match the job.

I also added a job application tracker so users can save jobs and keep track of their application status.

## Features

- Upload a resume as a PDF
- Extract text from the resume
- Compare resume skills with a job description
- Recognize different names for the same technical skill
- Calculate a match percentage
- Show matched and missing skills
- Give a recommendation based on the match
- Save jobs to a job application tracker
- Update application status
- Delete saved jobs
- View total jobs, interviews, offers, and average match score
- Access saved jobs through API endpoints

## Technologies Used

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- PyPDF2
- Git and GitHub

## How the Matching Works

ResumeMatch looks for technical skills in the job description and checks whether those skills are also found in the uploaded resume.

The matcher can recognize different names for some skills. For example, AWS and Amazon Web Services are treated as the same skill.

The score is calculated using:

`Match Score = (Matched Skills / Required Skills) × 100`

## API Endpoints

Get all saved jobs:

`GET /api/jobs`

Get one saved job by ID:

`GET /api/jobs/<id>`

## Running the Project

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
py app.py
```

Then open:

`http://127.0.0.1:5000`

## Why I Made This

I wanted to build something related to the job search process while improving my Python and web development skills. I started with a simple resume matcher and gradually added PDF processing, Flask, SQLite, a job tracker, API endpoints, and improved skill detection.

I'm continuing to improve the project as I learn more.