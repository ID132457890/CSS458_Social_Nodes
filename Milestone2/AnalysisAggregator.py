import Model
import DataExporter
import numpy as np
import Personality
import Person


class AnalysisAggregator(object):
    def __init__(self):
        self.results = []

    def reset(self):
        self.results = []

    def collector(self, model, round_totals, data_map):
        self.results.append(round_totals)

    def simple_exec(self, reset = True, repeat = 3, modifications = None, **kwargs):
        if reset == True:
            self.reset()

        for x in range(repeat):
            m = Model.Model(**kwargs)
            restore = []

            if modifications != None:
                for mod in modifications:
                    if hasattr(mod[0], '__call__'):
                        mod[0](m)
                    else:
                        restore.append((mod[0], eval(mod[0])))
                        exec("%s=%s" % (mod[0], mod[1]))
            m.run_simulation()

            for item in restore:
                exec("%s=%s" % (item[0], item[1]))

        result_array = np.zeros((repeat,5))
        for x in range(len(self.results)):
            test = self.results[x]
            for round in test:
                result_array[x, 0] += round['num_messages_sent'] / round['num_online_agents']
                result_array[x, 1] += round['num_messages_received'] / round['num_online_agents']
                result_array[x, 2] += round['num_total_friend'] / round['num_online_agents']
                result_array[x, 3] += round['num_total_enemies'] / round['num_online_agents']
                result_array[x, 4] += round['num_knowledge'] / round['num_online_agents']

            result_array[x] = result_array[x] / len(test)

        return (np.average(result_array[:, 0]), np.std(result_array[:, 0]),
                np.average(result_array[:, 1]), np.std(result_array[:, 1]),
                np.average(result_array[:, 2]), np.std(result_array[:, 2]),
                np.average(result_array[:, 3]), np.std(result_array[:, 3]),
                np.average(result_array[:, 4]), np.std(result_array[:, 4]))

result_list = []

a = AnalysisAggregator()
#----------------
# Tests as agent count increases

result_list.append(("20% fame",
                    a.simple_exec(modifications=(("Personality.percent_probability_famous", 20),),
                                  num_agents=200, topics=10, data_collector=DataExporter.DataExporter,
                                  time_to_run=10, data_collector_results=a.collector, log_level=10)))
result_list.append(("50% fame",
                    a.simple_exec(modifications=(("Personality.percent_probability_famous", 50),),
                                  num_agents=200, topics=10, data_collector=DataExporter.DataExporter,
                                  time_to_run=10, data_collector_results=a.collector, log_level=10)))
result_list.append(("dft fame",
                    a.simple_exec(num_agents=200, topics=10, data_collector=DataExporter.DataExporter,
                                  time_to_run=10, data_collector_results=a.collector, log_level=10)))
"""
result_list.append((" 50A 10T",
                    a.simple_exec(num_agents=50, topics=10, data_collector=DataExporter.DataExporter,
                                  time_to_run=5, data_collector_results=a.collector, log_level=10)))

result_list.append(("100A 10T",
                    a.simple_exec(num_agents=100, topics=10, data_collector=DataExporter.DataExporter,
                                  time_to_run=20, data_collector_results=a.collector, log_level=10)))
result_list.append(("200A 10T",
                    a.simple_exec(num_agents=200, topics=10, data_collector=DataExporter.DataExporter,
                                  time_to_run=20, data_collector_results=a.collector, log_level=10)))
result_list.append(("300A 10T",
                    a.simple_exec(num_agents=300, topics=10, data_collector=DataExporter.DataExporter,
                                  time_to_run=20, data_collector_results=a.collector, log_level=10)))
result_list.append(("400A 10T",
                    a.simple_exec(num_agents=400, topics=10, data_collector=DataExporter.DataExporter,
                                  time_to_run=20, data_collector_results=a.collector, log_level=10)))
result_list.append(("500A 10T",
                    a.simple_exec(num_agents=500, topics=10, data_collector=DataExporter.DataExporter,
                                  time_to_run=20, data_collector_results=a.collector, log_level=10)))

#----------------
# Tests as topic count increases
result_list.append(("200A 10T",
                    a.simple_exec(num_agents=200, topics=10, data_collector=DataExporter.DataExporter,
                                  time_to_run=20, data_collector_results=a.collector, log_level=10)))
result_list.append(("200A 20T",
                    a.simple_exec(num_agents=200, topics=20, data_collector=DataExporter.DataExporter,
                                  time_to_run=20, data_collector_results=a.collector, log_level=10)))
result_list.append(("200A 40T",
                    a.simple_exec(num_agents=200, topics=40, data_collector=DataExporter.DataExporter,
                                  time_to_run=20, data_collector_results=a.collector, log_level=10)))

result_list.append(("200A 80T",
                    a.simple_exec(num_agents=200, topics=80, data_collector=DataExporter.DataExporter,
                                  time_to_run=20, data_collector_results=a.collector, log_level=10)))
result_list.append(("200A 160T",
                    a.simple_exec(num_agents=200, topics=160, data_collector=DataExporter.DataExporter,
                                  time_to_run=20, data_collector_results=a.collector, log_level=10)))
result_list.append(("200A 320T",
                    a.simple_exec(num_agents=200, topics=320, data_collector=DataExporter.DataExporter,
                                  time_to_run=20, data_collector_results=a.collector, log_level=10)))

#----------------
# Tests as round count increases
result_list.append(("10 Turn  ",
                    a.simple_exec(num_agents=100, topics=30, data_collector=DataExporter.DataExporter,
                                  time_to_run=10, data_collector_results=a.collector, log_level=10)))
result_list.append(("20 Turn  ",
                    a.simple_exec(num_agents=100, topics=30, data_collector=DataExporter.DataExporter,
                                  time_to_run=20, data_collector_results=a.collector, log_level=10)))
result_list.append(("40 Turn  ",
                    a.simple_exec(num_agents=100, topics=30, data_collector=DataExporter.DataExporter,
                                  time_to_run=40, data_collector_results=a.collector, log_level=10)))

result_list.append(("80 Turn  ",
                    a.simple_exec(num_agents=100, topics=30, data_collector=DataExporter.DataExporter,
                                  time_to_run=80, data_collector_results=a.collector, log_level=10)))
result_list.append(("160 Turn ",
                    a.simple_exec(num_agents=100, topics=30, data_collector=DataExporter.DataExporter,
                                  time_to_run=160, data_collector_results=a.collector, log_level=10)))
result_list.append(("320 Turn ",
                    a.simple_exec(num_agents=100, topics=30, data_collector=DataExporter.DataExporter,
                                  time_to_run=320, data_collector_results=a.collector, log_level=10)))
"""

print("Test           Sent      Dev       Resent      Dev         Friend      Dev         Enemy       Dev         Known       Dev")
for result in result_list:
    print("%s %10.2f\t%10.2f\t%10.2f\t%10.2f\t%10.2f\t%10.2f\t%10.2f\t%10.2f\t%10.2f\t%10.2f\t" %
          (result[0], result[1][0],result[1][1],result[1][2],result[1][3],result[1][4],result[1][5]
           , result[1][6],result[1][7],result[1][8],result[1][9]))