from huffman import HuffmanCode
import sys

path = "sampletext.txt"

h_text = HuffmanCode(path)

output_path = h_text.compressor()
print("File path of compressed file: " + output_path)

decompressed_path = h_text.decompressor(output_path)
print("File path of decompressed file: " + decompressed_path)