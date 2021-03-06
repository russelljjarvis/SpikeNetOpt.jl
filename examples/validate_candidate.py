import sciunit
from networkunit import models, tests, scores, plots, capabilities
import sciunit
import neo
import numpy as np
from networkunit import tests, scores, models
from networkunit.capabilities.cap_ProducesSpikeTrains import ProducesSpikeTrains
import julia
from julia.api import JuliaInfo
from julia import Base
import julia

try:
    from julia import Julia
    from julia.api import Julia
except:
    julia.install()
    from julia import Julia
    from julia.api import Julia

jl = Julia(compiled_modules=False)
from julia import Main
import matplotlib

matplotlib.use("agg")

import matplotlib.pyplot as plt

from networkunit.capabilities.cap_ProducesSpikeTrains import ProducesSpikeTrains
from networkunit.plots.plot_rasterplot import rasterplot

from networkunit import models, tests, scores, plots, capabilities
from networkunit.plots import sample_histogram
import neo
import numpy as np
import quantities as qt
import sciunit

jl.using("JLD")

exec_string = """
if isfile("GAsolution.jld")
    spkd_ground = load("GAsolution.jld","spkd_ground")
    spkd_found = load("GAsolution.jld","spkd_found")
    Ne = load("GAsolution.jld","Ne")
    Ni = load("GAsolution.jld","Ni")
    sim_length = load("GAsolution.jld","sim_length")
end
"""
Main.eval(exec_string)

spkd_found = Main.spkd_found
spkd_ground = Main.spkd_ground
Ni = Main.Ni
Ne = Main.Ne
sim_length = Main.sim_length

# spkd_found = Main.spkd_found
# spkd_ground = Main.spkd_ground


class polychrony_data(models.spiketrain_data, ProducesSpikeTrains):
    """
    Re-define NetworkUnits
    """

    def __init__(self, t_stop, Ne, Ni, spike_times):
        self = self
        self.t_start = 0
        self.t_stop = t_stop
        self.nbr_neurons = Ne
        self.spike_times = spike_times
        spiketrains = [[]] * self.nbr_neurons
        n = 0
        for i, st in enumerate(self.spike_times[0]):
            spiketrains[i] = neo.core.SpikeTrain(
                st, units="ms", t_start=self.t_start, t_stop=self.t_stop
            )
        self.spiketrains = spiketrains

    def produce_spiketrains(self, **kwargs):
        """
        overwrites function in capability class ProduceSpiketrains
        """
        return self.spiketrains

    def show_rasterplot(self, **kwargs):
        return rasterplot(self.spiketrains, **kwargs)


class FR_test_class(sciunit.TestM2M, tests.firing_rate_test):
    score_type = scores.effect_size


class LV_test_class(sciunit.TestM2M, tests.isi_variation_test):
    score_type = scores.effect_size
    params = {"variation_measure": "lv"}


class isi_ttest_class(sciunit.TestM2M, tests.isi_variation_test):
    score_type = scores.students_t
    params = {"variation_measure": "isi"}

    def compute_score(self, prediction1, prediction2):
        score = self.score_type.compute(prediction1, prediction2, **self.params)
        return score


m1 = polychrony_data(sim_length, Ne, Ni, spkd_ground)  # ,name='ground truth')
m2 = polychrony_data(sim_length, Ne, Ni, spkd_found)  # ,name='optimized candidate')
FR_test = FR_test_class()
LV_test = LV_test_class()
isi_ttest = isi_ttest_class()


class fr_ttest_class(sciunit.TestM2M, tests.firing_rate_test):
    score_type = scores.students_t
    params = {"equal_var": False}  # True: Student's t-test; False: Welch's t-test

    def compute_score(self, prediction1, prediction2):
        score = self.score_type.compute(prediction1, prediction2, **self.params)
        return score


class fr_effect_class(sciunit.TestM2M, tests.firing_rate_test):
    score_type = scores.effect_size


fr_effect = fr_effect_class()


fr_ttest = fr_ttest_class(equal_var=False)
pred0 = fr_ttest.generate_prediction(m1)
pred1 = fr_ttest.generate_prediction(m2)
score = fr_ttest.compute_score(pred0, pred1)
print(score)
# plot results
fig, ax = plt.subplots(ncols=2, sharey=True, gridspec_kw={"wspace": 0}, figsize=(20, 8))
# FR_test.generate_prediction(C);
# FR_test.generate_prediction(m1)
FR_test.visualize_samples(
    m1, m2, ax=ax[0], var_name="Firing Rate (Hz)", bins=45, density=True, c="b"
)
LV_test.visualize_samples(
    m1, m2, ax=ax[1], var_name="Local Variation", bins=45, density=True, c="r"
)
fig.savefig("firing_rates.png")
fig, ax = plt.subplots(ncols=1, gridspec_kw={"wspace": 0}, figsize=(20, 8))
LV_test.visualize_samples(m1, m2, ax=ax, var_name="LV", bins=30, density=False)
fig.savefig("isi_tests.png")
# ax1 =
m1.show_rasterplot()
fig, ax = plt.subplots(ncols=1, gridspec_kw={"wspace": 0}, figsize=(20, 8))

ax = sample_histogram(m1.spiketrains[1], m2.spiketrains[1], ax=ax)
fig.savefig("histogram.png")

# print(dir(ax1))
# ax2 =
# m2.show_rasterplot()
# fig.savefig("raster.png")
# fig2.savefig("raster2.png")

"""
Not using this code


class fr_mwu_class(sciunit.TestM2M, tests.firing_rate_test):
    score_type = scores.mwu_statistic


fr_mwu = fr_mwu_class()

class fr_ttest_class(sciunit.TestM2M, tests.firing_rate_test):
    score_type = scores.students_t
    params = {"equal_var": False}  # True: Student's t-test; False: Welch's t-test

    def compute_score(self, prediction1, prediction2):
        score = self.score_type.compute(prediction1, prediction2, **self.params)
        return score


fr_ttest = fr_ttest_class(equal_var=False)
"""
"""
class isi_effect_class(sciunit.TestM2M, tests.isi_variation_test):
    score_type = scores.effect_size
    params = {"variation_measure": "isi"}

    def compute_score(self, prediction1, prediction2):
        score = self.score_type.compute(prediction1, prediction2, **self.params)
        return score


isi_effect = isi_effect_class()


class isi_mwu_class(sciunit.TestM2M, tests.isi_variation_test):
    score_type = scores.mwu_statistic
    params = {"variation_measure": "isi"}

    def compute_score(self, prediction1, prediction2):
        score = self.score_type.compute(prediction1, prediction2, **self.params)
        return score


isi_mwu = isi_mwu_class()

"""
