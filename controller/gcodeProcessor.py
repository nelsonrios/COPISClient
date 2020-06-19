import time

class GcodeProcessor(object):
    def __init__(self, parent):
        super(GcodeProcessor, self).__init__()
        self.parent = parent
        self.visualizer = None
        self.isAbsoluteMode = True


    def processCommand(self, cmd):
        if not self.visualizer:
            self.visualizer = self.parent.visualizer_panel

        cmd_ls = cmd.split()
        gcode = cmd_ls[0]
        params = cmd_ls[1:]
        if gcode in ["G0", "G1"]:
            self.processG0(params)
        elif gcode == "G2":
            self.processG2(params)
        elif gcode == "G3":
            pass
        elif gcode == "G4":
            self.processG4(params)
        elif gcode == "G90":
            self.isAbsoluteMode = True
        elif gcode == "G91":
            self.isAbsoluteMode = False
        else:
            self.parent.console_panel.print(gcode + " is not defined.")

        self.visualizer.canvas.OnDraw()
        #self.parent.serial_controller.sendCommand(cmd)

        
    def processG0(self, params):
        # G0 C[cam_id] X[mm] Y[mm] Z[mm] T[dd] P[dd]
        cam_id = 1
        i = 0

        if "C" in params[0]:
            cam_id = int(params[0][1:])
            i = 1
        cam = self.visualizer.getCamById(cam_id - 1)

        for p in params[i:]:
            if not self.isAbsoluteMode:
                cam.onMove(Axis(p[0].lower()), float(p[1:]))
            else:
                coord = p[0].lower()
                val = float(p[1:])

                if coord == "x":
                    cam.x = val
                elif coord == "y":
                    cam.y = val
                elif coord == "z":
                    cam.z = val
                elif coord == "p":
                    cam.p = val
                elif coord == "t":
                    cam.t = val
        


    def processG2(self, params):
        pass


    def processG4(self, params):
        total_sec = 0
        for p in params:
            if p[0].lower() == "s":
                total_sec += float(p[1:])
            elif p[0].lower() == "p":
                total_sec += float(p[1:]) * 0.001

        time.sleep(total_sec)