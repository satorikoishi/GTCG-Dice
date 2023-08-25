#!/usr/bin/python3

import sys
import random

# Matching 1, Matching 2..., Unaligned, Omni
ELEM_TYPES = 8
ELEM_OMNI = ELEM_TYPES - 1
INIT_DICE_COUNT = 8
TEST_COUNT = 100000
DICE_COUNT_UPPER_BOUND = 16

def unaligned_range(needs):
    return range(len(needs), ELEM_OMNI)

def init_dices(init_omni=0):
    dices = [0] * INIT_DICE_COUNT
    dices[ELEM_OMNI] += init_omni
    return dices

def dice_type_count(dices):
    count = 0
    for elem in dices:
        if elem:
            count += 1
    if dices[ELEM_OMNI]:
        count += dices[ELEM_OMNI] - 1
    return count

def dice_effective_count(dices, num_elem):
    count = 0
    for i in range(num_elem):
        count += dices[i]
    count += dices[ELEM_OMNI]
    return count

def dice_analyze(dices, needs):
    lack = 0
    for idx, x in enumerate(needs):
        if dices[idx] < x:
            lack += x - dices[idx]

    omni_count = dices[ELEM_OMNI]
    if lack < omni_count:
        lack = 0
    else:
        lack -= omni_count
    
    return lack

def toss(dices, toss_count):
    for _ in range(toss_count):
        elem = random.randrange(ELEM_TYPES)
        dices[elem] += 1

def conditional_toss(dices, needs):
    retoss_count = 0
    
    # print(f'dices after first toss: {dices}')

    # Retoss all unaligned elems
    for i in unaligned_range(needs):
        retoss_count += dices[i]
        dices[i] = 0
    
    # Retoss elems over needs
    for idx, x in enumerate(needs):
        if dices[idx] > x:
            retoss_count += dices[idx] - x
            dices[idx] = x
    
    # print(f'dices before retoss: {dices}, # of retoss: {retoss_count}')
    toss(dices, retoss_count)

# For tenshukaku, Priority: keep 5 types of elems, may retoss effective elems if types not enough
def toss_conservative(num_elem, init_omni=0):
    dices = init_dices(init_omni)
    toss(dices, INIT_DICE_COUNT)
    # print(f'Dice before: {dices}')
    
    retoss_count = 0
    types = dice_type_count(dices)
    if types >= 5:
        # Retoss redundant unaligned elems
        keep_types = 5 - dices[ELEM_OMNI]
        for i in range(num_elem):
            # We have effective dices
            if dices[i]:
                keep_types -= 1
        # Unaligned ones
        for idx, dice in enumerate(dices[num_elem:-1], num_elem):
            if dice:
                if keep_types == 0:
                    # Retoss all
                    retoss_count += dice
                    dices[idx] = 0
                else:
                    # Keep one
                    retoss_count += dice - 1
                    dices[idx] = 1
                    keep_types -= 1
    else:
        # Keep one elem per type
        for idx, dice in enumerate(dices[:-1]):
            if dice:
                retoss_count += dice - 1
                dices[idx] = 1
    # print(f'Dice after: {dices}, retoss count {retoss_count}')
    
    # Retoss
    toss(dices, retoss_count)
    
    return dices

# For tenshukaku
def toss_aggresive(num_elem, init_omni=0):
    dices = init_dices(init_omni)
    toss(dices, INIT_DICE_COUNT)
    needs = []
    for _ in range(num_elem):
        needs.append(DICE_COUNT_UPPER_BOUND)
    conditional_toss(dices, needs)
    return dices

def test(needs, init_omni, dice_count=INIT_DICE_COUNT):
    total = 0
    for x in needs:
        total += x
    lacks = [0] * (total + 1)
    
    for i in range(TEST_COUNT):
        dices = init_dices(init_omni)
        
        toss(dices, dice_count)
        conditional_toss(dices, needs)
        
        lack = dice_analyze(dices, needs)
        lacks[lack] += 1
    
    accum_prob = 0
    expectation = 0
    for idx, x in enumerate(lacks):
        accum_prob += x
        expectation += x * idx / TEST_COUNT
        print(f'Lack {idx} elems prob: {x / TEST_COUNT}, accum prob: {accum_prob / TEST_COUNT}')
    print(f'Expectation: {expectation}')

if __name__ == '__main__':
    needs = [int(x) for x in sys.argv[1].split(',')]
    if len(sys.argv) > 2:
        init_omni = int(sys.argv[2])
    else:
        init_omni = 0
    print(f'Testing with needs: {needs}, run {TEST_COUNT} times')
    test(needs, init_omni)
