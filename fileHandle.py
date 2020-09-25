import os

def find_name_in_file(filename, name_to_find):
	result = False
	f = open("img_names.txt", "r")
	# Wlaking top-down from the root
	contents = f.read().split()
	for filename in contents:
		if filename == name_to_find:
			result = True
	f.close()
	return result

def find_files_and_wirte_to_txt(search_path, filename):
	f = open(filename, "a+")
	# Wlaking top-down from the rootf
	for root, dir, files in os.walk(search_path):
		for file in files:
			f.write("%s\n" % file)
	f.close()   
# find_files_and_wirte_to_txt('./images','img_names.txt')
print('Done')

print(find_name_in_file('img_names.txt', '8xmre2.jpg'))
