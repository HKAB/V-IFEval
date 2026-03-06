# coding=utf-8
# Copyright 2024 The Google Research Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Utility library of instructions."""

import functools
import json
import random
import re
from typing import List
import unicodedata

import nltk
from underthesea import sent_tokenize, word_tokenize

nltk.download('punkt_tab')

# WORD_LIST = ["occidental", "phrase", "signal", "château", "tache", "opposé", "bas", "pomme de terre", "administration", "étoile"]  # pylint: disable=line-too-long
WORD_LIST = [
    "chứng minh", "thành kiến", "tín hiệu", "lâu đài", "đối lập", "thấp", "khoai tây",  "hành chính", "ngôi sao", "huyền thoại"
]  # pylint: disable=line-too-long

# To test forbidden words, we choose common Vietnamese words.
FORBIDDEN_WORDS_LIST = [
    "và", "là", "của", "có", "cho", "một", "trong", "những", "được", "để"
]

# Starter words list (For easier check, only check single-word starters)
STARTER_WORDS_LIST = [
    "Mực", "Kiến", "Hẵng", "Mắc", "Lục", "Bắc", "Danh", "Lóng", "Choáng"
]

def split_into_sentences(text):
    """Split the text into sentences.

    Args:
      text: A string that consists of more than or equal to one sentences.

    Returns:
      A list of strings where each string is a sentence.
    """
    sentences = sent_tokenize(text)
    return sentences


def count_words(text):
  """Counts the number of words.
  
  ChatGPT and Qwen3 has very different definition of what is a word in Vietnamese.
  For ChatGPT, a Vietnamese word is separated by space (Not really true though).
  For Qwen3, a Vietnamese word is more like a tokenized unit (~underthesea word tokenization).
  We are testing Qwen3, so we use underthesea word tokenization.

  """
  # tokenizer = nltk.tokenize.RegexpTokenizer(r"\w+")
  tokens = word_tokenize(text)
  num_words = len(tokens)
  return num_words

def split_into_words(text):
  """Splits the text into words."""
  # tokenizer = nltk.tokenize.RegexpTokenizer(r"\w+")
  # remove all punctuations from text
  text = re.sub(r'[^\w\sáàảãạăắằẳẵặâấầẩẫậđéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ]', '', text)
  tokens = word_tokenize(text)
  if len(tokens) == 0:
    return [""]
  return tokens

def count_sentences(text):
  """Count the number of sentences using underthesea."""
  return len(sent_tokenize(text))

def generate_exisitence_keywords(num_keywords):
  """Randomly generates a few keywords."""
  return random.sample(WORD_LIST, k=num_keywords)

def generate_forbidden_keywords(num_keywords):
  """Randomly generates a few keywords."""
  return random.sample(FORBIDDEN_WORDS_LIST, k=num_keywords)

def generate_started_keywords(num_keywords):
  """Randomly generates a few keywords."""
  return random.sample(STARTER_WORDS_LIST, k=num_keywords)


def remove_accents(text):
    """
    Remove accents from the input string.

    Args:
        text (str): The input string with accents.

    Returns:
        (str): The input string with accents removed.
    """
    nfkd_form = unicodedata.normalize('NFKD', text)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])