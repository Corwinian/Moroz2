class LZW(object):
	"""LZW archivator"""

	bytes = None

	def __init__(self, byteArray):
		self.bytes = byteArray

	def encode (self):
		dict_size = 256
		dictionary = {}
		for i in range(256):
			dictionary[i] = i
		w = 0
		result = []
		for c in self.bytes:
			wc = w + c
			if dict_size >= 65536:
				dictionary = {}
#			for i in range(256):
#				dictionary[chr(i)] = i
			dict_size = 256
			if wc in dictionary:
				w = wc
			else:
				result.append(dictionary[w])
				dictionary[wc] = dict_size
				dict_size += 1
				w = 0 + c
		result.append(dictionary[w])
		res = bytearray([])
		byte = 0
		first = True
		for ch in result:
			if first:
				res.append(ch // 2**4)
				byte = ch % 2**4
				first = False
			else:
				res.append((byte << 4) + ch // 2**8)
				res.append(ch // 2**4)
				byte = 0
				first = True
		if not first:
				res.append((byte << 4))
		return res
