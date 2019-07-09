import json

json_file = open('fam_dict.json', 'r')
fam_dicts = json.load(json_file)
json_file.close()

spouses = fam_dicts["spouses"]


def return_spouse(fam_name, search_name):
	"""returns the spouse of an individual from the spouses dictionary"""
	for member, spouse_name in spouses[fam_name].items():
		if search_name in member:
			return spouse_name
		elif search_name in spouse_name:
			return member


def return_siblings(fam_name, search_name):
	"""returns the person's list of siblings"""
	for gen_dict in fam_dicts[fam_name]:
		for parent, children in gen_dict.items():
			if search_name in children:
				sibling_list = [child for child in children if child != search_name]
				return sibling_list
	
	return []


def return_parent(fam_name, search_name):
	"""returns the person's parent's name"""
	for generation_dict in fam_dicts[fam_name]:
		for parent, children in generation_dict.items():
			if search_name in children:
				return parent


def return_both_parents(fam_name, search_name):
	"""returns the name of the parent and that parent's spouse"""
	first_parent = return_parent(fam_name, search_name)
	second_parent = return_spouse(fam_name, first_parent)
	parent_list = [first_parent, second_parent]

	return parent_list


def return_children(fam_name, search_name):
	"""returns the list of children given a specific parents name"""
	if search_name in spouses[fam_name].values():
		search_name = return_spouse(fam_name, search_name)

	for generation_dict in fam_dicts[fam_name]:
		for parent, children in generation_dict.items():
			if search_name in parent:
				return children

	return []


def return_aunts(fam_name, search_name):
	"""returns the list of aunts or uncles of an individuaL"""
	parent = return_parent(fam_name, search_name)
	parent_siblings = return_siblings(fam_name, parent)

	return parent_siblings


def return_auntz(fam_name, search_name):
	"""returns the list of aunts or uncles of an individuaL"""
	parent = return_parent(fam_name, search_name)
	parent_siblings = return_siblings(fam_name, parent)

	just_spouses = []
	for name in parent_siblings:
		spouse = return_spouse(fam_name, name)
		if spouse != None:
			just_spouses.append(spouse)

	aunts_and_spouses = just_spouses + parent_siblings
	return aunts_and_spouses


def return_great_auntz(fam_name, search_name):
	"""returns a list of a person's great auntz"""
	parent = return_parent(fam_name, search_name)
	parent_auntz = return_auntz(fam_name, parent) 

	return parent_auntz


def return_nieces(fam_name, search_name):
	"""returns the list of nieces given a specific person's name"""
	nieces_list = []
	if search_name in spouses[fam_name].values():
		search_name = return_spouse(fam_name, search_name)

	sibling_list = return_siblings(fam_name, search_name)

	for sib in sibling_list:
		sib_children_list = return_children(fam_name, sib)
		for sib_child in sib_children_list:
			nieces_list.append(sib_child)

	return nieces_list


def return_great_nieces(fam_name, search_name):
	"""returns a list of great nieces for a person"""
	nieces_list = return_nieces(fam_name, search_name)
	great_nieces_list = []

	for niece in nieces_list:
		nieces_children_list = return_children(fam_name, niece)
		for niece_child in nieces_children_list:
			great_nieces_list.append(niece_child)

	return great_nieces_list


def return_cousins(fam_name, search_name):
	"""returns the cousins of the person"""
	aunts = return_aunts(fam_name, search_name)
	cousins_list = []

	for aunt in aunts:
		aunt_kiddos_list = return_children(fam_name, aunt)
		for kid in aunt_kiddos_list:
			cousins_list.append(kid)

	return cousins_list


def return_first_cousins_once_removed(fam_name, search_name):
	"""returns a list of a person's 1st cousins once removed (a person's parents' cousins or a persons' cousins children"""
	first_cousins_once_removed = []
	cousin_list = return_cousins(fam_name, search_name)

	for cousin_name in cousin_list:
		cousin_kids = return_children(fam_name, cousin_name)
		for kid_name in cousin_kids:
			first_cousins_once_removed.append(kid_name)

	parent_name = return_parent(fam_name, search_name)
	parent_cousins = return_cousins(fam_name, parent_name)

	for parent_cousin in parent_cousins:
		first_cousins_once_removed.append(parent_cousin)

	return first_cousins_once_removed


def return_second_cousins(fam_name, search_name):
	"""returns a list of second cousins (the children of an person's parent's cousins)"""
	second_cousins = []
	parent_name = return_parent(fam_name, search_name)
	parent_cousins = return_cousins(fam_name, parent_name)

	for parent_cousin in parent_cousins:
		cousin_kids = return_children(fam_name, parent_cousin)
		for cousin_kid in cousin_kids:
			second_cousins.append(cousin_kid)

	return second_cousins


def return_grandchildren(fam_name, search_name):
	"""returns the list of grandchildren"""
	grandchildren_list = []
	child_list = return_children(fam_name, search_name)

	for child in child_list:
		child_children_list = return_children(fam_name, child)
		for gchild in child_children_list:
			grandchildren_list.append(gchild)

	return grandchildren_list


def return_great_grandchildren(fam_name, search_name):
	"""returns the list of great grandchildren for a given name"""
	great_grandchildren_list = []
	grand_children_list = return_grandchildren(fam_name, search_name)
	for grandchild in grand_children_list:
		grand_child_children = return_children(fam_name, grandchild)
		for grand_child_child in grand_child_children:
			great_grandchildren_list.append(grand_child_child)

	return great_grandchildren_list


def return_grandparents(fam_name, search_name):
	"""returns the grandparent's name given an individual"""
	parent = return_parent(fam_name, search_name)
	grandparent = return_parent(fam_name, parent)
	grandparent_spouse = return_spouse(fam_name, grandparent)
	both_grand_parents_list = [grandparent, grandparent_spouse]

	return both_grand_parents_list


def return_great_grandparents(fam_name, search_name):
	"""returns the person's great grandparents"""
	parent = return_parent(fam_name, search_name)
	parent_grandparents = return_grandparents(fam_name, parent)
	return parent_grandparents


def return_all_family(fam_name, search_name):
	"""returns the list of each family member without any duplicates"""
	all_family = []
	childrens_list = []
	parent_list = []
	spouses_list = [spouse_name for spouse_name in spouses[fam_name].values()]

	for generation_dict in fam_dicts[fam_name]:
		for parent, children in generation_dict.items():
			parent_list.append(parent)
			for child in children:
				childrens_list.append(child)
	
	for parent in parent_list:
		all_family.append(parent)

	for child in childrens_list:
		if child not in all_family:
			all_family.append(child)

	all_family = all_family + spouses_list
	return all_family
	

def print_singular(fam_name, search_name, func_name, title):
	"""prints the returns of the function when the return is not a list"""
	relationship_person = func_name(fam_name, search_name)
	print("%s's %s is %r" % (search_name, title, relationship_person))


def print_list(fam_name, search_name, func_name, title, singular):
	"""takes all this info and then prints out the info"""
	relationship_people_list = func_name(fam_name, search_name)
	num_relationship_people = len(relationship_people_list)
	
	if num_relationship_people < 1:
		print("%s doesn't have any %s" % (search_name, title))

	elif num_relationship_people >= 1:
		if num_relationship_people == 1:
			new_string = "%s's has 1 %s: %r" % (search_name, singular, relationship_people_list[0])
		elif num_relationship_people > 1:
			new_string = "%s has %r %s: %r" % (search_name, num_relationship_people, title, ", ".join(relationship_people_list))
		newer_string = new_string.replace("'", "")
		print(newer_string)


def look_up():
	which_fam = input("what family would you like to look in? ")
	search_name = input("what's their name? ")
	find_out = input("which relationship would you like to find out? ")

	#dictionaries for functions that will either return a list(pl_dict) or a single individual(sn_dict)
	sn_dict = {"spouse": [return_spouse, "spouse"],
	"parent": [return_parent, "parent"]}

	pl_dict = {"parents": [return_both_parents, "parents", "parent"],
	"children": [return_children, "children", "child"],
	"siblings": [return_siblings, "siblings", "sibling"],
	"nieces": [return_nieces, "nieces/nephews", "niece/nephew"],
	"great nieces": [return_great_nieces, "great nieces/nephews", "great niece/nephew"],
	"auntz": [return_auntz, "aunts/uncles", "aunt/uncle"], 
	"great aunts": [return_great_auntz, "great aunts/uncles", "great aunt/uncle"],
	"cousins": [return_cousins, "cousins", "cousin"],
	"first cousins once removed": [return_first_cousins_once_removed, "first cousins once removed", "first cousin once removed"],
	"second cousins": [return_second_cousins, "second cousins", "second cousin"],
	"grandchildren": [return_grandchildren, "grandchildren", "grandchild"], 
	"great grandchildren": [return_great_grandchildren, "great grandchildren", "great grandchild"],
	"grandparents": [return_grandparents, "grandparents", "grandparent"],
	"great grandparents": [return_great_grandparents, "great grandparents", "great grandparent"]
	}

	one_side = ["parents", "children", "siblings", "nieces", "grandchildren", "great grandchildren", "great nieces"]
	both_sides = ["great grandparents", "grandparents", "auntz", "great aunts", "cousins", "first cousins once removed", "second cousins"]

	if which_fam == "both":
		fam_names_list = [last_name for last_name in fam_dicts.keys() if last_name != "spouses"]
	elif which_fam != "both":
		fam_names_list = [which_fam]

	if find_out in sn_dict.keys():
		print_singular(fam_names_list[0], search_name, sn_dict[find_out][0], sn_dict[find_out][1])
	elif find_out in pl_dict.keys():
		for fam_name in fam_names_list:
			print_list(fam_name, search_name, pl_dict[find_out][0], pl_dict[find_out][1], pl_dict[find_out][2])

	elif find_out == "whole family":
		print_singular(fam_names_list[0], search_name, sn_dict["spouse"][0], sn_dict["spouse"][1])
		for relationship in one_side:
			print_list(fam_names_list[0], search_name, pl_dict[relationship][0], pl_dict[relationship][1], pl_dict[relationship][2])
		for fam_name in fam_names_list:
			for relationship in both_sides:
				print_list(fam_name, search_name, pl_dict[relationship][0], pl_dict[relationship][1], pl_dict[relationship][2])

	else:
		print("that wasn't an option. try again.")


def add_spouse(fam_name, fam_member_name):
	"""adds a spouse for an existing family member """
	new_spouse = input("what's the name of the new spouse? ")
	if fam_member_name == "blank":
		fam_member_name = input("who're they married to in the family? ")

	if fam_name == "both":
		for family_name in spouses.keys():
			spouses[family_name][fam_member_name] = new_spouse
	elif fam_name != "both":
		spouses[fam_name][fam_member_name] = new_spouse

	write_2_json_file()


def add_child(fam_name, new_person_parent):
	"""adds a child to an existing family member"""
	new_person = input("what's the child's name? ")

	if new_person_parent == "blank":
		new_person_parent = input("who is their parent? ")
		quest_spouse = input("are they married(y/n)? ")
		if quest_spouse == "y":
			add_spouse(fam_name, new_person)

	# elif new_person_parent != "blank":

	# if fam_name == "both":
	# 	fam_dicts_keys = fam_dicts.keys()
	# 	family_names = [fam_dicts_keys[0], fam_dicts_keys[1]]
	# 	for family_name in family_names:
	# 		for index, gen_dict in enumerate(fam_dicts[family_name]):
	# 			for parent, current_children in gen_dict.items():
	# 				if new_person_parent in parent:
	# 					current_children.append(new_person)
	# 					gen_dict[parent] = current_children
	# 					if index < 2:
	# 						fam_dicts[family_name][index+1][new_person] = []

	# elif fam_name != "both":

	for index, gen_dict in enumerate(fam_dicts[fam_name]):
		for parent, current_children in gen_dict.items():
			if new_person_parent in parent:
				current_children.append(new_person)
				gen_dict[parent] = current_children
				if index < 2:
					fam_dicts[fam_name][index+1][new_person] = []

	write_2_json_file()

	quest_child = input("do they have children(y/n)? ")
	if quest_child == "y":
		add_child(fam_name, new_person)


def add_fam_member():
	"""directs the user to choose what type of person to add to the family"""
	fam_name = input("which family? ")
	add_spouse_or_add_child = input("do you want to add a (child) or a (spouse)? ")
	if add_spouse_or_add_child == "child":
		add_child(fam_name, "blank")
	elif add_spouse_or_add_child == "spouse":
		add_spouse(fam_name, "blank")


def start_question():
	"""gets the user input to make the queries"""
	direction = input("Would you like to (look) someone up or (add) someone in or (test)? ")

	if direction == "look":
		look_up()
	elif direction == "add":
		add_fam_member()
	elif direction == "test":
		test_function()
	else:
		print("dude, totes not an option")
		print("try again.")
		start_question()


def write_2_json_file():
	json_file_w = open('fam_dict.json', 'w')
	json.dump(fam_dicts, json_file_w)
	json_file_w.close()


def test_function():
	what_test = input("what test?")
	what_fam = input("what family?")
	what_name = input("what name?")

	if what_test == "great_nieces":
		return_great_nieces(what_fam, what_name)


start_question()