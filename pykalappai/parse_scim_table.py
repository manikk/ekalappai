__author__ = 'manikk'
class ScimTableParser:
    start = False
    scimMappings = {}
    def parse(self, fileName):
        f = open(fileName,encoding="utf-8")
        for line in f:
            str = line.strip().encode("utf-8").decode()
            if str == "BEGIN_TABLE":
                self.start = True
                continue

            if self.start == True and str != "END_TABLE":
                mapping = str.split(" ")
                self.scimMappings[mapping[0]] = mapping[-1]

            if str == "END_TABLE":
                self.start = False

        f.close()
        return  self.scimMappings

