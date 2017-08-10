#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

write = sys.stdout.write

###########################################################################
#                                                                         #
#                                                                         #
#                                                                         #
#                                                                         #
#                                                                         #
###########################################################################

class stat_node:
	def __init__(self):
		# node has {id, depth, name, fullname, item_id, unique_cnt, value, parent, children}
		self.id = None
		self.depth = None
		self.name = None
		self.fullname = None
		self.item_id = None
		self.unique_cnt = 0
		self.value = 0
		self.parent = None
		self.children = {}

		self.delim_name = '/'

		self.encode_type = 'cp932' #'utf8'
		self.branch1_u = '   ┣'
		self.branch2_u = '   ┗'
		self.branch3_u = '   ┃'
		self.branch1 = self.branch1_u.encode(self.encode_type)
		self.branch2 = self.branch2_u.encode(self.encode_type)
		self.branch3 = self.branch3_u.encode(self.encode_type)
		self.indent_0 = ''
		self.indent_1 = ' '

	##### set functions
	def set_id(self, id):
		self.id = id

	def set_name(self, name):
		self.name = name

	def set_item_id(self, item_id):
		self.item_id = item_id

	def set_parent(self, parent):
		self.parent = parent

	def set_child(self, child_id, child_node):
		self.children[child_id] = child_node

	def set_depth(self, depth):
		self.depth = depth

	def set_fullname(self, fullname):
		self.fullname = fullname

	def init(self, id, depth, name, fullname, item_id, parent):
		self.set_id(id)
		self.set_depth(depth)
		self.set_name(name)
		self.set_fullname(fullname)
		self.set_item_id(item_id)
		self.set_parent(parent)
		
	##### pretty nodes
	def pretty_node_downward(self, depth, parent_fullname, flg_fullname):
		self.set_depth(depth)

		fullname = ''
		if flg_fullname == 1:
			fullname = parent_fullname + self.delim_name + self.name
			self.set_fullname(fullname)

		for k, child in self.children.items():
			child = self.children[k]
			child.pretty_node_downward(depth+1, fullname, 1)


	##### aggregate functions
	def add_value(self, value):
		self.value += value

	def add_unique_cnt(self, item_id, cnt):
		if self.item_id is None or self.item_id != item_id:
			self.item_id = item_id
			self.unique_cnt += cnt

	def aggregate(self, item_id, value, cnt):
		self.add_value(value)
		self.add_unique_cnt(item_id, cnt)

	# aggregate value (go upward the tree)
	def aggregate_upward(self, item_id, value, cnt):
		self.aggregate(item_id, value, cnt)
		parent = self.get_parent()
		if parent is not None:
			parent.aggregate_upward(item_id, value, cnt)


	##### get functions
	def get_id(self):
		return self.id

	def get_name(self):
		return self.name

	def get_fullname(self):
		return self.fullname

	def get_depth(self):
		return self.depth

	def get_item_id(self):
		return self.item_id

	def get_unique_cnt(self):
		return self.unique_cnt

	def get_value(self):
		return self.value

	def get_parent(self):
		return self.parent

	def get_child(self, child_id):
		return self.children.get(child_id)

	def print_children(self):
		for k, v in self.children.items():
			print(k)

	def print_node(self, delim):
		write(str(self.depth))
		write(delim)
		write(self.id)
		write(delim)
		write(self.fullname)
		write(delim)
		write(str(self.unique_cnt))
		write(delim)
		write(str(self.value))
		write('\n')

	def print_report_downward(self, delim):
		self.print_node(delim)
		#print "<-------children-----------"
		#self.print_children()
		#print "------------------>"
		for k, child in self.children.items():
			child = self.children[k]
			child.print_report_downward(delim)

	def print_tree_downward(self, delim, header, last_flag):
		write(header)

		if header == '':
			write(self.indent_0)
		elif last_flag == 1:
			write(self.branch2_u)
		else:
			write(self.branch1_u)

		write(' '+self.get_name()+' ['+str(self.get_value())+' / '+str(self.get_unique_cnt())+']')
		write('\n')
		
		if last_flag == 1:
			header_new = header + self.indent_1
		else:
			header_new = header + self.branch3_u

		num_children = len(self.children.keys())
		loop = 0
		for k, ptr in self.children.items():
			if loop == num_children - 1:
				last_flag_new = 1
			else:
				last_flag_new = 0
			ptr.print_tree_downward(delim, header_new, last_flag_new)
			loop += 1

###########################################################################
#                                                                         #
#                                                                         #
#                                                                         #
#                                                                         #
#                                                                         #
###########################################################################

class stat_tree:
	def __init__(self):
		self.root = stat_node()
		self.root.init('0', 0, 'ROOT', 'ROOT', None, None)

		self.id2node = {}
		self.id2node['0'] = self.root

		self.outdelim = '\t'
		self.delim_name = '/'

	def get_node_by_id(self, id):
		return self.id2node.get(id)

	# create tree by adding (parent, child) pair
	def add_node(self, id, parent_id, name, parent_name):
		ptr_child = self.id2node.get(id)
		if ptr_child is None:
			ptr_child = stat_node()
			ptr_child.init(id, None, name, None, None, None)
			self.id2node[id] = ptr_child

		ptr_parent = self.id2node.get(parent_id)
		if ptr_parent is None:
			ptr_parent = stat_node()
			ptr_parent.init(parent_id, None, parent_name, None, None, None)
			self.id2node[parent_id] = ptr_parent

		ptr_child.set_parent(ptr_parent)
		ptr_parent.set_child(id, ptr_child)

	# create tree by adding
	# (node(0), node(1), node(2), ..., node(depth-1)) under root
	def add_fullpath(self, ids, names, depth):
		flg = 0
		name = None
		if names is None:
			flg = 1

		ptr = self.root
		fullname = ''
		for loop in range(depth):
			ptr1 = ptr.get_child(ids[loop])
			if ptr1 is None:
				ptr1 = stat_node()
				if flg == 0:
					name = names[loop]
					fullname = fullname + self.delim_name + name
				ptr1.init(ids[loop], loop+1, name, fullname, None, ptr)
				ptr.set_child(ids[loop], ptr1)
				id2node.setdefault(ids[loop], ptr1)
			ptr = ptr1
		return ptr


	# aggregate value (go upward the tree)
	def aggregate_upward(self, id, item_id, value):
		node = self.id2node[id]
		if node is not None:
			node.aggregate_upward(item_id, value, 1)

	# aggregate value (go downward the tree)
	def aggregate_downward(self, ids, idx_st, idx_ed, item_id, value):
		ptr = self.root
		ptr.aggregate(item_id, value, 1)

		fullname = ''
		for loop in range(idx_st, idx_ed):
			ptr1 = ptr.get_child(ids[loop])
			if ptr1 is None:
				ptr1 = stat_node()
				if loop > idx_st:
					parent_fullname = ptr.get_fullname()
				else:
					parent_fullname = ''
				fullname = parent_fullname + self.delim_name + ids[loop]
				#write(loop, ': Register ', fullname
				ptr1.init(ids[loop], loop-idx_st+1, None, fullname, None, ptr)
				ptr.set_child(ids[loop], ptr1)
				#write("================"
				#ptr.print_children()
				#write("================"
				self.id2node.setdefault(ids[loop], ptr1)
			ptr = ptr1
			ptr.aggregate(item_id, value, 1)

		return ptr

	# set depth, fullname
	def pretty_tree(self):
		self.root.pretty_node_downward(0, '', 0)


	def print_report(self):
		self.root.print_report_downward(self.outdelim)

	def print_tree(self):
		self.root.print_tree_downward('\t', '', 1)

	def print_id2node(self):
		for k, v in self.id2node.items():
			print(k+str(v.get_id())+v.get_fullname())

###########################################################################
#                                                                         #
#                                                                         #
#                                                                         #
#                                                                         #
#                                                                         #
###########################################################################

# input data:
# 0: item/customer id
# 1: path1
# 2: path2
# 3: path3
# ...
# n: path(n)
# n+1: value
def aggregate_path_data():
	hd = stat_tree()

	header = sys.stdin.readline()
	indelim = '\t'

	for line in sys.stdin:
		data = line[:-1].split(indelim)
		hd.aggregate_downward(data, 1, len(data)-1, data[0], float(data[len(data)-1]))

	write('Depth'+'\t'+'ID'+'\t'+'PATH'+'\t'+'UniqueCount'+'\t'+'Value'+'\n')
	hd.print_report()

	#print "-------------------------"
	#hd.print_id2node()

# tree_fname format:
# 0: id
# 1: id (parent)
# 2: path
# 3: path (parent)
def make_tree(hd, tree_fname):
	fp = open(tree_fname, "r")
	for line in fp:
		data = line[:-1].split('\t')
		hd.add_node(data[0], data[1], data[2], data[3])
	fp.close()

# input data:
# 0: item/customer id
# 1: path_id
# 2: value
def aggregate_id_data(tree_fname):
	hd = stat_tree()
	make_tree(hd, tree_fname)
	hd.pretty_tree()

	header = sys.stdin.readline()
	indelim = '\t'

	for line in sys.stdin:
		data = line[:-1].split(indelim)
		hd.aggregate_upward(data[1], data[0], float(data[2]))

	write('Depth'+'\t'+'ID'+'\t'+'PATH'+'\t'+'UniqueCount'+'\t'+'Value'+'\n')
	hd.print_report()
	print("--------------------------")
	hd.print_tree()

def main():
	flg = 2
	if flg == 1:
		aggregate_path_data()
	else:
		if len(sys.argv) < 2:
			print("usage: cat datafile | python mkreport.py (tree_fname) > output")
		else:
			aggregate_id_data(sys.argv[1])

if __name__=='__main__':
	main()



