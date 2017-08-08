import numpy

from sh import ffmpeg
from io import BytesIO

from PIL import Image



class Video(object):

    def __init__(self, file):

        super(Video, self).__init__()

        self.file = file

    def done(self, *args):
        """
        Callback once ffmpeg is done reading the frame.
        """
        print("Frame read.")
        frame = self.out.getvalue()
        frame = numpy.fromstring(frame, dtype='uint8')
        frame.shape = (1080, 1440, 3)
        self.frame = Image.fromarray(frame)

    def readFrame(self):
        """
        Async command to read frames.
        Returns an object that can block execution using .wait() on it.
        """
        self.out = BytesIO()
        return ffmpeg(
            "-i",
            self.file,
            "-frames:v",
            "1",
            "-f",
            "image2pipe",
            '-pix_fmt',
            'rgb24',
            '-vcodec',
            'rawvideo',
            '-',
            _out=self.out,
            _done=self.done,
            _bg=True)


if __name__ == '__main__':
    fp = 'assets/videos/poyz/Poyz_DV_0024.mov'
    v = Video(fp)
    a = v.readFrame()

    print( "a is Async so you can do stuff while ffmpeg reads the frame")
    print( "Add a.wait() when you need to access data outputed from the command.")

    a.wait()
    im = v.frame.show()
