from jmetal.algorithm import NSGAII
from jmetal.algorithm.multiobjective import randomSearch
from jmetal.component.comparator import RankingAndCrowdingDistanceComparator
from jmetal.operator import  SP, BitFlip, BinaryTournamentSelection
from miniaturization import Miniaturization
from jmetal.component.quality_indicator import HyperVolume
from jmetal.util.laboratory import experiment, display

algorithm = [
    (NSGAII, {'population_size': 10, 'max_evaluations': 250, 'mutation': BitFlip(probability=0.04), 'crossover': SP(probability=0.9),
              'selection': BinaryTournamentSelection(RankingAndCrowdingDistanceComparator())}),
    (randomSearch, {'max_evaluations': 250})
]
metric = [HyperVolume(reference_point=[1, 1, 1, 1])]
problem = [(Miniaturization, {})]

results = experiment(algorithm, metric, problem)
display(results)