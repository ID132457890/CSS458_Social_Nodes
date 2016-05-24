import Model
import DataExporter
import ModelMangler
import numpy as np

results = []

def collector(model, round_totals, data_map):
    results.append(round_totals)

def simple_exec(**kwargs):
    for x in range(10):
        m = Model.Model(**kwargs)
        m.run_simulation()

    total_posts = 0
    total_recv = 0
    total_friends = 0
    total_enemies = 0
    total_knowledge = 0

    result_array = np.zeros((10,5))
    for x in range(len(results)):
        test = results[x]
        for round in test:
            result_array[x, 0] += round['num_messages_sent']
            result_array[x, 1] += round['num_messages_received']
            result_array[x, 2] += round['num_total_friend']
            result_array[x, 3] += round['num_total_enemies']
            result_array[x, 4] += round['num_knowledge']

        print ("avg sent %r \t\t std dev %r" % (np.average(result_array[:,0]), np.std(result_array[:,0])))
        print("avg rcv %r \t\t std dev %r" % (np.average(result_array[:, 1]), np.std(result_array[:, 1])))
        print("avg friends %r \t\t std dev %r" % (np.average(result_array[:, 2]), np.std(result_array[:, 2])))
        print("avg enemies %r \t\t std dev %r" % (np.average(result_array[:, 3]), np.std(result_array[:, 3])))
        print("avg known %r \t\t std dev %r" % (np.average(result_array[:, 4]), np.std(result_array[:, 4])))

print ("Averages with 50 agents, 10 topics:")
simple_exec(num_agents = 50, topics = 10, data_collector = DataExporter.DataExporter,
                        data_collector_results = collector, log_level = 10)

results = []

print ("Averages with 200 agents, 10 topics:")
simple_exec(num_agents=50, topics=10, data_collector=DataExporter.DataExporter,
            data_collector_results=collector, log_level=10)

results = []

print ("Averages with 50 agents, 50 topics:")
simple_exec(num_agents=50, topics=50, data_collector=DataExporter.DataExporter,
            data_collector_results=collector, log_level=10)
results = []
print ("Averages with 200 agents, 50 topics:")
simple_exec(num_agents=200, topics=50, data_collector=DataExporter.DataExporter,
            data_collector_results=collector, log_level=10)
