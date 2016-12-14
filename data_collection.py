import ctypes

frame = controller.frame()

serialized_tuple = frame.serialize
serialized_data = serialized_tuple[0]
serialized_length = serialized_tuple[1]
data_address = serialized_data.cast().__long__()
buffer = (ctypes.c_ubyte * serialized_length).from_address(data_address)
with open(os.path.realpath('frame.data'), 'wb') as data_file:
    data_file.write(buffer)