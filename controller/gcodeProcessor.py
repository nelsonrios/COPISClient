

class GcodeProcessor(object):
    def __init__(self, *args, **kwargs):
        super(GcodProcessor, self).__init__(*args, **kwargs)

        self.isAbsoluteMode = True
        self.motionMode = None

    def processCommand(self, cmd):
        pass

    def processG0(self, params):
        # G0 C[cam_id] X[mm] Y[mm] Z[mm] T[dd] P[dd]
        cam = 1

        for p in params:
            if p[0] == "C":
                cam = int(p[1:])