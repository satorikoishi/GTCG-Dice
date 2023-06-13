# GTCG-DICE

Emulate Genshin TCG (Genius Invokation) dice toss, analyze probability

Assumption: 8 dices, toss twice

Arg1: elem combination, split by ','

Arg2: additional omni elems

## Usage

If you want Elem 5

```bash
python3 toss.py 5
```

If you want Elem 3+3

```bash
python3 toss.py 3,3
```

If you want Elem 5+3, with additional 2 omni elems

```bash
python3 toss.py 5,3 2
```