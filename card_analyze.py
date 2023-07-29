#!/usr/bin/python3
import sys
from toss import *

valid_card = ['toss_up']

def analyze_toss_up(dice_count, needs):
    test(needs, 0, dice_count)

if __name__ == '__main__':
    card = sys.argv[1].lower()
    
    if card not in valid_card:
        print(f'Not valid card, available: {valid_card}')
        exit(1)
    
    # toss_up
    if card == 'toss_up':
        dice_count = int(sys.argv[2])
        needs = [int(x) for x in sys.argv[3].split(',')]
    
        print(f'Toss_up, with {dice_count} dices, needs: {needs}, run {TOSS_COUNT} times')
        analyze_toss_up(dice_count, needs)