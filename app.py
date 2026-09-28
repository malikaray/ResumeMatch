from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

from matcher import extract_text_from_pdf, analyze_resume


app = Flask(__name__)

DATABASE = "database.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def create_database():
    connection = get_db_connection()

    # Job Tracker table
    connection.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            position TEXT NOT NULL,
            score REAL,
            status TEXT DEFAULT 'Saved',
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Match History table
    connection.execute("""
        CREATE TABLE IF NOT EXISTS match_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            position TEXT,
            score REAL,
            matched_skills TEXT,
            missing_skills TEXT,
            date_analyzed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


create_database()


# -------------------------
# Resume Analyzer
# -------------------------

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        resume_file = request.files.get("resume")
        job_description = request.form.get("job_description", "")
        company = request.form.get("company", "")
        position = request.form.get("position", "")

        if not resume_file or resume_file.filename == "":
            return render_template(
                "index.html",
                error="Please upload a PDF resume."
            )

        if not resume_file.filename.lower().endswith(".pdf"):
            return render_template(
                "index.html",
                error="Please upload a PDF file."
            )

        if not job_description.strip():
            return render_template(
                "index.html",
                error="Please enter a job description."
            )

        try:
            resume_text = extract_text_from_pdf(resume_file)

            if not resume_text.strip():
                return render_template(
                    "index.html",
                    error="No readable text was found in this PDF."
                )

            result = analyze_resume(
                resume_text,
                job_description
            )

            # Automatically save analysis to Match History
            connection = get_db_connection()

            connection.execute(
                """
                INSERT INTO match_history
                (company, position, score, matched_skills, missing_skills)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    company.strip() or "Not specified",
                    position.strip() or "Not specified",
                    result["score"],
                    ", ".join(result["matched"]),
                    ", ".join(result["missing"])
                )
            )

            connection.commit()
            connection.close()

            return render_template(
                "results.html",
                result=result,
                company=company,
                position=position
            )

        except Exception as e:
            print("Error processing resume:", e)

            return render_template(
                "index.html",
                error="The resume could not be processed. Please try another PDF."
            )

    return render_template("index.html")


# -------------------------
# Save Job to Tracker
# -------------------------

@app.route("/save", methods=["POST"])
def save_application():

    company = request.form.get("company", "").strip()
    position = request.form.get("position", "").strip()
    score = request.form.get("score", 0)

    if not company:
        company = "Not specified"

    if not position:
        position = "Not specified"

    try:
        score = float(score)
    except (TypeError, ValueError):
        score = 0

    connection = get_db_connection()

    connection.execute(
        """
        INSERT INTO applications
        (company, position, score, status)
        VALUES (?, ?, ?, ?)
        """,
        (company, position, score, "Saved")
    )

    connection.commit()
    connection.close()

    return redirect(url_for("tracker"))


# -------------------------
# Match History
# -------------------------

@app.route("/history")
def history():

    connection = get_db_connection()

    matches = connection.execute(
        "SELECT * FROM match_history ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return render_template(
        "history.html",
        matches=matches
    )


# Delete a Match History entry
@app.route("/history/delete/<int:match_id>", methods=["POST"])
def delete_history(match_id):

    connection = get_db_connection()

    connection.execute(
        "DELETE FROM match_history WHERE id = ?",
        (match_id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("history"))


# -------------------------
# Job Tracker
# -------------------------

@app.route("/tracker")
def tracker():

    connection = get_db_connection()

    applications = connection.execute(
        "SELECT * FROM applications ORDER BY id DESC"
    ).fetchall()

    connection.close()

    total = len(applications)

    interviews = sum(
        1 for application in applications
        if application["status"] == "Interview"
    )

    offers = sum(
        1 for application in applications
        if application["status"] == "Offer"
    )

    if total > 0:
        average_score = round(
            sum(application["score"] for application in applications)
            / total,
            1
        )
    else:
        average_score = 0

    return render_template(
        "tracker.html",
        applications=applications,
        total=total,
        interviews=interviews,
        offers=offers,
        average_score=average_score
    )


# -------------------------
# Update Job Status
# -------------------------

@app.route("/status/<int:application_id>", methods=["POST"])
def update_status(application_id):

    status = request.form.get("status")

    allowed_statuses = [
        "Saved",
        "Applied",
        "Interview",
        "Offer",
        "Rejected"
    ]

    if status in allowed_statuses:

        connection = get_db_connection()

        connection.execute(
            "UPDATE applications SET status = ? WHERE id = ?",
            (status, application_id)
        )

        connection.commit()
        connection.close()

    return redirect(url_for("tracker"))


# -------------------------
# Delete Job
# -------------------------

@app.route("/delete/<int:application_id>", methods=["POST"])
def delete_application(application_id):

    connection = get_db_connection()

    connection.execute(
        "DELETE FROM applications WHERE id = ?",
        (application_id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("tracker"))


# -------------------------
# API - Get All Jobs
# -------------------------

@app.route("/api/jobs", methods=["GET"])
def get_jobs():

    connection = get_db_connection()

    applications = connection.execute(
        "SELECT * FROM applications ORDER BY id DESC"
    ).fetchall()

    connection.close()

    jobs = []

    for application in applications:
        jobs.append({
            "id": application["id"],
            "company": application["company"],
            "position": application["position"],
            "score": application["score"],
            "status": application["status"],
            "date_added": application["date_added"]
        })

    return jsonify(jobs)


# -------------------------
# API - Get One Job
# -------------------------

@app.route("/api/jobs/<int:job_id>", methods=["GET"])
def get_job(job_id):

    connection = get_db_connection()

    job = connection.execute(
        "SELECT * FROM applications WHERE id = ?",
        (job_id,)
    ).fetchone()

    connection.close()

    if job is None:
        return jsonify({"error": "Job not found"}), 404

    return jsonify({
        "id": job["id"],
        "company": job["company"],
        "position": job["position"],
        "score": job["score"],
        "status": job["status"],
        "date_added": job["date_added"]
    })


# -------------------------
# Run Website
# -------------------------

if __name__ == "__main__":
    app.run(debug=True)