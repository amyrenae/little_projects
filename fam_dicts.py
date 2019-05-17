import json

json_file = open('fam_dict.json', 'r')
fam_dicts = json.load(json_file)
json_file.close()
spouses = fam_dicts["spouses"]


def return_spouse(fam_name, search_name):
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


def return_cousins(fam_name, search_name):
	"""returns the cousins of the person"""
	aunts = return_aunts(fam_name, search_name)
	cousins_list = []
	for aunt in aunts:
		aunt_kiddos_list = return_children(fam_name, aunt)
		for kid in aunt_kiddos_list:
			cousins_list.append(kid)
	return cousins_list


def return_grandchildren(fam_name, search_name):
	"""returns the list of grandchildren"""
	grandchildren_list = []
	child_list = return_children(fam_name, search_name)

	for child in child_list:
		child_children_list = return_children(fam_name, child)
		for gchild in child_children_list:
			grandchildren_list.append(gchild)

	return grandchildren_list


def return_grandparents(fam_name, search_name):
	"""returns the grandparent's name given an individual"""
	parent = return_parent(fam_name, search_name)
	grandparent = return_parent(fam_name, parent)
	grandparent_spouse = return_spouse(fam_name, grandparent)
	both_grand_parents_list = [grandparent, grandparent_spouse]
	return both_grand_parents_list


def return_all_family(fam_name):
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

	print("all_family list", all_family)
	return all_family
	


def print_singular(fam_name, search_name, func_name, title):
	"""prints the returns of other functions if the result is not a list"""
	relationship_person = func_name(fam_name, search_name)
	print("%s's %s is %r" % (search_name, title, relationship_person))

	start_question()


def print_list(fam_name, search_name, func_name, title, singular):
	"""takes all this info and then prints out the info"""
	relationship_people_list = func_name(fam_name, search_name)
	num_relationship_people = len(relationship_people_list)
	if num_relationship_people < 1:
		print("Sorry, %s doesn't have any %s" % (search_name, title))
	elif num_relationship_people == 1:
		print("%s's has 1 %s: %r" % (search_name, singular, relationship_people_list))
	elif num_relationship_people > 1:
		print("%s has %r %s: %r" % (search_name, num_relationship_people, title, relationship_people_list))

	start_question()


def look_up():
	fam_name = input("what family would you like to look in? ")
	search_name = input("what's their name? ")
	find_out = input("which relationship would you like to find out? ")

	if find_out == "siblings":
		print_list(fam_name, search_name, return_siblings, find_out, "sibling")
	elif find_out == "spouse":
		print_singular(fam_name, search_name, return_spouse, find_out)
	elif find_out == "parent":
		print_singular(fam_name, search_name, return_parent, find_out)
	elif find_out == "parents":
		print_list(fam_name, search_name, return_both_parents, find_out, "parent")
	elif find_out == "children":
		print_list(fam_name, search_name, return_children, find_out, "child")
	elif find_out == "aunts":
		print_list(fam_name, search_name, return_aunts, "aunts/uncles", "aunt/uncle")
	elif find_out == "auntz":
		print_list(fam_name, search_name, return_auntz, "aunts/uncles", "aunt/uncle")		
	elif find_out == "nieces":
		print_list(fam_name, search_name, return_nieces, "nieces/nephews", "niece/nephew")
	elif find_out == "cousins":
		print_list(fam_name, search_name, return_cousins, "cousins", "cousin")
	elif find_out == "grandchildren":
		print_list(fam_name, search_name, return_grandchildren, find_out, "grandchild")
	elif find_out == "grandparents":
		print_list(fam_name, search_name, return_grandparents, find_out, "grandparent")
	elif find_out == "whole family":
		return_all_family(fam_name)
	else:
		print("that wasn't an option. try again.")


def add_spouse(fam_name, fam_member_name):
	"""adds a spouse for an existing family member """
	new_spouse = input("what's the name of the new spouse? ")
	if fam_member_name == "blank":
		fam_member_name = input("who're they married to in the family? ")

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
		add_child(fam_name, new_person_parent)


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
	direction = input("Would you like to (look) someone up or (add) someone in? ")

	if direction == "look":
		look_up()
	elif direction == "add":
		add_fam_member()
	else:
		print("dude, totes not an option")
		print("try again.")
		start_question()


def write_2_json_file():
	json_file_w = open('fam_dict.json', 'w')
	json.dump(fam_dicts, json_file_w)
	json_file_w.close()


start_question()