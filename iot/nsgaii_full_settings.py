from jmetal.algorithm import NSGAII
from jmetal.component import VisualizerObserver, ProgressBarObserver, RankingAndCrowdingDistanceComparator
from miniaturization import Miniaturization
from jmetal.operator import SP, BitFlip, BinaryTournamentSelection
from jmetal.util import ScatterMatplotlib, SolutionList


if __name__ == '__main__':
    problem = Miniaturization()

    algorithm = NSGAII(
        problem=problem,
        population_size=100,
        max_evaluations=25000,
        mutation=BitFlip(probability=0.04), #use the same values that in MoMS
        crossover=SP(probability=0.9),#use the same values that in MoMS
        selection=BinaryTournamentSelection(comparator=RankingAndCrowdingDistanceComparator())
    )

    observer = VisualizerObserver(problem)
    progress_bar = ProgressBarObserver(step=100, maximum=25000)
    algorithm.observable.register(observer=observer)
    algorithm.observable.register(observer=progress_bar)

    algorithm.run()
    front = algorithm.get_result()

    # Plot frontier to file
    pareto_front = ScatterMatplotlib(plot_title='NSGAII for IoT-Min', number_of_objectives=problem.number_of_objectives)
    pareto_front.plot(front, reference=problem.get_reference_front(), output='NSGAII-IoT-Min', show=False)

    # Save variables to file
    SolutionList.print_function_values_to_file(front, 'FUN.NSGAII.' + problem.get_name())
    SolutionList.print_variables_to_file(front, 'VAR.NSGAII.' + problem.get_name())

    print('Algorithm (binary problem): ' + algorithm.get_name())
    print('Problem: ' + problem.get_name())
    print('Computing time: ' + str(algorithm.total_computing_time))
