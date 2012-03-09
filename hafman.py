#!/usr/bin/env python

import sys
import heapq


class Hafman(object):
	"""Hafman archivator"""

	class Tree(object):
		"""Tree node"""
		def __init__(self, weight, ch=None, left=None, right=None):
			super(Tree, self).__init__()
			self.ch = ch
			self.left = left
			self.right = right
			self.weight = weight

		def __lt__(self, other):
			return self.weight < other.weight

		def __str__(self):
			return "w-{0} ch {1})".format(self.weight, self.ch)

		def hameChildren(self):
			return self.left != None or self.right != None

	bytes = None
	freq_table = {}
	hafman_table = {}

	def __init__(self, byteArray):
		self.bytes = byteArray

	def create_freq_table(self):
		for byte in bytes:
			if byte in raw_table:
				freq_table[byte] += 1
			else:
				freq_table[byte] = 1

	def make_tree(self):
		tree = [ Tree(v,k) for k, v in raw_table.items()]
		heapq.heapify(tree)
		while len(tree) > 1:
			left, right = heapq.heappop(tree), heapq.heappop(tree)
			parent = Tree(left.weight  + right.weight, left=left, right = right)
			heapq.heappush(tree, parent)

		def convert(tree, l):
			if tree.hameChildren():
				convert(tree.left, l.append(False))
				convert(tree.right, l.append(True))
			else:
				hafman_table[tree.ch] = l

		convert(tree[0], [])

	def encode_freq_table(self):
		res = bytearray([])
		for byte in freq_table.keys:
			res.append(byte)
			count = freq_table[byte]
			res.append(count//2**BITS_IN_BYTE)
			res.append(count%2**BITS_IN_BYTE)
		return res

	def	encode_file(self):
		BITS_IN_BYTE=8

		bit_res = [self.hafman_table[byte] for byte in self.bytes]
		step = 0
		temp = 0
		res = bytearray ([])
		for bit in bit_res:
			if step == BITS_IN_BYTE:
				res.append(temp)
				step =0
				temp =0
			temp <<= 1
			temp |= bit
			step +=1

		if step != 0:
			while step != BITS_IN_BYTE:
				temp <<= 1
				step += 1
			res.append(temp)
		return res

	def encode(self):
		create_freq_tabl()
		make_tree()
		res = bytearray([len(self.freq_table)])
		res.extend(encode_freq_table())
		res.extend(encode_file())
		return res

