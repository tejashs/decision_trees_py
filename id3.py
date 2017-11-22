import math
import numpy as np
import featurization

f_train = "Updated_Dataset/updated_train.txt"
f_test = "Updated_Dataset/updated_test.txt"

f_cross = "Updated_Dataset/Updated_CVSplits/updated_training.txt"

depths = {1, 2, 3, 4, 5, 10, 15, 20}

def main():

	#The file contains information about the features
	#Format -> Feature name:Values it can take (seperated by commas)
	with open("info.txt") as f:
	    data_info = f.readlines()

	#Transform the data
	data_train = featurization.featurize(f_train)
	data_test = featurization.featurize(f_test)

	#Create feature nodes
	features = feature_info(data_info)

	print("Accuracy on Train ", test(data_train, data_train, features, -1))
	print("Accuracy on Test ", test(data_train, data_test, features, -1))

	for depth in depths:
		cross_validation(depth, features)
	
def cross_validation(depth, features):
	data = []
	accs = []
	for i in range(4):
		indexs = [j for j in range(4)]
		indexs.remove(i)
		f_test = f_cross.replace(".", '0' + str(i) + '.')
		data_t = featurization.featurize(f_test)
		data = []
		for index in indexs:
			data += featurization.featurize(f_cross.replace(".", '0' + str(index) + '.'))
		accs.append(test(data, data_t, features, depth))
	print("Depth ", depth, "Avg. Accuracy ", np.mean(accs), "Std. Deviation ", np.std(accs))

def test(data_train, data_test, features, depth):
	r = ID3(data_train, features, 0, depth)
	tot = 0.0
	for d in data_test:
		tot += walk_down(r, d[0], d[1])
	return tot/len(data_test)

def walk_down(node, point, label):
	if node.name == "leaf":
		if node.value == label:
			return 1
	if node.branches:
		for b in node.branches:
			if b.value == point[node.index]:
				return walk_down(b.child, point, label)
	return 0

def ID3(data_samples, attributes, depth, depth_limit):

	if not attributes or depth == depth_limit:
		leaf = Node()
		leaf.set_is_leaf(most_common(data_samples))
		return leaf
	
	if(all_same(data_samples)):
		label = data_samples[0][1]
		root = Node()
		root.set_is_leaf(label)
		return root

	base_entropy = calculate_base_entropy(data_samples)
	root = best_attribute(data_samples, base_entropy, attributes)
	root = Node(root.name, root.possible_vals, root.index)
	depth += 1
	
	for val in root.possible_vals:
		b = Branch(val)
		root.add_branch(b)
		subset = subset_val(data_samples, root.index, val)
		if not subset:
			leaf = Node()
			leaf.set_is_leaf(most_common(data_samples))
			b.set_child(leaf)
		else:
			attributes = remove_attribute(attributes, root)
			b.set_child(ID3(subset, attributes, depth, depth_limit))
	return root


def best_attribute(data, base_entropy, attributes):
	max_ig = 0
	max_a = None
	for a in attributes:
		tmp_ig = base_entropy - expected_entropy(data, a)
		tmp_a = a
		if tmp_ig >= max_ig:
			max_ig = tmp_ig
			max_a = a
	return max_a

# Returns the most common label
def most_common(data_samples):
	p = sum(d[1] for d in data_samples)
	if p >= len(data_samples)/2:
		return 1
	else:
		return 0

def expected_entropy(data, attribute):
	data_total = float(len(data))
	e_entropy = 0.0
	for val in attribute.possible_vals:
		entropy, total = calculate_entropy(data, attribute, val)
		e_entropy += (total/data_total) * entropy
	return e_entropy
	
def calculate_entropy(data, attribute, value):
	subset = subset_val(data, attribute.index, value)
	if not subset:
		return [0, 0]

	return [calculate_base_entropy(subset), len(subset)]

def calculate_base_entropy(data):
	l = len(data)
	p = sum(d[1] for d in data)

	if not p or l == p:
		return 0

	n = l - p

	probP = p/l
	probN = n/l

	return (-probP*math.log(probP)) - (probN*math.log(probN))

# Returns a subset of the data where the given feature has the given value
def subset_val(data, feature_index, val):
	return [d for d in data if d[0][feature_index] == val]

# Returns true if all the labels are the same in the sample data
def all_same(data_samples):
	label = data_samples[0][1]
	for s in data_samples:
		if s[1] != label:
			return False
	return True

 
def remove_attribute(attributes, attribute):
	new_attributes = []
	for a in attributes:
		if a.name != attribute.name:
			new_attributes.append(a)
	return new_attributes

def feature_info(data):
	data_inf = []
	for i, d in enumerate(data):
		d = d.split(":")
		r = list(map(int, d[1].rstrip().split(",")))
		a = Node(d[0], r, i)
		data_inf.append(a)

	return data_inf

class Node:
	
	def __init__(self, name ="leaf", vals=None, index=-1):
		self.name = name
		self.possible_vals = vals
		self.index = index
		self.branches = []

	def set_is_leaf(self, value):
		self.leaf = True
		self.value = value

	def add_branch(self, b):
		self.branches.append(b)

class Branch:
	
	def __init__(self, value):
		self.value = value

	def set_child(self, child):
		self.child = child

if __name__ == '__main__':
	main()