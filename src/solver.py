
def filter_words(words,feedback):
    correct_pos = {}
    present=[]
    absent=[]

    for i,(letter,evaluation) in enumerate(feedback):
        if evaluation == "correct":
            correct_pos[i] = letter
        elif evaluation =="present":
            present.append((i,letter))
        elif evaluation =="absent":
            absent.append(letter)

    protected = set(correct_pos.values()) | {letter for _,letter in present}

    new_words = []
    for word in words:
        if is_valid(word,correct_pos,present,absent,protected):
            new_words.append(word)

    return new_words

def is_valid(word,correct_pos,present,absent,protected):
    for i,letter in correct_pos.items():
        if word[i]!= letter:
            return False
    for i,letter in present:
        if letter not in word:
            return False
        if word[i]==letter:
            return False
        
    for letter in absent:
        if letter not in protected and letter in word:
            return False
    
    return True

def best_guess(words,used):
    freq={}
    for w in words:
        for letter in set(w):
            freq[letter] = freq.get(letter,0)+1

    best_word = None
    best_score = -1

    for w in words:

        if w in used:
            continue
        
        score=sum(freq[letter] for letter in set(w))
        if score > best_score:
            best_score = score
            best_word = w
        
    return best_word