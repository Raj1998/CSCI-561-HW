from collections import defaultdict, namedtuple, deque
from itertools import count
import sys
# import random
import copy
import time

with open('input8.txt', 'r') as f:
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
    if "=>" in m_clause:
        m_clause_split = [x.strip() for x in m_clause.split("=>")]
        m_clause_premise = m_clause_split[0]
        m_clause_conclusion = m_clause_split[1]

        premise_split = [x.strip() for x in m_clause_premise.split("&")]

        for idx, i in enumerate(premise_split):
            if i[0] == "~":
                premise_split[idx] = i[1:]
            else:
                premise_split[idx] = "~"+i

        m_clause_premise = "|".join(premise_split)
        m_clause = m_clause_premise + "|" + m_clause_conclusion
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

# KB_list = []
KB = defaultdict(lambda: defaultdict(dict))
class Literal(namedtuple("Literal", ["name", "is_false", "args"])):
    def __str__(self):
        # args_to_show = [x if not is_var(x) else 'v' for x in self.args]
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
        return '|'.join(sentence_str)
        # return f"{self.raw_sentence} \n{self.positive_predicates} \n{self.negative_predicates} \n{self.variables} \n{self.constants} \n{self.list_of_literals}"
    
    def __repr__(self):
        return self.__str__()


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

    atomic_sentences = m_sentence.split('|')

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
    unify2(obj_sentence1, obj_sentence)


def update_theta(m_theta):
    for key, val in m_theta.items():
        if is_var(key):
            final_val = val
            while_counter = 0
            while final_val in m_theta and is_var(final_val) and while_counter < 36:        
                final_val = m_theta[final_val]
                while_counter += 1
            m_theta[key] = final_val
    
    return m_theta

# print(update_theta({'a':'b', 'Raj':'Raj', 'b':'Raj'}))


def unify2(obj_sentence1, obj_sentence2):
    print("Testing: ", obj_sentence1, "<->", obj_sentence2)
    # input()
    new_goals = []
    # all_resolutions = []

    visited1 = set()
    visited2 = set()
    # pairs = set()

    # for idx1, item1 in enumerate(obj_sentence1.list_of_literals):
    idx1 = 0
    item1 = obj_sentence1.list_of_literals[0]
    for idx2, item2 in enumerate(obj_sentence2.list_of_literals):
        if item1.name == item2.name and item1.is_false != item2.is_false:
            
            theta = {}
            theta2 = {}
            can_resolve_without_theta = True
            
            for i1, i2 in zip(item1.args, item2.args):
                if (i1[0].isupper() and i2[0].isupper()) and (i1 != i2):
                    theta = {}
                    can_resolve_without_theta = False
                    break
                elif (i1[0].isupper() and i2[0].isupper()) and (i1 == i2):
                    theta[i1] = i2
                elif (i1[0].isupper() and not i2[0].isupper()):
                    if i2 in theta and theta[i2] != i1:
                        theta ={}
                        break
                    else:
                        theta[i2] = i1

                elif (not i1[0].isupper() and i2[0].isupper()):
                    if i1 in theta and theta[i1] != i2:
                        theta = {}
                        break
                    else:
                        theta[i1]  = i2
                elif (not i1[0].isupper() and not i2[0].isupper()):
                    #TODO
                    # 
                    # can variables be unified?
                    # if i1 in theta -> and i2 not in theta -> theta[i2] = i1
                    # same for if i1 in theta and theta[i1] != i2 -> cant unify... !!????
                    
                    if i1 in theta:
                        theta = {}
                        break
                    else:
                        theta[i1]  = i2
                
            theta = update_theta(theta)
                    
            
            if not theta:
                for i1, i2 in zip(item2.args, item1.args):
                    if (i1[0].isupper() and i2[0].isupper()) and (i1 != i2):
                        theta2 = {}
                        break
                    elif (i1[0].isupper() and i2[0].isupper()) and (i1 == i2):
                        theta2[i1] = i2
                    elif (i1[0].isupper() and not i2[0].isupper()):
                        if i2 in theta2 and theta2[i2] != i1:
                            theta2 ={}
                            break
                        else:
                            theta2[i2] = i1

                    elif (not i1[0].isupper() and i2[0].isupper()):
                        if i1 in theta2 and theta2[i1] != i2:
                            theta2 = {}
                            break
                        else:
                            theta2[i1]  = i2
                    elif (not i1[0].isupper() and not i2[0].isupper()):
                        #TODO
                        # 
                        # can variables be unified?
                        # if i1 in theta2 -> and i2 not in theta2 -> theta2[i2] = i1
                        # same for if i1 in theta2 and theta2[i1] != i2 -> cant unify... !!????
                        
                        if i1 in theta2:
                            theta2 = {}
                            break
                        else:
                            theta2[i1]  = i2
                    
                theta = update_theta(theta2)

            
            
            if can_resolve_without_theta or theta:
                temp_sent1 = copy.deepcopy(obj_sentence1)
                temp_i1 = [x for x in temp_sent1.list_of_literals if x!=item1]
                temp_sent2 = copy.deepcopy(obj_sentence2)
                temp_i2 = [x for x in temp_sent2.list_of_literals if x != item2]
                temp_i = temp_i1+temp_i2

                if can_resolve_without_theta:
                    # print(")))) ", item1, "---- ", item2)
                    # print(">>>>> Before: ",temp_i)
                    # temp_i = resolution_without_theta(temp_i)
                    pass
                    # print(">>>>> After: ",temp_i)

                if theta:
                    # print(temp_i)
                    # all_resolutions.append(theta)
                    visited1.add(idx1)
                    visited2.add(idx2)

                    #TODO
                    # change this

                    for i, j in theta.items():
                        for new_i in temp_i:
                            for idx, arg in enumerate(new_i.args):
                                if arg == i:
                                    new_i.args[idx] = j
                                # new_i.args[j for x in new_i.args if x==i]
                    print("************** after substn **************")
                    print("Theta is : ", theta, "\n  *** removed clauses- ", item1, item2)
                
                # temp_i = resolution_without_theta(temp_i)
            


                temp_i = generate_sentence_from_list(temp_i)
                
                if temp_i.list_of_literals == []:
                    print("^^^^^^^^^^^^^^^^^^^^^^^ CONTRADICTION FOUND ^^^^^^^^^^^^^^^^^^^^^^^")
                    return False, []

                print("---> NEW GOAL: ", temp_i)
                new_goals.append(temp_i)
                        
                # else:
                #     print("Can't unify on: ", item1, item2)
            # else:
            #     print("Can't unify Sentences")
    
    # print(all_resolutions)
    # if len(new_goals) > 1:
    #     print("============ Lannnnnnnnnnnnn", len(new_goals))
    return True, new_goals



# def unify(obj_sentence1, obj_sentence2):
#     print("Testing: ", obj_sentence1, "<->", obj_sentence2)
#     # input()
#     new_goals = []
#     # all_resolutions = []

#     visited1 = set()
#     visited2 = set()
#     pairs = set()

#     for idx1, item1 in enumerate(obj_sentence1.list_of_literals):
#         for idx2, item2 in enumerate(obj_sentence2.list_of_literals):
#             if item1.name == item2.name and item1.is_false != item2.is_false:
                
#                 theta = {}
#                 can_resolve_without_theta = True
                
#                 for i1, i2 in zip(item1.args, item2.args):
#                     if (i1[0].isupper() and i2[0].isupper()) and (i1 != i2):
#                         theta = {}
#                         can_resolve_without_theta = False
#                         break
#                     elif (i1[0].isupper() and not i2[0].isupper()):
#                         theta[i2] = i1
#                     elif (not i1[0].isupper() and i2[0].isupper()):
#                         theta[i1]  = i2
#                     elif (not i1[0].isupper() and not i2[0].isupper()):
#                         #TODO
#                         # 
#                         # can variables be unified?
#                         # if i1 in theta -> and i2 not in theta -> theta[i2] = i1
#                         # same for if i1 in theta and theta[i1] != i2 -> cant unify... !!????
#                         theta[i1]  = i2
#                         pass
                
#                 if can_resolve_without_theta or theta:
#                     temp_sent1 = copy.deepcopy(obj_sentence1)
#                     temp_i1 = [x for x in temp_sent1.list_of_literals if x!=item1]
#                     temp_sent2 = copy.deepcopy(obj_sentence2)
#                     temp_i2 = [x for x in temp_sent2.list_of_literals if x != item2]
#                     temp_i = temp_i1+temp_i2

#                     if can_resolve_without_theta:
#                         # print(")))) ", item1, "---- ", item2)
#                         # print(">>>>> Before: ",temp_i)
#                         temp_i = resolution_without_theta(temp_i)
#                         # print(">>>>> After: ",temp_i)

#                     if theta:
#                         # print(temp_i)
#                         # all_resolutions.append(theta)
#                         visited1.add(idx1)
#                         visited2.add(idx2)

#                         for i, j in theta.items():
#                             for new_i in temp_i:
#                                 for idx, arg in enumerate(new_i.args):
#                                     if arg == i:
#                                         new_i.args[idx] = j
#                                     # new_i.args[j for x in new_i.args if x==i]
#                         print("************** after substn **************")
#                         print("Theta is : ", theta, "\n  *** removed clauses- ", item1, item2)
                    
#                     temp_i = resolution_without_theta(temp_i)



#                     temp_i = generate_sentence_from_list(temp_i)
                    
#                     if temp_i.list_of_literals == []:
#                         print("^^^^^^^^^^^^^^^^^^^^^^^ CONTRADICTION FOUND ^^^^^^^^^^^^^^^^^^^^^^^")
#                         return False, []

#                     print("---> NEW GOAL: ", temp_i)
#                     new_goals.append(temp_i)
                        
#                 # else:
#                 #     print("Can't unify on: ", item1, item2)
#             # else:
#             #     print("Can't unify Sentences")
    
#     # print(all_resolutions)
#     if len(new_goals) > 1:
#         print("============ Lannnnnnnnnnnnn", len(new_goals))
#         pass
#     return True, new_goals

def unify_tester():
    # sent = "Alert(x,VitE))"
    # sent = "~B(Bob, y) | ~C(Bob, y)"
    # sent = "Predicate(x,x) | A(Ram)"
    # sent1 = "P(v_0)|P(v_1)"
    # sent1 = "~HighBP(Tim,John)|Alert(x,VitE)|~HighBP(Tim,Jkon)"
    sent1 = "A(x,x)"
    data = parse_sentence(sent1)
    obj_sentence1 = generate_sentence_from_list(data['list_of_literals'])

    # sent2 = "~Alert(Alice,VitE)"
    # sent2 = "~Predicate(y,z) | B(Shyam)"
    # sent2 = "~P(v_3)|~P(v_4)|T(v_5)"
    # sent2 = "Migraine(Bob)|Alert(Alice,VitE)|HighBP(Tim,John)|Make(r,Car)"
    sent2 = "~A(y,z)"
    data = parse_sentence(sent2)
    obj_sentence2 = generate_sentence_from_list(data['list_of_literals'])
    
    print("unfy tester : ", unify2(obj_sentence1, obj_sentence2))


# unify_tester()


# def give_all_possible_sentences_from_kb(Sentence, )


def backtracking(m_kb, goal, seen_goals, last_resolved_with, no_of_clauses, depth = 0):
    # input()
    # random.shuffle(m_kb)
    print(depth)
    if depth > max_recursion_depth_limit - 50:
        print("Depth limit !!!")
        return False
    for sentence in m_kb:
        result, new_goals = unify2(goal, sentence)
        
        if not result:
            return True
        elif result:
            
            for new_goal in new_goals:
                new_kb = m_kb + [goal]
                # random.shuffle(new_kb)
                # if sentence == last_resolved_with and len(new_goal.list_of_literals) > no_of_clauses:
                #     print("----------->>>>>>>>")
                #     return
                if new_goal.__str__() in seen_goals:
                    continue
                last_resolved_with = sentence
                can_resolve = backtracking(new_kb, new_goal, seen_goals, last_resolved_with, len(new_goal.list_of_literals), depth=depth+1)
                seen_goals.add(new_goal.__str__())
                print("BACKTRACKING----")
                if can_resolve:
                    return True
        # else:
        #     return True
    
    
    return False


def timeout_or_not(timeout):
    if time.time() > timeout:
        return True


def backtracking2(m_kb, goal, seen_goals, timeout, depth = 0):
    # input()
    # random.shuffle(m_kb)
    print(depth)
    if depth > max_recursion_depth_limit - 50 or timeout_or_not(timeout):
        print("Depth limit !!! or Timeout !!!")
        return False, True
    for sentence in m_kb:
        result, new_goals = unify2(goal, sentence)
        
        if not result:
            return True, False
        elif result:
            
            for new_goal in new_goals:
                new_kb = m_kb + [goal]
                # random.shuffle(new_kb)
                # if sentence == last_resolved_with and len(new_goal.list_of_literals) > no_of_clauses:
                #     print("----------->>>>>>>>")
                #     return
                if new_goal.__str__() in seen_goals:
                    continue
                # last_resolved_with = sentence
                can_resolve, did_timeout = backtracking2(new_kb, new_goal, seen_goals, timeout, depth=depth+1)
                if did_timeout:
                    return False, True
                seen_goals.add(new_goal.__str__())
                print("BACKTRACKING----")
                if can_resolve:
                    return True, False
        # else:
        #     return True
    
    
    return False, False


# def bfs(m_kb, goal, seen_goals):
#     q = deque()
#     q.append(goal)

#     while q:
#         curr_goal = q.popleft()
#         print(q)
#         # input()

#         for sentence in m_kb:
#             result, new_goals = unify(curr_goal, sentence)
#             if not result:
#                 return True
#             elif result:
#                 for new_goal in new_goals:
                    
#                     if new_goal.__str__() not in seen_goals:
#                         m_kb.append(new_goal)
#                         q.append(new_goal)
                        
#                     # can_resolve = backtracking(new_kb, new_goal, seen_goals, depth=depth+1)
#                     # seen_goals.add(new_goal.__str__())
#                     # print("BACKTRACKING----")
#                     # if can_resolve:
#                     #     return True
    
#     return False


# def bfs2(m_kb, goal, seen_goals):
#     m_kb.append(goal)
#     q = deque()
#     q.append(m_kb[0])

#     new = set()
#     m_kb = set(m_kb)

#     while True:
#         for i in m_kb:
#             for j in m_kb:
#                 result, new_goals = unify(i, j)
#                 # input()
#                 if not result: return True
#                 new = new.union(set(new_goals))
#             if new.issubset(m_kb):
#                 print("^^^^^^^^^^^^^^^^^^^^^subset found ^^^^^^^^^^^^^^^^^^^^^")
#                 return False
        
#         m_kb = m_kb.union(new)
    


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

# def single_tester():
#     KB_list = []
#     query = "Ancestor(Liz,Bob)"
#     neg_query = negate_query(query)
#     print("Negated query = ", neg_query)
#     goal = generate_sentence_from_list(parse_sentence(neg_query)['list_of_literals'])
    
#     process_kb(knowledge_base, KB_list)
#     KB_list.append(goal)
#     print_kb_list(KB_list)

#     random.shuffle(KB_list)

#     for i in range(len(KB_list)-1):
#         for j in range(i+1, len(KB_list)):
#             can, all = unify(KB_list[i], KB_list[j])
#             if can and all:
#                 goal = all[0]
#                 break
#     print('ne', goal)
#     # input()
#     seen_goals = set()
#     seen_goals.add(goal.__str__())
#     print(backtracking(KB_list, goal, seen_goals))

# single_tester()

answer = []


for query in queries:
    KB_list = []
    process_kb(knowledge_base, KB_list)
    # KB_list.sort(key=lambda x: len(x.list_of_literals))
    print_kb_list(KB_list)

    neg_query = negate_query(query)
    print("Negated query = ", neg_query)
    goal = generate_sentence_from_list(parse_sentence(neg_query)['list_of_literals'])
    KB_list.append(goal)

    seen_goals = set()
    seen_goals.add(goal.__str__())
    answer.append( backtracking2(KB_list, goal, seen_goals, time.time()+20)[0] )
#     # answer.append(bfs(KB_list, goal, seen_goals))
    # answer.append(bfs2(KB_list, goal, seen_goals))


print(answer)

with open('output.txt', 'w') as op_file:
    for idx, ans in enumerate(answer):
        op_file.write(str(ans).upper())
        if idx!=len(answer)-1:
            op_file.write("\n")
