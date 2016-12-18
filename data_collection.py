import Leap
import sys
import ctypes,numpy

from PIL import Image
import struct

class DataPersistentListener(Leap.Listener):
    """
	def __init__(self,serialize_file):
		super.__init__()
		self.serialize_stream = open(serialize_file,'wb')
    """
    def on_connect(self, controller):
        print "Connected"


    def on_frame(self, controller):
        # get a frame
        frame = controller.frame()
        if not frame.images.is_empty:
      		
      		# get the raw data in the frame
          	serialized_tuple = frame.serialize

          	data = serialized_tuple[0]
          	size = serialized_tuple[1]

          	# write the length of the frame data, but we use 4 byte to represent the length with "int"

          	self.serialize_stream.write(struct.pack("i",size))

          	data_address = data.cast().__long__()

          	data_buffer  = (ctypes.c_ubyte * size).from_address(data_address)

          	self.serialize_stream.write(data_buffer)



class Deserialization(object):

    def __init__(self,serialized_stream):
        self.frames = self.deserialize_frame(serialized_stream)

    def deserialize_frame(self,serialized_stream):
        frames = []

        controller = Leap.Controller()
        with open(serialized_stream,"rb") as frame_file:
            next_block_size = frame_file.read(4)

            while  next_block_size:
                size = struct.unpack("i",next_block_size)[0]
                data = frame_file.read(size)
                leap_byte_array = Leap.byte_array(size)

                address = leap_byte_array.cast().__long__()

                ctypes.memmove(address,data,size)

                frame = Leap.Frame()

                frame.deserialize((leap_byte_array,size))
                frames.append(frame)

                next_block_size = frame_file.read(4)
        return frames





def main():
    # Create a sample listener and controller

    listener = DataPersistentListener()
    listener.serialize_stream = open(sys.argv[1],'wb')
    controller = Leap.Controller()
    controller.set_policy(Leap.Controller.POLICY_IMAGES)

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:

        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        listener.serialize_stream.close()
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()
