#!/usr/bin/env python3

import sys, argparse, random

class Hand:
  Right, Left = range(2)

class Finger:
  def __init__(self, keys, home_key, hand):
    self.keys = keys
    self.home_key = home_key
    self.hand = hand
    self.position = home_key

  def has_key(self, key):
    return key in self.keys

  def move(self, key):
    self.position = key

  def reset(self):
    self.position = self.home_key

def get_finger(fingers, c):
  for finger in fingers:
    if finger.has_key(c):
      return finger

  raise Exception("Finger not found for " + c)

def get_row(key):
  if key in list('`1234567890-=~!@#$%^&*()_+'):
    return 3
  elif key in list('qwertyuiop[]'):
    return 2
  elif key in list('asdfghjkl;\''):
    return 1
  elif key in list('zxcvbnm,./'):
    return 0

def key_dist(c1, c2):
  return abs(get_row(c1) - get_row(c2))

def typeability(str):
  score = 0
  prevFinger = None
  fingers = create_fingers()
  penalty = 0

  for char in str:
    c = char.lower()
    finger = get_finger(fingers, c)

    if finger == prevFinger:
      # same finger moves to new key
      score += key_dist(finger.position, c)
    else:
      if prevFinger != None:
        if prevFinger.hand == finger.hand:
          # same hand penalty
          penalty += 1

        # prev finger moves back to home row
        score += key_dist(prevFinger.position, prevFinger.home_key)
        prevFinger.reset()

      # new finger moves to new key
      score += key_dist(finger.home_key, c)
      finger.move(c)
      prevFinger = finger

  return score / len(str) + penalty

def create_fingers():
  LeftPinky = Finger(list('qaz'), 'a', Hand.Left)
  LeftRing = Finger(list('wsx'), 's', Hand.Left)
  LeftMiddle = Finger(list('edc'), 'd', Hand.Left)
  LeftIndex = Finger(list('rfvtgb'), 'f', Hand.Left)
  RightIndex = Finger(list('yhnujm'), 'j', Hand.Right)
  RightMiddle = Finger(list('ik,'), 'k', Hand.Right)
  RightRing = Finger(list('ol.'), 'l', Hand.Right)
  RightPinky = Finger(list('p;/[\']\\-'), ';', Hand.Right)
  return [LeftPinky, LeftRing, LeftMiddle, LeftIndex, RightIndex, RightMiddle, RightRing, RightPinky]

def generate_words(scores, difficulty, numWords):
  n = 0
  words = []

  useableWords = {k: v for k, v in scores.items() if v <= difficulty}

  for i in range(numWords):
    words.append(random.choice(list(useableWords.keys())))

  return words


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-w', dest='numWords', type=int, default=5, help='number of words per passphrase')
  parser.add_argument('-d', dest='maxDifficulty', type=int, default=10, help='maximum typing difficulty')
  parser.add_argument('-n', dest='numResults', type=int, default=5, help='number of passphrases to generate')
  parser.add_argument('--dump', dest='dump', help='dump words and their scores instead of generating passphrases', action='store_true')

  args = parser.parse_args()

  scores = dict()
  for line in sys.stdin:
    word = line.strip().lower()
    scores[word] = typeability(word)

  if args.dump:
    # sortedWords =
    for w in sorted(scores.items(), key=lambda x:x[1]):
      print(str(round(w[1], 2)) + '\t' + w[0])
    sys.exit()

  for i in range(args.numResults):
    words = generate_words(scores, args.maxDifficulty, args.numWords)
    print(' '.join(words))
