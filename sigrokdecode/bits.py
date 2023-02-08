from .output import Output

class BitsOutput(Output):
    name = "bits"
    desc = "ASCII rendering with 0/1"
    def __init__(self, openfile, driver, logic_channels=[], analog_channels=[], *, width="64"):
        self.width = int(width)
        self.logic_channels = logic_channels
        self.samplenum = 0

    def decode(self, startsample, endsample, data):
        ptype = data[0]
        if ptype == "logic":
            values = []
            for b in range(len(self.logic_channels)):
                if data[1] & (1 << b) != 0:
                    values.append("1")
                else:
                    values.append("0")
            for s in range(startsample, endsample):
                if s % self.width == 0:
                    if s > 1:
                        print("\n".join(("".join(l) for l in self.lines)))
                    self.lines = [[c, ":"] for c in self.logic_channels]
                for bit in range(len(self.logic_channels)):
                    self.lines[bit].append(values[bit])
                if s % 8 == 7:
                    for bit in range(len(self.logic_channels)):
                        self.lines[bit].append(" ")
        elif ptype == "analog":
            # print(data)
            pass

    def stop(self):
        print("\n".join(("".join(l) for l in self.lines)))
