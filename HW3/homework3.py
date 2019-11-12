from collections import defaultdict

with open('input3.txt', 'r') as f:
    line = f.readline()
    arr = [0]
    while line:
        arr.append(line.replace('\n', ''))
        line = f.readline()

no_of_queries    = int(arr[1])
no_of_kb_clauses = int(arr[2 + no_of_queries])

queries          = arr[2: 2+no_of_queries]
knowledge_base   = arr[2+no_of_queries+1:]

# print("------")
# print(arr)
# print("------")
# print(no_of_queries, "-", queries)
print("--- KB before ---")
print("# of sentences - ",no_of_kb_clauses)
for i in knowledge_base:
    print(i)

def remove_implication(m_clause):
    if " => " in m_clause:
        m_clause_split = m_clause.split(" => ")
        m_clause_premise = m_clause_split[0]
        m_clause_conclusion = m_clause_split[1]

        premise_split = m_clause_premise.split(" & ")

        for idx, i in enumerate(premise_split):
            if i[0] == "~":
                premise_split[idx] = i[1:]
            else:
                premise_split[idx] = "~"+i

        m_clause_premise = " | ".join(premise_split)
        m_clause = m_clause_premise + " | " + m_clause_conclusion
        return m_clause
    else:
        return m_clause

def remove_implication_tester():
    clause = "~Take(x,Warfarin) & Take(x,Timolol) => Alert(x,VitE)"
    clause = "~Take(x,Warfarin)"
    clause = "Take(x,Timolol) => Alert(x,VitE)"
    print("Before - " + clause)
    clause = remove_implication(clause)
    print("After - " + clause)

# remove_implication_tester()

print("--- KB after ---")
knowledge_base = list(map(remove_implication, knowledge_base))
for i in knowledge_base:
    print(i)


KB = defaultdict(lambda: defaultdict(dict))

class Sentence:
    def __init__(self, raw_sentence, predicates, variables, constants):
        self.raw_sentence = raw_sentence
        self.predicates = predicates
        self.variables = variables
        self.constants = constants

    def __str__(self):
        return f"{self.raw_sentence} \n{self.predicates} \n{self.variables} \n{self.constants}"
    
    # def __repr__(self):
    #     return f"{self.raw_sentence}"

def parse_sentence(m_sentence):
    # sentence must be in CNF, else it wont work
    parsed_data = {
        'predicates' : set(),
        'variables' : set(),
        'constants' : set(),
        'negative_predicates': set()
    }
    predicates = parsed_data['predicates']
    variables = parsed_data['variables']
    constants = parsed_data['constants']
    negative_predicates = parsed_data['negative_predicates']

    atomic_sentences = m_sentence.split(' | ')

    for atomic in atomic_sentences:
        curr = atomic if atomic[0] != "~" else atomic[1:]

        # TODO 
        # negative predicate checking
        brace_start_idx = curr.find("(")
        brace_end_idx = curr.find(")")

        predicate = curr[:brace_start_idx]
        if atomic[0] != "~":
            predicates.add(predicate)
        else:
            negative_predicates.add(predicate)

        arguments = curr[brace_start_idx+1:brace_end_idx]
        arguments = arguments.split(',')

        for arg in arguments:
            if arg.islower():
                variables.add(arg)
            else:
                constants.add(arg)
    return parsed_data

def parse_sentence_tester():

    sent = "~Take(x,Warfarin) | ~Take(x,Timolol) | Alert(x,VitE) | ~Alert(Raj, Kay)"
    data = parse_sentence(sent)
    obj_sentence = Sentence(sent, data['predicates'], data['variables'], data['constants'] )
    for i in data['predicates']:
        KB[i].setdefault('positive', []).append(obj_sentence)
    for i in data['negative_predicates']:
        KB[i].setdefault('negative', []).append(obj_sentence)
    # print(obj_sentence)

parse_sentence_tester()

print(KB)

