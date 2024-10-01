import os
import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.visualization.process_tree import visualizer as pt_visualizer


def create_pt(input_path):
    # Import the .xes log
    xes_content = xes_importer.apply(input_path)

    # Convert the log to a process tree using inductive algorithm
    process_tree = pm4py.discover_process_tree_inductive(xes_content)

    # Print and visualize the process tree
    print(f"Process Tree for {input_path}:")
    print(process_tree)
    # All outputs can be found in the folder 'data_files'.
    file_name = os.path.splitext(os.path.basename(input_path))[0]
    output_path = f'../data_files/{file_name}.png'
    pm4py.save_vis_process_tree(process_tree, file_path=output_path, rankdir='TB')  # TB: Vertical View


# Input paths
best_input_path = "../data_files/Best_attacker.xes"
bestB_input_path = "../data_files/BestB_attacker.xes"
average_input_path = "../data_files/Average_attacker.xes"
worst_input_path = "../data_files/Worst_attacker.xes"

create_pt(best_input_path)
create_pt(bestB_input_path)
create_pt(average_input_path)
create_pt(worst_input_path)
