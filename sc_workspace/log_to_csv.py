import csv
from datetime import datetime, timezone, timedelta


# Get content of the .log file of a specific attacker
def read_log(input_path):
    with open(input_path, 'r') as file:
        content = file.readlines()
    return content


# Filter the log content to keep only successful attack traces and valid entries.
def filter_traces(log_content):
    successful_case = []  # Record the case_ID of successful attacks.
    for i in range(len(log_content)):
        if i != 0 and log_content[i].split(",")[-1].strip()[4:-1] == "A" and log_content[i].split(",")[0] not in successful_case:
            successful_case.append(log_content[i].split(",")[0])

    removed_index = []  # Record the indices of entries for failed attack traces in descending order
    for i in range(len(log_content)):
        if i == 0 or (log_content[i].split(",")[0] not in successful_case):  # Also remove the header of the .log file.
            removed_index.insert(0, i)

    for i in removed_index:  # Remove all entries of failed attack paths.
        log_content.pop(i)

    return log_content


# Create a CSV file and write the log contents into it
def write_csv(log_content, output_path):
    with open(output_path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Case_ID', 'Timestamp', 'Activity'])  # Write the CSV header

        for i in range(len(log_content)):
            attack_event = log_content[i].split(",")
            attack_event[-1] = attack_event[-1].strip()

            if attack_event[-1] == "reset" or attack_event[-1] == "deadlock":  # Skip the unnecessary entries.
                pass
            # Remove unnecessary activities performed after completing the attack, such as trace: "gbc...EAaD", we remove the trailing "aD".
            elif attack_event[1] != 0 and any(log_content[i-j].split(",")[-1].strip()[4:-1] == "A" for j in range(1, int(attack_event[1]))):
                pass
            else:
                now = datetime.now(timezone(timedelta(hours=1)))
                formatted_time = now.strftime('%Y-%m-%dT%H:%M:%S%z')
                formatted_time = formatted_time[:22] + ':' + formatted_time[22:]
                performed_attack = attack_event[-1][4:-1]
                writer.writerow(["case_id" + attack_event[0], formatted_time, performed_attack])


def log_to_csv(input_path, output_path):
    log_content = read_log(input_path)
    successful_attack_entries = filter_traces(log_content)
    write_csv(successful_attack_entries, output_path)
    print(f'Successfully read from \033[1m{input_path}\033[0m and written to \033[1m{output_path}\033[0m')


# Input and output paths
best_input_path = "../data_files/Best.log"
best_output_path = "../data_files/Best_attacker.csv"

bestB_input_path = "../data_files/BestB.log"
bestB_output_path = "../data_files/BestB_attacker.csv"

average_input_path = "../data_files/Average.log"
average_output_path = "../data_files/Average_attacker.csv"

worst_input_path = "../data_files/Worst.log"
worst_output_path = "../data_files/Worst_attacker.csv"

log_to_csv(best_input_path, best_output_path)
log_to_csv(bestB_input_path, bestB_output_path)
log_to_csv(average_input_path, average_output_path)
log_to_csv(worst_input_path, worst_output_path)
