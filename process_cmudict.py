#!/usr/bin/python

import json
import random
import re

def main():
  input_file = open("cmudict-0.7b")
  benedicts = []
  cumberbatches = []
  words = []
  for line in input_file:
    if line.startswith(";;;"):
      continue
    (word, phonemes) = line.split("  ")
    word = clean_word(word)
    phonemes = [phoneme.strip() for phoneme in phonemes.split(" ")]
    if is_benedict(phonemes) and not is_inflected(word, words):
      benedicts.append(word)
    if is_cumberbatch(phonemes) and not is_inflected(word, words):
      cumberbatches.append(word)
    words.append(word)
  input_file.close()

  output_file = open("betamaxcrinkledash.json", "w")
  result = {
    "benedict": benedicts,
    "cumberbatch": cumberbatches
  }
  json.dump(result, output_file, indent=2, separators=(",", ": "))
  output_file.close()

  print "random examples:"
  for _ in range(10):
    print "  ", random.choice(benedicts), random.choice(cumberbatches)

def clean_word(word):
  regex = re.compile("[^a-zA-Z]")
  return regex.sub("", word).title()

def is_inflected(word, words):
  if word.endswith("s"):
    if word[:-1] in words:
      return True
  if word.endswith("es"):
    if word[:-2] in words:
      return True
  if word.endswith("d"):
    if word[:-1] in words:
      return True
  if word.endswith("ed"):
    if word[:-2] in words:
      return True
  return word in words

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

def is_plosive(phoneme):
  PLOSIVES = ("B", "D", "G", "K", "P", "T")
  return phoneme in PLOSIVES

def is_fricative(phoneme):
  FRICATIVES = ("F", "V", "DH", "TH", "S", "Z", "SH", "ZH")
  return phoneme in FRICATIVES

def is_affricate(phoneme):
  AFFRICATES = ("CH", "JH")
  return phoneme in AFFRICATES

def is_semivowel(phoneme):
  SEMIVOWELS = ("W", "Y")
  return phoneme in SEMIVOWELS

def is_liquid(phoneme):
  LIQUIDS = ("L", "R")
  return phoneme in LIQUIDS

def is_aspirate(phoneme):
  return phoneme == "HH"

def is_voiceless(phoneme):
  VOICELESS = ("P", "T", "K", "F", "S", "SH", "TH", "CH", "HH")
  return phoneme in VOICELESS

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
    and (
      is_affricate(phonemes[-1])
      or is_plosive(phonemes[-1])
      or (
        is_fricative(phonemes[-1])
        and is_voiceless(phonemes[-1])
      )
    )
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
    and phonemes[0] in ("K", "G")
    and (
      is_affricate(phonemes[-1])
      or vowels[-1] == "AE"
      or (
        is_voiceless(phonemes[-1])
        and (is_plosive(phonemes[-1]) or is_fricative(phonemes[-1]))
      )
      or (
        (is_plosive(phonemes[-1]) or is_fricative(phonemes[-1]) or is_liquid(phonemes[-1]))
        and (is_plosive(phonemes[-2]) or is_fricative(phonemes[-2]))
      )
    )
  )

if __name__ == "__main__":
  main()
