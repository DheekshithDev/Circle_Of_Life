import random
import sys
import numpy as np
import heapq as heap


def agent_2_game(agent_pos, prey_pos, predator_pos):
    current_agent_pos = agent_pos
    current_prey_pos = prey_pos
    current_predator_pos = predator_pos

    iterations = 0
    max_iterations = 500

    while iterations <= 500:
        iterations += 1

        # Agent Movement
        cur_node_pos = current_agent_pos

        def agent_prey_c1_loop():
            prey_dists = {}
            # unchecked_nodes = []
            # checked_nodes = []
            # heap.heapify(checked_nodes)
            for h in main_graph[cur_node_pos]:
                unchecked_nodes = [[h]]
                checked_nodes = []
                heap.heapify(checked_nodes)
                checked_nodes.append(cur_node_pos)
                while len(unchecked_nodes) != 0:
                    m = unchecked_nodes.pop(0)
                    last_node = m[-1]
                    if last_node == current_prey_pos:
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
                        if n == current_prey_pos:
                            # print("Shortest prey path = ", path)
                            prey_dists[h] = path
                            unchecked_nodes = []
                            break
                    checked_nodes.append(last_node)
            return prey_dists

        def agent_predator_c1_loop():
            pred_dists = {}
            # unchecked_nodes = []
            # checked_nodes = []
            # heap.heapify(checked_nodes)
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
                            # print("Shortest predator path = ", path)
                            pred_dists[h] = path
                            unchecked_nodes = []
                            break
                    checked_nodes.append(last_node)
            return pred_dists

        total_cost_to_prey_path = agent_prey_c1_loop()

        total_cost_to_predator_path = agent_predator_c1_loop()

        sorted_prey_vals = []
        sorted_pred_vals = []

        for k1 in sorted(total_cost_to_prey_path, key=lambda k: len(total_cost_to_prey_path[k]), reverse=False):
            sorted_prey_vals.append(k1)

        for k2 in sorted(total_cost_to_predator_path, key=lambda k: len(total_cost_to_predator_path[k]), reverse=True):
            sorted_pred_vals.append(k2)

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

        if current_agent_pos == current_prey_pos == current_predator_pos:
            return None

        if current_agent_pos == current_predator_pos:
            return 'P1'

        if current_agent_pos == current_prey_pos:
            return 'A1'

        # Prey Movement
        if len((main_graph[current_prey_pos] + [current_prey_pos])) == 4:
            current_prey_pos_list = random.choices((main_graph[current_prey_pos] + [current_prey_pos]), [25, 25, 25, 25], k=1)
        else:
            current_prey_pos_list = random.choices((main_graph[current_prey_pos] + [current_prey_pos]), [33.33, 33.33, 33.33], k=1)

        current_prey_got_pos = current_prey_pos_list[-1]

        if current_prey_got_pos == current_agent_pos:
            pass
        else:
            current_prey_pos = current_prey_got_pos

        predator_path = []
        for a2 in main_graph[current_predator_pos]:
            predator_path.append(abs(a2 - current_agent_pos))
        predator_path.sort()
        current_predator_pos = predator_path[0]

        if current_predator_pos == current_agent_pos:
            return 'P1'


if __name__ == '__main__':

    begin_agent_pos = 0
    begin_prey_pos = 0
    begin_predator_pos = 0
    #Change 50
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

    count = 0
    agent_won_times = 0
    predator_won_times = 0
    nobody_won = 0

    while count < 25:
        count += 1

        final_answer = agent_2_game(agent_pos, prey_pos, predator_pos)
        if final_answer == 'A1':
            agent_won_times += 1

        elif final_answer == 'P1':
            predator_won_times += 1

        elif final_answer is None:
            nobody_won += 1

    print('agent_won_times = ', agent_won_times)
    print('predator_won_times = ', predator_won_times)
    print('nobody_won = ', nobody_won)

