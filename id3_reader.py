import logging
import argparse
import struct
import settings
from id3 import ID3Tag

def read_header_string_into_new_tag(id3_header_string):
	if id3_header_string[0:3] != 'ID3':
		logging.error('fart.') # Read up on Pythonic error handling.
		return

	file_identifier, major_version, minor_version, flag = struct.unpack('>3sBBB', id3_header_string)
	return ID3Tag(major_version, minor_version, flag)

def create_tag_with_file_socket(file_socket):
	file_socket.seek(settings.ID3_HEADER_START_LOCATION	,0)
	tag = read_header_string_into_new_tag(file_socket.read(settings.ID3_HEADER_LENGTH))
	read_frames_into_tag(file_socket, tag)
	return tag

def convert_synch_safe_array_into_number(raw_synchsafe_data):
	return_value = 0

	for index, raw_synchsafe in enumerate(raw_synchsafe_data):
		bit_offset = ((len(raw_synchsafe_data) - 1) - index) * 7
		return_value += raw_synchsafe << bit_offset

	return return_value

def read_frames_into_tag(file_socket, tag):
	file_socket.seek(settings.ID3_FRAMES_START_LOCATION, 0)

	frames_body_size = convert_synch_safe_array_into_number(struct.unpack('BBBB', file_socket.read(4)))

	logging.info("Frames body size: %d" % frames_body_size)

	current_position = settings.ID3_FRAMES_START_LOCATION + 4 # TODO: determine this dynamically

	while file_socket.tell() < frames_body_size:
		read_frame_into_tag(file_socket, tag)

def read_frame_into_tag(file_socket, tag):
	framesize = None
	if tag.major_version == 2:
		frame_id = struct.unpack('>3s', file_socket.read(3))
		raw_size = struct.unpack('BBB', file_socket.read(3))
		framesize = convert_synch_safe_array_into_number(raw_size)
	elif tag.major_version == 3 or tag.major_version == 4:
		frame_id = struct.unpack('>4s', file_socket.read(4))
		framesize = struct.unpack('>I', file_socket.read(4))[0]

		# Throw out flags for now.
		file_socket.read(2)

	if framesize > 0:
		logging.info("ID: %s Framesize: %s" % (frame_id, framesize))

	data = file_socket.read(framesize)

	if framesize > 0:
		tag.frames[frame_id] = data
		if len(data) < 100:
			logging.info("Frame data: %s" % data)

def main():
	logging.getLogger().setLevel(logging.DEBUG)

	parser = argparse.ArgumentParser(description='Reads an ID3 tag and prints out frame information.')
	parser.add_argument("mp3_file", help="path to MP3 file to parse")
	args = parser.parse_args()

	f = open(args.mp3_file)
	tag = create_tag_with_file_socket(f)

	print(tag)

if __name__ == "__main__":
	main()