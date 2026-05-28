import os

from flask import Flask, jsonify, render_template, request
import mysql.connector


app = Flask(__name__)

# map for statecodes because the tables only have the numeric version
state_map = {
    'AL':'01','AK':'02','AZ':'04','AR':'05','CA':'06','CO':'08','CT':'09',
    'DE':'10','DC':'11','FL':'12','GA':'13','HI':'15','ID':'16','IL':'17',
    'IN':'18','IA':'19','KS':'20','KY':'21','LA':'22','ME':'23','MD':'24',
    'MA':'25','MI':'26','MN':'27','MS':'28','MO':'29','MT':'30','NE':'31',
    'NV':'32','NH':'33','NJ':'34','NM':'35','NY':'36','NC':'37','ND':'38',
    'OH':'39','OK':'40','OR':'41','PA':'42','RI':'44','SC':'45','SD':'46',
    'TN':'47','TX':'48','UT':'49','VT':'50','VA':'51','WA':'53','WV':'54',
    'WI':'55','WY':'56'
}

# the advanced qs from prev task
adv_qs = {
    "q1": """
        SELECT s.state_name, COUNT(m.monitor_id) AS num_monitors
        FROM state s
        JOIN location l ON s.state_code = l.state_code
        JOIN monitor m ON l.location_id = m.location_id
        WHERE l.lat > 35 AND l.lng > -92
        GROUP BY s.state_name
        ORDER BY num_monitors DESC
        LIMIT 15
    """,
    "q2": """
        SELECT c.county_name, COUNT(d.death_id) AS death_count
        FROM county c
        JOIN death d USING (county_code)
        WHERE d.gender = 'Male' AND d.race = 'Asian or Pacific Islander'
        GROUP BY c.county_name
        ORDER BY death_count DESC
        LIMIT 15
    """,
    "q3": """
        SELECT l.location_id, l.city_name, l.state_code, COUNT(m.monitor_id) AS num_monitors
        FROM location l
        JOIN monitor m ON l.location_id = m.location_id
        WHERE m.monitor_type = 'SPM' AND m.first_year_of_data > 2000
        GROUP BY l.location_id, l.city_name, l.state_code
        HAVING COUNT(m.monitor_id) > (
            SELECT AVG(cnt) FROM (
                SELECT COUNT(monitor_id) AS cnt
                FROM monitor
                WHERE monitor_type = 'SPM' AND first_year_of_data > 2000
                GROUP BY location_id
            ) AS avg_table
        )
        ORDER BY num_monitors DESC
        LIMIT 15
    """,
    "users": """
        SELECT user_id, first_name, last_name, age_group, race, hispanic_ethnicity, sex
        FROM user
        ORDER BY user_id DESC
        LIMIT 15
    """,
}

# descriptions of the preset qs
adv_qs_desc = {
    "q1": "Shows the 15 states with the highest number of monitors in locations above latitude 35 and longitude -92.",
    "q2": "Shows the 15 counties with the highest count of deaths for Asian or Pacific Islander males.",
    "q3": "Shows locations that have an above-average number of SPM monitors after the year 2000.",
    "users": "Shows the 15 most recently created user accounts so you can verify inserts.",
}

# helper functions

# connect to mysql db
def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "appuser"),
        password=os.getenv("DB_PASSWORD", "prgumoja"),
        database=os.getenv("DB_NAME", "polutracker"),
        use_pure=True
    )

# help run the adv qs
def run_query(query_key):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(adv_qs[query_key])
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return rows


# route to the pretty cool looking website
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# runs the adv qs when button clicky
@app.route("/api/queries/<query_key>", methods=["GET"])
def api_query(query_key):
    if query_key not in adv_qs:
        return jsonify({"error": "Unknown query"}), 404
    return jsonify(
        {
            "query": query_key.upper(),
            "description": adv_qs_desc[query_key],
            "rows": run_query(query_key),
        }
    )

# creation of account
@app.route("/api/users", methods=["POST"])
def add_user():
    payload = request.get_json(silent=True) or request.form

    first_name = payload.get("first_name")
    last_name = payload.get("last_name")
    age_group = payload.get("age_group")
    race = payload.get("race")
    hispanic_ethnicity = payload.get("hispanic_ethnicity")
    sex = payload.get("sex")
    
    # insert user info into db
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        """
        INSERT INTO user (
            first_name,
            last_name,
            age_group,
            race,
            hispanic_ethnicity,
            sex
        ) VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            first_name,
            last_name,
            age_group,
            race,
            hispanic_ethnicity,
            sex,
        ),
    )
    db.commit()
    user_id = cursor.lastrowid
    cursor.close()
    db.close()

    # let front end know the job's done
    return jsonify(
        {
            "message": "User added successfully",
            "user": {
                "user_id": user_id,
                "first_name": first_name,
                "last_name": last_name,
                "age_group": age_group,
                "race": race,
                "hispanic_ethnicity": hispanic_ethnicity,
                "sex": sex,
            },
        }
    )


# CRUD - update/deleate 
# edit user info just incase information was entered incorrectly
@app.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    payload = request.get_json(silent=True) or request.form

    first_name = payload.get("first_name")
    last_name = payload.get("last_name")
    age_group = payload.get("age_group")
    race = payload.get("race")
    hispanic_ethnicity = payload.get("hispanic_ethnicity")
    sex = payload.get("sex")

    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        """
        UPDATE user SET
            first_name = %s,
            last_name = %s,
            age_group = %s,
            race = %s,
            hispanic_ethnicity = %s,
            sex = %s
        WHERE user_id = %s
        """,
        (first_name, last_name, age_group, race, hispanic_ethnicity, sex, user_id),
    )
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"message": "User updated", "user_id": user_id})


# delete user
@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        """

        delete from user where user_id = %s

        """
        ,(user_id,)
    )
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"message": "User deleted", "user_id": user_id})

# keyword search 
# allows the user to search their county or state to get the corresponding state code
@app.route("/api/search", methods=["GET"])
def search():
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify({"error": "No search term provided"}), 400
    
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(
            """

            select distinct 
                state_code,
                state_name,
                county_name,
                city_name
            from location join state using(state_code)
                join county using (state_code)
            where 
                county_name like %s
                or city_name like %s
                or state_name like %s
            order by county_name, city_name
            limit 20

            """,
            (f"%{q}%", f"%{q}%", f"%{q}%"),
        )
        rows = cursor.fetchall()
        return jsonify({
            "query": q, 
            "results": rows,
            "count": len(rows)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

# stored procedure
# allows the user to learn about the air quality monitoring in their state
# shows the total number of monitors, total locations the monitors are found
# the most monitored pollutant
# also shows death stats: total num of deaths, most common gender and race that dies
@app.route("/api/procedure/state-summary", methods=["GET"])
def state_summary():
    state_code = request.args.get("state_code", "").strip().upper()
    
    if state_code in state_map:
        state_code = state_map[state_code]
    elif state_code not in state_map.values():
        return jsonify({"error": "Invalid state code"}), 400
    
    db = None
    cursor = None

    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.callproc("GetStatePollutionSummary", [state_code])
        
        # to loop through the different result sets returned by the union all
        results = []
        for result_set in cursor.stored_results(): 
            results.extend(result_set.fetchall()) # get the data and put it in the results list
        
        # return the data and a confirmation that the data was recieved
        return jsonify({
            "state_code": state_code,
            "success": True,
            "data": results
        })
    
    except Exception as e:
        print(f"Error calling procedure: {str(e)}")
        return jsonify({"error": f"Procedure call failed: {str(e)}"}), 500
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


# trigger log - table to show new users
@app.route("/api/audit", methods=["GET"])
def get_audit():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        """
        select * from user_audit
        order by audit_id desc
        limit 15

        """
    )
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify({"rows": rows})


# transaction
# returns the number of monitors in given state and proportion of deaths by race
# used to make super cool pie chart ;)
@app.route("/api/transaction/state-report", methods=["GET"])
def state_report():
    state_code = request.args.get("state_code", "").strip().upper()
    if not state_code:
        return jsonify({"error": "state_code required"}), 400
    
    if state_code in state_map:
        numeric_state_code = state_map[state_code]
    elif state_code in state_map.values():
        numeric_state_code = state_code
    else:
        return jsonify({"error": "Invalid state code"}), 400
    
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        db.start_transaction(isolation_level="REPEATABLE READ")
        # num of monitors
        cursor.execute(
            """
            SELECT 
                s.state_name, 
                COUNT(DISTINCT m.monitor_id) AS total_monitors
            FROM 
                state s
            JOIN location l ON s.state_code = l.state_code
            JOIN monitor m ON l.location_id = m.location_id
            WHERE s.state_code = %s
            GROUP BY s.state_name
            """,
            (numeric_state_code,),
        )
        monitor_data = cursor.fetchall()

        # deaths per race
        cursor.execute(
            """
            SELECT race, COUNT(*) AS death_count
            FROM death
            JOIN county c USING (county_code)
            WHERE c.state_code = %s
            GROUP BY race
            ORDER BY death_count DESC

            """,
            (numeric_state_code,),
        )
        death_data = cursor.fetchall()
 
        db.commit()
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()
 
    return jsonify({
        "state_code": numeric_state_code,
        "monitor_summary": monitor_data,
        "death_summary": death_data,
    })

# bar plots
# shows death counts by race
@app.route("/api/deaths/by-race", methods=["GET"])
def deaths_by_race():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT 
            race, 
            COUNT(*) AS death_count
        FROM death
        GROUP BY race
        ORDER BY death_count DESC
        """
    )
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify({"rows": rows})

# most monitored pollutants
@app.route("/api/pollutants/by-count", methods=["GET"])
def pollutants_by_count():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT 
                pt.pollutant_name,
                COUNT(m.monitor_id) AS monitor_count
            FROM 
            pollutant_type pt JOIN pollutant p USING(pollutant_type_id)
            JOIN monitor m ON p.pollutant_id = m.pollutant_id
            GROUP BY pt.pollutant_name
            ORDER BY monitor_count DESC
            LIMIT 15

            """
        )
        rows = cursor.fetchall()
        return jsonify({"rows": rows})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()


# make rating features
# allows the user to rate their specifc county's air polution level with stars on a scale of 1-5
# will also make interactive heat map to allow other users to see the ratings acorss the country

# use the state code to get the specific county that use wants to rate
@app.route("/api/counties/by-state", methods=["GET"])
def counties_by_state():
   
   state_input = request.args.get("state_code", "").strip().upper()
   if not state_input:
       return jsonify({"error": "state_code required"}), 400
   state_code = state_map.get(state_input, state_input)


   db = get_db()
   cursor = db.cursor(dictionary=True)


   cursor.execute(
       """
                 
       SELECT county_code, county_name
       FROM county
       WHERE state_code = %s
       ORDER BY county_name
                 
        """
   , (state_code,))


   rows = cursor.fetchall()
   cursor.close()
   db.close()
   return jsonify({"rows": rows})


@app.route("/api/ratings", methods=["POST"])
def submit_rating():
    # get user info and rating
    payload = request.get_json(silent=True) or request.form
    user_id = payload.get("user_id")
    state_input = payload.get("state_code", "").strip().upper()
    county_code = payload.get("county_code", "").strip()
    rating = payload.get("rating")

    # make sure all the info in submitted
    if not all([user_id, state_input, county_code, rating]):
        return jsonify({"error": "All fields required"}), 400
    state_code = state_map.get(state_input, state_input)

    # insert info into db
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            """
                       
            INSERT INTO county_rating (user_id, state_code, county_code, rating)
            VALUES (%s, %s, %s, %s)
                       
            """
        , (user_id, state_code, county_code, int(rating)))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Rating submitted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# for the heat map, get the avg rating from each state
@app.route("/api/ratings/by-state", methods=["GET"])
def ratings_by_state():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT s.state_name, cr.state_code,
               ROUND(AVG(cr.rating), 2) AS avg_rating,
               COUNT(*) AS total_ratings
        FROM county_rating cr
        JOIN state s ON cr.state_code = s.state_code
        GROUP BY cr.state_code, s.state_name
        ORDER BY avg_rating DESC
        """
    )
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify({"rows": rows})




# for table to see the ratings by state 
# get the avg rating for that county
@app.route("/api/ratings/counties", methods=["GET"])
def ratings_by_county():
    state_input = request.args.get("state_code", "").strip().upper()
    if not state_input:
        return jsonify({"error": "state_code required"}), 400
    state_code = state_map.get(state_input, state_input)
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT c.county_name, cr.county_code,
               ROUND(AVG(cr.rating), 2) AS avg_rating,
               COUNT(*) AS total_ratings
        FROM county_rating cr
        JOIN county c ON cr.state_code = c.state_code AND cr.county_code = c.county_code
        WHERE cr.state_code = %s
        GROUP BY cr.county_code, c.county_name
        ORDER BY avg_rating DESC
        """
    , (state_code,))
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify({"rows": rows})



# pull the lever kronk!
if __name__ == "__main__":
    app.run(
        host=os.getenv("FLASK_HOST", "0.0.0.0"),
        port=int(os.getenv("FLASK_PORT", "5000")),
        debug=os.getenv("FLASK_DEBUG", "false").lower() == "true",
    )
