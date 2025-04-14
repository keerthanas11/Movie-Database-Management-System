from flask import Flask, request, render_template, render_template_string
import mysql.connector

app = Flask(__name__)

db_config = {
    'user': 'root',
    'password': 'your password',
    'host': 'localhost',
    'database': 'moviee'
}

def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search_by_actor')
def search_by_actor():
    return render_template('actors.html')

@app.route('/search_by_movie')
def search_by_movie():
    return render_template('movies.html')



@app.route('/search_by_age_language')
def search_by_age_language():
    return render_template('search4.html')
# Route to render search5.html for complex search
@app.route('/search_by_count')
def search_by_count():
    return render_template('search5.html')


@app.route('/search', methods=['POST'])
def search():
    actor_name = request.form['actor_name']
    
    query = """
    SELECT m.moviename, m.lang
    FROM movies m
    JOIN actors a ON m.moviename = a.moviesname
    WHERE a.name = %s
    """
    
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(query, (actor_name,))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    
    """  if results:
        output = '<h2>Movies featuring actor: {}</h2><ul>'.format(actor_name)
        for row in results:
            output += '<li>Movie: {}, Language: {}</li>'.format(row[0], row[1])
        output += '</ul>'
    else:
        output = '<h2>No movies found featuring actor: {}</h2>'.format(actor_name)"""
    
    return render_template('actor.html', actor_name=actor_name, results=results)

@app.route('/search2', methods=['POST'])
def search2():
    movie_name = request.form['movie_name']
    
    query = """
    SELECT 
        m.moviename, 
        m.lang, 
        m.genre, 
        m.length,
        d.directorname,
        a.name AS actor_name,
        p.companyname
    FROM movies m
    LEFT JOIN directors d ON m.moviename = d.moviename
    LEFT JOIN actors a ON m.moviename = a.moviesname
    LEFT JOIN prodcompany p ON m.moviename = p.movie_name
    WHERE m.moviename = %s
    """
    
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(query, (movie_name,))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    
    """if results:
        movie_info = results[0]  # Assuming only one movie is returned
        output = '''
            <h2>Details for movie: {}</h2>
            <ul>
                <li>Language: {}</li>
                <li>Genre: {}</li>
                <li>Movie Length: {}</li>
                <li>Director: {}</li>
                <li>Actors: {}</li>
                <li>Production Company: {}</li>
            </ul>
        '''.format(movie_info[0], movie_info[1], movie_info[2], movie_info[3], movie_info[4], movie_info[5], movie_info[6])
    else:
        output = '<h2>No details found for movie: {}</h2>'.format(movie_name)
    
    return render_template_string(output)"""
    return render_template('movide.html', movie_name=movie_name, results=results)

@app.route('/search_by_c')
def search_by_c():
    return render_template('age.html')

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
    return render_template('age.html')

@app.route('/search5', methods=['POST'])
def search5():
    movie_count = request.form['movie_count']

    query = """
    SELECT DISTINCT m.moviename, m.year, m.lang
    FROM movies m
    LEFT JOIN actors a ON m.moviename = a.moviesname
    LEFT JOIN directors d ON m.moviename = d.moviename
    LEFT JOIN prodcompany p ON m.moviename = p.movie_name
    WHERE 
        (SELECT COUNT(*) FROM actors WHERE actors.name = a.name) >= %s
        OR (SELECT COUNT(*) FROM directors WHERE directors.directorname = d.directorname) >= %s
        OR (SELECT COUNT(*) FROM prodcompany WHERE prodcompany.companyname = p.companyname) >= %s;
    """

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(query, (movie_count, movie_count, movie_count))
    results = cursor.fetchall()
    """if results:
        output = '<h2>Movies where actor, director, or production company have been involved in at least {} movies</h2><ul>'.format(movie_count)
        for row in results:
            movie_name = row[0]
            year_of_release = row[1]
            language = row[2]
            output += '<li>Movie: {}, Year of Release: {}, Language: {}</li>'.format(movie_name, year_of_release, language)
        output += '</ul>'
    else:
        output = '<h2>No movies found where actor, director, or production company have been involved in at least {} movies</h2>'.format(movie_count)
"""
    cursor.close()
    connection.close()

    return render_template('search_results.html', results=results, movie_count=movie_count)


@app.route('/search4', methods=['POST'])
def search4():
    min_age = request.form['age']
    language = request.form['language']
    birth_month = request.form['birth_month']

    query = """
    SELECT m.moviename, m.year, m.lang,
           a.name AS actor_name, a.dob AS actor_age, a.age
    FROM movies m
    JOIN actors a ON m.moviename = a.moviesname
    WHERE m.lang = %s
    AND (a.gender = 'male' OR a.gender = 'female')
    AND a.dob >= %s
    AND MONTHNAME(a.age) = %s
    """

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(query, (language, min_age, birth_month))
    results = cursor.fetchall()
    """if results:
        output = '<h2>Movies in {} where actors are {} years old or older and born in month {}</h2><ul>'.format(language, min_age, birth_month)
        for row in results:
            movie_name = row[0]
            year_of_release = row[1]
            actor_name = row[3]
            actor_age = row[4]
            actor_dob = row[5]
            output += '<li>Movie: {}, Year of Release: {}, Language: {}</li>'.format(movie_name, year_of_release, language)
            output += '<ul>'
            output += '<li>Actor: {}, Age: {}, Date of Birth: {}</li>'.format(actor_name, actor_age, actor_dob)
            output += '</ul>'
        output += '</ul>'
    else:
        output = '<h2>No movies found in {} where actors are {} years old or older and born in month {}</h2>'.format(language, min_age, birth_month)
"""
    cursor.close()
    connection.close()

    return render_template('search_results_actors.html', results=results, language=language, min_age=min_age, birth_month=birth_month)







if __name__ == '__main__':
    app.run(debug=True)
