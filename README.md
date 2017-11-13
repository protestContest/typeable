# Typeable

This is a simple script to generate a number of random words to be used as a password, [XKCD style](https://www.xkcd.com/936/). This script, however, restricts itself to words that are easy to type on a QWERTY keyboard.

Currently a word's "typeability" is determined by the distance it takes to move fingers between rows, plus a penalty for not switching hands between characters. It's based on the algorithm described [here](https://colemak.com/Compare).

## Usage

```
usage: Generates easy-to-type passphrases from words given in STDIN
       [-h] [-w NUMWORDS] [-d MAXDIFFICULTY] [-n NUMRESULTS] [-t TEST]
       [--dump]

optional arguments:
  -h, --help        show this help message and exit
  -w NUMWORDS       number of words per passphrase
  -d MAXDIFFICULTY  maximum typing difficulty
  -n NUMRESULTS     number of passphrases to generate
  -t TEST           print typeability of a single word instead of generating
                    passphrases
  --dump            dump words and their scores instead of generating
                    passphrases
```

## Future Work

- Improve distance function, ideally from empirically determined data
- Adjust penalties for reusing the same hand or finger between characters, ideally from empirically determined data
- Allow easy swapping of keyboard layouts
