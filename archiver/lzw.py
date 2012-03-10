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
#			if dict_size >= 65536:
#			for i in range(256):
#				dictionary[chr(i)] = i
#			dict_size = 256
			if wc in dictionary:
				w = wc
			else:
				if dict_size < 4096:
					dictionary[wc] = dict_size
					dict_size += 1
				result.append(dictionary[w])
				w = 0 + c
		result.append(dictionary[w])
		res = bytearray([])
		byte = 0
		first = True
		print("ar size - {0}".format(len(result)))
		print("first byte - {0}".format(result[0]))
		print("second byte - {0}".format(result[1]))
		for ch in result:
			if first:
				if (ch // 2**4 ) > 255:
					print ("ch - {0} // 2**4 {1}".format(ch, ch // 2**4))
				res.append(ch // 2**4)
				byte = ch % 2**4
				first = False
			else:
				res.append((byte << 4) + ch // 2**8)
				res.append(ch % 2**8)
				byte = 0
				first = True
		if not first:
				res.append((byte << 4))
		return res

	def decode (self):
		dict_size = 256
		byte = 0
		step = 0
		compressed = []
		for b in self.bytes:
			if step == 0:
				byte = b
				step += 1
			elif step == 1:
				step += 1
				compressed.append((byte << 4) + (b // 2**4))
				byte = b % 2**4
			elif step == 2:
				#print ("b - {0} byte {1}".format(b, byte) )
				compressed.append((byte << 8) + b)
				step =0
		dictionary = {}
		for i in range(256):
			dictionary[i] = chr(i)
		w = "" + chr(compressed.pop(0))
		result = w
		for k in compressed:
			if k in dictionary:
				entry = dictionary[k]
			elif k == dict_size:
				entry = w + w[0]
			else:
				raise Exception("Bad compressed k: {0}".format(k))
			result+= entry
			dictionary[dict_size] = w + entry[0]
			dict_size += 1
			w = entry
		return bytearray([ord(t) for t in result])
