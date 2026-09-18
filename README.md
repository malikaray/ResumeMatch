# ResumeMatch

ResumeMatch is a project I built to practice Python and web development. The idea is simple: upload a resume, paste a job description, and the program checks how well the skills in the resume match the skills needed for the job.

I also added a job tracker so the user can save jobs and keep track of their application status.

## What it does

- Upload a resume as a PDF
- Read text from the resume
- Compare resume skills with a job description
- Calculate a match percentage
- Show matched skills
- Show missing skills
- Give a recommendation based on the match
- Save jobs to a job tracker
- Change a job status to Saved, Applied, Interview, Offer, or Rejected
- Delete jobs from the tracker
- Show total jobs, interviews, offers, and average match score

## Technologies I used

- Python
- Flask
- SQLite
- HTML
- CSS
- PyPDF2
- Git and GitHub

## How the matching works

The program first looks for skills mentioned in the job description. It then checks if those same skills can be found in the resume.

The score is calculated like this:

Match Score = (matched skills / required skills) * 100

For example, if 8 out of 10 detected skills are found in the resume, the match score is 80%.

## Running the project

First install the required packages:

    pip install -r requirements.txt

Then run:

    py app.py

Open the local address shown in the terminal. By default it should be:

    http://127.0.0.1:5000

## Why I made this

I wanted to build something related to the job search process while improving my Python skills. I started with a simple Python program that compared a list of skills. After getting that working, I turned it into a Flask web application, added PDF resume reading, and then added a job application tracker using SQLite.

I'm still improving the project as I learn more.

## What I want to add next

- JavaScript for more interactive features
- API endpoints
- Better skill detection
- Search and filters for saved jobs
- A standalone app version