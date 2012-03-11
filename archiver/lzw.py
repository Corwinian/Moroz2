class LZW(object):
	"""LZW archivator"""

	bytes = None

	def __init__(self, byteArray):
		self.bytes = byteArray

	def encode (self):
		dict_size = 256
		dictionary = {}
		print("firs bytes {0}".format(self.bytes[0:6]))
		for i in range(256):
			dictionary[i] = i
		w =0 
		result = []

		for c in self.bytes:
			wc = (w << 8) + c
			if dict_size >= 65536: # wenn dictionary über 2**16 Einträge erreicht hat
				dictionary = {} # leeren
				for i in range(256): # neu initialisieren
					dictionary[i] = i
				dict_size = 256
#			if dict_size >= 65536:
#			for i in range(256):
#				dictionary[chr(i)] = i
#			dict_size = 256
			if wc in dictionary:
				w = wc
			else:
				dictionary[wc] = dict_size
				dict_size += 1
				result.append(dictionary[w])
				w = c
		result.append(dictionary[w])
		res = bytearray([])
		for byte in result:
			res.append(byte // 2**8)
			res.append(byte % (2**8))

		return res

	def decode (self):
		dict_size = 256
		byte = 0
		step = 0
		compressed = []

		i =0
		while (i+1 < len(self.bytes)):
			compressed.append((self.bytes[i]<< 8) + self.bytes[i+1])
			i+=2

		print("ar size - {0}".format(len(compressed)))
		print("first byte - {0}".format(compressed[0]))
		print("second byte - {0}".format(compressed[1]))
		dictionary = {}
		for i in range(256):
			dictionary[i] = [i]
		dict_size = 256

		w = [compressed.pop(0)]
		result = [w[0]]
		for k in compressed:
			if len(dictionary) >= 65536:
				dictionary = {}
				for i in range(256):
					dictionary[i] = [i]
				dict_size = 256
			if k in dictionary:
				entry = dictionary[k]
			elif k == dict_size:
				entry = w + [w[0]]
			else:
				raise Exception("Bad compressed k: {0}".format(k))
			result += entry
			dictionary[dict_size] = w + [entry[0]]
			dict_size += 1
			w = entry
		print("firs bytes {0}".format(self.bytes[0:6]))
		print("end decompres" )
		print("first byte - {0}".format(result[0]))
		print("second byte - {0}".format(result[1]))
		return bytearray(result)
