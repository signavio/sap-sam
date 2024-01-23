import json
import pandas as pd


def filter_example_processes(dataset):
    with open("../src/sapsam/prefilled_example_processes.json") as data_file:    
        examples = json.load(data_file)

    example_names = []
    for batch in examples["example_processes"]:
        example_names.extend(batch["content"])
    example_names = set(example_names)
    dataset = dataset[~dataset["name"].isin(example_names)]
    return dataset

def filter_namespaces(dataset, value=None, threshold=None):
    if 'Notation' in dataset.columns and value == "max":
        pass
    elif 'Notation' in dataset.columns and isinstance(value, str):
        print(value)
        dataset = dataset[dataset['Notation'] == value]
        if dataset.empty:
            raise ValueError(f"Filter error: notation not included in dataset")
    elif 'Frequency' in dataset.columns and isinstance(value, int):
        dataset = dataset[dataset['Notation'] != 'Other']
        dataset = dataset.nlargest(value, 'Frequency')
    else:
        raise ValueError(f"Filter error: unexpected dataset format")

    if 'Frequency' in dataset.columns and isinstance(threshold, int):
        def aggregate(row):
            if row['Frequency'] < threshold:
                row['Notation'] = 'Other'
            return row
        dataset = dataset.apply(aggregate, axis=1)
        dataset = dataset.groupby('Notation', as_index=False).agg({'Frequency': 'sum'})
        dataset = dataset.sort_values(by='Frequency', ascending=False)
    
    dataset = dataset.reset_index(drop=True)
    return dataset

filters = {
    'example_processes': filter_example_processes,
    'namespaces': filter_namespaces,
}

class DataFilter:
    '''
    Considering using static method to remove the need of class instantiation.
    ex: df_meta = DataFilter.df_meta.filter_data(df_meta, "example_processes")
    '''
    def __init__(self, dataset):
        self.dataset = dataset
    
    def filter_data(self, filter_key: str, value=None, threshold=None):
        if filter_key in filters:
            if filter_key == "example_processes":
                return filters[filter_key](self.dataset)
            elif filter_key == "namespaces":
                if value is None:
                    raise ValueError(f"Namespaces filter requires at least one argument")
                elif value is not None:
                    return filters[filter_key](self.dataset, value, threshold)
        else:
            raise ValueError(f"Invalid filter key: {filter_key}\n\
Available filters:\n\
    - example_processes\n\
    - namespaces <value> (optional) <threshold>\n\
    - empty_models")