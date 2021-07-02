from decoder import decode_string


class Level:
    def __init__(self,matcher_type):
        self.width = None
        self.height = None
        self.string = None
        self.name = None
        self.tutorial_text = None

        self.cells = []
        self.matcher_type = matcher_type
        self.matcher_rotation = [0,3,2,1]
        self.dictout = {}
        self.dupout = {} #these are for efficienclt with seeking through arrays
        self.rotout = {} #they're just copies of the dictout,
        self.pshout = {} #but with only a specifc cell type
        

    def init_dimensions(self, width, height):
        self.width = width
        self.height = height

        for column in range(width):
            self.cells.append([None] * height)
        return False

    def set_cell(self, c, i):
        # c is cell type index, i is the level position index
        if c >= 72:
            return
        self.cells[i % self.width][i // self.width] = (((c // 2) % 9), [0, 3, 2, 1][c // 18])


    def load_string(self, string):
        self.string = string
        components = self.string.split(";")
        self.cells = []
        self.dictout = {}
        
        if components[0] == "V1":
            self.init_dimensions(int(components[1]), int(components[2]))

            self.tutorial_text = components[5]
            self.name = components[6]

            bg_cells = components[3].split(",")
            cells = components[4].split(",")
            if bg_cells != [""]:
                for bg_cell in bg_cells:
                    contents = [int(c) for c in bg_cell.split(".")]
            if cells != [""]:
                for cell in cells:
                    contents = [int(c) for c in cell.split(".")]
                    #print(contents[1])
                    self.cells[contents[2]][contents[3]] = ((contents[0]), self.matcher_rotation[contents[1]])

        elif components[0] == "V2":

            if self.init_dimensions(decode_string(components[1]), decode_string(components[2]), max_size):
                return False, "Level too big. Max: " + str(max_size) + "x" + str(max_size)

            self.tutorial_text = components[4]
            self.name = components[5]

            data = components[3]

            level_cells = ""
            data_index = 0
            data = components[3]
            while data_index < len(data):
                if data[data_index] == "(" or data[data_index] == ")":
                    if data[data_index] == ")":
                        level_cells += data[data_index - 1] * decode_string(data[data_index + 1])
                        data_index += 2
                    else:
                        cell = data[data_index - 1]
                        distance = ""
                        data_index += 1
                        while data[data_index] != ")":
                            distance += data[data_index]
                            data_index += 1

                        level_cells += cell * decode_string(distance)
                        data_index += 1
                else:
                    level_cells += data[data_index]
                    data_index += 1

            for i in range(len(level_cells)):
                self.set_cell(decode_string(level_cells[i]), i)


        elif components[0] == "V3":

            self.init_dimensions(decode_string(components[1]), decode_string(components[2]))

            self.tutorial_text = components[4]
            self.name = components[5]

            level_cells = ""
            data_index = 0  # iterate through data optimally without re-slicing it every step
            data = components[3]
            while data_index < len(data):
                if data[data_index] == "(" or data[data_index] == ")":
                    if data[data_index] == ")":
                        offset = data[data_index + 1]
                        distance = data[data_index + 2]
                        data_index += 3

                    else:
                        offset = ""
                        data_index += 1
                        while data[data_index] != "(" and data[data_index] != ")":
                            offset += data[data_index]
                            data_index += 1
                        if data[data_index] == ")":
                            distance = data[data_index + 1]
                            data_index += 2
                        else:
                            distance = ""
                            data_index += 1
                            while data[data_index] != ")":
                                distance += data[data_index]
                                data_index += 1
                            data_index += 1


                    for d in range(decode_string(distance)):
                        level_cells += level_cells[-decode_string(offset) - 1]

                else:
                    level_cells += data[data_index]
                    data_index += 1
            #[print(i) for i in self.cells]
            #print()
            for i in range(len(level_cells)):
                self.set_cell(decode_string(level_cells[i]), i)
                
            #[print(i) for i in self.cells]

        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                cur = self.cells[i][j]

                if cur != None:
                    cur = list(cur)
                    cur[0] = self.matcher_type[cur[0]]
                    cur[1] = self.matcher_rotation[cur[1]]
                    tup = (i-(self.width//2),(j-(self.height//2))*-1)
                    self.dictout[tup] = cur
                    if cur[0] == 0:
                        self.dupout[tup] = cur
                    elif cur[0] == 1:
                        self.pshout[tup] = cur
                    elif cur[0] == 2 or cur[0] == 3:
                        self.rotout[tup] = cur
                    
            
        return (self.dictout,(self.dupout,self.rotout,self.pshout),(self.width,self.height))

if __name__=="__main__":
    level = Level()
    print(level.load_string("V3;5;5;{)0a6oGY)da;;"))
