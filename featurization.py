def featurize(fname):

	labels = {'+': 1, '-': 0}

	with open(fname, encoding = "utf-8") as f:
	    data = [line.rstrip() for line in f]
	    
	new_data = []
	vowels = ['a','e','i','o','u']
	for d in data:
		has_middle = longer = same_f_l = first_before_last = second_vowel = last_name_even = 0
		d = d.split(" ")
		label = labels[d[0]]
		first_name = d[1].lower()
		last_name = d[len(d) - 1].lower()
		# Do they have a middle name?
		if len(d) > 3:
			has_middle = 1
		# Is their first name longer than their last name?
		if len(first_name) > len(last_name):
			longer = 1
		# Does their first name start and end with the same letter? (ie "Ada")
		if first_name[0] == first_name[len(first_name) - 1]:
			same_f_l = 1
		# Does their first name come alphabetically before their last name? (ie "Dan Klein" because "d" comes before "k")
		if ord(first_name[0]) < ord(last_name[0]):
			first_before_last = 1
		# Is the second letter of their first name a vowel (a,e,i,o,u)?
		if len(first_name) > 1 and first_name[1] in vowels:
			second_vowel = 1
		# Is the number of letters in their last name even?
		if len(last_name) % 2 == 0:
			last_name_even = 1

		new_data.append([[has_middle, longer, same_f_l, first_before_last, second_vowel, last_name_even], label])

	return new_data