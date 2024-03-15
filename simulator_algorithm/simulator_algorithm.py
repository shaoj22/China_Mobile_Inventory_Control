

import sys
sys.path.append('..')


class InventorySimulation:
    def __init__(self, inst, policy):
        self.inst = inst
        self.policy = policy
        self.current_inventory = inst.init_inv  # 初始库存量
        for i in range(len(self.policy.s)):
            if self.policy.s[i] == float('inf'):
                self.policy.s[i] = 0
            if self.policy.S[i] == float('inf'):
                self.policy.S[i] = 0

    def run_simulation(self):
        order_quantities = [0 for i in range(self.inst.n)]  # 记录每个周期的订货量
        initial_inventory_levels = [0 for i in range(self.inst.n)]  # 记录每个周期的期初库存
        final_inventory_levels = [0 for i in range(self.inst.n)]  # 记录每个周期的期末库存
        short_inventory_levels = [0 for i in range(self.inst.n)]  # 记录每个周期的缺货库存
        need_inventory_levels = [0 for i in range(self.inst.n)]  # 记录每个周期的需求量
        consumption_inventory_levels = [0 for i in range(self.inst.n)]  # 记录每个周期的消耗量
        real_inventory_levels = [0 for i in range(self.inst.n)]  # 记录每个周期的真实库存
        result_info = {}
        for t in range(self.inst.n):
            # 计算今日期初库存：
            if t == 0:
                initial_inventory_levels[t] = self.current_inventory
            else:
                initial_inventory_levels[t] = final_inventory_levels[t - 1]
            # 计算今日订货量
            order_quantities[t] = self.policy.R[t] * (self.policy.S[t] - initial_inventory_levels[t])
            # 计算及时到货后的库存
            real_inventory_levels[t] = initial_inventory_levels[t] + order_quantities[t]
            # 计算今日需求
            if t == 0:
                need_inventory_levels[t] = self.inst.means[t]
            else:
                need_inventory_levels[t] = self.inst.means[t] - short_inventory_levels[t-1]
            # 计算今日消耗
            if real_inventory_levels[t] > need_inventory_levels[t]:
                consumption_inventory_levels[t] = need_inventory_levels[t]
            else:
                consumption_inventory_levels[t] = real_inventory_levels[t]
            # 计算今日缺货待补量
            if real_inventory_levels[t] < need_inventory_levels[t]:
                short_inventory_levels[t] = real_inventory_levels[t] - need_inventory_levels[t]
            else:
                short_inventory_levels[t] = 0
            # 计算今日期末库存
            final_inventory_levels[t] = initial_inventory_levels[t] - consumption_inventory_levels[t] + order_quantities[t]
        result_info["order_quantities"] = order_quantities
        result_info["short_inventory_levels"] = short_inventory_levels
        result_info["consumption_inventory_levels"] = consumption_inventory_levels
        result_info["final_inventory_levels"] = final_inventory_levels
        result_info["need_inventory_levels"] = need_inventory_levels
        result_info["initial_inventory_levels"] = initial_inventory_levels
        result_info["real_inventory_levels"] = real_inventory_levels

        return result_info