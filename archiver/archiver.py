#!/usr/bin/env python

import os
import sys
import optparse
import hafman
import lzw

def parse_options():
	parser = optparse.OptionParser(usage='archivaor.py [options]')
	parser.add_option('-a', '--archive', dest='archive', help='compress metod', metavar='FILE', default= 'hafman')
	parser.add_option('-m', '--method', dest='method', help='compress or decompress', metavar='FILE', default = 'decode')
	parser.add_option('-f', '--file', dest='file', help='road to file to compress', metavar='FILE')
	parser.add_option('-o', '--output', dest='output', help='road to output file', metavar='FILE')
	return parser.parse_args()

def main():
	(options, args ) = parse_options()
	fh = None
	try:
		fh = open(options.file, "rb")
		data = fh.read()
		ar = hafman.Hafman(data) if options.archive == "hafman" else lzw.LZW(data)

		rh = open(options.output, "wb")
		rh.write(ar.encode() if options.method == "code" else ar.decode())
	finally:
		if fh != None:
			fh.close()
	return 0

if __name__=="__main__":
	try:
		sys.exit(main())
	except KeyboardInterrupt:
		print('inerrupted by user')
	sys.exit(1)
