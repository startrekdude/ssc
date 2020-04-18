from __future__ import division

from hashlib import sha256
from os import listdir, mkdir
from os.path import basename, getsize, join, splitext
from subprocess import call, check_output
from sys import argv as args, exit

def _hash(o):
	return sha256(o.encode("ascii")).hexdigest()

def avg(a):
	return sum(a)/len(a)
	
def test_all(program):
	scores = []
	i = 1
	for song in listdir("songs"):
		song = join("songs", song)
		name = splitext(basename(song))[0]
		output = "_gen\\%s.py" % name
		
		print( "Case %s: %s" % (i, name) )
		print( "[!] %s %s %s" % (program, song, output) )
		call(["python", program, song, output])
		result = check_output(["python", output]).decode("ascii").replace("\r\n", "\n")[:-1] # print adds an extra newline
		with open(song) as f:
			expect = f.read()
		result, expect = _hash(result), _hash(expect)
		print( "%s -> %s" % (expect, result) )
		if result != expect:
			print( "FAILURE!" )
			break
		score = (getsize(output) / getsize(song)) * 100
		print( "Score: %s\n" % score )
		scores.append(score)
		
		i += 1
	
	print( "Final Score: %s" % avg(scores) )

def main():
	if len(args) < 2:
		print( "Usage: test <prog.py>" )
		exit(-1)
	program = args[1]
	test_all(program)

if __name__ == "__main__":
	main()