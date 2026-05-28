# PoluTracker-Project-CS411
Air Pollution Dashboard with a team of 4 for CS 411 (Database Systems) at UIUC

# Air Pollution Tracking Dashboard

## Overview
This project is a full-stack web application and dashboard designed to track, display, and manage air pollution data. By integrating external air quality APIs with a cloud-hosted relational database, the application provides real-time insights and a platform for user-driven pollution tracking. 

## Tech
* **Frontend:** HTML, CSS, JavaScript
* **Backend:** Python, Flask
* **Database:** SQL, Google Cloud Platform (GCP)
* **Version Control:** GitHub (release tags for versioning)

## Features
* **Live Data Integration:** Aggregates air quality data pulled from external Air Pollution APIs alongside internal database records.
* **Full CRUD Functionality:** Users can Create, Read, Update, and Delete pollution data points through the frontend interface.
* **Advanced Database Automation:** Utilizes SQL stored procedures and triggers (adding a new pollution input automatically updates the recent user input tracking table).
* **Versioned Releases:** Project milestones and updates are tracked via GitHub release tags with detailed markdown documentation.

## Database Architecture
A major focus of this project was designing a highly optimized, scalable database on Google Cloud Platform:
1. **Design:** Built conceptual and logical database designs with a fully normalized schema to reduce data redundancy.
2. **Implementation:** Deployed the database instance on GCP.
3. **Optimization:** Executed advanced queries via the GCP terminal and implemented strategic database indexing to optimize query performance and reduce load times.

## Setup & Installation
To run this project locally:

1. Clone the repository:

   git clone https://github.com/morgancahill21/PoluTracker-Project-CS411.git

2. Navigate to the project directory:

     cd [PoluTracker-Project-CS411]

3. Install the required Python dependencies:

   pip install -r requirements.txt

4. Set up your environment variables (API keys, GCP database credentials).

5. Run the Flask application:

   flask run

## My Contributions
* Collaborated on the frontend interface and integrated some Python logic
* Assisted in testing advanced SQL queries and indexing the database for optimized preformance
* Worked on the logical and relational database schema design
