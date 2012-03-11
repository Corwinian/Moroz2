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
					dictionary[chr(i)] = i
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

		print("ar size - {0}".format(len(compressed)))
		print("first byte - {0}".format(compressed[0]))
		print("second byte - {0}".format(compressed[1]))
		dictionary = {}
		for i in range(256):
			dictionary[i] = [i]
		w = [compressed.pop(0)]
		result = [w[0]] 
		for k in compressed:
			if k in dictionary:
				entry = dictionary[k]
#				print ("in dic")
			elif k == dict_size:
				w.append(w[0])
				entry = w
			else:
				raise Exception("Bad compressed k: {0}".format(k))
#			print (k)
#			print ("dic size {0}".format(dict_size))
			result.extend(entry)
			w.append(entry[0])
		#	print("w - {0}".format(w) )
			dictionary[dict_size] = w
			dict_size += 1

			w = entry
		print("end decompres" )
		print("first byte - {0}".format(result[0]))
		print("second byte - {0}".format(result[1]))
		return bytearray(result)
