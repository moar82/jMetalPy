import sys
from jmetal.algorithm import NSGAII
from jmetal.component import VisualizerObserver, ProgressBarObserver, RankingAndCrowdingDistanceComparator
from miniaturization import Miniaturization
from jmetal.operator import SP, BitFlip, BinaryTournamentSelection
from jmetal.util import  SolutionList
from jmetal.component.quality_indicator import HyperVolume


if __name__ == '__main__':
    problem = Miniaturization()
    if  len (sys.argv) < 3:
        print ('You must provide 2 arguments: number of run, js script to miniaturize')
        sys.exit(1)
    else:
        problem.run_id = '_' + sys.argv[1] # we use this value to name the solution output
        problem.script = sys.argv[2] # we parametrize the script
    algorithm = NSGAII(
        problem=problem,
        population_size=10,
        max_evaluations=250,
        mutation=BitFlip(probability=0.1), #the best according to our test
        crossover=SP(probability=0.8),#the best according to our test
        selection=BinaryTournamentSelection(comparator=RankingAndCrowdingDistanceComparator())
    )

    ##observer = VisualizerObserver(problem)
    progress_bar = ProgressBarObserver(step=10, maximum=250)
    ##algorithm.observable.register(observer=observer)
    algorithm.observable.register(observer=progress_bar)

    algorithm.run()
    front = algorithm.get_result()

    ## Plot frontier to file
    ##pareto_front = ScatterMatplotlib(plot_title='NSGAII for IoT-Min', number_of_objectives=problem.number_of_objectives)
    ##pareto_front.plot(front, reference=problem.get_reference_front(), output='NSGAII-IoT-Min', show=False)

    ## Save variables to file
    SolutionList.print_function_values_to_file(front, 'FUN.NSGAII.'  + problem.script + '.' + problem.run_id.replace('_','')  +
                                               '.' + problem.get_name())
    SolutionList.print_variables_to_file(front, 'VAR.NSGAII.' + problem.script + '.' + problem.run_id.replace('_','')  +
                                          '.' + problem.get_name())
    reference_point = [1, 1, 1]
    #reference_point = [1, 1, 1 ,1]
    hv = HyperVolume(reference_point)
    value = hv.compute(front)
    with open("HV." + problem.script + '.' +problem.run_id.replace('_','')  + '.' + problem.get_name(), "w") as text_file:
        print(f"{value}", file=text_file)
    print('Algorithm (binary problem): ' + algorithm.get_name())
    print('Problem: ' + problem.get_name())
    print ('HyperVolume: %f' % value)
    print('Computing time: ' + str(algorithm.total_computing_time))
    problem.sf.plog.logError('Run: ' + problem.run_id.replace('_','') + ' js script: ' + problem.script + '\n')
    problem.sf.plog.logError('Computing time: ' + str(algorithm.total_computing_time)+ '\n')
    problem.sf.plog.logError('Repeated solutions:'+str(len(problem.sf.js_engine_helper.tested_solutions))+'\n')
    problem.save_values_achieved(front,'values_achieved_'+problem.script.split('.')[0] + problem.run_id.replace('_','') + '.csv')
