from .metrics import log_metrics
from .process.handler import PreprocessHandler
from .train.handler import ModelHandler
from .essentials.handler import EssentialsHandler
from .graph import Graph


def generate_file(graph, target_column,task_type,colab=False):
    g = Graph(len(graph['nodes']))
    map = {}
    j=0
    while j <(len(graph['nodes'])):
        for i in graph['nodes']:
            map[(i['id'])]=j
            j+=1
    map2 = {y: x for x, y in map.items()}
    for i in graph['edges']:
        g.addEdge(map[i['source']], map[i['target']])
    res=g.topologicalSort()
    steps=[]
    for i in res:
        steps.append(map2[i])
    steps_list={}
    for i in steps:
        for j in range(len(graph['nodes'])):
            if i == graph['nodes'][j]['id']:
                steps_list[(graph['nodes'][j]['data']['name'])]=graph['nodes'][j]['data']['node_type']
    if colab:
      output_file = "/content/output.py"
    else:
      output_file = "output.py"
    with open(output_file, "w") as f:
        f.write("import huble\n")
        
        for i in steps_list:
            for node in graph['nodes']:
                if i == node['data']['name']:
                    print(node['data']['name'])
                    if steps_list[i]=='preprocess':
                        preprocess = PreprocessHandler()
                        f.write(preprocess.return_function(function_name=node['data']['name'], params=node['data']['parameters']))
                        f.write("\n")
                    elif steps_list[i] == 'model':
                        train = ModelHandler()
                        f.write(train.return_function(function_name=node['data']['name'], params=node['data']['parameters']))
                        f.write("\n")
                    elif steps_list[i] == 'essential':
                        essentials = EssentialsHandler()
                        f.write(essentials.return_function(function_name=node['data']['name'], params=node['data']['parameters']))
                        f.write("\n")
                    elif steps_list[i] == 'evaluate_model':
                        f.write(f"metrics = huble.evaluate_model(model=Model, test_dataset=test_dataset, target_column= '{target_column}', task_type='{task_type}' )")
                        f.write("\n")
                    elif steps_list[i] == 'primary_dataset':
                        f.write("df = Dataset()")
                        f.write(f"data=df.load_dataset('{node['data']['url']}')")
                        f.write("\n")





