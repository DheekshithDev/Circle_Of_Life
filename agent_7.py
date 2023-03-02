import random
import sys
import time
import numpy as np
import heapq as heap
from collections import defaultdict


def agent_7_game(agent_pos, prey_pos, predator_pos):
    current_agent_pos = agent_pos
    current_prey_pos = prey_pos
    current_predator_pos = predator_pos

    def reset():
        iterations = 0
        uncalculated_nodes_predator.clear()
        uncalculated_nodes_prey.clear()
        head_nodes_predator.clear()
        head_nodes_prey.clear()
        t = 0
        predator_initial_found_loc = 0
        prey_initial_found_loc = 0
        belief_states_prey = {}
        for i in range(1, 51):
            belief_states_prey[i] = 0
        belief_states_predator = {}
        for i in range(1, 51):
            belief_states_predator[i] = 0

        print("I AM RESETTING!")

    def BFS(node_from, node_to_go_to):
        cur_node_pos = node_from
        dists = {}
        for h in main_graph[cur_node_pos]:
            unchecked_nodes = [[h]]
            checked_nodes = []
            heap.heapify(checked_nodes)
            checked_nodes.append(cur_node_pos)
            while len(unchecked_nodes) != 0:
                m = unchecked_nodes.pop(0)
                last_node = m[-1]
                if last_node == node_to_go_to:
                    path = list(m)
                    dists[h] = path
                    unchecked_nodes = []
                    break
                for n in main_graph[last_node]:
                    if n in checked_nodes:
                        continue
                    path = list(m)
                    path.append(n)
                    unchecked_nodes.append(path)
                    if n == node_to_go_to:
                        dists[h] = path
                        unchecked_nodes = []
                        break
                checked_nodes.append(last_node)
        return dists

    # START
    iterations = 0

    belief_states_prey = {}
    for i in range(1, 51):
        belief_states_prey[i] = 0

    belief_states_predator = {}
    for i in range(1, 51):
        belief_states_predator[i] = 0

    # t = 0
    pred_max_prob = -1
    prey_max_prob = -1
    agent_survey_node_loc = 0
    prey_initial_found_loc = 0
    prey_move_prob = 0.25
    predator_initial_found_loc = 0
    pred_prob_move_random = 0.2
    pred_prob_move_to_agent = 0.6
    prey_atleast_found_once = False
    predator_atleast_found_once = False

    uncalculated_nodes_prey = []
    head_nodes_prey = []
    uncalculated_nodes_predator = []
    head_nodes_predator = []

    while iterations <= 500:
        iterations += 1

        # t = t + 1

        temp_dict = defaultdict(list)
        temp_dict_2 = {}

        # AGENT MOVEMENT
        highest_prob_val_node_list = []

        if predator_atleast_found_once:
            # This should only run once when prey is found initially i.e. belief states has prob 1 in it
            if 1 in belief_states_predator.values():

                head_nodes_predator.append(predator_initial_found_loc)

            # Start Prob
            head_nodes_predator = list(dict.fromkeys(head_nodes_predator))

            for i in head_nodes_predator:
                sorted_pred_to_agent_vals = []
                shortest_to_agent_frm_predator = BFS(i, current_agent_pos)

                for s1 in sorted(shortest_to_agent_frm_predator, key=lambda k: len(shortest_to_agent_frm_predator[k]),
                                 reverse=False):
                    sorted_pred_to_agent_vals.append(s1)

                best_path_to_agent = sorted_pred_to_agent_vals[0]

                for j in main_graph[i]:
                    uncalculated_nodes_predator.append(j)

                for k in uncalculated_nodes_predator:
                    if len(main_graph[i]) == 3:
                        if current_agent_pos in uncalculated_nodes_predator:
                            temp_dict[k].append((belief_states_predator[i] * (1 / 2)))
                        elif current_agent_pos not in uncalculated_nodes_predator:
                            if k == best_path_to_agent:
                                temp_dict[k].append((belief_states_predator[i] * pred_prob_move_to_agent))
                                continue
                            temp_dict[k].append((belief_states_predator[i] * pred_prob_move_random))
                    else:
                        if current_agent_pos in uncalculated_nodes_predator:
                            temp_dict[k].append((belief_states_predator[i] * 1))
                        elif current_agent_pos not in uncalculated_nodes_predator:
                            if k == best_path_to_agent:
                                temp_dict[k].append((belief_states_predator[i] * pred_prob_move_to_agent))
                                continue
                            temp_dict[k].append((belief_states_predator[i] * (pred_prob_move_random * 2)))

                uncalculated_nodes_predator.clear()
                belief_states_predator[i] = 0

            for lk in temp_dict.keys():
                if len(temp_dict[lk]) == 1:
                    belief_states_predator[lk] = temp_dict[lk][-1]
                else:
                    belief_states_predator[lk] = sum(temp_dict[lk])

            belief_states_predator[current_agent_pos] = 0
            uncalculated_nodes_predator.clear()

            for i in head_nodes_predator:
                for j in main_graph[i]:
                    uncalculated_nodes_predator.append(j)
                # uncalculated_nodes.append(i)

            if current_agent_pos in uncalculated_nodes_predator:
                [uncalculated_nodes_predator.remove(r) for r in uncalculated_nodes_predator if r == current_agent_pos]

            temp_dict.clear()

            highest_prob_val_node_list.clear()
            for p2 in sorted(belief_states_predator, key=lambda k: belief_states_predator[k], reverse=True):
                highest_prob_val_node_list.append(p2)
            pred_max_prob = belief_states_predator[highest_prob_val_node_list[0]]
            # l2 = [k for k in highest_prob_val_node_list if belief_states[k] == m]
            # print('l2 = ', l2)
            # highest_prob_val_node = random.choice(l2)
            highest_prob_val_node = highest_prob_val_node_list[0]
            agent_survey_node_loc = highest_prob_val_node

        if prey_atleast_found_once:
            if 1 in belief_states_prey.values():

                head_nodes_prey.append(prey_initial_found_loc)

            # Start Prob
            head_nodes_prey = list(dict.fromkeys(head_nodes_prey))

            for i in head_nodes_prey:
                for j in main_graph[i]:
                    uncalculated_nodes_prey.append(j)
                uncalculated_nodes_prey.append(i)

                for k in uncalculated_nodes_prey:
                    if len(main_graph[i]) == 3:
                        if current_agent_pos in uncalculated_nodes_prey:
                            temp_dict[k].append((belief_states_prey[i] * (1 / 3)))
                        elif current_agent_pos not in uncalculated_nodes_prey:
                            temp_dict[k].append((belief_states_prey[i] * prey_move_prob))

                    else:
                        if current_agent_pos in uncalculated_nodes_prey:
                            temp_dict[k].append((belief_states_prey[i] * (1 / 2)))
                        elif current_agent_pos not in uncalculated_nodes_prey:
                            temp_dict[k].append((belief_states_prey[i] * (1 / 3)))

                uncalculated_nodes_prey.clear()

            for lk in temp_dict.keys():
                if len(temp_dict[lk]) == 1:
                    belief_states_prey[lk] = temp_dict[lk][-1]
                else:
                    belief_states_prey[lk] = sum(temp_dict[lk])

            belief_states_prey[current_agent_pos] = 0
            uncalculated_nodes_prey.clear()

            for i in head_nodes_prey:
                for j in main_graph[i]:
                    uncalculated_nodes_prey.append(j)
                uncalculated_nodes_prey.append(i)

            if current_agent_pos in uncalculated_nodes_prey:
                [uncalculated_nodes_prey.remove(r) for r in uncalculated_nodes_prey if r == current_agent_pos]

            temp_dict.clear()

            highest_prob_val_node_list.clear()
            for p2 in sorted(belief_states_prey, key=lambda k: belief_states_prey[k], reverse=True):
                highest_prob_val_node_list.append(p2)
            m = belief_states_prey[highest_prob_val_node_list[0]]

            l2 = [k for k in highest_prob_val_node_list if belief_states_prey[k] == m]

            highest_prob_val_node = random.choice(l2)
            # highest_prob_val_node = highest_prob_val_node_list[0]
            agent_survey_node_loc = highest_prob_val_node

        if not prey_atleast_found_once and not predator_atleast_found_once:

            er_check = list(main_graph.keys())
            er_check.remove(current_agent_pos)
            agent_survey_node_loc = random.choice(er_check)

        if agent_survey_node_loc != current_predator_pos and agent_survey_node_loc != current_prey_pos:
            # This condition below will never run after finding prey atleast once
            if prey_atleast_found_once == False and predator_atleast_found_once == False:
                # t = 0
                for i in belief_states_prey.keys():
                    if i == agent_survey_node_loc or i == current_agent_pos:
                        belief_states_prey[i] = 0
                        continue

                    belief_states_prey[i] = (1 / 48)

                for i in belief_states_predator.keys():
                    if i == agent_survey_node_loc or i == current_agent_pos:
                        belief_states_predator[i] = 0
                        continue

                    belief_states_predator[i] = (1 / 48)

            if predator_atleast_found_once:

                if pred_max_prob == 0:
                    reset()
                    continue

                [uncalculated_nodes_predator.remove(r) for r in uncalculated_nodes_predator if r == agent_survey_node_loc]

                for j in uncalculated_nodes_predator:
                    temp_dict_2[j] = belief_states_predator[j] / (1 - belief_states_predator[agent_survey_node_loc])

                head_nodes_predator.clear()
                for add in uncalculated_nodes_predator:
                    head_nodes_predator.append(add)
                uncalculated_nodes_predator.clear()

                for lk in temp_dict_2.keys():
                    belief_states_predator[lk] = temp_dict_2[lk]

                belief_states_predator[agent_survey_node_loc] = 0

                temp_dict_2.clear()

            if prey_atleast_found_once:

                if prey_max_prob == 0:
                    reset()
                    continue

                [uncalculated_nodes_prey.remove(r) for r in uncalculated_nodes_prey if r == agent_survey_node_loc]

                for j in uncalculated_nodes_prey:
                    temp_dict_2[j] = belief_states_prey[j] / (1 - belief_states_prey[agent_survey_node_loc])

                head_nodes_prey.clear()
                for add in uncalculated_nodes_prey:
                    head_nodes_prey.append(add)
                uncalculated_nodes_prey.clear()

                for lk in temp_dict_2.keys():
                    belief_states_prey[lk] = temp_dict_2[lk]

                belief_states_prey[agent_survey_node_loc] = 0

                temp_dict_2.clear()

        elif agent_survey_node_loc == current_prey_pos and agent_survey_node_loc == current_predator_pos:
            print('I found prey and predator here once!')
            prey_initial_found_loc = agent_survey_node_loc
            predator_initial_found_loc = agent_survey_node_loc
            head_nodes_prey.clear()
            head_nodes_predator.clear()
            uncalculated_nodes_prey.clear()
            uncalculated_nodes_predator.clear()
            for i in belief_states_prey.keys():
                if i == agent_survey_node_loc:
                    belief_states_prey[i] = 1
                    continue
                belief_states_prey[i] = 0
            for i in belief_states_predator.keys():
                if i == agent_survey_node_loc:
                    belief_states_predator[i] = 1
                    continue
                belief_states_predator[i] = 0

        elif agent_survey_node_loc == current_prey_pos and agent_survey_node_loc != current_predator_pos:
            print('I found prey here once!')
            prey_initial_found_loc = agent_survey_node_loc
            head_nodes_prey.clear()
            uncalculated_nodes_prey.clear()
            for i in belief_states_prey.keys():
                if i == agent_survey_node_loc:
                    belief_states_prey[i] = 1
                    continue
                belief_states_prey[i] = 0

            if predator_atleast_found_once == False:
                for i in belief_states_predator.keys():
                    if i == agent_survey_node_loc or i == current_agent_pos:
                        belief_states_predator[i] = 0
                        continue
                    belief_states_predator[i] = (1 / 48)

            elif predator_atleast_found_once:
                if pred_max_prob == 0:
                    reset()
                    continue

                [uncalculated_nodes_predator.remove(r) for r in uncalculated_nodes_predator if r == agent_survey_node_loc]

                for j in uncalculated_nodes_predator:
                    temp_dict_2[j] = belief_states_predator[j] / (1 - belief_states_predator[agent_survey_node_loc])

                head_nodes_predator.clear()
                for add in uncalculated_nodes_predator:
                    head_nodes_predator.append(add)
                uncalculated_nodes_predator.clear()

                for lk in temp_dict_2.keys():
                    belief_states_predator[lk] = temp_dict_2[lk]

                belief_states_predator[agent_survey_node_loc] = 0

                temp_dict_2.clear()

        elif agent_survey_node_loc == current_predator_pos and agent_survey_node_loc != current_prey_pos:
            print('I found predator here once!')
            predator_initial_found_loc = agent_survey_node_loc
            head_nodes_predator.clear()
            uncalculated_nodes_predator.clear()
            for i in belief_states_predator.keys():
                if i == agent_survey_node_loc:
                    belief_states_predator[i] = 1
                    continue
                belief_states_predator[i] = 0

            if prey_atleast_found_once == False:
                for i in belief_states_prey.keys():
                    if i == agent_survey_node_loc or i == current_agent_pos:
                        belief_states_prey[i] = 0
                        continue
                    belief_states_prey[i] = (1 / 48)
            else:
                pass

        sorted_prey_vals = []
        sorted_pred_vals = []

        # Find prey dist to agent here
        total_cost_to_prey_path = BFS(current_agent_pos, current_prey_pos)
        for k2 in sorted(total_cost_to_prey_path, key=lambda k: len(total_cost_to_prey_path[k]), reverse=False):
            sorted_prey_vals.append(k2)

        if predator_initial_found_loc != 0:
            highest_prob_val_node_list.clear()

            for p3 in sorted(belief_states_predator, key=lambda k: belief_states_predator[k], reverse=True):
                highest_prob_val_node_list.append(p3)
            highest_prob_val_node = highest_prob_val_node_list[0]

            total_cost_to_survey_pred_path = BFS(current_agent_pos, highest_prob_val_node)

            for k1 in sorted(total_cost_to_survey_pred_path, key=lambda k: len(total_cost_to_survey_pred_path[k]),
                             reverse=True):
                sorted_pred_vals.append(k1)

            # C1
            if sorted_prey_vals[0] == sorted_pred_vals[0]:
                current_agent_pos = sorted_prey_vals[0]

            # C2
            elif sorted_prey_vals[0] == sorted_pred_vals[1]:
                current_agent_pos = sorted_prey_vals[0]

            # C3
            elif sorted_prey_vals[1] == sorted_pred_vals[0]:
                current_agent_pos = sorted_prey_vals[1]

            # C4
            elif sorted_prey_vals[1] == sorted_pred_vals[1]:
                current_agent_pos = sorted_prey_vals[1]

            # C5
            elif sorted_pred_vals[0] != sorted_pred_vals[1]:
                current_agent_pos = sorted_pred_vals[0]

            # C6
            elif sorted_pred_vals[1] != sorted_prey_vals[2]:
                current_agent_pos = sorted_pred_vals[1]

            # C7
            else:

                pass

        else:
            current_agent_pos = sorted_prey_vals[0]

        # This here also only runs till I find prey atleast once

        if current_agent_pos == current_prey_pos == current_predator_pos:
            print('GAME OVER! EVERYBODY DIED!')
            return

        if current_agent_pos == current_predator_pos:
            print("PREDATOR WON! AGENT DIED!")
            return 'P1'

        if current_agent_pos == current_prey_pos:
            print('AGENT WON!')
            return 'A1'

        # PREY MOVEMENT
        if len((main_graph[current_prey_pos] + [current_prey_pos])) == 4:
            current_prey_pos_list = random.choices((main_graph[current_prey_pos] + [current_prey_pos]),
                                                   [25, 25, 25, 25], k=1)
        else:
            current_prey_pos_list = random.choices((main_graph[current_prey_pos] + [current_prey_pos]),
                                                   [33.33, 33.33, 33.33], k=1)

        current_prey_got_pos = current_prey_pos_list[-1]

        if current_prey_got_pos == current_agent_pos:
            # Might need to change probabilities for prey jump nodes here
            pass
        else:
            current_prey_pos = current_prey_got_pos

        sorted_agent_vals = []
        total_cost_to_agent_path = BFS(current_predator_pos, current_agent_pos)
        for h1 in sorted(total_cost_to_agent_path, key=lambda k: len(total_cost_to_agent_path[k]), reverse=False):
            sorted_agent_vals.append(h1)

        possible_jump_nodes = main_graph[current_predator_pos]
        possible_jump_nodes.remove(sorted_agent_vals[0])
        possible_jump_nodes.append(sorted_agent_vals[0])

        if len(possible_jump_nodes) == 3:
            rd = random.choices(possible_jump_nodes, [0.2, 0.2, 0.6], k=1)[-1]
        else:
            rd = random.choices(possible_jump_nodes, [0.4, 0.6], k=1)[-1]

        current_predator_pos = rd

        print('current_predator_pos Taken = ', current_predator_pos)

        if current_predator_pos == current_agent_pos:
            print("PREDATOR WON! AGENT DIED!")
            return 'P1'


if __name__ == '__main__':

    begin_agent_pos = 0
    begin_prey_pos = 0
    begin_predator_pos = 0
    # Change 50
    main_graph = {1: [2, 50]}

    all_random_nodes = []
    # Change 50
    for node in range(2, 51):
        # Change 50
        if node == 50:
            main_graph[node] = [1, node - 1]
            continue
        main_graph[node] = [node + 1, node - 1]
    # Change 50
    while len(all_random_nodes) != 50:
        random_node_r_neigh = []
        random_node_l_neigh = []
        random_node_neighs = []

        random_node = random.choice(list(main_graph.keys()))
        if random_node in all_random_nodes:
            continue
        all_random_nodes.append(random_node)

        if len(main_graph[random_node]) == 2:
            n = 2
            # Change 50
            last_element = 50
            first_element = 1
            while n <= 5:
                if (random_node - n) > 0:
                    random_node_l_neigh.append(random_node - n)
                else:
                    random_node_l_neigh.append(random_node - n + last_element)
                    # There is a slight problem here because for node 10 & 1 it is taking immediate adjacent neighbours #SOLVED
                    # last_element = last_element - 1

                    # Change 50
                if (random_node + n) <= 50:
                    random_node_r_neigh.append(random_node + n)
                else:
                    random_node_r_neigh.append(random_node + n - last_element)
                    # first_element = first_element + 1
                n = n + 1

            random_node_neighs = random_node_l_neigh + random_node_r_neigh

            for i in range(len(random_node_neighs)):
                attach_node_rand = random.choice(random_node_neighs)
                if len(main_graph[attach_node_rand]) != 2:
                    continue
                main_graph[random_node].append(attach_node_rand)
                main_graph[attach_node_rand].append(random_node)
                break
        else:
            continue

    print(main_graph)
    agent_random_loc = random.choice(list(main_graph.keys()))

    while True:
        prey_random_loc = random.choice(list(main_graph.keys()))
        predator_random_loc = random.choice(list(main_graph.keys()))
        if prey_random_loc == agent_random_loc or predator_random_loc == agent_random_loc:
            continue
        break

    agent_pos = agent_random_loc
    prey_pos = prey_random_loc
    predator_pos = predator_random_loc

    print('current_agent_pos = ', agent_pos)
    print('current_prey_pos = ', prey_pos)
    print('current_predator_pos = ', predator_pos)

    final_answer = agent_7_game(agent_pos, prey_pos, predator_pos)
    if final_answer == 'A1':
        print('AGENT WON! GAME OVER')
    if final_answer == 'P1':
        print('PREDATOR WON! GAME OVER')
