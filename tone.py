#This might have been better off being a class.

import random 
import re

from tone_words import *


# (min_score, max_score, label) (where bounds meet, the more negative score is chosen)
sentiment_ranges = [
    (-1.0, -0.1, "negative"),
    (-0.1, -0.02, "melancholic"),
    (-0.02, 0.03, "neutral"),
    (0.03, 0.14, "hopeful"),
    (0.14, 1.0, "positive")
]

positive_sentiment = ["hopeful", "positive"]
negative_sentiment = ["melancholic", "negative"]


def get_sentiment_label(score, ranges=sentiment_ranges):
    for min_val, max_val, label in ranges:
        if min_val <= score <= max_val:
            return label
        
symbol = "Neural Network"
house = "category"
tone = "neutral"

#second sentence must have some prediction in it. let us say there are some base templates
neutral_templates = ["Expect {} in your future.",
             "There are {} nearing you.",
             "You will be visited by {}.",
             "Only {} await you.",
             "You may find {} ahead.",
             "Be not afraid of the {} ahead.",
             "Your omen comes in the form of {}.",
             "There will be {}.",
             "Your path is lined with {}.",
             "Try to understand the {}.",
             "Some {} are in your future."]

negative_templates = ["Visions of {} will follow you.",
                      "Be wary of the {}.",
                      "Watch carefully of the {}.",
                      "Be warned of the {}.",
                      "There will be {} that haunt you.",
                      "You will be befallen by the {}.",
                      "Evil {} are in your future."]

positive_templates = ["Your luck will lead you to {}.",
                      "Prosperity and {} will visit you.",
                      "Your path will be plentifully lined with {}.",
                      "You will be rewarded with {}.",
                      "Gifts of {} await you.",
                      "Golden {} are in your future."]

def get_symbol(prop_nouns):
    prop_nouns = [x for x in prop_nouns if len(x) > 2] #filter for only symbols above 2 characters
    if len(prop_nouns) == 0:
        return "King of Knights" #default
    index = random.randint(0, len(prop_nouns)-1)
    return prop_nouns[index].title()


def get_house(categories):
    meta_keywords = [
        "articles", "pages", "wikipedia", "stub", "short description",
        "coordinates", "infobox", "template", "use dmy", "use mdy",
        "all articles", "commons", "dead external links", "official website",
        "redirects", "containing", "Cs1"
    ]
    
    filtered = []
    for cat in categories:
        cat_lower = cat.lower()
        # remove meta keywords
        if any(mk in cat_lower for mk in meta_keywords):
            continue
        # remove purely numeric/date categories
        if re.match(r"^\d{3,4}.*", cat):
            continue
        # remove categories with too generic words (optional)
        if any(word in cat_lower for word in ["list", "links", "cs1"]):
            continue
        filtered.append(cat)
    
    if len(filtered) == 0:
        return "Mirrors" #default in case no good category
    else:
        index = random.randint(0, len(filtered)-1)
        return filtered[index].title()


def get_tone_word(tone):
    tone_mapping = {
    "neutral": neutral,
    "hopeful": hopeful,
    "positive": positive,
    "melancholic": melancholic,
    "negative": negative
    }

    words = tone_mapping[tone]
    return random.choice(words)


def get_omen_sentence(tone, nouns):
    sentence = ""
    filler = get_sentence_filler(nouns)
    if tone in positive_sentiment:
        index = random.randint(0, len(positive_templates)-1)
        sentence = positive_templates[index]
    elif tone in negative_sentiment:
        index = random.randint(0, len(negative_templates)-1)
        sentence = negative_templates[index]
    else:
        index = random.randint(0, len(neutral_templates)-1)
        sentence = neutral_templates[index]

    return sentence.format(filler)


def get_sentence_filler(sing_nouns):
    if len(sing_nouns) == 0:
        return "infinite paths"
    sing_nouns = [x for x in sing_nouns if x != "links"] #appears a lot, is useless
    index = random.randint(0, len(sing_nouns)-1)
    return sing_nouns[index].lower()

def get_omen(tone_score, prop_nouns, sing_nouns, categories):
    sentiment = get_sentiment_label(tone_score)

    symbol = get_symbol(prop_nouns)

    house = get_house(categories)

    tone = get_tone_word(sentiment)

    sentence = get_omen_sentence(sentiment, sing_nouns)

    omen = f"You have drawn {symbol} from the house of {house}, a sign of {tone}. {sentence}"

    return omen


