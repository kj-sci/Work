# -*- coding: shift_jis -*-
import math
import sys

write = sys.stdout.write

indent = '\t'

class make_graphviz:
	def __init__(self, graph_label, node_fname, edge_fname):
		self.node2id = {}
		self.rank_nodes = {}
		
		self.graph_name = 'test'
		
		if graph_label is None:
			self.graph_label = 'test'
		else:
			self.graph_label = graph_label

		self.node_fname = node_fname
		self.edge_fname = edge_fname
		
		self.node_attr = ['label', 'charset', 'fontname', 'fontsize', 'shape', 'style', 'color']
		self.edge_attr = ['label', 'charset', 'fontname', 'fontsize', 'style', 'color']
		
		self.node_list = {}
		self.node_list['blank'] = []
		self.edge_list = {}
		

	###########################################################################################
	#                                                                                         #
	#                      API                                                                #
	#                                                                                         #
	###########################################################################################
	def process(self):
		self.print_header()
		self.read_node_data()
		self.print_node_list()
		
		self.read_edge_data()
		
		#self.print_rank()
		self.print_footer()
	
	
	
	###########################################################################################
	#                                                                                         #
	#                  HELP FUNCTIONS                                                         #
	#                                                                                         #
	###########################################################################################
		
	def read_node_data(self):
		##########################################
		#            process node                #
		##########################################
		#sys.stderr.write("Open "+self.node_fname+"\n")
		fp = open(self.node_fname, 'r')
		header = fp.readline()
		field_name = header[:-1].split('\t')
		#sys.stderr.write("field_name\n")
		#for loop in range(len(field_name)):
		#	sys.stderr.write(str(loop)+': '+field_name[loop]+"\n")

		num_nodes = 0
		# input data
		# 0: name_space
		# 1: layer
		# 2: label
		# 3: shape
		# 4: style
		# 5: color
		# 6: charset
		# 7: fontname
		# 8: fontsize
		for line in fp:
			data = line[:-1].split('\t')
			node = {}
			for loop in range(len(field_name)):
				if len(data[loop]) > 0:
					node[field_name[loop]] = data[loop].lower()
					#sys.stderr.write(field_name[loop]+": "+data[loop]+"\n")

			if node['label'] in self.node2id.keys():
				sys.stderr.write('Error, '+node['label']+' already exists\n')
				# do something (pending)
				
			node['NODE_ID'] = 'node_' + str(num_nodes)
			num_nodes += 1
			
			if 'name_space' in node.keys():
				self.node2id[node['name_space']+'.'+node['label']] = node['NODE_ID']
				if node['name_space'] not in self.node_list.keys():
					self.node_list[node['name_space']] = []
				ptr = self.node_list[node['name_space']]
			else:
				self.node2id[node['label']] = node['NODE_ID']
				ptr = self.node_list['blank']
			ptr.append(node)

			# print node
			#self.print_node(node)

			# set rank
			if node.has_key('layer'):
				rank = node['layer']
				if not self.rank_nodes.has_key(rank):
					dummy = ''
					self.rank_nodes[rank] = dummy
				self.rank_nodes[rank] = self.rank_nodes[rank] + ' ' + node['NODE_ID']

		fp.close()
		
	def read_edge_data(self):
		##########################################
		#            process edge                #
		##########################################
		#sys.stderr.write("Open "+self.edge_fname+"\n")
		fp = open(self.edge_fname, 'r')
		header = fp.readline()
		field_name = header[:-1].split('\t')
		#sys.stderr.write("field_name\n")
		#for loop in range(len(field_name)):
		#	sys.stderr.write(str(loop)+': '+field_name[loop]+"\n")

		# input data
		# 0: name_space_from
		# 1: name_space_to
		# 2: node_label_from
		# 3: node_label_to
		# 4: label(?)
		# 5: stle
		# 6: color
		# 7: fontname
		# 8: fontsize
		# ...
		for line in fp:
			data = line[:-1].split('\t')
			edge = {}
			for loop in range(len(field_name)):
				if len(data[loop]) > 0:
					edge[field_name[loop]] = data[loop].lower()

			# def node_from
			if 'name_space_from' in edge.keys():
				node_identifier_from = edge['name_space_from'] + '.' + edge['node_label_from']
			else:
				node_identifier_from = edge['node_label_from']

			# def node_to
			if 'name_space_to' in edge.keys():
				node_identifier_to = edge['name_space_to'] + '.' + edge['node_label_to']
			else:
				node_identifier_to = edge['node_label_to']
			
			# find node_id_from
			if node_identifier_from not in self.node2id.keys():
				self.node2id[node_identifier_from] = 'node_' + str(num_nodes)
				sys.stderr.write('ERROR: No node for '+node_identifier_from+'\n')
				num_nodes += 1
			edge['NODE_ID_FROM'] = self.node2id[node_identifier_from]

			# find node_id_to
			if node_identifier_to not in self.node2id.keys():
				self.node2id[node_identifier_to] = 'node_' + str(num_nodes)
				sys.stderr.write('ERROR: No node for '+node_identifier_to+'\n')
				num_nodes += 1
			edge['NODE_ID_TO'] = self.node2id[node_identifier_to]
				
			# print edge
			self.print_edge(edge)
		fp.close()
		
	###########################################################################################
	#                                                                                         #
	#                     PRINT FUNCTIONS                                                     #
	#                                                                                         #
	###########################################################################################
	def print_header(self):
		#'rotate=90', 'fontsize=20'
		options = ['labelloc=t', 'rankdir=LR']
		option_str = ', '.join(options)

		print 'digraph ' + self.graph_name + '{'
		print indent + 'graph [label="' + self.graph_label + '", ' + option_str + '];'
		print indent + 'node [shape=box, style=rounded]; edge [labelfloat=true];'
		print indent
		
	def print_footer(self):
		print '}'
	
	def print_node_list(self):
		if len(self.node_list.keys()) == 1:
			# no sub graph
			ptr = self.node_list['blank']
			for node in ptr:
				self.print_node(node, 1)
		else:
			cnt_cluster = 1
			for name_sp, ptr in self.node_list.items():
				cluster_name = 'cluster_'+str(cnt_cluster)
				write(indent+'subgraph '+cluster_name+'{\n')
				for node in ptr:
					self.print_node(node, 2)
				if name_sp == 'blank':
					write(indent+indent+'label=""\n')
				else:
					write(indent+indent+'label="'+name_sp+'"\n')
				write(indent+'}\n')
				cnt_cluster += 1
	
		
	# node attributes
	# - label: (name)
	# - charset: UTF-8
	# - fontname: MS UI Gothic/
	# - fontsize: 10/
	# - shape: Mrecord/box/ellipse
	# - style: filled/rounded/etc.
	# - color: white/blue/black/blue/red/etc.
	def print_node(self, node, num_indents):
		for loop in range(num_indents):
			write(indent)
		write(node['NODE_ID'])
		loop = 0
		for item in self.node_attr:
			if node.has_key(item):
				if loop == 0:
					write(' [')
				else:
					write(', ')
				if item == 'label':
					write(item+'="'+node[item]+'"')
				else:
					write(item+'='+node[item])
				loop += 1
		if loop > 0:
			write(']')
		write(';\n')

	def print_rank(self):
		for (k, v) in self.rank_nodes.items():
			write(indent+indent+'{rank=same; ' + v + ';}\n')
			
	# edge attributes
	# - label
	# - style: dashed/
	# - fontsize: 10/
	def print_edge(self, edge):
		write(indent + indent + edge['NODE_ID_FROM'] + ' -> ' + edge['NODE_ID_TO'])
		loop = 0
		for item in self.node_attr:
			if edge.has_key(item):
				if loop == 0:
					write(' [')
				else:
					write(', ')
				if item == 'label':
					write(item+'="'+edge[item]+'"')
				else:
					write(item+'='+edge[item])
				loop += 1
		if loop > 0:
			write(']')
		write(';\n')


###########################################################################################
#                                                                                         #
#                                   MAIN                                                  #
#                                                                                         #
###########################################################################################
def main():
	if len(sys.argv) < 4:
		sys.stderr.write('Usage: python $0 graph_name node_fname edge_fname > graphviz_file\n')
		sys.exit(1)
	
	graph_name = sys.argv[1]
	node_fname = sys.argv[2]
	edge_fname = sys.argv[3]

	hd = make_graphviz(graph_name, node_fname, edge_fname)
	hd.process()

if __name__ == '__main__':
	main()
	
		