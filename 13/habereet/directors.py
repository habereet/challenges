import csv
from collections import defaultdict
from collections import namedtuple
from collections import Counter

DATAFILE = 'movie_metadata.csv'

Movie = namedtuple('Movie', 'title year score')

def get_movies_by_director(data=DATAFILE):
		"""Extracts all movies from csv and stores them in a dictionary
			 where keys are directors, and values is a list of movies (named tuples)"""
		directors = defaultdict(list)
		with open(data, encoding='utf-8') as f:
				for line in csv.DictReader(f):
						if line['title_year'] != '' and int(line['title_year']) >= 1960:
							try:
								director = line['director_name']
								movie = line['movie_title'].replace('\xa0', '')
								year = int(line['title_year'])
								score = float(line['imdb_score'])
							except ValueError:
								continue

							m = Movie(title=movie, year=year, score=score)
							directors[director].append(m)

		return directors

def get_directors_with_five_movies(my_five_directors):
	five_directors_dict = defaultdict(list)
	for director in my_five_directors:
		if len(my_five_directors[director]) >= 4:
			for movie in my_five_directors[director]:
				five_directors_dict[director].append(movie)
	return(five_directors_dict)

def get_averages(my_average_directors):
	averages = {}
	for director in my_average_directors:
		average = 0
		total = 0
		for movie in my_average_directors[director]:
			total += movie.score
		average = total / len(my_average_directors[director])
		averages[director] = average
	return averages

def print_directors(print_directors, top_averages):
	count = 1
	dashes = "-"*84
	for director in top_averages:
		print("{:>02d}. {:40}{:>40.1f}".format(count, director[0], director[1]))
		print(dashes)
		for movie in print_directors[director[0]]:
			print("{:<04d}] {:75}{:>3.1f}".format(movie.year, movie.title, movie.score))
		print(f'\n')
		count += 1



directors = get_movies_by_director()
five_directors = get_directors_with_five_movies(directors)
average_directors = get_averages(five_directors)
print_directors(five_directors, Counter(average_directors).most_common(20))
