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

"""Registry of all instructions."""
from instructions import vi_instructions

_KEYWORD = "keywords:"

_LANGUAGE = "language:"

_LENGTH = "length_constraints:"

_CONTENT = "detectable_content:"

_FORMAT = "detectable_format:"

_MULTITURN = "multi-turn:"

_COMBINATION = "combination:"

_STARTEND = "startend:"

_CHANGE_CASES = "change_case:"

_PUNCTUATION = "punctuation:"

_LETTERS = "letters:"

_SPECIAL_CHARACTER = "special_character:"

VI_INSTRUCTION_DICT = {
    _KEYWORD + "existence": vi_instructions.KeywordChecker,
    _KEYWORD + "frequency": vi_instructions.KeywordFrequencyChecker,
    _KEYWORD + "forbidden_words": vi_instructions.ForbiddenWords,
    _KEYWORD + "letter_frequency": vi_instructions.LetterFrequencyChecker,
    _LENGTH + "number_sentences": vi_instructions.NumberOfSentences, #ok
    _LENGTH + "number_paragraphs": vi_instructions.ParagraphChecker,
    _LENGTH + "number_words": vi_instructions.NumberOfWords,
    _LENGTH + "nth_paragraph_first_word": vi_instructions.ParagraphFirstWordCheck,
    _CONTENT + "number_placeholders": vi_instructions.PlaceholderChecker, #ok
    _CONTENT + "postscript": vi_instructions.PostscriptChecker,
    _FORMAT + "number_bullet_lists": vi_instructions.BulletListChecker, #ok
    _FORMAT + "constrained_response": vi_instructions.ConstrainedResponseChecker, #ok
    _FORMAT + "number_highlighted_sections": (
        vi_instructions.HighlightSectionChecker), #ok
    _FORMAT + "multiple_sections": vi_instructions.SectionChecker, #ok 
    _FORMAT + "json_format": vi_instructions.JsonFormat,
    _FORMAT + "title": vi_instructions.TitleChecker,
    _COMBINATION + "two_responses": vi_instructions.TwoResponsesChecker,
    _COMBINATION + "repeat_prompt": vi_instructions.RepeatPromptThenAnswer,
    _STARTEND + "end_checker": vi_instructions.EndChecker,
    _CHANGE_CASES
    + "capital_word_frequency": vi_instructions.CapitalWordFrequencyChecker,
    _PUNCTUATION + "no_comma": vi_instructions.CommaChecker,
    _STARTEND + "quotation": vi_instructions.QuotationChecker,
    # Vietnamese addition
    _SPECIAL_CHARACTER + "forbidden_char": vi_instructions.ForbiddenChar,
    _SPECIAL_CHARACTER + "no_tones": vi_instructions.NoTones,
    _CONTENT + "no_digits": vi_instructions.NumbersInWords,
}

INSTRUCTION_DICT = {}
INSTRUCTION_DICT.update({"vi:" + k: v for k, v in VI_INSTRUCTION_DICT.items()})