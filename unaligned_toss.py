#!/usr/bin/python3
from toss import *

IDX_OMNI = 0
IDX_EFFECTIVE = 1
IDX_UNALIGNED = 2
IDX_FIRST_TUNE = 3
IDX_SECOND_TUNE = 4
IDX_METHOD = 5

def first_toss_stat(dices, needs):
    highest_unaligned, _ = dice_highest_unaligned(dices, needs)
    return dices[ELEM_OMNI], dices[0], highest_unaligned

def test_unaligned_toss(needs, unaligned_need, results, method=None):
    for _ in range(TEST_COUNT):
        dices = init_dices(0)
        toss(dices, INIT_DICE_COUNT)
        first_tune = dice_tune_check(dices, needs, unaligned_need)
        omni_count, effective_count, unaligned_count = first_toss_stat(dices, needs)
        # print(f'First toss dice: {dices}, tune {first_tune}, stats {omni_count}, {effective_count}, {unaligned_count}')
        
        if not method:
            conditional_toss(dices, needs)
        elif method == 'u':
            conditional_toss_keep_unaligned(dices, needs, unaligned_need)
        second_tune = dice_tune_check(dices, needs, unaligned_need)
        # print(f'Second toss dice: {dices}, tune {second_tune}')
        
        results.append([omni_count, effective_count, unaligned_count, first_tune, second_tune, method])
    
def analyze_unaligned_toss(results, method=None):
    # Overall
    overall_result = [x for x in results if x[IDX_METHOD] == method]
    
    first_tune_sum = 0
    second_tune_sum = 0
    worse_count = 0
    for res in overall_result:
        first_tune_sum += res[IDX_FIRST_TUNE]
        second_tune_sum += res[IDX_SECOND_TUNE]
        if res[IDX_FIRST_TUNE] < res[IDX_SECOND_TUNE]:
            worse_count += 1
    print(f'Method: {method}, First tune: {first_tune_sum / TEST_COUNT}, Second tune: {second_tune_sum / TEST_COUNT}, Worse: {worse_count / TEST_COUNT}')
    
    # TODO: Different Cases

if __name__ == '__main__':
    for need in [[3], [5]]:
        for unaligned_need in [2, 3]:
            print(f'Need: {need[0]}, Unaligned: {unaligned_need}')
            results = []
            for method in [None, 'u']:
                test_unaligned_toss(need, unaligned_need, results, method)
            for method in [None, 'u']:
                analyze_unaligned_toss(results, method)
            print('---------------------------------------------------------------------------------------------------')
            