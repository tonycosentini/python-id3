import logging
import argparse
from id3_reader import ID3Reader

def main():
	parser = argparse.ArgumentParser(description='Reads an ID3 tag and prints out frame information.')
	parser.add_argument("mp3_file", help="path to MP3 file to parse")
	args = parser.parse_args()

	f = open(args.mp3_file)
	tag = ID3Reader.create_tag_with_file_socket(f)

	print(tag)

if __name__ == "__main__":
	main()