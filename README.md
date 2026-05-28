# PoluTracker-Project-CS411
Air Pollution Dashboard with a team of 4 for CS 411 (Database Systems) at UIUC

# Air Pollution Tracking Dashboard

## Overview
This project is a full-stack web application and interactive dashboard designed to track and display air pollution data. By integrating external air quality data with a cloud-hosted relational database, the application provides real-time insights, interactive data visualizations, and a platform for crowdsourced, user-reported county ratings.

## Tech Stack
* **Frontend:** HTML, CSS, JavaScript (Chart.js for Data Visualizations)
* **Backend:** Python, Flask
* **Database:** SQL, Google Cloud Platform (GCP Compute Engine VM)
* **Networking:** Cloudflare Tunnels (for consistent URL hosting)
* **Version Control:** GitHub (release tags for versioning)

## Key Features
* **Interactive Visualizations:** Includes interactive heatmaps, bar charts, and pie charts to display complex pollution and mortality data intuitively.
* **Crowdsourced County Ratings:** Allows users to submit personal air/water quality ratings for specific counties, identifying high-risk areas based on community-driven data.
* **User Management (CRUD):** Full Create, Read, Update, and Delete functionality for user profiles.
* **Advanced Database Automation:** * **Triggers:** Automatically tracks new account creations and logs them into a secure `user_audit` table to monitor system access.
  * **Transactions:** Utilizes `REPEATABLE READ` isolation levels to generate consistent State Reports displaying total monitors and proportional death rates categorized by race.
  * **Stored Procedures:** Generates comprehensive Pollution Summary Reports, utilizing `UNION ALL` and nested aggregations to combine monitoring station data and mortality statistics efficiently.

## Database Architecture
A major focus of this project was designing an optimized, scalable database on Google Cloud Platform:
1. **Design:** Built conceptual and logical database designs with a fully normalized schema (including resolving a many-to-many relationship between users and locations).
2. **Implementation:** Deployed the database instance on GCP, integrating custom tables for `county_rating` and `user_audit`.
3. **Optimization:** Executed advanced queries via the GCP terminal and implemented strategic database indexing on frequently joined columns (like `state_code` and `location_id`) to significantly reduce query latency and compute costs.

## Setup & Installation
*(Note: The live application relied on a GCP MySQL instance which is no longer active. The code below demonstrates the core logic and architecture.)*
To run this project locally:

1. Clone the repository:

   git clone https://github.com/morgancahill21/PoluTracker-Project-CS411.git

2. Navigate to the project directory:

     cd PoluTracker-Project-CS411

3. Install the required Python dependencies:

   pip install -r requirements.txt

4. Set up your environment variables (API keys, GCP database credentials).

5. Run the Flask application:

   flask run

## My Contributions
* Collaborated on the frontend interface and integrated some Python logic
* Assisted in testing advanced SQL queries and indexing the database for optimized preformance
* Worked on the logical and relational database schema design
