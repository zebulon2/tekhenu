import random
import enum

class Owner(enum.Enum):
    none = 0
    player = 1
    bot = 9


class Building:
    def __init__(self, owner):
        self.owner = Owner(owner)


class Pillar(Building):
    def __init__(self, owner):
        super().__init__(owner)

    def __str__(self):
        if self.owner == Owner.none:
            return '0'
        elif self.owner == Owner.bot:
            return 'p'
        elif self.owner == Owner.player:
            return 'P'


class House(Building):
    def __init__(self, owner):
        super().__init__(owner)

    def __str__(self):
        if self.owner == Owner.none:
            return '0'
        elif self.owner == Owner.bot:
            return 'h'
        elif self.owner == Owner.player:
            return 'H'


class HouseRow:
    def __init__(self):
        self.house = []
        for x in range(5):
            self.house.append(House(Owner.none))

    def __str__(self):
        st = ''
        for house in self.house:
            st += str(house) + ' '
        return st

    def get(self, idx):
        return self.house[idx]

    def set(self, idx, owner):
        self.house[idx] = House(owner)


class Grid:
    def __init__(self):
        self.tile = [[Pillar(Owner.none) for x in range(5)] for y in range(5)]
        self.score = [[0 for x in range(5)] for y in range(5)]
        self.score_init_set()

    def __str__(self):
        st = ''
        for row in range(5):
            for col in range(5):
                if self.get_tile(row, col).owner != Owner.none:
                    st = st + str(self.get_tile(row, col)) + ' '
                else:
                    st = st + str(self.get_score(row, col)) + ' '
            st = st + '\n'
        return str(self.tile)

    def get_tile(self, row, col):
        return self.tile[row][col]

    def get_score(self, row, col):
        return self.score[row][col]

    def set_tile(self, row, col, owner):
        self.tile[row][col] = Pillar(owner)

    def score_init_set(self):
        for x in range(5):
            for y in range(5):
                self.score[x][y] = 0
        self.score[0][0] = 2
        self.score[0][1] = 1
        self.score[0][2] = 1
        self.score[0][3] = 1
        self.score[0][4] = 2
        self.score[1][0] = 1
        self.score[2][0] = 1
        self.score[3][0] = 1
        self.score[4][0] = 2
        self.score[4][1] = 1
        self.score[4][2] = 1
        self.score[4][3] = 1
        self.score[4][4] = 2
        self.score[1][4] = 1
        self.score[2][4] = 1
        self.score[3][4] = 1


class Temple:
    def __init__(self):
        self.hsrow_h = HouseRow()
        self.hsrow_v = HouseRow()
        self.grid = Grid()

    def __str__(self):
        st = ''
        for row in range(5):
            st = st + str(self.hsrow_v.get(row)) + '  '
            for col in range(5):
                if self.get_tile(row, col).owner != Owner.none:
                    st = st + str(self.get_tile(row, col)) + ' '
                else:
                    st = st + str(self.get_score(row, col)) + ' '
            st = st + '\n'
        st = st + '   '
        for col in range(5):
            st = st + str(self.hsrow_h.get(col)) + ' '
        return st

    def get_house_v(self, idx):
        return self.hsrow_v.get(idx)

    def get_house_h(self, idx):
        return self.hsrow_h.get(idx)

    def get_tile(self, x, y):
        return self.grid.get_tile(x, y)

    def set_tile(self, x, y, owner):
        self.grid.set_tile(x, y, owner)
        self.recalc_scores()
        return

    def get_score(self, x, y):
        return self.grid.get_score(x, y)

    def set_house_v(self, idx, owner):
        self.hsrow_v.set(idx, owner)
        self.recalc_scores()
        return

    def set_house_h(self, idx, owner):
        self.hsrow_h.set(idx, owner)
        self.recalc_scores()
        return

    def recalc_scores(self):
        self.grid.score_init_set()
        for x in range(5):
            for y in range(5):
                # add 1 if house in row or col unless pillar
                if self.get_tile(x, y).owner != Owner.none:
                    continue

                else:
                    if self.get_house_v(x).owner != Owner.none:
                        self.grid.score[x][y] = self.grid.score[x][y] + 1
                    if self.get_house_h(y).owner != Owner.none:
                        self.grid.score[x][y] = self.grid.score[x][y] + 1

                    # add 1 if pillar north south east west
                    if (x - 1) > -1 and self.get_tile(x - 1, y).owner != Owner.none:  # north
                        self.grid.score[x][y] = self.grid.score[x][y] + 1
                    if (y - 1) > -1 and self.get_tile(x, y - 1).owner != Owner.none:  # west
                        self.grid.score[x][y] = self.grid.score[x][y] + 1
                    if (y + 1) < 5 and self.get_tile(x, y + 1).owner != Owner.none:  # south
                        self.grid.score[x][y] = self.grid.score[x][y] + 1
                    if (x + 1) < 5 and self.get_tile(x + 1, y).owner != Owner.none:  # east
                        self.grid.score[x][y] = self.grid.score[x][y] + 1
        return

    def choose_place(self):
        # make a list of places with max score
        possibles = []
        max_score = 0
        msg = ''
        for x in range(5):
            for y in range(5):
                score = self.grid.score[x][y]
                if score >= max_score:
                    max_score = score
        for x in range(5):
            for y in range(5):
                score = self.grid.score[x][y]
                if score == max_score:
                    possibles.append((x, y))
        msg = msg + 'Max score: ' + str(max_score) + '\n'
        msg = msg + '\n'
        msg = msg + str(len(possibles)) + ' place(s) with max score: ' + possibles.__str__() + '\n'
        if len(possibles) == 1:
            msg = msg + 'Only one possible place in ' + possibles.__str__() + '\n'
            return (msg, possibles[0])

        # look at places with owned pillar
        possibles_owned = []
        for possible in possibles:
            x = possible[0]
            y = possible[1]
            if self.get_house_v(x).owner == Owner.bot or self.get_house_h(y).owner == Owner.bot:
                possibles_owned.append(possible)
        msg = msg + '\n'
        msg = msg + '1st tie: ' + str(
            len(possibles_owned)) + ' place(s) with at least 1 owned house: ' + possibles_owned.__str__() + '\n'
        if len(possibles_owned) == 1:
            msg = msg + 'Only one possible place with at least 1 owned house in ' + possibles_owned[0].__str__() + '\n'
            return (msg, possibles_owned[0])
        else:
            if not (possibles_owned):
                msg = msg + 'No place with at least 1 owned house, look at 2nd tie break rule' + '\n'
                possibles_owned = possibles.copy()
            else:
                msg = msg + 'Several possible choices left, look at 2nd tie break rule' + '\n'

        # if tie, look at places away from the edges
        possibles_away = []
        for possible in possibles_owned:
            # print(possible)
            x = possible[0]
            y = possible[1]
            # print(x, ' ',y)
            if x != 0 and x != 4 and y != 0 and y != 4:
                possibles_away.append(possible)

        msg = msg + '\n'
        msg = msg + '2nd tie: ' + str(
            len(possibles_away)) + ' place(s) away from edges: ' + possibles_away.__str__() + '\n'
        if len(possibles_away) == 1:
            msg = msg + 'Only one possible place away from edges in ' + possibles_away[0].__str__() + '\n'
            return (msg, possibles_away[0])
        elif not (possibles_away):
            msg = msg + 'No place away from edges, choose random in ' + possibles_owned.__str__() + '\n\n'
            rc = random.choice(possibles_owned)
            msg = msg + 'I propose ' + rc.__str__() + '\n'
            return (msg, rc)
        else:
            msg = msg + 'Several possible choices left, choose random in ' + possibles_away.__str__() + '\n\n'
            rc = random.choice(possibles_away)
            msg = msg + 'I propose ' + rc.__str__() + '\n'
            return (msg, rc)
        # print(possibles_owned)

if __name__ == '__main__':
    t = Temple()
    print(t)
    print()
    t.set_tile(2, 3, Owner.bot)
    t.set_tile(0, 1, Owner.player)
    print(t)
    print()
    t.set_house_v(2, Owner.player)
    print(t)
    print()
    t.set_house_h(1, Owner.bot)
    print(t)
    print()
    t.set_tile(3, 1, Owner.bot)
    print(t)
    print()
    print(t.choose_place()[0])
