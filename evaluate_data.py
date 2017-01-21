import pickle

dictionary = pickle.load(open('tweets.p', 'rb'))
final_dict = {}

with open('../data/training/NEEL2016-training_neel.gs') as file_reader:
	for line in file_reader:
		line = line.strip()
		tweet = dictionary[line.split('\t')[0].strip()]
		start_index = int(line.split('\t')[1].strip())
		end_index = int(line.split('\t')[2].strip())
		if line.split('\t')[0].strip() in final_dict:
			temp = final_dict[line.split('\t')[0].strip()]
			temp.append(tweet[start_index:end_index])
			final_dict[line.split('\t')[0].strip()] = temp
		else:
			temp = []
			temp.append(tweet[start_index:end_index])
			final_dict[line.split('\t')[0].strip()] = temp

	for key, value in final_dict.iteritems():
		print key + ":" + str(value)
