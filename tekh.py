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
    print()
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


def add_house(bld, npos, pl):
    bld[npos - 1] = pl
    return


def add_pil(tpl, nx, ny):
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
    print('Max score:', max_score)
    print(len(possibles), 'place(s) with max score:', possibles)
    if len(possibles) == 1:
        print('Only one possible place in', possibles)
        return

    # look at places with owned pillar
    possibles_owned = []
    for possible in possibles:
        x = possible[0]
        y = possible[1]
        if bldv[x] == 9 or bldh[y] == 9:  # 9 is the owned for Bot
            possibles_owned.append(possible)
    print()
    print('1st tie:',len(possibles_owned),'place(s) with at least 1 owned house:', possibles_owned)
    if len(possibles_owned) == 1:
        print('Only one possible place with at least 1 owned house in', possibles_owned)
        return
    else:
        if not(possibles_owned):
            print('No place with at least 1 owned house, look at 2nd tie break rule')
            possibles_owned = possibles.copy()
        else:
            print('Several possible choices left, look at 2nd tie break rule')

    # if tie, look at places away from the edges
    possibles_away = []
    for possible in possibles_owned:
        # print(possible)
        x = possible[0]
        y = possible[1]
        # print(x, ' ',y)
        if x != 0 and x != 4 and y != 0 and y != 4:
            possibles_away.append(possible)

    print()
    print('2nd tie:',len(possibles_away),'place(s) away from edges:', possibles_away)
    if len(possibles_away) == 1:
        print('Only one possible place away from edges in', possibles_away)
        return
    elif not(possibles_away):
        print('No place away from edges, choose random in', possibles_owned)
        print('I propose ', random.choice(possibles_owned))
    else:
        print('Several possible choices left, choose random in', possibles_away)
        print('I propose ', random.choice(possibles_away))
    # print(possibles_owned)


tpl = np.zeros((5, 5), dtype=np.int8)
bldv = np.zeros(5, dtype=np.int8)
bldh = np.zeros(5, dtype=np.int8)


set_base_scores(tpl)
# print(tpl_base)
display_all(tpl, bldv, bldh, True)

# add_house(bldv, 1, 0)
# add_house(bldv, 2, 1)  # 9 is the owned for Bot
# add_house(bldh, 1, 9)
# #add_house(bldh, 2, 1)
# add_house(bldh, 3, 1)
# add_pil(tpl, 2, 3)
# # add_pil(tpl, 3, 2)
# add_pil(tpl, 3, 3)
# add_pil(tpl, 2, 4)
# add_pil(tpl, 1, 2)
# display_all(tpl, bldv, bldh, True)

# # Example with all ties, several choices
# add_pil(tpl, 5, 5)
# add_pil(tpl, 4, 5)
# add_house(bldh, 4, 9)
# add_pil(tpl, 5, 1)
# add_pil(tpl, 3, 4)
# add_pil(tpl, 2, 4)
# add_pil(tpl, 2, 2)
# add_pil(tpl, 1, 1)
# add_pil(tpl, 4, 1)
# add_house(bldh, 3, 9)

add_pil(tpl, 1, 1)
add_pil(tpl, 5, 1)
add_house(bldh, 1, 9)
add_house(bldh, 2, 1)
add_pil(tpl, 3, 2)
add_house(bldh, 3, 9)
add_house(bldv, 3, 1)
add_pil(tpl, 3, 4)

update_scores(tpl, bldv, bldh)
display_all(tpl, bldv, bldh, True)

choose_place(tpl, bldv, bldh)
