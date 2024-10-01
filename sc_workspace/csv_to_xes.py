import pandas as pd
import pm4py


# Read from csv file
def read_csv(input_path):
    csv_content = pd.read_csv(input_path)
    return csv_content


def write_xes(csv_content, output_path):

    # Convert the DataFrame to the event log format that pm4py can use
    csv_content.rename(columns={
        'Case_ID': 'case:concept:name',
        'Activity': 'concept:name',
        'Timestamp': 'time:timestamp'
    }, inplace=True)   # Change Column Name Directly
    event_log = pm4py.format_dataframe(csv_content)

    # Use pm4py to write the event log to an XES file
    pm4py.write_xes(event_log, output_path)


def csv_to_xes(input_path, output_path):
    csv_content = read_csv(input_path)
    write_xes(csv_content, output_path)
    print(f'Successfully read from \033[1m{input_path}\033[0m and written to \033[1m{output_path}\033[0m')


# Input and output paths
best_input_path = "../data_files/Best_attacker.csv"
best_output_path = "../data_files/Best_attacker.xes"

bestB_input_path = "../data_files/BestB_attacker.csv"
bestB_output_path = "../data_files/BestB_attacker.xes"

average_input_path = "../data_files/Average_attacker.csv"
average_output_path = "../data_files/Average_attacker.xes"

worst_input_path = "../data_files/Worst_attacker.csv"
worst_output_path = "../data_files/Worst_attacker.xes"

csv_to_xes(best_input_path, best_output_path)
csv_to_xes(bestB_input_path, bestB_output_path)
csv_to_xes(average_input_path, average_output_path)
csv_to_xes(worst_input_path, worst_output_path)








