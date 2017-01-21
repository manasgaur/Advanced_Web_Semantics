import pickle
from nltk.corpus import stopwords

stop = stopwords.words('english')

def load_data_in_list():
	with open('../data/dbpedia/dbpedia_names_title_map') as file_reader:
		count = 0
		for line in file_reader:
			print count
			count += 1
			if len(line.strip().split('\t')) == 2:
				title = line.strip().split('\t')[1].strip()
				title_map[line.strip().split('\t')[0].strip()] = title
		pickle.dump(title_map, open('../data/dbpedia/dbpedia_names_title_map.p', 'wb'))

def spot_in_tweet(title_map):
	count = 0
	file_writer = open("../data/dbpedia/annotations", 'a')
	with open('../data/training/training_cleaned_lower') as file_reader:
		for line in file_reader:
			terms = {}
			print count
			count += 1
			line = ' ' + line.strip() + ' '
			for key, value in title_map.iteritems():
				if ' ' + value + ' ' in line:
					if len(value.strip()) > 3 and not value in stop:
						if value.strip() not in terms:
							terms[value.strip()] = 1
			write_to_file(file_writer, terms)

def write_to_file(file_writer, terms):
	output = ""
	for key, value in terms.iteritems():
		temp_dict = dict(terms)
		del temp_dict[key]
		flag = True
		for temp_key, temp_value in temp_dict.iteritems():
			if key in temp_key:
				flag = False
				break
		if flag:
			output = output + key + ','
	file_writer.write(output + '\n')

def load_dict():
	title_map = pickle.load(open('../data/dbpedia/dbpedia_names_title_map.p', 'rb'))
	return title_map

if __name__ == '__main__':
	title_map = load_dict()
	spot_in_tweet(title_map)
