import sys
import random

# Matching 1, Matching 2..., Unaligned, Omni
ELEM_TYPES = 8
ELEM_OMNI = ELEM_TYPES - 1
INIT_DICE_COUNT = 8
TOSS_COUNT = 100000

def unaligned_range(needs):
    return range(len(needs), ELEM_OMNI)

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
    
def first_toss(dices):
    for _ in range(INIT_DICE_COUNT):
        elem = random.randrange(ELEM_TYPES)
        dices[elem] += 1

def conditional_toss(dices, needs):
    retoss_count = 0
    for i in unaligned_range(needs):
        retoss_count += dices[i]
        dices[i] = 0
    
    for _ in range(retoss_count):
        elem = random.randrange(ELEM_TYPES)
        dices[elem] += 1

def test(needs):
    total = 0
    for x in needs:
        total += x
    lacks = [0] * (total + 1)
    
    for i in range(TOSS_COUNT):
        dices = [0] * INIT_DICE_COUNT
        
        first_toss(dices)
        conditional_toss(dices, needs)
        
        lack = dice_analyze(dices, needs)
        lacks[lack] += 1
    
    accum_prob = 0
    expectation = 0
    for idx, x in enumerate(lacks):
        accum_prob += x
        expectation += x * idx / TOSS_COUNT
        print(f'Lack {idx} elems prob: {x / TOSS_COUNT}, accum prob: {accum_prob / TOSS_COUNT}')
    print(f'Expectation: {expectation}')

if __name__ == '__main__':
    needs = [int(x) for x in sys.argv[1].split(',')]
    print(f'Testing with needs: {needs}, run {TOSS_COUNT} times')
    test(needs)
