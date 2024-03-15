import matplotlib.pyplot as plt


def visualize_inventory_management(result_info):
    fig, axs = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle('Inventory Management Data Visualization', fontsize=18)
    data_keys = ['order_quantities', 'short_inventory_levels', 'consumption_inventory_levels',
                 'final_inventory_levels', 'need_inventory_levels', 'initial_inventory_levels']
    titles = ['Order Quantities', 'Short Inventory Levels', 'Consumption Inventory Levels',
              'Final Inventory Levels', 'Need Inventory Levels', 'Initial Inventory Levels']
    colors = ['b', 'g', 'r', 'c', 'm', 'orange']
    linestyles = ['-', '--', '-.', '-', '--', '-.']
    for i, ax in enumerate(axs.flat):
        data_key = data_keys[i]
        data = result_info[data_key]
        months = list(range(1, len(data) + 1))
        # 使用不同的图表类型展示不同的数据集
        if data_key in ['order_quantities', 'need_inventory_levels']:
            ax.plot(months, data, color=colors[i], linestyle=linestyles[i], linewidth=2, marker='o', markersize=8, label=data_key)
        else:
            ax.bar(months, data, color=colors[i], label=data_key)
        ax.set_xlabel('Month')
        ax.set_ylabel('Quantity')
        ax.set_title(titles[i], fontsize=14)
        ax.grid(True)
        ax.legend()
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()