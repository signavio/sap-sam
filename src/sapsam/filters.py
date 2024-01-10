import json

def filter_example_processes(dataset):
    with open("../src/sapsam/prefilled_example_processes.json") as data_file:    
        examples = json.load(data_file)

    example_names = []
    for batch in examples["example_processes"]:
        example_names.extend(batch["content"])
    example_names = set(example_names)
    dataset = dataset[~dataset["name"].isin(example_names)]
    return dataset

filters = {
    'example_processes': filter_example_processes,
}

class DataFilter:
    def __init__(self, dataset):
        self.dataset = dataset
    
    def filter_data(self, filter_key: str):
        if filter_key in filters:
            return filters[filter_key](self.dataset)
        else:
            raise ValueError(f"Invalid filter key: {filter_key}\n\
Available filters:\n\
    - example_processes")