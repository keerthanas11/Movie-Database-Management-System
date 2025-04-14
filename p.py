from flask import Flask, request, render_template,render_template_string
import mysql.connector

app = Flask(__name__)

# Database configuration
db_config = {
    'user': 'root',
    'password': 'your password',
    'host': 'localhost',
    'database': 'moviee'
}

# Function to establish database connection
def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

@app.route('/')
def index():
    return render_template('s.html')

@app.route('/search_by_c')
def search_by_actor():
    return render_template('p.html')

# Route to render search form and process the search
@app.route('/search_by_criteria', methods=['POST','GET'])
def search_by_criteria():
    if request.method == 'POST':
        min_age = request.form['min_age']
        max_age = request.form['max_age']
        release_year = request.form['release_year']
        
        # Example SQL query, replace with your actual query logic
        query = """
        SELECT m.moviename, m.lang
        FROM movies m
        JOIN actors a ON m.moviename = a.moviesname
        WHERE a.dob BETWEEN %s AND %s
        AND m.year > %s
        """
        
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(query, (min_age, max_age, release_year))
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        
        return render_template('t.html', results=results)
    
    # If method is GET, render the search form
    return render_template('p.html')

@app.route('/search4', methods=['POST'])
def search4():
    director_name = request.form['director_name']

    query = """
        SELECT 
    d.directorname,
    COUNT(DISTINCT m.lang) AS distinct_languages_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY d.directorname), 2) AS percentage_of_movies,
    m.lang
    FROM 
    directors d
    JOIN 
    movies m ON d.moviename = m.moviename
    GROUP BY 
    d.directorname, m.lang
    ORDER BY 
    d.directorname, distinct_languages_count DESC;"""


               




# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
