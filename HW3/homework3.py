from collections import defaultdict, namedtuple

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
    # clause = "~Take(x,Warfarin)"
    # clause = "Take(x,Timolol) => Alert(x,VitE)"
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
    def __init__(self, raw_sentence, positive_predicates, negative_predicates, variables, constants, list_of_literals):
        self.raw_sentence = raw_sentence
        self.positive_predicates = positive_predicates
        self.negative_predicates = negative_predicates
        self.variables = variables
        self.constants = constants

        self.list_of_literals = list_of_literals



    def __str__(self):
        return f"{self.raw_sentence} \n{self.positive_predicates} \n{self.negative_predicates} \n{self.variables} \n{self.constants} \n{self.list_of_literals}"
    
    # def __repr__(self):
    #     return f"{self.raw_sentence}"
Literal = namedtuple("Literal", ["name", "is_false", "args"])

def parse_sentence(m_sentence):
    # sentence must be in CNF, else it wont work
    parsed_data = {
        'positive_predicates' : set(),
        'variables' : set(),
        'constants' : set(),
        'negative_predicates': set(),
        'list_of_literals': []
    }
    positive_predicates = parsed_data['positive_predicates']
    variables = parsed_data['variables']
    constants = parsed_data['constants']
    negative_predicates = parsed_data['negative_predicates']
    list_of_literals = parsed_data['list_of_literals']

    atomic_sentences = m_sentence.split(' | ')

    for atomic in atomic_sentences:
        curr = atomic if atomic[0] != "~" else atomic[1:]
        is_false = None
        # TODO 
        # negative predicate checking
        brace_start_idx = curr.find("(")
        brace_end_idx = curr.find(")")

        predicate = curr[:brace_start_idx]
        
        if atomic[0] != "~":
            is_false = False
            positive_predicates.add(predicate)
        else:
            is_false = True
            negative_predicates.add(predicate)

        arguments = curr[brace_start_idx+1:brace_end_idx]

        
        
        arguments = arguments.split(',')
        single_literal = Literal(predicate, is_false, arguments)
        list_of_literals.append(single_literal)

        for arg in arguments:
            if arg.islower():
                variables.add(arg)
            else:
                constants.add(arg)
        # raw_sentence = 
        print(variables)
    return parsed_data

def parse_sentence_tester():

    # sent = "~Take(x,Warfarin) | ~Take(x,Timolol) | Alert(x,VitE) | ~Alert(y, VitD)"
    sent = "~Take(x,Warfarin) | ~Take(x,Timolol) | Alert(x,VitE)"
    data = parse_sentence(sent)
    obj_sentence = Sentence(sent, data['positive_predicates'], data['negative_predicates'], data['variables'], data['constants'], data['list_of_literals'])
    for i in data['positive_predicates']:
        KB[i].setdefault('positive', []).append(obj_sentence)
    for i in data['negative_predicates']:
        KB[i].setdefault('negative', []).append(obj_sentence)
    print("Obj sent---")
    print(obj_sentence)

    sent1 = "~Alert(Alice,VitE)"
    data = parse_sentence(sent1)
    obj_sentence1 = Sentence(sent1, data['positive_predicates'], data['negative_predicates'], data['variables'], data['constants'], data['list_of_literals'])
    for i in data['positive_predicates']:
        KB[i].setdefault('positive', []).append(obj_sentence1)
    for i in data['negative_predicates']:
        KB[i].setdefault('negative', []).append(obj_sentence1)
    print("Obj sent 1---")
    print(obj_sentence1)

    print("---->><<----")

    theta = {}
    for item1 in obj_sentence1.list_of_literals:
        for item2 in obj_sentence.list_of_literals:
            if item1.name == item2.name and item1.is_false != item2.is_false:
                for i1, i2 in zip(item1.args, item2.args):
                    if (i1[0].isupper() and i2[0].isupper()) and (i1 != i2):
                        theta = {}
                        break
                    elif (i1[0].isupper() and not i2[0].isupper()):
                        theta = {i2: i1}
                    elif (not i1[0].isupper() and i2[0].isupper()):
                        theta = {i1: i2}
                    else:
                        #TODO
                        # can variables be unified?
                        pass
    
    print(theta)
    sent_new = sent[:]
    for i, j in theta.items():
        print(i, j)
        sent_new = sent_new.replace(i, j)
    print(sent_new)

parse_sentence_tester()

# print(KB)

