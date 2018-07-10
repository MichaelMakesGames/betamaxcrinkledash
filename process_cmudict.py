#!/usr/bin/python

import json
import random
import re

def main():
  input_file = open("cmudict-0.7b")
  benedicts = []
  cumberbatches = []
  for line in input_file:
    if line.startswith(";;;"):
      continue
    (word, phonemes) = line.split("  ")
    word = clean_word(word)
    phonemes = [phoneme.strip() for phoneme in phonemes.split(" ")]
    if is_benedict(phonemes):
      benedicts.append(word)
    if is_cumberbatch(phonemes):
      cumberbatches.append(word)
  input_file.close()

  output_file = open("betamaxcrinkledash.json", "w")
  result = {
    "benedict": benedicts,
    "cumberbatch": cumberbatches
  }
  json.dump(result, output_file)
  output_file.close()

  print "random examples:"
  for _ in range(10):
    print "  ", random.choice(benedicts), random.choice(cumberbatches)

def clean_word(word):
  regex = re.compile("[^a-zA-Z]")
  return regex.sub("", word).title()

def is_vowel(phoneme):
  VOWELS = (
    "AA", "AE", "AH", "AO", "AW", "AY",
    "EH", "ER", "EY",
    "IH", "IY",
    "OW", "OY",
    "UH", "UW"
  )
  stressless_phoneme = phoneme.strip("012")
  return stressless_phoneme in VOWELS

def get_vowels(phonemes):
  return [phoneme for phoneme in phonemes if is_vowel(phoneme)]

def fits_stress_rhythm(vowels):
  return (
  "1" in vowels[0]
  and "0" in vowels[1]
  and "2" in vowels[2]
  )

def is_benedict(phonemes):
  vowels = get_vowels(phonemes)
  return (
    phonemes[0] in ("B", "P", "V")
    and (not is_vowel(phonemes[-1]))
    and len(vowels) == 3
    and fits_stress_rhythm(vowels)
  )

def is_cumberbatch(phonemes):
  vowels = get_vowels(phonemes)
  return (
    (not is_vowel(phonemes[0]))
    and (not is_vowel(phonemes[-1]))
    and len(vowels) == 3
    and fits_stress_rhythm(vowels)
    and (
      phonemes[0] in ("K", "G")
      or phonemes[-1] in ("CH", "JH")
    )
  )

if __name__ == "__main__":
  main()
