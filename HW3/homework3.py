from collections import defaultdict, namedtuple
from itertools import count
import sys

with open('input5.txt', 'r') as f:
    line = f.readline()
    arr = [0]
    while line:
        arr.append(line.replace('\n', ''))
        line = f.readline()

no_of_queries    = int(arr[1])
no_of_kb_clauses = int(arr[2 + no_of_queries])

queries          = arr[2: 2+no_of_queries]
knowledge_base   = arr[2+no_of_queries+1:]
global_variable_counter = count()
max_recursion_depth_limit = sys.getrecursionlimit()

# print("------")
# print(arr)
# print("------")
# print(no_of_queries, "-", queries)

# print("--- KB before ---")
# print("# of sentences - ",no_of_kb_clauses)
# for i in knowledge_base:
#     print(i)

def is_var(m_string):
    return m_string[0].islower()

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

knowledge_base = list(map(remove_implication, knowledge_base))

# print("--- KB after ---")
# for i in knowledge_base:
#     print(i)

KB_list = []
KB = defaultdict(lambda: defaultdict(dict))
class Literal(namedtuple("Literal", ["name", "is_false", "args"])):
    def __str__(self):
        single_l = ""
        if self.is_false:
            single_l+="~"
        single_l+=self.name+"("
        single_l+=','.join(self.args)+")"
        return single_l
    
    def __repr__(self):
        single_l = ""
        if self.is_false:
            single_l+="~"
        single_l+=self.name+"("
        single_l+=','.join(self.args)+")"
        return single_l

class Sentence:
    # def __init__(self, raw_sentence, positive_predicates, negative_predicates, variables, constants, list_of_literals):
    def __init__(self, list_of_literals):
        # self.raw_sentence = raw_sentence
        # self.positive_predicates = positive_predicates
        # self.negative_predicates = negative_predicates
        # self.variables = variables
        # self.constants = constants

        self.list_of_literals = list_of_literals

        # self.predicate_map = defaultdict(lambda: defaultdict(list))
        # for literal in self.list_of_literals:
        #     if literal.is_false:
        #         self.predicate_map[literal.name]['neg'].append(literal)
        #     elif not literal.is_false:
        #         self.predicate_map[literal.name]['pos'].append(literal)

        
        

    def __str__(self):
        sentence_str = []
        for i in self.list_of_literals:
            single_l = i.__str__()
            sentence_str.append(single_l)
        return ' | '.join(sentence_str)
        # return f"{self.raw_sentence} \n{self.positive_predicates} \n{self.negative_predicates} \n{self.variables} \n{self.constants} \n{self.list_of_literals}"
    
    # def __repr__(self):
    #     return f"{self.raw_sentence}"


def print_kb(KB):
    for key, val in KB.items():
        print(f"\"{key}\"")
        print("\t+ve")
        
        for s in val['positive']:
            print("\t  "+str(s))
            pass
        print("\t+ve")
        for s in val['negative']:
            print("\t  "+str(s))
            pass
        
        pass

def print_kb_list(KB_list):
    for i in KB_list:
        print(i)
        pass

def parse_sentence(m_sentence):
    # sentence must be in CNF, else it wont work
    # this will parse sentence from string form 
    parsed_data = {
        # 'positive_predicates' : set(),
        # 'variables' : set(),
        # 'constants' : set(),
        # 'negative_predicates': set(),
        'list_of_literals': []
    }
    # positive_predicates = parsed_data['positive_predicates']
    # variables = parsed_data['variables']
    # constants = parsed_data['constants']
    # negative_predicates = parsed_data['negative_predicates']
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
        #     positive_predicates.add(predicate)
        else:
            is_false = True
        #     negative_predicates.add(predicate)

        arguments = curr[brace_start_idx+1:brace_end_idx]

        
        
        arguments = arguments.split(',')
        single_literal = Literal(predicate, is_false, arguments)
        list_of_literals.append(single_literal)

        # for arg in arguments:
        #     if arg.islower():
        #         variables.add(arg)
        #     else:
        #         constants.add(arg)
        
        # print(variables)
    return parsed_data


def resolution_without_theta(literals):
    # To remove HighBP(Tim, John) and ~HignBP(Tim, John)
    # HighBP(Tim,John) | ~Take(Alice,Warfarin) | ~HighBP(z,Jkon) | ~HighBP(Tim,John)
    remove_items_idx = set()
    for i in range(len(literals)-1):
        for j in range(i+1, len(literals)):
            if (literals[i].name == literals[j].name) and (literals[i].is_false != literals[j].is_false):
                if literals[i].args == literals[j].args:
                    remove_items_idx.add(i)
                    remove_items_idx.add(j)
    
    literals = [x for idx, x in enumerate(literals) if idx not in remove_items_idx]
    return literals


def generate_sentence_from_list(list_of_literals):
    
    temp_dict = {}
    for literal in list_of_literals:
        for var in literal.args:
            if is_var(var) and var not in temp_dict:
                temp_dict[var] = 'v_'+str(next(global_variable_counter))
    
    for literal in list_of_literals:
        for idx, var in enumerate(literal.args):
            if is_var(var) and var in temp_dict:
                literal.args[idx] = temp_dict[var]

    # print(temp_dict)

    obj_sentence = Sentence(list_of_literals)
    # pos = set()
    # neg = set()
    # for literal in list_of_literals:
    #     if literal.is_false:
    #         neg.add(literal.name)
    #     else:
    #         pos.add(literal.name)

    # for i in pos:
    #     KB[i].setdefault('positive', []).append(obj_sentence)
    
    # for i in neg:
    #     KB[i].setdefault('negative', []).append(obj_sentence)

    # KB_list.append(obj_sentence)
    return obj_sentence



def parse_sentence_tester():

    # sent = "~Take(x,Warfarin) | ~Take(x,Timolol) | Alert(x,VitE) | ~Alert(y, VitD)"
    sent = "~Take(x,Warfarin) | Alert(x,VitE) | ~HighBP(Tim,Jkon) | ~HighBP(Tim,John)"
    # sent = "Alert(x,Bob)"
    # sent = "Alert(x,Bob) | Kake(Abc,Bob)"

    data = parse_sentence(sent)
    # obj_sentence = Sentence(sent, data['positive_predicates'], data['negative_predicates'], data['variables'], data['constants'], data['list_of_literals'])
    obj_sentence = generate_sentence_from_list(data['list_of_literals'])
    # for i in data['positive_predicates']:
    #     KB[i].setdefault('positive', []).append(obj_sentence)
    # for i in data['negative_predicates']:
    #     KB[i].setdefault('negative', []).append(obj_sentence)
    print("Obj sent---")
    print(obj_sentence)

    sent1 = "Migraine(Bob) | ~Alert(Alice,VitE) | HighBP(Tim,John) | Make(r,Car)"
    # sent1 = "~Alert(Abc,y) | Take(y,x)"
    # sent1 = "~Alert(Abc,y) | Take(y,x) | ~Kake(Abc,Bob)"

    data = parse_sentence(sent1)
    obj_sentence1 = generate_sentence_from_list(data['list_of_literals'])
    # for i in data['positive_predicates']:
    #     KB[i].setdefault('positive', []).append(obj_sentence1)
    # for i in data['negative_predicates']:
    #     KB[i].setdefault('negative', []).append(obj_sentence1)
    print("Obj sent 1---")
    print(obj_sentence1)

    print("---->><<----")
    unify(obj_sentence1, obj_sentence)


def unify(obj_sentence1, obj_sentence2):
    print("Testing: ", obj_sentence1, "<->", obj_sentence2)
    # input()
    new_goals = []
    # all_resolutions = []
    for item1 in obj_sentence1.list_of_literals:
        for item2 in obj_sentence2.list_of_literals:
            if item1.name == item2.name and item1.is_false != item2.is_false:
                theta = {}
                can_resolve_without_theta = True
                
                for i1, i2 in zip(item1.args, item2.args):
                    if (i1[0].isupper() and i2[0].isupper()) and (i1 != i2):
                        theta = {}
                        can_resolve_without_theta = False
                        break
                    elif (i1[0].isupper() and not i2[0].isupper()):
                        theta[i2] = i1
                    elif (not i1[0].isupper() and i2[0].isupper()):
                        theta[i1]  = i2
                    elif (not i1[0].isupper() and not i2[0].isupper()):
                        #TODO
                        # can variables be unified?
                        theta[i1]  = i2
                        # pass
                
                if can_resolve_without_theta or theta:
                    temp_i1 = [x for x in obj_sentence1.list_of_literals if x!=item1]
                    temp_i2 = [x for x in obj_sentence2.list_of_literals if x != item2]
                    temp_i = temp_i1+temp_i2

                    if can_resolve_without_theta:
                        # print(")))) ", item1, "---- ", item2)
                        # print(">>>>> Before: ",temp_i)
                        temp_i = resolution_without_theta(temp_i)
                        # print(">>>>> After: ",temp_i)

                    if theta:
                        # print(temp_i)
                        # all_resolutions.append(theta)

                        for i, j in theta.items():
                            for new_i in temp_i:
                                for idx, arg in enumerate(new_i.args):
                                    if arg == i:
                                        new_i.args[idx] = j
                                    # new_i.args[j for x in new_i.args if x==i]
                        print("************** after substn **************")
                        print("Theta is : ", theta, "\n  *** removed clauses- ", item1, item2)
                    temp_i = generate_sentence_from_list(temp_i)
                    
                    if temp_i.list_of_literals == []:
                        print("^^^^^^^^^^^^^^^^^^^^^^^ CONTRADICTION FOUND ^^^^^^^^^^^^^^^^^^^^^^^")
                        return False, []

                    print("---> NEW GOAL: ", temp_i)
                    new_goals.append(temp_i)
                        
                # else:
                #     print("Can't unify on: ", item1, item2)
            else:
                "Can't unify Sentences"
    
    # print(all_resolutions)
    return True, new_goals

def unify_tester():
    sent = "Alert(x,VitE))"
    # sent = "~B(Bob, y) | ~C(Bob, y)"
    data = parse_sentence(sent)
    obj_sentence1 = generate_sentence_from_list(data['list_of_literals'])

    sent1 = "~Alert(Alice,VitE)"
    data = parse_sentence(sent1)
    obj_sentence2 = generate_sentence_from_list(data['list_of_literals'])
    print(unify(obj_sentence1, obj_sentence2))


# unify_tester()


# def give_all_possible_sentences_from_kb(Sentence, )


def backtracking(m_kb, goal, depth = 0):
    if depth > max_recursion_depth_limit - 20:
        return True
    for sentence in m_kb:
        result, new_goals = unify(goal, sentence)
        if result:
            for new_goal in new_goals:
                return backtracking(m_kb + [goal], new_goal, depth=depth+1)
        else:
            return False
    return True


def negate_query(m_query):
    if m_query[0] == "~":
        m_query = m_query[1:]
    else:
        m_query = "~"+m_query
    return m_query


def process_kb(knowledge_base, m_kb_list):
    for sent in knowledge_base:
        data = parse_sentence(sent)
        m_kb_list.append(generate_sentence_from_list(data['list_of_literals']))


# process_kb(knowledge_base, KB_list)
# parse_sentence_tester()
# print_kb(KB)
# print_kb_list(KB_list)


# q = "~Alert(Alice,VitE)"
# goal_data = parse_sentence(q)
# goal = generate_sentence_from_list(goal_data['list_of_literals'])


# print(not backtracking(KB_list, goal))

# print(sys.getsizeof(KB))
# print(sys.getsizeof(KB_list))

answer = []
for query in queries:
    KB_list = []
    process_kb(knowledge_base, KB_list)
    print_kb_list(KB_list)
    neg_query = negate_query(query)
    print(neg_query)
    goal = generate_sentence_from_list(parse_sentence(neg_query)['list_of_literals'])
    answer.append(not backtracking(KB_list, goal))


print(answer)

with open('output.txt', 'w') as op_file:
    for idx, ans in enumerate(answer):
        op_file.write(str(ans).upper())
        if idx!=len(answer)-1:
            op_file.write("\n")
