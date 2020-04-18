from sys import argv as args, exit

def compress(d):
	def to_two(n):
		b = bin(n).replace("0b","").zfill(12)
		return chr(int(b[:6], 2)+32) + chr(int(b[6:], 2)+32)
	def enc(b, l):
		return "~" + to_two(b) + to_two(l)
	
	s = ""
	i = 0
	while i < len(d):
		c = False
		for j in reversed(range(6, min(len(d)-i, 4095))):
			n = d[i:i+j]
			h = d[max(i-4095,0):i]
			if n in h:
				b = len(h)-h.index(n)
				l = len(n)
				
				s += enc(b, l)
				i += l
				c = True
				break
		if not c:
			s += d[i]
			i += 1
	return s

DECOMPRESSOR = """
z="int(f'REPLACEs',2)"REPLACE(2*'{ord(d.pop())-32:06b}')
while d:*d,c=d;s+=eval('c#'*(c<'~')+f's[-{z}:][:{z}]')
print(s)"""
	
def create_decompressor(d):
	return (('*d,s="""%s"""'+DECOMPRESSOR) % (d[::-1])).replace("REPLACE", "%")
	
def main():
	if len(args) < 3:
		print("Usage: ssc <file.txt> <out.py>")
		exit(-1)
	name = args[1]
	result = args[2]
	with open(name, errors="ignore") as f:
		data = f.read()
	c = compress(data)
	with open(result, "wb") as f:
		f.write(create_decompressor(c).encode("ascii"))

if __name__ == "__main__":
	main()