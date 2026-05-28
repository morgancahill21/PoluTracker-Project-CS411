<mark>** Note: Claude was used to help us with our front-end **<mark>


## Please list out changes in the directions of your project if the final project is different from your original proposal (based on your stage 1 proposal submission).


* Originally we planned on having a slider that showed air quality data and pollution trends over the years. This was scrapped in the final project.
* The Air Quality rating and Water Quality rating that we had in the original web design was scrapped and we just kept an overall rating for each county.
* The web design looks different from what we originally planned even though we did include a heatmap, bar charts, and pie charts (these aspects were used in a way that was different than we originally planned).


## Discuss what you think your application achieved or failed to achieve regarding its usefulness.
* We successfully achieved the goal of allowing users to submit personal ratings for their specific county, which addresses one of our goals being community involvement. This interactive dashboard gives users a way to identify high risk areas based on user-reported data. This app is also useful in the sense that users can look up specific counties to see current ratings, which makes this more location relevant. One failure that we had was the lack of walk-assist, which would probably make our application more user friendly.


## Discuss if you changed the schema or source of the data for your application
* We didn’t end up needing to use the Google Earth API in order to build out our application. The other sources mentioned in our proposal were used.
* Our original ER diagram had extra foreign keys that weren’t supposed to be included. Then, we made the user table and location table a many-to-many as that felt truer to the real relationship. Another change we made was adding an audit table to log when a new user account was created, this table is called user_audit. Lastly, another change we made was a county_rating table so we could handle crowdsourced data.


## Discuss what you change to your ER diagram and/or your table implementations. What are some differences between the original design and the final design? Why? What do you think is a more suitable design? 
* From our original design to our final design we had to make a couple of changes. In our original design we had included extra foreign keys which we weren’t supposed to include in an ER diagram. Originally user locations was its own separate table, but in our final design we decided to change it to make it a many to many relationship between user and location as we were suggested to make that change. I believe our final design is more suitable as it didn’t break any of the rules of how an ER diagram should  look like.


## Discuss what functionalities you added or removed. Why?
* The slider was removed as it was quite an ambitious idea originally, we found that it would be very challenging to implement.
* The air quality and water quality was scrapped because we figured it would be simpler for a user to just implement an overall score rather than 2 based on aspects that can be hard to give a rating for.
* We added the ability to add, remove users, and update user info. This was done as it was a part of the rubric, and also could be helpful if information was incorrectly inputted.
* We also added something that tracks the most recent users added and a user audit. We could see users being added and help us see that we were able to add, remove, and update users.


## Explain how you think your advanced database programs complement your application.
* The trigger tracks new users and adds them to the user_audit table. It makes sure that the user imputed a first name and that it is not a null value before inserting it. This helps track all accounts.
* The transaction was used to generate a state report, allowing users to view the total number of monitors and the proportion of deaths categorized by race for a specific state. We chose a repeatable read isolation level to ensure the data remained consistent across multiple related queries. Since additional death and monitor data may be added in the future, this approach ensures that all results are drawn from the same snapshot of the database at a specific point in time.
* The stored procedure was used to generate a pollution summary report, allowing users to view a concise overview of monitoring and mortality data. When a user inputs a state for the monitoring data, the report displays the total number of monitors, the total number of monitoring locations, and the most frequently tracked pollutant. For the mortality data, the report shows the total number of deaths, as well as the gender and race with the highest number of deaths. The implementation uses UNION ALL and nested aggregations to combine and summarize the data efficiently.

## Each team member should describe one technical challenge that the team encountered.  This should be sufficiently detailed such that another future team could use this as helpful advice if they were to start a similar project or where to maintain your project. 
* Maclain: I was tasked with making sure the frontend and backend could both be hosted on the GCP platform, as well as assembling and setting up the GCP Virtual Machine. I have experience developing hosted web applications, but GCP was more or less completely unfamiliar to me. When porting the assembled flask application and html frontend, I ran into trouble when setting up a linux service that would automatically restart and display our application. This was because of version mismatching within the files we had created. We didn’t really adhere to strict git version control, so when I transferred files from my local device to the GCP VM, the files ended up being old versions, as I didn’t do a thorough check. My advice to future developers working on this project would be to make sure your group works within your github repository, even when you’re submitting any work.
* Morgan: A technical challenge I felt like I faced was determining which tables to join and which columns to index on. Initially, working with these complex queries involved massive datasets that felt like my actions had little impact on cost. To fix this, I decided to join on frequently joined columns such as state_code and location_id. If I had a tip for future teams it would be to plan your indexes alongside your ER diagram, not just as an afterthought.
* Colin: One technical challenge was figuring how to update the VM files on Windows. Since I was working on Windows and my teammates were working on Macs, I originally wasn’t able to figure out why I wasn’t able to update the VM files while my teammates were able to. It turned out that my windows version of Gcloud was not able to properly read ‘~/’  and it turned out that I had to specify the full path rather than use that shortcut. Future teams should take this into account and take note that there will be some differences in how things are implemented based on what computer you are using.
* Jada: Before we began working on the Python file to build the website, we had created some initial queries (the advanced queries for stage 3), but we hadn’t fully thought through which queries were necessary to make the site fully functional and aligned with our original goals. Due to that, we frequently switched between our SQL Server and the app.py file, testing queries to ensure they produced useful results. This process was not only time consuming but computationally heavy, causing our queries to run slow (~5 minutes) and crash, which forced us to restart our instance multiple times. My advice to future developers is to plan out the required queries before starting the app.py file, using the proposal as a guide. This approach will make the Python development process much smoother.


## Are there other things that changed comparing the final application with the original proposal?
* No other things were changed that have not been mentioned in previous questions


## Describe future work that you think, other than the interface, that the application can improve on
* For future work, integrating the Google Earth Air Quality API for real time updates and expanding the historical data archive would let users track pollution trends over months or years. Machine learning could identify patterns, like which neighborhoods spike during rush hour, and send targeted alerts before poor conditions hit. Connecting to local health departments' data would help correlate air quality with reported respiratory issues in each area.

## Describe the final division of labor and how well you managed teamwork.
* We worked very well together as a team. Teamwork wasn’t a problem for our group. We worked together often over discord, and communication was done using discord as well as an IMessage groupchat. 
* Maclain: I was tasked with the GCP setup, as well as making sure our frontend and backend could both be hosted on the GCP VM. I also connected our VM to an existing cloudflare tunnel so our app could have a consistent URL (air.mtprom.dev). I helped with SQL queries as well.
* Colin: Worked on implementing the interactive heatmap and on the rating system and the account creation set up.
* Morgan: I gave input on the frontend things to include on the final deliverable and I worked primarily on indexing, the associated costs, and advanced querying.
* Jada: Worked on the transaction, stored procedure, key word search and bar plot for pollutants.

