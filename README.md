# SSC (Sam's Song Compressor)

Python script that automagically compresses textual data and outputs a Python script that prints the input data. Originally written in December 2017 for a codegolfing exercise.

The algorithm used is (loosely) based on [LZ77](https://en.wikipedia.org/wiki/LZ77_and_LZ78). In simple terms, it finds repeated substrings in the input data and, for every repetition but the first, stores only a reference as a pair of integers—how many characters to go back, and how many to copy.

## License

[ISC License](https://choosealicense.com/licenses/isc/)

## Usage

    python ssc.py input.txt output.py
    # or, to test compression ratio
    python test.py ssc.py

## Decompressor

The decompressor was originally written in December 2017 and has been revised many times since. It was 195 bytes, 16 lines in the original version and has been golfed down to 108 bytes, 3 lines:

```python
z="int(f'%s',2)"%(2*'{ord(d.pop())-32:06b}')
while d:*d,c=d;s+=eval('c#'*(c<'~')+f's[-{z}:][:{z}]')
print(s)
```
## Z-Coding

SSC uses a mechanism I call Z-Coding to store the integers used by the decompression algorithm within the compressed data string. This is desirable, as splitting the string and integer components of the compressed data would cost precious bytes—bad for what is fundamentally a code-golfing exercise. (also, as it happens, the output of the z-coding procedure is shorter than a decimal encoding)

The algorithm is as follows:
 1. Convert the integer into a 12-digit binary representation. (456 → 000111001000)
 2. Split that into two 6-digit binary numbers. (000111, 001000)
 3. Add 32. This ensures that the resulting characters will be printable—no escape sequences necessary. (100111, 101000)
 4. Convert to ASCII. (" **'(** ")

This mechanism encodes any integer between 0 and 4095 into exactly two printable ASCII characters, suitable for embedding in a longer string.

(it's called Z-Coding as the function in the original decompressor that reversed the process was called ```z```)

