import random
import sys
import time
import numpy as np
import heapq as heap


def agent_4_game(agent_pos, prey_pos, predator_pos):
    current_agent_pos = agent_pos
    current_prey_pos = prey_pos
    current_predator_pos = predator_pos

    # BFS to highest probability prey node location
    def agent_prey_loop(highest_prob_val_node):
        # NTC Shadow Naming Error
        cur_node_pos = current_agent_pos
        prey_dists = {}
        for h in main_graph[cur_node_pos]:
            unchecked_nodes = [[h]]
            checked_nodes = []
            heap.heapify(checked_nodes)
            checked_nodes.append(cur_node_pos)
            while len(unchecked_nodes) != 0:
                m = unchecked_nodes.pop(0)
                last_node = m[-1]
                if last_node == highest_prob_val_node:
                    path = list(m)
                    prey_dists[h] = path
                    unchecked_nodes = []
                    break
                for n in main_graph[last_node]:
                    if n in checked_nodes:
                        continue
                    path = list(m)
                    path.append(n)
                    unchecked_nodes.append(path)
                    if n == highest_prob_val_node:
                        # print("Shortest prey path = ", path)
                        prey_dists[h] = path
                        unchecked_nodes = []
                        break
                checked_nodes.append(last_node)
        return prey_dists

    # BFS to always known predator node location
    def agent_predator_loop():
        cur_node_pos = current_agent_pos
        pred_dists = {}
        for h in main_graph[cur_node_pos]:
            unchecked_nodes = [[h]]
            checked_nodes = []
            heap.heapify(checked_nodes)
            checked_nodes.append(cur_node_pos)
            while len(unchecked_nodes) != 0:
                m = unchecked_nodes.pop(0)
                last_node = m[-1]
                if last_node == current_predator_pos:
                    path = list(m)
                    pred_dists[h] = path
                    unchecked_nodes = []
                    break
                for n in main_graph[last_node]:
                    if n in checked_nodes:
                        continue
                    path = list(m)
                    path.append(n)
                    unchecked_nodes.append(path)
                    if n == current_predator_pos:

                        pred_dists[h] = path
                        unchecked_nodes = []
                        break
                checked_nodes.append(last_node)
        return pred_dists

    iterations = 0

    belief_states = {}
    for i in range(1, 51):
        belief_states[i] = 0

    t = 0
    n = 0
    m = -1
    agent_survey_node_loc = -1
    prey_initial_found_loc = 0
    prob_stay = 0.1
    prob_move = 0.3

    uncalculated_nodes = []
    head_nodes = []

    while iterations <= 500:
        iterations += 1

        t = t + 1

        temp_dict = {}

        # AGENT MOVEMENT

        highest_prob_val_node_list = []
        if t > 1:

            # This should only run once when prey is found initially i.e. belief states has prob 1 in it
            if 1 in belief_states.values():

                head_nodes.append(prey_initial_found_loc)

            # Start Prob
            head_nodes = list(dict.fromkeys(head_nodes))
            temp_er = []
            for i in head_nodes:

                for j in main_graph[i]:
                    uncalculated_nodes.append(j)
                uncalculated_nodes.append(i)
                uncalculated_nodes = list(dict.fromkeys(uncalculated_nodes))

                for k in uncalculated_nodes:
                    if k in temp_er:
                        temp_dict[k] = (temp_dict[k] * 2)
                        continue
                    if k in head_nodes:
                        temp_dict[k] = (belief_states[i] * prob_stay)
                        continue
                    if len(main_graph[i]) == 3:
                        temp_dict[k] = (belief_states[i] * prob_move)
                    else:
                        temp_dict[k] = (belief_states[i] * (prob_move + 0.15))

                    temp_er.append(k)
                uncalculated_nodes.clear()

            for lk in temp_dict.keys():
                belief_states[lk] = temp_dict[lk]

            belief_states[current_agent_pos] = 0

            temp_dict.clear()

            # for i in head_nodes:
            #     time.sleep(0.5)
            #     print('belief_states[i] = ', belief_states[i])
            #     for j in uncalculated_nodes:
            #         print('belief_states[j]_initial = ', belief_states[j])
            #         if j in head_nodes:
            #             belief_states[j] = (belief_states[i] * prob_stay)
            #             print('belief_states[j]_1 = ', belief_states[j])
            #             continue
            #         if len(main_graph[i]) == 3:
            #             belief_states[j] = (belief_states[i] * prob_move)
            #             print('belief_states[j]_2 = ', belief_states[j])
            #         else:
            #             belief_states[j] = (belief_states[i] * (prob_move + 0.15))
            #             print('belief_states[j]_3 = ', belief_states[j])

            highest_prob_val_node_list.clear()
            for p2 in sorted(belief_states, key=lambda k: belief_states[k], reverse=True):
                highest_prob_val_node_list.append(p2)
            m = belief_states[highest_prob_val_node_list[0]]

            l2 = [k for k in highest_prob_val_node_list if belief_states[k] == m]

            highest_prob_val_node = random.choice(l2)
            # highest_prob_val_node = highest_prob_val_node_list[0]
            agent_survey_node_loc = highest_prob_val_node

        elif 1 not in belief_states.values():

            er_check = list(belief_states.keys())
            er_check.remove(current_agent_pos)
            agent_survey_node_loc = random.choice(er_check)

        if agent_survey_node_loc != current_prey_pos:
            if t > 1:

                if m == 0:
                    head_nodes.clear()
                    # uncalculated_nodes.clear()
                    t = 0
                    prey_initial_found_loc = 0
                    for i in range(1, 51):
                        belief_states[i] = 0
                    print("I AM RESETTING!")
                    continue

                tempo = []

                for i in head_nodes:
                    for j in main_graph[i]:
                        uncalculated_nodes.append(j)
                    uncalculated_nodes.append(i)

                    uncalculated_nodes = list(dict.fromkeys(uncalculated_nodes))

                    if agent_survey_node_loc in uncalculated_nodes:
                        # uncalculated_nodes.remove(agent_survey_node_loc)
                        for k in uncalculated_nodes:
                            # NEED TO CHECK THIS HERE
                            # if k == agent_survey_node_loc:
                            #     temp_dict[k] = 0
                            #     continue
                            temp_dict[k] = belief_states[k] / (1 - belief_states[agent_survey_node_loc])

                        uncalculated_nodes.remove(i)
                        uncalculated_nodes.remove(agent_survey_node_loc)

                        for add in uncalculated_nodes:
                            tempo.append(add)

                    uncalculated_nodes.clear()

                for lk in temp_dict.keys():
                    belief_states[lk] = temp_dict[lk]

                belief_states[agent_survey_node_loc] = 0

                temp_dict.clear()
                head_nodes.clear()
                for jj in tempo:
                    head_nodes.append(jj)

                # uncalculated_nodes.remove(agent_survey_node_loc)

                # for j in uncalculated_nodes:
                #     belief_states[j] = belief_states[j] / (1 - belief_states[agent_survey_node_loc])
                # belief_states[agent_survey_node_loc] = 0
                # for rem in head_nodes:
                #     uncalculated_nodes.remove(rem)
                # head_nodes.clear()
                # for add in uncalculated_nodes:
                #     head_nodes.append(add)
                # uncalculated_nodes.clear()

            # This condition below will never run after finding prey atleast once
            if t == 1:
                t = 0
                print('2 I came here')
                for i in belief_states.keys():
                    if i == agent_survey_node_loc or i == current_agent_pos:
                        belief_states[i] = 0
                        continue

                    belief_states[i] = (1 / 48)
                # n = n + 1
                # print('n = ', n)

        elif agent_survey_node_loc == current_prey_pos:
            print('I found prey here once!')
            prey_initial_found_loc = agent_survey_node_loc
            head_nodes.clear()
            uncalculated_nodes.clear()
            for i in belief_states.keys():
                if i == agent_survey_node_loc:
                    belief_states[i] = 1
                    continue
                belief_states[i] = 0
        print('agent_survey_node_loc = ', agent_survey_node_loc)

        sorted_pred_vals = []
        sorted_prey_vals = []

        # Find predator dist to agent here
        total_cost_to_predator_path = agent_predator_loop()
        for k2 in sorted(total_cost_to_predator_path, key=lambda k: len(total_cost_to_predator_path[k]), reverse=True):
            sorted_pred_vals.append(k2)

        print('total_cost_to_predator_path = ', total_cost_to_predator_path)
        print('sorted_pred_vals = ', sorted_pred_vals)

        print('prey_initial_found_loc = ', prey_initial_found_loc)

        if prey_initial_found_loc != 0:
            highest_prob_val_node_list.clear()

            for p3 in sorted(belief_states, key=lambda k: belief_states[k], reverse=True):
                highest_prob_val_node_list.append(p3)
            highest_prob_val_node = highest_prob_val_node_list[0]

            print('highest_prob_val_node_list = ', highest_prob_val_node_list)
            print('highest_prob_val_node = ', highest_prob_val_node)

            total_cost_to_survey_prey_path = agent_prey_loop(highest_prob_val_node)

            for k1 in sorted(total_cost_to_survey_prey_path, key=lambda k: len(total_cost_to_survey_prey_path[k]),
                             reverse=False):
                sorted_prey_vals.append(k1)

            print('total_cost_to_survey_prey_path = ', total_cost_to_survey_prey_path)
            print('sorted_prey_vals = ', sorted_prey_vals)

            # C1
            if sorted_prey_vals[0] == sorted_pred_vals[0]:
                current_agent_pos = sorted_prey_vals[0]
                print('C1 Agent Pos = ', current_agent_pos)
            # C2
            elif sorted_prey_vals[0] == sorted_pred_vals[1]:
                current_agent_pos = sorted_prey_vals[0]
                print('C2 Agent Pos = ', current_agent_pos)
            # C3
            elif sorted_prey_vals[1] == sorted_pred_vals[0]:
                current_agent_pos = sorted_prey_vals[1]
                print('C3 Agent Pos = ', current_agent_pos)
            # C4
            elif sorted_prey_vals[1] == sorted_pred_vals[1]:
                current_agent_pos = sorted_prey_vals[1]
                print('C4 Agent Pos = ', current_agent_pos)
            # C5
            elif sorted_pred_vals[0] != sorted_pred_vals[1]:
                current_agent_pos = sorted_pred_vals[0]
                print('C5 Agent Pos = ', current_agent_pos)
            # C6
            elif sorted_pred_vals[1] != sorted_prey_vals[2]:
                current_agent_pos = sorted_pred_vals[1]
                print('C6 Agent Pos = ', current_agent_pos)
            # C7
            else:
                print('C7 Agent Pos = ', current_agent_pos)
                pass

        else:
            current_agent_pos = sorted_pred_vals[0]
        print('t = ', t)
        # This here also only runs till I find prey atleast once
        print('Current agent pos = ', current_agent_pos)

        if current_agent_pos == current_prey_pos == current_predator_pos:
            print('GAME OVER! EVERYBODY DIED!')
            return

        if current_agent_pos == current_predator_pos:
            return 'P1'

        if current_agent_pos == current_prey_pos:
            print('AGENT WON!')
            return 'A1'

        # PREY MOVEMENT
        if len((main_graph[current_prey_pos] + [current_prey_pos])) == 4:
            current_prey_pos_list = random.choices((main_graph[current_prey_pos] + [current_prey_pos]),
                                                   [30, 30, 30, 10], k=1)
        else:
            current_prey_pos_list = random.choices((main_graph[current_prey_pos] + [current_prey_pos]),
                                                   [42.8, 42.8, 14.4], k=1)

        current_prey_got_pos = current_prey_pos_list[-1]

        if current_prey_got_pos == current_agent_pos:
            # Might need to change probabilities for prey jump nodes here
            pass
        else:
            current_prey_pos = current_prey_got_pos

        # PREDATOR MOVEMENT
        def predator_movement():
            cur_pred_node_pos = current_predator_pos
            checked_nodes = []
            unchecked_nodes = [[cur_pred_node_pos]]
            heap.heapify(checked_nodes)
            while len(unchecked_nodes) != 0:
                m = unchecked_nodes.pop(0)
                last_node = m[-1]
                for n in main_graph[last_node]:
                    if n in checked_nodes:
                        continue
                    path = list(m)
                    path.append(n)
                    unchecked_nodes.append(path)
                    if n == current_agent_pos:
                        # print('I see Agent!')
                        return path
                checked_nodes.append(last_node)

        predator_path = predator_movement()
        # print('Predator Path = ', predator_path)
        current_predator_pos = predator_path[1]

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

    final_answer = agent_4_game(agent_pos, prey_pos, predator_pos)
    if final_answer == 'A1':
        print('AGENT WON! GAME OVER')
    if final_answer == 'P1':
        print('PREDATOR WON! GAME OVER')
