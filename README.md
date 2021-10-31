# Description
A Network and single cell spiking neuron optimizer written in Julia.
### Motivation
[Previous attempts](https://github.com/russelljjarvis/BluePyOpt/blob/neuronunit_reduced_cells/examples/neuronunit/OptimizationMulitSpikingIzhikevichModel.ipynb)
 to do data driven optimization of spiking neurons in Python where slower and more complex than they needed to be. Reduced model spiking neurons models have compact equations, and they should be fast to simulate, but Python often calls external codes and programes (C,C++,NEURON,brian2,NEST,PyNN) to achieve a speed up for network simulations, however approaches for speeding up network simulations are not efficient for speeding up single cell simulations.  This strategy of calling external code causes an intolerable run-time cost for single neuron simulations. The Python tool numba JIT partially remedies this problem, however code from the Python optimization framework DEAP/BluePyOpt also induces an additional overhead. An almost pure Julia SNN optimization routine seems to be the solution to efficient optimization of Reduced SNN models.

- The Evolutionary.jl package provides Genetic Algorithms that are used to optimize spiking neural networks

- In a network the loss function is constructed by computing Spike Distance between all pairs of neurons
Networks are optimized using pair wise spike-distance metric on each pair of neurons
Pythons NetworkUnit package is used to perform a posthoc evaluation of the optimized network.

<!---See the figure below where local variation and firing rates are compared against every neuron between two model networks.-->

For example this is a ground truth model versus an optimized model t-test of firing rates:
```
Student's t-test
	datasize: 200 	 200
	t = 11.811 	 p value = 1.82e-25
```


# DONE

- [x] Used spike distance and genetic algorithms to optimize networks quickly
- [x] Implemented multi-threading
- [x] Used pythons NetworkUnit to validate results
- [x] NetworkUnit t-tests of results
- [x] Created single cell model fitting to Allen Brain Observatory Spike Train Data.
- [x] Implemented multi-threading
## TODO
- [ ] Parallel Coprocessor Based GA fitness calculation in Evolutionary.jl.] Implemented multi-processing
- [ ] Animation of Genetic Algorithm Convergence.
- [ ] Different Spiking Neural Network Backends (WaspNet.jl,SpikingNN.jl)
@russelljjarvis
- [ ] Multiprocessing as opposed to multi-threading
- [ ] GPU
- [ ] NeuroEvolution @russelljjarvis
- [ ] ADAM-Opt predictions using evolved population.
