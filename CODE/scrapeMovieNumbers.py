import numpy as np
import pandas as pd
import argparse
import json
import subprocess
import time
from functools import reduce
import os
import matplotlib.pyplot as plt


#############################################################
#DATABASE TABLE COLUMN HEADERS
#############################################################
DB_COLUMNS = ['title', 'year', 'mpaa', 'runtime', 'genres', 'star_rating','metascore_rating','description','director','stars','gross']
#'release_date']

def main(args):
    # If the generate option is specified, then re-generate the imdb_movies.json data store from the original web page.
    if args.generate:
        print("Generating the_numbers_movies.json...")
        try:
            os.remove('./the_numbers_movies.json')
        except:
            pass

        processResult = subprocess.call(['scrapy runspider NumbersSpider.py -o the_numbers_movies.json'], shell=True, universal_newlines=True)
        if processResult != 0:
            print("Failed to create the_numbers_movies.json file with scrappy!")
            return 1
        else:
            print("Done!")
    else:
        print('Using previously generated the_numbers_movies.json...')

    # Read in the json data store, parse each json object into a pandas dataframe row, and
    # store the entire pandas dataframe as a csv file.
    print("Generating thenumbers.csv...")
    jsonString = []
    with open('the_numbers_movies.json', 'r') as f:
        jsonString = f.readlines()
    moviesList = json.loads(reduce(lambda sum, item: sum + item, jsonString))
    moviesTable = []
    index = 0
    for movie in moviesList:
        row = []
        if index % 1000 == 0:
            print(index)
        row.append(movie['title'].strip())
        #row.append(movie['year'].replace("(","").replace(")","").strip())
        row.append(movie['release_date'].split(",")[1].replace("(","").replace(")","").strip())
        try:
            row.append(movie['mpaa'])
        except:
            row.append("")
        try:
            row.append(movie['runtime'].strip())
        except:
            row.append("")
        row.append(",".join(movie['genres']))
        try:
            row.append(movie['star_rating'].strip())
        except:
            row.append("")
        row.append("") #metascore rating
        row.append("") #empty description
        row.append(movie['director'].strip())
        row.append(",".join(movie['stars']))
        if '$' not in movie['gross']:
            row.append("")
        else:
            row.append(movie['gross'])
        #row.append(movie['release_date'])
        moviesTable.append(row)
        index += 1

    # Save the database to a csv database file.
    moviesDF = pd.DataFrame(moviesTable, index=np.arange(len(moviesList)), columns=DB_COLUMNS)
    moviesDF.to_csv('thenumbers.csv', index=False)

    # Plot the histogram of year values to see outliers that need to be parsed.
    d = pd.DataFrame(moviesDF['year'])
    d.apply(pd.value_counts).plot(kind='bar', subplots=True)
    plt.show()
    print("Done!")
    print("Finished!")




if __name__ == "__main__":
    #Parse command line arguments
    parser = argparse.ArgumentParser(description="""movie numbers csv database generator. This script trains and tests multiple classifiers
    on the pandas data frame passed to this.""")
    parser.add_argument('--generate', action="store_true",
                        help="Optional argument that causes the website scraper to be run to generate the the_numbers_movies.json file.")
    args = parser.parse_args()
    main(args)













