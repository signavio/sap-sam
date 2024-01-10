import json

def filter_exampleprocesses():
    with open("prefilled_example_processes.json") as data_file:    
        examples = json.load(data_file)

    example_names = []
    for batch in examples["example_processes"]:
        example_names.extend(batch["content"])
    example_names = set(example_names)
    print(example_names)
    return

filters = {
    'exampleprocesses': filter_exampleprocesses,
}

def filter_data(filter_key: str):
    if filter_key in filters:
        filter_function = filters[filter_key]
        filtered_data = filter_function()
        return filtered_data
    else:
        raise ValueError(f"Invalid filter key: {filter_key}\n\
Available filters:\n\
    - exampleprocesses")

def main():
    try:
        filter_data("examplprocesses")
    except ValueError as error:
        print(error)

main()