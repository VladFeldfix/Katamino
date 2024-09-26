class Blocks:
    def __init__(self):
        # 01 Navy
        self.Navy = {}
        self.Navy['Name'] = "01_Navy"
        self.Navy[0] = ((0,0),(0,1),(0,2),(0,3),(0,4))
        self.Navy[1] = ((0,0),(1,0),(2,0),(3,0),(4,0))
        
        # 02 Orange
        self.Orange = {}
        self.Orange['Name'] = "02_Orange"
        self.Orange[0] = ((0,0),(0,1),(1,0),(2,0),(3,0))
        self.Orange[1] = ((0,0),(0,1),(0,2),(0,3),(1,3))
        self.Orange[2] = ((0,1),(1,1),(2,1),(3,0),(3,1))
        self.Orange[3] = ((0,0),(1,0),(1,1),(1,2),(1,3))
        self.Orange[4] = ((0,0),(0,1),(1,1),(2,1),(3,1))
        self.Orange[5] = ((0,0),(0,1),(0,2),(0,3),(1,0))
        self.Orange[6] = ((0,0),(1,0),(2,0),(3,0),(3,1))
        self.Orange[7] = ((0,3),(1,0),(1,1),(1,2),(1,3))

        # 03 Brown
        self.Brown = {}
        self.Brown['Name'] = "03_Brown"
        self.Brown[0] = ((0,1),(1,0),(1,1),(1,2),(1,3))
        self.Brown[1] = ((0,0),(1,0),(1,1),(2,0),(3,0))
        self.Brown[2] = ((0,0),(0,1),(0,2),(0,3),(1,2))
        self.Brown[3] = ((0,1),(1,1),(2,0),(2,1),(3,1))
        self.Brown[4] = ((0,2),(1,0),(1,1),(1,2),(1,3))
        self.Brown[5] = ((0,1),(1,0),(1,1),(2,1),(3,1))
        self.Brown[6] = ((0,0),(0,1),(0,2),(0,3),(1,1))
        self.Brown[7] = ((0,0),(1,0),(2,0),(2,1),(3,0))

        # 04 Purple
        self.Purple = {}
        self.Purple['Name'] = "04_Purple"
        self.Purple[0] = ((0,0),(0,1),(0,2),(1,2),(1,3))
        self.Purple[1] = ((0,1),(1,1),(2,0),(2,1),(3,0))
        self.Purple[2] = ((0,0),(0,1),(1,1),(1,2),(1,3))
        self.Purple[3] = ((0,1),(1,0),(1,1),(2,0),(3,0))
        self.Purple[4] = ((0,1),(0,2),(0,3),(1,0),(1,1))
        self.Purple[5] = ((0,0),(1,0),(2,0),(2,1),(3,1))
        self.Purple[6] = ((0,2),(0,3),(1,0),(1,1),(1,2))
        self.Purple[7] = ((0,0),(1,0),(1,1),(2,1),(3,1))

        # 05 Ocean
        self.Ocean = {}
        self.Ocean['Name'] = "05_Ocean"
        self.Ocean[0] = ((0,0),(0,1),(0,2),(1,2),(2,2))
        self.Ocean[1] = ((0,2),(1,2),(2,0),(2,1),(2,2))
        self.Ocean[2] = ((0,0),(1,0),(2,0),(2,1),(2,2))
        self.Ocean[3] = ((0,0),(0,1),(0,2),(1,0),(2,0))

        # 06 Pink
        self.Pink = {}
        self.Pink['Name'] = "06_Pink"
        self.Pink[0] = ((0,1),(0,2),(1,0),(1,1),(1,2))
        self.Pink[1] = ((0,0),(0,1),(1,0),(1,1),(2,1))
        self.Pink[2] = ((0,0),(0,1),(0,2),(1,0),(1,1))
        self.Pink[3] = ((0,0),(1,0),(1,1),(2,0),(2,1))
        self.Pink[4] = ((0,0),(0,1),(1,0),(1,1),(1,2))
        self.Pink[5] = ((0,0),(0,1),(1,0),(1,1),(2,0))
        self.Pink[6] = ((0,0),(0,1),(0,2),(1,1),(1,2))
        self.Pink[7] = ((0,1),(1,0),(1,1),(2,0),(2,1))

        # 07 Yellow
        self.Yellow = {}
        self.Yellow['Name'] = "07_Yellow"
        self.Yellow[0] = ((0,0),(0,1),(0,2),(1,0),(1,2))
        self.Yellow[1] = ((0,0),(0,1),(1,1),(2,0),(2,1))
        self.Yellow[2] = ((0,0),(0,2),(1,0),(1,1),(1,2))
        self.Yellow[3] = ((0,0),(0,1),(1,0),(2,0),(2,1))

        # 08 Blue
        self.Blue = {}
        self.Blue['Name'] = "08_Blue"
        self.Blue[0] = ((0,0),(0,1),(1,1),(2,1),(2,2))
        self.Blue[1] = ((0,2),(1,0),(1,1),(1,2),(2,0))
        self.Blue[2] = ((0,1),(0,2),(1,1),(2,0),(2,1))
        self.Blue[3] = ((0,0),(1,0),(1,1),(1,2),(2,2))

        # 09 Grey
        self.Grey = {}
        self.Grey['Name'] = "09_Grey"
        self.Grey[0] = ((0,1),(1,0),(1,1),(2,1),(2,2))
        self.Grey[1] = ((0,1),(1,0),(1,1),(1,2),(2,0))
        self.Grey[2] = ((0,0),(0,1),(1,1),(1,2),(2,1))
        self.Grey[3] = ((0,2),(1,0),(1,1),(1,2),(2,1))
        self.Grey[4] = ((0,1),(1,1),(1,2),(2,0),(2,1))
        self.Grey[5] = ((0,1),(1,0),(1,1),(1,2),(2,2))
        self.Grey[6] = ((0,1),(0,2),(1,0),(1,1),(2,1))
        self.Grey[7] = ((0,0),(1,0),(1,1),(1,2),(2,1))

        # 10 Green
        self.Green = {}
        self.Green['Name'] = "10_Green"
        self.Green[0] = ((0,0),(0,1),(0,2),(1,1),(2,1))
        self.Green[1] = ((0,2),(1,0),(1,1),(1,2),(2,2))
        self.Green[2] = ((0,1),(1,1),(2,0),(2,1),(2,2))
        self.Green[3] = ((0,0),(1,0),(1,1),(1,2),(2,0))

        # 11 Olive
        self.Olive = {}
        self.Olive['Name'] = "11_Olive"
        self.Olive[0] = ((0,2),(1,1),(1,2),(2,0),(2,1))
        self.Olive[1] = ((0,0),(1,0),(1,1),(2,1),(2,2))
        self.Olive[2] = ((0,1),(0,2),(1,0),(1,1),(2,0))
        self.Olive[3] = ((0,0),(0,1),(1,1),(1,2),(2,2))

        # 12 Red
        self.Red = {}
        self.Red['Name'] = "12_Red"
        self.Red[0] = ((0,1),(1,0),(1,1),(1,2),(2,1))

        # all
        self.activation_list = {}
        self.activation_list["01_Navy"] = self.Navy
        self.activation_list["02_Orange"] = self.Orange
        self.activation_list["03_Brown"] = self.Brown
        self.activation_list["04_Purple"] = self.Purple
        self.activation_list["05_Ocean"] = self.Ocean
        self.activation_list["06_Pink"] = self.Pink
        self.activation_list["07_Yellow"] = self.Yellow
        self.activation_list["08_Blue"] = self.Blue
        self.activation_list["09_Grey"] = self.Grey
        self.activation_list["10_Green"] = self.Green
        self.activation_list["11_Olive"] = self.Olive
        self.activation_list["12_Red"] = self.Red