import sys
sys.path.append("..")
import time
import random
from util import instance
from util import policy as pol
from util import simulator
from util import render
from solvers.RsS import rss_branch_and_bound_sdp, rss_brute_force_baseline, rss_binary_tree_sdp, rss_sdp_kconv_memo
from simulator_algorithm.simulator_algorithm import InventorySimulation


# use these list of seeds to make the simulation replicable. The simulation number is the length
# of this list
seed = 1989
random.seed(seed)
n = 12
simulate = False
runs = 100000


# generate and instance of the RsS problem
inst = instance.InventoryInstance()
inst.n = n                              # number of periods
inst.ch = 10                             # holding cost
inst.cp = 15                            # penalty cost
inst.co = 5                           # order cost
inst.cr = 1                            # review cost
inst.cl = 0                             # linear ordering cost
inst.init_inv = 0                       # initial inventory
inst.cv = 0.3                           # coefficient of variation of the normal distributions
means = inst.gen_means("ERR")           # needs for each period.
inst.means = means
threshold = 0.0001


inst.gen_non_stationary_poisson_demand(threshold)
inst.max_inv_bouding(threshold)
inst.probability_convolution()
print("probability convolution is over")
print(means)
print(sum(means)/n)
print("Max_demand = " + str(inst.max_demand))
print("Max_inventory = " + str(inst.max_inv_level))

### SOLVING ###

policies = []
solvers = []

## Baseline
# solvers.append(rss_brute_force_baseline.RsS_BruteForceBaseline())
# solvers.append(sol)

## Binary tree
# solvers.append(rss_binary_tree_sdp.RsS_BinaryTreeSDP())
# solvers.append(sol)

## B&B
# solvers.append(rss_branch_and_bound_sdp.RsS_BranchAndBound())
# solvers.append(sol)

## B&B random
# sol = rss_branch_and_bound_sdp.RsS_BranchAndBound()
# solvers.append(sol)

## B&B random
# sol = rss_branch_and_bound_sdp.RsS_BranchAndBound()
# sol.use_random = True
# solvers.append(sol)

## SDP
sol = rss_sdp_kconv_memo.RsS_SDP_KConv_Memo()
solvers.append(sol)

print("\n######################"
      "\nSTARTING SOLVING PHASE"
      "\n######################")

for s in solvers:
    print("\nStarting " + s.name)
    start_time = time.time()
    policy = s.solve(inst)
    end_time = time.time() - start_time
    print("Solved in:\t" + str(round(end_time, 2)))
    print("Cost:\t\t" + str(round(policy.expected_cost, 2)))
    print("Reviews:\t" + str(policy.R))
    print("s:\t\t\t" + str(policy.s))
    print("S:\t\t\t" + str(policy.S))
    print("P_perc:\t\t" + str(round(policy.pruning_percentage*100,2)))
    policies.append(policy)

if simulate:
    print("\n#########################"
          "\nSTARTING SIMULATING PHASE"
          "\n#########################")

    print("\nNumber of runs: " + str(runs))
    sim = simulator.Simulator()
    sim.instance = inst
    for p in policies:
        sim.policy = p
        cost = sim.multiple_simulations(runs, seed)
        act_cost = sim.calc_expected_cost()
        print("\nSimulate policy " + p.name)
        print("Expected cost:\t" + str(round(p.expected_cost, 2)))
        print("Actual cost:\t" + str(round(act_cost, 2)))
        print("Observed cost:\t" + str(round(cost, 2)))

SIM = InventorySimulation(inst, policy)
result_info = SIM.run_simulation()
result_info['demand'] = inst.means
print("demand:\t\t\t\t\t\t\t\t", result_info['demand'])
print("initial_inventory_levels:\t\t\t", result_info["initial_inventory_levels"])
print("today's demand:\t\t\t\t\t\t", result_info["need_inventory_levels"])
print("order_quantities:\t\t\t\t\t", result_info["order_quantities"])
print("today's real inventory:\t\t\t\t", result_info["real_inventory_levels"])
print("today's real consumption:\t\t\t", result_info["consumption_inventory_levels"])
print("today's short:\t\t\t\t\t\t", result_info["short_inventory_levels"])
print("final_inventory_levels:\t\t\t\t", result_info["final_inventory_levels"])
render.visualize_inventory_management(result_info)