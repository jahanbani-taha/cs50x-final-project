# Final Project – Taha Jahanbani's Multilingual Portfolio Website

#### Video Demo:
https://youtu.be/nvKI5GcGPOY

## Project Description:
This is my final project for CS50x Iran, developed in Summer 1404(2025). It’s a personal multilingual portfolio website built using Flask. The site includes a downloadable
resume, project showcase, contact form, a simple chatbot, and a dark/light theme toggle.

It supports three languages: Persian, English, and Turkish. The layout is fully responsive and optimized for both desktop and mobile devices. My goal was to create a
professional platform that reflects my skills in programming, UI design, and personal branding.

## Design Decisions:
- I chose Flask for its simplicity and scalability.
- The dark/light theme is toggled using CSS classes and URL parameters.
- The chatbot is a lightweight feature designed to guide visitors through the site.
- I selected the Vazirmatn font for improved readability in Persian.

## Goals, Outcomes, and Use of AI Tools
My goal was to build a personal multilingual website that showcases my skills in programming, UI design, and branding. This project helped me deepen my understanding
of Flask and responsive design, while creating a resume platform that can live beyond the course.

During development, I collaborated with Microsoft Copilot (AI assistant) for planning, structuring, and refining the project documentation and technical decisions.
All core logic and implementation were done independently.

## File Overview:
app.py Main Flask application with routing and core logic
init_db.py Script to initialize the SQLite database (messages.db)
instance/messages.db SQLite database used to store contact form submissions
static/css/style.css Custom styles for layout, typography, and theme switching
static/images/ Image assets used across the site (e.g. profile, portfolio)
templates/index.html Homepage template
templates/contact.html Contact form page
templates/portfolio.html Project showcase page
templates/resume.html Resume viewer page
templates/resume_printable.html Printable version of resume
templates/layout.html Shared layout structure for all pages
templates/Taha_Jahanbani_Resume.pdf Embedded resume file for viewing and download
venv/ Python virtual environment (excluded from deployment)
requirements.txt Python dependencies required to run the project
README.md Project documentation (this file)

## Contact me:
You can reach me via the contact form on the website or by email: jahanbani.taha.923@gmail.com

## Screenshots:
![screenshots](screenshots/)

## How to Run:
```bash
pip install -r requirements.txt
flask run
