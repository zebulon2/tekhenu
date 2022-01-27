import numpy as np
import random


def display_all(tpl, bldv, bldh, symbolic=False):
    for x in range(5):
        if symbolic:
            if bldv[x] == 9:
                bldv_c = 'B'
            elif bldv[x] == 0:
                bldv_c = '.'
            else:
                bldv_c = 'P'
        else:
            bldv_c = str(bldv[x])
        print(bldv_c, end='')
        print('  ', end='')
        for y in range(5):
            if symbolic:
                if tpl[x, y] == 9:
                    tpl_c = 'I'
                else:
                    tpl_c = str(tpl[x, y])
            else:
                tpl_c = str(tpl[x, y])
            print(tpl_c + ' ', end='')
        print()
    #print()
    print('   ', end='')
    for y in range(5):
        if symbolic:
            if bldh[y] == 9:
                bldh_c = 'B'
            elif bldh[y] == 0:
                bldh_c = '.'
            else:
                bldh_c = 'P'
        else:
            bldh_c = str(bldh[y])
        print(bldh_c + ' ', end='')
    print()
    print()
    print()


def set_base_scores(tpl):
    for i in range(5):
        for j in range(5):
            tpl[i, j] = 0
    tpl[0, 0] = 2
    tpl[0, 1] = 1
    tpl[0, 2] = 1
    tpl[0, 3] = 1
    tpl[0, 4] = 2
    tpl[1, 0] = 1
    tpl[2, 0] = 1
    tpl[3, 0] = 1
    tpl[4, 0] = 2
    tpl[4, 1] = 1
    tpl[4, 2] = 1
    tpl[4, 3] = 1
    tpl[4, 4] = 2
    tpl[1, 4] = 1
    tpl[2, 4] = 1
    tpl[3, 4] = 1
    tpl[4, 4] = 2


def add_house(bld, pos, pl):
    bld[pos] = pl
    return


def add_pil(tpl, x, y):
    tpl[x, y] = 9
    return


def add_house_natural(bld, npos, pl):
    bld[npos - 1] = pl
    return


def add_pil_natural(tpl, nx, ny):
    x = nx - 1
    y = ny - 1
    tpl[x, y] = 9
    return


def update_scores(tpl, bldv, bldh):
    for x in range(5):
        for y in range(5):

            # add 1 if house in row or col unless pillar
            if tpl[x, y] == 9:
                continue

            else:
                if bldv[x] > 0:
                    tpl[x, y] = tpl[x, y] + 1
                if bldh[y] > 0:
                    tpl[x, y] = tpl[x, y] + 1

                # add 1 if pillar north south east west
                if (x - 1) > -1 and tpl[x - 1, y] == 9:  # north
                    tpl[x, y] = tpl[x, y] + 1
                if (y - 1) > -1 and tpl[x, y - 1] == 9:  # west
                    tpl[x, y] = tpl[x, y] + 1
                if (y + 1) < 5 and tpl[x, y + 1] == 9:  # south
                    tpl[x, y] = tpl[x, y] + 1
                if (x + 1) < 5 and tpl[x + 1, y] == 9:  # east
                    tpl[x, y] = tpl[x, y] + 1

    return


def choose_place(tpl, bldv, bldh):
    # make a list of places with max score
    possibles = []
    max_score = 0
    msg = ''
    for x in range(5):
        for y in range(5):
            score = tpl[x, y]
            if score <= 6 and score >= max_score:  # 6 is maximal score, 9 is for pillars
                max_score = score
    for x in range(5):
        for y in range(5):
            score = tpl[x, y]
            if score == max_score:
                possibles.append((x,y))
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
        if bldv[x] == 9 or bldh[y] == 9:  # 9 is the owned for Bot
            possibles_owned.append(possible)
    msg = msg + '\n'
    msg = msg + '1st tie: ' + str(len(possibles_owned)) + ' place(s) with at least 1 owned house: ' + possibles_owned.__str__() + '\n'
    if len(possibles_owned) == 1:
        msg = msg + 'Only one possible place with at least 1 owned house in ' + possibles_owned[0].__str__() + '\n'
        return (msg, possibles_owned[0])
    else:
        if not(possibles_owned):
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
    msg = msg + '2nd tie: ' + str(len(possibles_away)) + ' place(s) away from edges: ' + possibles_away.__str__() + '\n'
    if len(possibles_away) == 1:
        msg = msg + 'Only one possible place away from edges in ' + possibles_away[0].__str__() + '\n'
        return (msg, possibles_away[0])
    elif not(possibles_away):
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

if __name__ == "__main__":
    tpl = np.zeros((5, 5), dtype=np.int8)
    bldv = np.zeros(5, dtype=np.int8)
    bldh = np.zeros(5, dtype=np.int8)


    set_base_scores(tpl)
    # print(tpl_base)
    display_all(tpl, bldv, bldh, True)
    #
    # # add_house(bldv, 0, 0)
    # # add_house(bldv, 1, 1)  # 9 is the owned for Bot
    # # add_house(bldh, 0, 9)
    # # #add_house(bldh, 1, 1)
    # # add_house(bldh, 2, 1)
    # # add_pil(tpl, 1, 2)
    # # # add_pil(tpl, 2, 1)
    # # add_pil(tpl, 2, 2)
    # # add_pil(tpl, 1, 3)
    # # add_pil(tpl, 0, 1)
    # # display_all(tpl, bldv, bldh, True)
    #
    # # # Example with all ties, several choices
    # # add_pil(tpl, 4, 4)
    # # add_pil(tpl, 3, 4)
    # # add_house(bldh, 3, 9)
    # # add_pil(tpl, 4, 0)
    # # add_pil(tpl, 2, 3)
    # # add_pil(tpl, 1, 3)
    # # add_pil(tpl, 1, 1)
    # # add_pil(tpl, 0, 0)
    # # add_pil(tpl, 3, 0)
    # # add_house(bldh, 2, 9)
    #
    # # add_pil(tpl, 0, 0)
    # # add_pil(tpl, 4, 0)
    # # add_house(bldh, 0, 9)
    # # add_house(bldh, 1, 1)
    # # add_pil(tpl, 1, 1)
    # # add_pil(tpl, 2, 1)
    # # add_house(bldh, 2, 9)
    # # add_house(bldv, 2, 1)
    # # add_pil(tpl, 2, 3)
    #
    # # YT Video Thekenu Solo Variant Board Games Unlocked
    # # add_pil(tpl, 0, 2) # 24:00
    # # add_house(bldh, 4, 9)
    # # add_house(bldv, 0, 1)
    # # add_house(bldh, 0, 9) # 46:00
    # # add_pil(tpl, 0, 4)
    # # add_pil(tpl, 4, 0)
    # # add_pil(tpl, 0, 0) # 49:20
    # # #add_pil(tpl, 0, 0) # 49:30
    #
    # # YT Video Brettspiel Live Tekhenu Solo Variante
    # # add_house(bldv, 0, 9) # 1:49:20
    # # add_house(bldv, 1, 1)
    # # add_house(bldh, 1, 1)
    # # add_pil(tpl, 1, 1) # 1:49:20
    # # add_pil(tpl, 0, 1)
    # # add_house(bldv, 2, 1)
    # # add_pil(tpl, 2, 3) # 2:26:20
    #
    # # YT Video Spielwald Tekhenu Let's play Solo
    #
    # ###
    #
    # add_pil(tpl, 0, 4)
    # add_pil(tpl, 4, 4)
    # add_pil(tpl, 0, 3)
    # add_pil(tpl, 0, 2)
    # add_pil(tpl, 4, 3)
    # add_house(bldv, 0, 9)
    # #add_house(bldv, 1, 1)
    # add_house(bldh, 1, 9)
    # add_pil(tpl, 0, 1)
    # add_house(bldh, 4, 9)
    # add_pil(tpl, 0, 0)
    #
    # update_scores(tpl, bldv, bldh)
    # display_all(tpl, bldv, bldh, True)
    #
    # (msg, pos)=choose_place(tpl, bldv, bldh)
    # print(msg, pos)
