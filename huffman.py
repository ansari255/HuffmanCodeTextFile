import os
import heapq

class HuffmanCode:
	def __init__(self, path):
		self.path = path
		self.heap = []
		self.code = {}
		self.map_reverse = {}

	class Branch:
		def __init__(self, char, occur):
			self.char = char
			self.occur = occur
			self.right = None
			self.left = None

		def __lt__(self, new):
			return self.occur < new.occur

		def __eq__(self, new):
			if(new == None):
				return False
			if(not isinstance(new, Branch)):
				return False
			return self.occur == new.occur

	#Compression functions:

	def occurence_dictionary(self, text):
		occurence = {}
		for character in text:
			if not character in occurence:
				occurence[character] = 0
			occurence[character] += 1
		return occurence

	def heap_maker(self, occurence):
		for key in occurence:
			node = self.Branch(key, occurence[key])
			heapq.heappush(self.heap, node)

	def branch_merging(self):
		while(len(self.heap)>1):
			branch1 = heapq.heappop(self.heap)
			branch2 = heapq.heappop(self.heap)
			merge = self.Branch(None, branch1.occur + branch2.occur)
			merge.left = branch1
			merge.right = branch2
			heapq.heappush(self.heap, merge)

	def coding_helper(self, node, code_instance):
		if(node == None):
			return

		if(node.char != None):
			self.code[node.char] = code_instance
			self.map_reverse[code_instance] = node.char
			return

		self.coding_helper(node.left, code_instance + "0")
		self.coding_helper(node.right, code_instance + "1")

	def code_maker(self):
		node = heapq.heappop(self.heap)
		code_instance = ""
		self.coding_helper(node, code_instance)

	def text_encoder(self, text):
		encoded_text = ""
		for character in text:
			encoded_text += self.code[character]
		return encoded_text

	def encoded_text_padder(self, encoded_text):
		padding = 8 - len(encoded_text) % 8
		for i in range(padding):
			encoded_text += "0"

		padding_info = "{0:08b}".format(padding)
		encoded_text = padding_info + encoded_text
		return encoded_text

	def byte_array(self, encoded_text_padded):
		if(len(encoded_text_padded) % 8 != 0):
			print("The encoded text is not padded properly")
			exit(0)

		b = bytearray()
		for i in range(0, len(encoded_text_padded), 8):
			byte = encoded_text_padded[i:i+8]
			b.append(int(byte, 2))
		return b

	def compressor(self):
		f_name, f_ext = os.path.splitext(self.path)
		output_path = f_name + ".bin"

		with open(self.path, 'r+') as file, open(output_path, 'wb') as output:
			text = file.read()
			text = text.rstrip()

			occurence = self.occurence_dictionary(text)
			self.heap_maker(occurence)
			self.branch_merging()
			self.code_maker()

			encoded_text = self.text_encoder(text)
			encoded_text_padded = self.encoded_text_padder(encoded_text)

			b = self.byte_array(encoded_text_padded)
			output.write(bytes(b))

		print("Compressed")
		return output_path
    
    #Decompression functions:

	def padding_remover(self, encoded_text_padded):
		padding_info = encoded_text_padded[:8]
		padding = int(padding_info, 2)

		encoded_text_padded = encoded_text_padded[8:] 
		encoded_text = encoded_text_padded[:-1*padding]
		return encoded_text

	def text_decoder(self, encoded_text):
		code_instance = ""
		decoded_text = ""

		for bit in encoded_text:
			code_instance += bit
			if(code_instance in self.map_reverse):
				character = self.map_reverse[code_instance]
				decoded_text += character
				code_instance = ""
		return decoded_text

	def decompressor(self, input_path):
		f_name, f_ext = os.path.splitext(self.path)
		output_path = f_name + "_retrieved" + ".txt"

		with open(input_path, 'rb') as file, open(output_path, 'w') as output:
			bit_string = ""
			byte = file.read(1)
			while(len(byte) > 0):
				byte = ord(byte)
				bits = bin(byte)[2:].rjust(8, '0')
				bit_string += bits
				byte = file.read(1)

			encoded_text = self.padding_remover(bit_string)
			decompressed_text = self.text_decoder(encoded_text)
			output.write(decompressed_text)

		print("Decompressed")
		return output_path

