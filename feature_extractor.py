import get_most_probable_pages

def read_file(file_name):
	file_reader = open(file_name, 'r')
	return file_reader.read().strip()

def get_commonness_feature(text):
	lines = text.split('\n')
	count = 0
	for line in lines:
		print count
		count += 1
		tokens = line.strip().split('\t')
		temp = []
		temp.append(tokens[0].strip())
		write_to_file('l2r_data', get_most_probable_pages.iterate_anchor_text(tokens[1].strip(), temp, 25, count))

def write_to_file(file_name, content):
	file_writer = open('../data/training/' + file_name, 'a')
	file_writer.write(content)
	file_writer.close()

if __name__ == '__main__':
	lines = read_file('../data/training/NEEL2016-training_neel_modified_unique_no_null.gs')
	get_commonness_feature(lines)
