import pandas as pd
import numpy as np


# Control-Flow Complexity (CFC)
# Description: CFC counts the occurrences of different types of splits (AND, XOR, OR) in the model.
def CFC(df):
    cfc = df[df["low_level_category"] == "Gateways"].groupby('model_id')['category'].count().reset_index(name='CFC')
    return cfc


# Number of Activities, Joins and Splits (NOAJS)
# Description: Splits in BPMN do not necessarily have corresponding joins.  NOAJS complexity metric can measure such not well structured processes based on counting activities, joins and splits together.
def NOAJS(df):
    noajs = df[df["low_level_category"].isin(["Activities", "Gateways"])].groupby('model_id')['category'].count().reset_index(name='NOAJS')
    return noajs


# Number of Activities (NOA)
# Description: NOA metric sums up activities in a business process model. It is a simple and popular metric that can be used to measure complexity.
def NOA(df):
    noa = df[df["low_level_category"] == "Activities"].groupby('model_id')['category'].count().reset_index(name='NOA')
    return noa


# Coefficient of Connectivity (CNC(G))
# Description: CNC(G) is a structural metric; the coefficient of connectivity gives the ratio of arcs to nodes in BPMN models. 
def CNC(df):
    nodes = df[df["high_level_category"] == "node"].groupby('model_id')['category'].count()
    edge = df[df["high_level_category"] == "edge"].groupby('model_id')['category'].count()
    cnc = edge / nodes
    cnc = cnc.reset_index(name='CNC')
    return cnc


# Number of Nodes metric (Sn(G))
# Description: Sn(G) is a structural metric that calculate the number of nodes of process model. 
def Node_Count(df):
    node_count = df[df["high_level_category"] == "node"].groupby('model_id')['category'].count().reset_index(name='Node_Count')
    return node_count


# Density
# Description: Density is a structural metric that calculates the ratio of the total number of arcs to the maximum number of arcs. 
def Density(df):
    nodes = df[df["high_level_category"] == "node"].groupby('model_id')['category'].count()
    edge = df[df["high_level_category"] == "edge"].groupby('model_id')['category'].count()
    density = edge / (nodes * (nodes - 1))
    density = density.reset_index(name='Density')
    return density


# Exported Coupling of a Process metric (ECP)
# Description: ECP is a coupling metric that focuses on a process and its influence on the whole model based on how many other processes depend on its services.
def ECP(df):
    # Keep only tasks and subprocesses and calculate maximum outgoing count within each model
    ecp = df[df['category'].str.contains('Task|Subprocess')].groupby('model_id')['outgoing_count'].max().reset_index(name='EPC')
    return ecp


# Imported Coupling of a Process metric (ICP)
# Description: ICP is a coupling metric that focuses on process if it is highly dependent on external services offered by other processes.
def ICP(df):
    # Keep only tasks and subprocesses and calculate maximum incoming count within each model
    icp = df[df['category'].str.contains('Task|Subprocess')].groupby('model_id')['ingoing_count'].max().reset_index(name='IPC')
    return icp


# Fan-in/Fan-out metric (FIO)
# Description: FIO metric can be used to analyze the complexity of a business process model based on the modular structure.
#              Modular modeling is supported in BPMN by sub-processes.
def FIO(df):
    # Filter on Subprocesses for calculating FIO
    df_fio = df[df['category'].str.contains('Subprocess')].copy()
    df_fio['FIO'] = (df_fio['outgoing_count'] * df_fio['ingoing_count']).pow(2)
    fio = df_fio.groupby('model_id')['FIO'].max().reset_index(name='FIO')
    return fio


# Interface complexity of an activity metric (IC)
# Description: IC metric can be used to evaluate the complexity of processes based on the interface complexity value of a BPMN model.
#              It is similar to FIO, but for IC, we are looking at activities instead of subprocesses.
def IC(df):
    # Filter on Tasks for calculating IC
    df_ic = df[df['category'].str.contains('Task')].copy()
    df_ic['IC'] = (df_ic['outgoing_count'] * df_ic['ingoing_count']).pow(2)
    ic = df_ic.groupby('model_id')['IC'].sum().round(1).reset_index(name='IC')
    return ic


# Halsted-based Metrics
# Helper function to preprocess the data for Halsted-based metrics
def preprocess_halsted(df):
    # Activities and control-flow elements
    df_act_cf = df[df['category'].str.contains('Task|Event|Gateway|SequenceFlow')].copy()
    unique_act_cf = df_act_cf.groupby('model_id')['label'].nunique().reset_index(name='unique_act_cf')
    total_act_cf = df_act_cf.groupby('model_id')['label'].count().reset_index(name='total_act_cf')
    # Data types
    df_data_types = df[df['category'].str.contains('DataObject|DataStore')].copy()
    unique_datatypes = df_data_types.groupby('model_id')['label'].nunique().reset_index(name='unique_datatypes')
    total_datatypes = df_data_types.groupby('model_id')['label'].count().reset_index(name='total_datatypes')
    # Merge all the results into a final DataFrame
    df_halsted = unique_act_cf.merge(total_act_cf, on='model_id', how='outer')\
                              .merge(unique_datatypes, on='model_id', how='outer')\
                              .merge(total_datatypes, on='model_id', how='outer')
    df_halsted.fillna(0, inplace=True)
    return df_halsted

# Halsted-based Process Difficulty metric (HPC_D)
# Description: HPC_D is a quantitative measure of complexity and is aimed to calculate the difficulty of the process.
def HPC_D(df):
    df_halsted = preprocess_halsted(df)
    df_halsted['HPC_D'] = df_halsted.apply(lambda row: (row['unique_act_cf'] / 2) * (row['total_datatypes'] / row['unique_datatypes']) if row['unique_datatypes'] > 0 else 0, axis=1)
    return df_halsted[['model_id', 'HPC_D']]

# Halsted-based Process Length metric (HPC_N)
# Description: HPC_N is a quantitative measure of complexity and is aimed to calculate the length of the process.
def HPC_N(df):
    df_halsted = preprocess_halsted(df)
    df_halsted['HPC_N'] = df_halsted.apply(lambda row: (row['unique_act_cf'] * np.log2(row['unique_act_cf']) if row['unique_act_cf'] > 0 else 0) + 
                                                    (row['unique_datatypes'] * np.log2(row['unique_datatypes']) if row['unique_datatypes'] > 0 else 0), axis=1)
    return df_halsted[['model_id', 'HPC_N']]

# Halsted-based Process Volume metric (HPC_V)
# Description: HPC_V is a quantitative measure of complexity and is aimed to calculate the volume of the process.
def HPC_V(df):
    df_halsted = preprocess_halsted(df)
    df_halsted['HPC_V'] = df_halsted.apply(lambda row: (row['total_act_cf'] + row['total_datatypes']) * np.log2(row['unique_act_cf'] + row['unique_datatypes']) if (row['unique_act_cf'] + row['unique_datatypes']) > 0 else 0, axis=1)
    return df_halsted[['model_id', 'HPC_V']]


# Cognitive complexity measure (W)
# Description: W is a cognitive weight proposed to measure the effort needed for comprehending the model.
#
# Cognitive weights for BPMN models in Cognitive Complexity Measure (Sadowska, 2015):
#    Single consecutive step in a work-flow: 1
#    Joints: 1
#    XOR-split (exactly one of two branches is chosen): 2
#    XOR-split (exactly one of more than two branches is chosen): 3
#    AND-split: 4
#    OR-split or Complex Gateway: 7
#    Sub-process: 2
#    Start or End event: 2
#    Intermediate event: 3

def update_category(row):
    if row['category'] == 'Exclusive_Databased_Gateway' and row['outgoing_count'] > 2:
        return 'Exclusive_Databased_Gateway_3'
    return row['category']

# Cognitive weights mapping
def assign_cognitive_weights(df):
    cognitive_weights = {
        "Task": 1,
        "CollapsedSubprocess": 2,
        "Subprocess": 2,
        "CollapsedEventSubprocess": 2,
        "EventSubprocess": 2,
        "Exclusive_Databased_Gateway": 2,
        "Exclusive_Databased_Gateway_3": 3,
        "EventbasedGateway": 2,
        "ParallelGateway": 4,
        "InclusiveGateway": 7,
        "ComplexGateway": 7,
        "StartNoneEvent": 2,
        "StartMessageEvent": 2,
        "StartTimerEvent": 2,
        "StartEscalationEvent": 2,
        "StartConditionalEvent": 2,
        "StartErrorEvent": 2,
        "StartCompensationEvent": 2,
        "StartSignalEvent": 2,
        "StartMultipleEvent": 2,
        "StartParallelMultipleEvent": 2,
        "IntermediateMessageEventCatching": 3,
        "IntermediateTimerEvent": 3,
        "IntermediateEscalationEvent": 3,
        "IntermediateConditionalEvent": 3,
        "IntermediateLinkEventCatching": 3,
        "IntermediateErrorEvent": 3,
        "IntermediateCancelEvent": 3,
        "IntermediateCompensationEventCatching": 3,
        "IntermediateSignalEventCatching": 3,
        "IntermediateMultipleEventCatching": 3,
        "IntermediateParallelMultipleEventCatching": 3,
        "IntermediateEvent": 3,
        "IntermediateMessageEventThrowing": 3,
        "IntermediateEscalationEventThrowing": 3,
        "IntermediateLinkEventThrowing": 3,
        "IntermediateCompensationEventThrowing": 3,
        "IntermediateSignalEventThrowing": 3,
        "IntermediateMultipleEventThrowing": 3,
        "EndNoneEvent": 2,
        "EndMessageEvent": 2,
        "EndEscalationEvent": 2,
        "EndErrorEvent": 2,
        "EndCancelEvent": 2,
        "EndCompensationEvent": 2,
        "EndSignalEvent": 2,
        "EndMultipleEvent": 2,
        "EndTerminateEvent": 2,
        "SequenceFlow": 1,
    }

    def get_weight(category):
        return cognitive_weights.get(category, 0)  # Default to 0 if category not found

    # Assign weights
    df['weight'] = df['category'].apply(get_weight)
    
    return df

# Cognitive complexity measure (W)
def cognitive_complexity(df):
    # Assign cognitive weights
    df = assign_cognitive_weights(df)
    # Calculate cognitive complexity measure (W) by summing the weights per model
    cognitive_complexity = df.groupby('model_id')['weight'].sum().reset_index(name='Cognitive_Complexity')
    
    return cognitive_complexity


# Sequentiality Metric (S(G))
# Description: S(G) is a structural metric. The sequentiality ratio is the number of arcs between non-connector nodes divided by the total number of arcs.
def sequentiality(df):
    # Identify non-connector nodes
    df['is_non_connector'] = df.apply(lambda row: not row['outgoing'] or not row['ingoing'], axis=1)

    df_exploded = df.explode('outgoing').reset_index()
    df_exploded.rename(columns={'outgoing': 'target_element_id'}, inplace=True)

    # Merge to determine if both source and target are non-connectors
    df_exploded = df_exploded.merge(
        df.reset_index()[['model_id', 'element_id', 'is_non_connector']],
        left_on=['model_id', 'target_element_id'],
        right_on=['model_id', 'element_id'],
        suffixes=('', '_target')
    )

    # Calculate the arcs between non-connectors
    df_exploded['is_arc_between_non_connectors'] = df_exploded['is_non_connector'] & df_exploded['is_non_connector_target']

    # Calculate the sequentiality ratio per model_id
    sequentiality_ratios = df_exploded.groupby('model_id').apply(
        lambda df: round(df['is_arc_between_non_connectors'].sum() / len(df), 2) if len(df) > 0 else 0
    ).reset_index(name='sequentiality_ratio')

    return sequentiality_ratios


# Coupling Metrics (CP)
# Description: CP metric calculates the degree of coupling, which is related to the number of interconnections among the tasks of a process model.
def coupling(df):
    df = df.reset_index()

    cp_results = []

    model_ids = df['model_id'].unique()

    for model_id in model_ids:
        model_df = df[df['model_id'] == model_id]

        # Filter tasks and sequence flows for the current model
        tasks_df = model_df[model_df['category'] == 'Task']
        sequence_flows = model_df[model_df['category'] == 'SequenceFlow']['element_id'].tolist()

        total_arcs = 0
        task_to_task_arcs = 0

        # Iterate over tasks
        for idx, row in tasks_df.iterrows():
            outgoing = row['outgoing']
            incoming = row['ingoing']

            # Filter outgoing and incoming to only include sequence flows
            outgoing_sequence_flows = [e for e in outgoing if e in sequence_flows]
            incoming_sequence_flows = [e for e in incoming if e in sequence_flows]

            # Count total arcs
            total_arcs += len(outgoing_sequence_flows)

            # Count task to task arcs
            for flow in outgoing_sequence_flows:
                target_task = model_df[model_df['element_id'] == flow]['outgoing'].tolist()
                if target_task and target_task[0] in tasks_df['element_id'].tolist():
                    task_to_task_arcs += 1

        # Calculate CP for the current model
        cp_ratio = task_to_task_arcs / total_arcs if total_arcs > 0 else 0
        cp_results.append({'model_id': model_id, 'CP': cp_ratio})

    return pd.DataFrame(cp_results)


# Process User
# Description: The number of employees involved in a given process
def process_user(df):
    df = df.reset_index()
    filtered_df = df[df['category'].isin(['processparticipant', 'Lane'])]
    user = filtered_df.groupby('model_id').agg(process_user=('element_id', 'nunique')).reset_index()
    return user


# Workload
# Description: Measures the volume of work handled by an employee, which could be the number of tasks, calls, or product units processed
def workload(df):
    task_df = df[df['category'].isin(['Task'])]
    workload = task_df.groupby(['model_id', 'parent']).size().reset_index(name='tasks_per_lane')
    max_workload = workload.groupby('model_id')['tasks_per_lane'].max().reset_index(name='max_workload')
    mean_workload = workload.groupby('model_id')['tasks_per_lane'].mean().reset_index(name='mean_workload')
    return max_workload, mean_workload


# Business Process Autonomy
# Description: Measures the extent to which a business process operates independently of other processes by assessing the proportion of activities relying on external inputs.
def business_process_autonomy(df):
    df = df.reset_index()
    # External categories
    external_categories = ['Data Elements', 'Events', 'Swimlanes', 'Artifacts']
    df['external_dependency'] = df['low_level_category'].isin(external_categories)
    
    # Calculate autonomy for each model_id
    autonomy_per_model = df.groupby('model_id').apply(
        lambda group: group['external_dependency'].sum() / len(group)
    ).reset_index(name='autonomy')
    return autonomy_per_model


# Operational Cost Propotion
# Description: Evaluates the efficiency of a business process by analyzing the proportion of non-value-added and human-performed activities relative to the total activities.
# Caution with categories: since we don't have the information which tasks are performed manually and which ones add value,
# this is just a subjective classification which might not be true for all process models
def operational_cost_proportion(df):

    # Identify human-performed and non-value-added activities
    manual_activities = ["Task"]
    # value_added_activities = ["Task", "Subprocess", "CollapsedSubprocess", "EventSubprocess", "CollapsedEventSubprocess"]
    non_value_added_elements = ["Exclusive_Databased_Gateway", "EventbasedGateway", "ParallelGateway", "InclusiveGateway", "ComplexGateway",
                                "IntermediateMessageEventCatching", "IntermediateTimerEvent", "SequenceFlow", "Association_Undirected", "MessageFlow"]

    df['is_manual'] = df['category'].isin(manual_activities)
    df['is_non_value_added'] = df['category'].isin(non_value_added_elements)
    
    # Calculate the proportion for each model_id
    operational_cost_proportion = df.groupby('model_id').apply(
        lambda group: (group['is_manual'].sum() + group['is_non_value_added'].sum()) / len(group)
    ).reset_index(name='operational_cost_proportion')
    return operational_cost_proportion


# Cycle Time Efficiency
# Description: Assesses the efficiency of a business process by examining the proportion of automated and parallel activities relative to the total activities, aiming for shorter processing times.
# Caution with categories: since we don't have the information which tasks are performed automated,
# this is just a workaround classification which might not be true for all process models
def cycle_time_efficiency_temp(df):
    
    df = df.reset_index()
    
    # Automated activities: Tasks performed by (IT)-Systems
    system_lanes = df[(df['category'] == 'Lane') & (df['label'].str.contains('System', na=False))]
    system_lane_ids = system_lanes.index.tolist()
    automated_activities = df[(df['low_level_category'] == 'Activity') & (df['parent'].isin(system_lane_ids))]
    
    # Parallel activities: count outgoing from Parallel-Gateways
    parallel_activities = df[df['category'] == 'ParallelGateway']
    parallel_activities_count = parallel_activities['outgoing'].apply(lambda x: len(x) if isinstance(x, list) and len(x) > 1 else 0).sum()

    # Calculate Cycle Time Efficiency
    total_activities = len(df[df['low_level_category'] == 'Activities'])
    num_automated_activities = len(automated_activities)
    
    if total_activities == 0:
        return 0
    
    cycle_time_efficiency_temp = (num_automated_activities + parallel_activities_count) / total_activities
    return cycle_time_efficiency_temp

# Calculate Cycle Time Efficiency for each model_id
def cycle_time_efficiency(df):
    cycle_time_efficiency = df.groupby('model_id').apply(cycle_time_efficiency_temp).reset_index(name='cycle_time_efficiency')
    return cycle_time_efficiency


# Up-to-date Business Process
# Description: Creation date or frequency of updates
def creation_date(df):
    df = df.sort_values(by='datetime', ascending=False)
    # Ranking the models based on their creation date (0 being the most recent date)
    df['creation_date_rank'] = df['datetime'].rank(method='dense', ascending=False).astype(int) - 1
    return pd.DataFrame(df['creation_date_rank']).reset_index()


# IT Activities
# Description: Steps in the process supported by IT, reflecting IT integration.
def it_activities_and_proportion(df):
    # IT activities for each model_id
    it_activities = df[df['category'] == 'ITSystem'].groupby('model_id').apply(
        lambda group: group['outgoing_count'].sum() + group['ingoing_count'].sum()
    ).reset_index(name='it_activities')
    
    # Total number of tasks and subprocesses for each model_id
    task_subprocess_count = df[df['category'].str.contains('Task|Subprocess')].groupby('model_id').size().reset_index(name='task_subprocess_count')
    
    result = pd.merge(it_activities, task_subprocess_count, on='model_id', how='left') 
    # Proportion
    result['it_activities_proportion'] = result['it_activities'] / result['task_subprocess_count']
    
    return result

