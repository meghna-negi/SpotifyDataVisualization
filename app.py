from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

app.config['MYSQL_HOST'] = '' #Enter the host name
app.config['MYSQL_USER'] = '' #Enter the user name 
app.config['MYSQL_PASSWORD'] = '' #Enter the password
app.config['MYSQL_DB'] = '' #Enter the database name
 
 
mysql = MySQL(app)

@app.route('/')
def Homepage():
    return render_template('index.html')

@app.route('/top_artist', methods=['GET'])
def top_song_artist():
    country_name = request.args.get('country')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Fetching the top artist and song for the given country
    cursor.execute("""
        SELECT Artists, Title 
        FROM spotifyChartByCountry 
        WHERE Country = %s 
        ORDER BY SongRank ASC 
        LIMIT 1;
    """, (country_name,))
    
    result = cursor.fetchone()
    cursor.close()

    if result:
        return jsonify({"Artists": result['Artists'], "Title": result['Title']})
    else:
        return jsonify({"error": "No data found"}), 404


if __name__ == "__main__":
    app.run(debug=True)