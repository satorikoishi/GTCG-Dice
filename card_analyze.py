#!/usr/bin/python3
import sys
from toss import *

valid_card = ['toss_up', 'tenshukaku', 'tsg']

def avg(lst):
    return sum(lst) / len(lst)

def analyze_toss_up(dice_count, needs):
    test(needs, 0, dice_count)

def analyze_tenshukaku(num_tsg, num_elem, init_omni=0, method='a'):
    total_summary = []
    effective_summary = []
    for _ in range(TEST_COUNT):
        if method == 'a':
            dices = toss_aggresive(num_elem, init_omni)
        else:
            dices = toss_conservative(num_elem, init_omni)
        
        dice_type = dice_type_count(dices)
        # Tenshukaku triggered
        if dice_type >= 5:
            dices[ELEM_OMNI] += num_tsg
        # Count total & effective
        total = sum(dices)
        assert total == INIT_DICE_COUNT + init_omni or total == INIT_DICE_COUNT + init_omni + num_tsg, f'Dices: {dices}, total {total}, init_omni {init_omni}, num_tsg {num_tsg}'
        total_summary.append(total)
        effective_summary.append(dice_effective_count(dices, num_elem))
    
    if method == 'a':
        print(f'Aggresive: Tenshukaku {num_tsg}, Effective elem type {num_elem}, Init omni {init_omni}, Average total {avg(total_summary)}, Effective total {avg(effective_summary)}')
    else:
        print(f'Conservative: Tenshukaku {num_tsg}, Effective elem type {num_elem}, Init omni {init_omni}, Average total {avg(total_summary)}, Effective total {avg(effective_summary)}')
    
if __name__ == '__main__':
    card = sys.argv[1].lower()
    
    if card not in valid_card:
        print(f'Not valid card, available: {valid_card}')
        exit(1)
    
    # Toss-Up
    if card == 'toss_up':
        dice_count = int(sys.argv[2])
        needs = [int(x) for x in sys.argv[3].split(',')]
    
        print(f'Toss_up, with {dice_count} dices, needs: {needs}, run {TEST_COUNT} times')
        analyze_toss_up(dice_count, needs)
        
    # Tenshukaku
    if card == 'tenshukaku' or card == 'tsg':
        for num_tsg in [0, 1, 2]:
            for num_elem in [1, 2]:
                for init_omni in [0, 1, 2]:
                    for method in ['a', 'c']:
                        analyze_tenshukaku(num_tsg, num_elem, init_omni, method=method)
                    print('---------------------------------------------------------------------------------------------------')