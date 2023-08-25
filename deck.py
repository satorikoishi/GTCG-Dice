#!/usr/bin/python3
import random

NUM_CARDS = 30
TEST_COUNT = 100000

def init_deck():
    return [0] * NUM_CARDS

def generate_deck(input_count):
    print(f'Input: {input_count}')
    
    deck = init_deck()
    marker = 1
    offset = 0
    for i in input_count:
        for j in range(i):
            deck[offset] = marker
            offset += 1
        marker += 1
    print(f'Deck: {deck}')
    
    return deck

def satisfy_need(draw_result, need):
    assert len(draw_result) == len(need)
    for i in range(len(draw_result)):
        if draw_result[i] < need[i]:
            return False
    return True

def analyze_deck(input_count, need):
    deck = generate_deck(input_count)
    print(f'Need: {need}')
    
    order_summary = init_deck()
    
    for _ in range(TEST_COUNT):
        random.shuffle(deck)
        draw_result = [0] * len(need)
        for idx, card in enumerate(deck):
            if card == 0:
                continue
            
            # We draw a needed card
            draw_result[card - 1] += 1
            if not satisfy_need(draw_result, need):
                continue
            
            # We draw all needed cards
            order_summary[idx] += 1
            break
    
    accum_prob = 0
    expectation = 0
    for i, x in enumerate(order_summary):
        prob = x / TEST_COUNT
        accum_prob += prob
        expectation += i * prob
        print(f'Card idx {i}, prob: {prob}, accum_prob: {accum_prob}')
    print(f'Expectaion: {expectation}')

if __name__ == '__main__':
    # Standard
    analyze_deck([1], [1])
    # Gambler, Tubby
    analyze_deck([2], [1])
    # Dice
    analyze_deck([2], [2])
    # Weapon + Artifact
    analyze_deck([2,2], [1,1])
    # Liusu + Calx
    analyze_deck([4], [1])
    # 3 Helm
    analyze_deck([4], [3])