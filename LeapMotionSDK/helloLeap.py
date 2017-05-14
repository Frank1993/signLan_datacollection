import Leap
import sys
import ctypes,numpy
import matplotlib

from PIL import Image
class SampleListener(Leap.Listener):

    def on_connect(self, controller):
        print "Connected"


    def on_frame(self, controller):
        #print "Frame available"
        frame = controller.frame()
        print frame.images.is_empty
        if not frame.images.is_empty:
            #print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
          #frame.id, frame.timestamp, len(frame.hands), len(frame.fingers))
            image = frame.images[0]
            image_buffer_ptr = image.data_pointer
            ctype_array_def = ctypes.c_ubyte * image.width * image.height

            # as ctypes array
            as_ctype_array = ctype_array_def.from_address(int(image_buffer_ptr))
            # as numpy array
            as_numpy_array = numpy.ctypeslib.as_array(as_ctype_array)

            im = Image.fromarray(as_numpy_array)
            im.save("%s.jpeg"%frame.id)


def main():
    # Create a sample listener and controller
    listener = SampleListener()
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
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()
