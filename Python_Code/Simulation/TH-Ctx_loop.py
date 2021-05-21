import copy
import matplotlib.pyplot as plt
from dipde.internals.internalpopulation import InternalPopulation
from dipde.internals.externalpopulation import ExternalPopulation
from dipde.internals.network import Network
from dipde.internals.simulation import Simulation
from dipde.internals.simulationconfiguration import SimulationConfiguration
from dipde.internals.connection import Connection as Connection
import itertools
import logging
# from brian.neurongroup import network
logging.disable(logging.CRITICAL) # pragma: no cover

def get_network(dv = .0001):

    nsyn_background = {
        ('SSp-m_Ips', 'e'): 1600,
        ('SSp-m_Ips', 'i'): 1500,
        ('SSp-m_Con', 'e'): 1600,
        ('SSp-m_Con', 'i'): 1500,
        ('SSs_Ips', 'e'): 2100,
        ('SSs_Ips', 'i'): 1900,
        ('SSs_Con', 'e'): 2100,
        ('SSs_Con', 'i'): 1900,
        ('MOp_Ips', 'e'): 2000,
        ('MOp_Ips', 'i'): 1900,
        ('MOp_Con', 'e'): 2000,
        ('MOp_Con', 'i'): 1900,
        ('LGv_Ips', 'e'): 2100,
        ('LGv_Ips', 'i'): 1900,
        ('LGv_Con', 'e'): 2100,
        ('LGv_Con', 'i'): 1900,
        ('LGd_Ips', 'e'): 2000,
        ('LGd_Ips', 'i'): 1900,
        ('LGd_Con', 'e'): 2000,
        ('LGd_Con', 'i'): 1900,
        ('VPM_Ips', 'e'): 2000,
        ('VPM_Ips', 'i'): 1900,
        ('VPM_Con', 'e'): 2000,
        ('VPM_Con', 'i'): 1900,
        ('VPMpc_Ips', 'e'): 2000,
        ('VPMpc_Ips', 'i'): 1900,
        ('VPMpc_Con', 'e'): 2000,
        ('VPMpc_Con', 'i'): 1900
    }

    background_firing_rate = 8
    
    background_delay = {
        'e': 0.005,
        'i': 0.0
    }
    
    internal_population_sizes = {
        ('SSp-m_Ips', 'e'): 19881,
        ('SSp-m_Ips', 'i'): 19881/4,
        ('SSp-m_Con', 'e'): 19881,
        ('SSp-m_Con', 'i'): 19881/4,
        ('SSs_Ips', 'e'): 28874,
        ('SSs_Ips', 'i'): 28874/4,
        ('SSs_Con', 'e'): 28874,
        ('SSs_Con', 'i'): 28874/4,
        ('MOp_Ips', 'e'): 36330,
        ('MOp_Ips', 'i'): 36330/4,
        ('MOp_Con', 'e'): 36330,
        ('MOp_Con', 'i'): 36330/4,
        ('LGv_Ips', 'e'): 1295,
        ('LGv_Ips', 'i'): 1295/4,
        ('LGv_Con', 'e'): 1295,
        ('LGv_Con', 'i'): 1295/4,
        ('LGd_Ips', 'e'): 2311,
        ('LGd_Ips', 'i'): 2311/4,
        ('LGd_Con', 'e'): 2311,
        ('LGd_Con', 'i'): 2311/4,
        ('VPM_Ips', 'e'): 5263,
        ('VPM_Ips', 'i'): 5263/4,
        ('VPM_Con', 'e'): 5263,
        ('VPM_Con', 'i'): 5263/4,
        ('VPMpc_Ips', 'e'): 686,
        ('VPMpc_Ips', 'i'): 686/4,
        ('VPMpc_Con', 'e'): 686,
        ('VPMpc_Con', 'i'): 686/4
    }
    
    connection_probabilities = {(('VPM_Ips','e'),('VPMpc_Ips','e')):0.013,(('VPM_Ips','e'),('VPMpc_Ips','i')):0.007,(('VPM_Ips','i'),('VPMpc_Ips','e')):0.001,(('VPM_Ips','i'),('VPMpc_Ips','i')):0.001,(('VPM_Ips','e'),('SSs_Ips','e')):0.000,(('VPM_Ips','e'),('SSs_Ips','i')):0.000,(('VPM_Ips','i'),('SSs_Ips','e')):0.000,(('VPM_Ips','i'),('SSs_Ips','i')):0.000,(('VPM_Ips','e'),('VPM_Con','e')):0.068,(('VPM_Ips','e'),('VPM_Con','i')):0.034,(('VPM_Ips','i'),('VPM_Con','e')):0.007,(('VPM_Ips','i'),('VPM_Con','i')):0.007,(('VPM_Ips','e'),('SSs_Con','e')):0.001,(('VPM_Ips','e'),('SSs_Con','i')):0.001,(('VPM_Ips','i'),('SSs_Con','e')):0.000,(('VPM_Ips','i'),('SSs_Con','i')):0.000,(('VPM_Ips','e'),('SSp-m_Con','e')):0.000,(('VPM_Ips','e'),('SSp-m_Con','i')):0.000,(('VPM_Ips','i'),('SSp-m_Con','e')):0.000,(('VPM_Ips','i'),('SSp-m_Con','i')):0.000,(('VPM_Ips','e'),('LGv_Ips','e')):0.001,(('VPM_Ips','e'),('LGv_Ips','i')):0.000,(('VPM_Ips','i'),('LGv_Ips','e')):0.000,(('VPM_Ips','i'),('LGv_Ips','i')):0.000,(('VPM_Ips','e'),('VPM_Ips','e')):0.014,(('VPM_Ips','e'),('VPM_Ips','i')):0.007,(('VPM_Ips','i'),('VPM_Ips','e')):0.001,(('VPM_Ips','i'),('VPM_Ips','i')):0.001,(('VPM_Ips','e'),('MOp_Ips','e')):0.011,(('VPM_Ips','e'),('MOp_Ips','i')):0.006,(('VPM_Ips','i'),('MOp_Ips','e')):0.001,(('VPM_Ips','i'),('MOp_Ips','i')):0.001,(('VPM_Ips','e'),('MOp_Con','e')):0.050,(('VPM_Ips','e'),('MOp_Con','i')):0.025,(('VPM_Ips','i'),('MOp_Con','e')):0.005,(('VPM_Ips','i'),('MOp_Con','i')):0.005,(('VPM_Ips','e'),('VPMpc_Con','e')):0.006,(('VPM_Ips','e'),('VPMpc_Con','i')):0.003,(('VPM_Ips','i'),('VPMpc_Con','e')):0.001,(('VPM_Ips','i'),('VPMpc_Con','i')):0.001,(('VPM_Ips','e'),('SSp-m_Ips','e')):0.000,(('VPM_Ips','e'),('SSp-m_Ips','i')):0.000,(('VPM_Ips','i'),('SSp-m_Ips','e')):0.000,(('VPM_Ips','i'),('SSp-m_Ips','i')):0.000,(('VPM_Ips','e'),('LGd_Con','e')):0.000,(('VPM_Ips','e'),('LGd_Con','i')):0.000,(('VPM_Ips','i'),('LGd_Con','e')):0.000,(('VPM_Ips','i'),('LGd_Con','i')):0.000,(('VPM_Ips','e'),('LGd_Ips','e')):0.118,(('VPM_Ips','e'),('LGd_Ips','i')):0.059,(('VPM_Ips','i'),('LGd_Ips','e')):0.012,(('VPM_Ips','i'),('LGd_Ips','i')):0.012,(('VPM_Ips','e'),('LGv_Con','e')):0.003,(('VPM_Ips','e'),('LGv_Con','i')):0.002,(('VPM_Ips','i'),('LGv_Con','e')):0.000,(('VPM_Ips','i'),('LGv_Con','i')):0.000,(('LGd_Ips','e'),('VPMpc_Ips','e')):0.009,(('LGd_Ips','e'),('VPMpc_Ips','i')):0.004,(('LGd_Ips','i'),('VPMpc_Ips','e')):0.001,(('LGd_Ips','i'),('VPMpc_Ips','i')):0.001,(('LGd_Ips','e'),('SSs_Ips','e')):0.000,(('LGd_Ips','e'),('SSs_Ips','i')):0.000,(('LGd_Ips','i'),('SSs_Ips','e')):0.000,(('LGd_Ips','i'),('SSs_Ips','i')):0.000,(('LGd_Ips','e'),('VPM_Con','e')):0.019,(('LGd_Ips','e'),('VPM_Con','i')):0.009,(('LGd_Ips','i'),('VPM_Con','e')):0.002,(('LGd_Ips','i'),('VPM_Con','i')):0.002,(('LGd_Ips','e'),('SSs_Con','e')):0.000,(('LGd_Ips','e'),('SSs_Con','i')):0.000,(('LGd_Ips','i'),('SSs_Con','e')):0.000,(('LGd_Ips','i'),('SSs_Con','i')):0.000,(('LGd_Ips','e'),('SSp-m_Con','e')):0.000,(('LGd_Ips','e'),('SSp-m_Con','i')):0.000,(('LGd_Ips','i'),('SSp-m_Con','e')):0.000,(('LGd_Ips','i'),('SSp-m_Con','i')):0.000,(('LGd_Ips','e'),('LGv_Ips','e')):0.003,(('LGd_Ips','e'),('LGv_Ips','i')):0.002,(('LGd_Ips','i'),('LGv_Ips','e')):0.000,(('LGd_Ips','i'),('LGv_Ips','i')):0.000,(('LGd_Ips','e'),('VPM_Ips','e')):0.000,(('LGd_Ips','e'),('VPM_Ips','i')):0.000,(('LGd_Ips','i'),('VPM_Ips','e')):0.000,(('LGd_Ips','i'),('VPM_Ips','i')):0.000,(('LGd_Ips','e'),('MOp_Ips','e')):0.002,(('LGd_Ips','e'),('MOp_Ips','i')):0.001,(('LGd_Ips','i'),('MOp_Ips','e')):0.000,(('LGd_Ips','i'),('MOp_Ips','i')):0.000,(('LGd_Ips','e'),('MOp_Con','e')):0.064,(('LGd_Ips','e'),('MOp_Con','i')):0.032,(('LGd_Ips','i'),('MOp_Con','e')):0.006,(('LGd_Ips','i'),('MOp_Con','i')):0.006,(('LGd_Ips','e'),('VPMpc_Con','e')):0.001,(('LGd_Ips','e'),('VPMpc_Con','i')):0.000,(('LGd_Ips','i'),('VPMpc_Con','e')):0.000,(('LGd_Ips','i'),('VPMpc_Con','i')):0.000,(('LGd_Ips','e'),('SSp-m_Ips','e')):0.000,(('LGd_Ips','e'),('SSp-m_Ips','i')):0.000,(('LGd_Ips','i'),('SSp-m_Ips','e')):0.000,(('LGd_Ips','i'),('SSp-m_Ips','i')):0.000,(('LGd_Ips','e'),('LGd_Con','e')):0.000,(('LGd_Ips','e'),('LGd_Con','i')):0.000,(('LGd_Ips','i'),('LGd_Con','e')):0.000,(('LGd_Ips','i'),('LGd_Con','i')):0.000,(('LGd_Ips','e'),('LGd_Ips','e')):0.009,(('LGd_Ips','e'),('LGd_Ips','i')):0.005,(('LGd_Ips','i'),('LGd_Ips','e')):0.001,(('LGd_Ips','i'),('LGd_Ips','i')):0.001,(('LGd_Ips','e'),('LGv_Con','e')):0.000,(('LGd_Ips','e'),('LGv_Con','i')):0.000,(('LGd_Ips','i'),('LGv_Con','e')):0.000,(('LGd_Ips','i'),('LGv_Con','i')):0.000,(('SSp-m_Ips','e'),('VPMpc_Ips','e')):0.005,(('SSp-m_Ips','e'),('VPMpc_Ips','i')):0.003,(('SSp-m_Ips','i'),('VPMpc_Ips','e')):0.001,(('SSp-m_Ips','i'),('VPMpc_Ips','i')):0.001,(('SSp-m_Ips','e'),('SSs_Ips','e')):0.000,(('SSp-m_Ips','e'),('SSs_Ips','i')):0.000,(('SSp-m_Ips','i'),('SSs_Ips','e')):0.000,(('SSp-m_Ips','i'),('SSs_Ips','i')):0.000,(('SSp-m_Ips','e'),('VPM_Con','e')):0.006,(('SSp-m_Ips','e'),('VPM_Con','i')):0.003,(('SSp-m_Ips','i'),('VPM_Con','e')):0.001,(('SSp-m_Ips','i'),('VPM_Con','i')):0.001,(('SSp-m_Ips','e'),('SSs_Con','e')):0.000,(('SSp-m_Ips','e'),('SSs_Con','i')):0.000,(('SSp-m_Ips','i'),('SSs_Con','e')):0.000,(('SSp-m_Ips','i'),('SSs_Con','i')):0.000,(('SSp-m_Ips','e'),('SSp-m_Con','e')):0.000,(('SSp-m_Ips','e'),('SSp-m_Con','i')):0.000,(('SSp-m_Ips','i'),('SSp-m_Con','e')):0.000,(('SSp-m_Ips','i'),('SSp-m_Con','i')):0.000,(('SSp-m_Ips','e'),('LGv_Ips','e')):0.001,(('SSp-m_Ips','e'),('LGv_Ips','i')):0.001,(('SSp-m_Ips','i'),('LGv_Ips','e')):0.000,(('SSp-m_Ips','i'),('LGv_Ips','i')):0.000,(('SSp-m_Ips','e'),('VPM_Ips','e')):0.000,(('SSp-m_Ips','e'),('VPM_Ips','i')):0.000,(('SSp-m_Ips','i'),('VPM_Ips','e')):0.000,(('SSp-m_Ips','i'),('VPM_Ips','i')):0.000,(('SSp-m_Ips','e'),('MOp_Ips','e')):0.002,(('SSp-m_Ips','e'),('MOp_Ips','i')):0.001,(('SSp-m_Ips','i'),('MOp_Ips','e')):0.000,(('SSp-m_Ips','i'),('MOp_Ips','i')):0.000,(('SSp-m_Ips','e'),('MOp_Con','e')):0.091,(('SSp-m_Ips','e'),('MOp_Con','i')):0.045,(('SSp-m_Ips','i'),('MOp_Con','e')):0.009,(('SSp-m_Ips','i'),('MOp_Con','i')):0.009,(('SSp-m_Ips','e'),('VPMpc_Con','e')):0.006,(('SSp-m_Ips','e'),('VPMpc_Con','i')):0.003,(('SSp-m_Ips','i'),('VPMpc_Con','e')):0.001,(('SSp-m_Ips','i'),('VPMpc_Con','i')):0.001,(('SSp-m_Ips','e'),('SSp-m_Ips','e')):0.000,(('SSp-m_Ips','e'),('SSp-m_Ips','i')):0.000,(('SSp-m_Ips','i'),('SSp-m_Ips','e')):0.000,(('SSp-m_Ips','i'),('SSp-m_Ips','i')):0.000,(('SSp-m_Ips','e'),('LGd_Con','e')):0.000,(('SSp-m_Ips','e'),('LGd_Con','i')):0.000,(('SSp-m_Ips','i'),('LGd_Con','e')):0.000,(('SSp-m_Ips','i'),('LGd_Con','i')):0.000,(('SSp-m_Ips','e'),('LGd_Ips','e')):0.019,(('SSp-m_Ips','e'),('LGd_Ips','i')):0.010,(('SSp-m_Ips','i'),('LGd_Ips','e')):0.002,(('SSp-m_Ips','i'),('LGd_Ips','i')):0.002,(('SSp-m_Ips','e'),('LGv_Con','e')):0.000,(('SSp-m_Ips','e'),('LGv_Con','i')):0.000,(('SSp-m_Ips','i'),('LGv_Con','e')):0.000,(('SSp-m_Ips','i'),('LGv_Con','i')):0.000,(('MOp_Ips','e'),('VPMpc_Ips','e')):0.031,(('MOp_Ips','e'),('VPMpc_Ips','i')):0.015,(('MOp_Ips','i'),('VPMpc_Ips','e')):0.003,(('MOp_Ips','i'),('VPMpc_Ips','i')):0.003,(('MOp_Ips','e'),('SSs_Ips','e')):0.000,(('MOp_Ips','e'),('SSs_Ips','i')):0.000,(('MOp_Ips','i'),('SSs_Ips','e')):0.000,(('MOp_Ips','i'),('SSs_Ips','i')):0.000,(('MOp_Ips','e'),('VPM_Con','e')):0.187,(('MOp_Ips','e'),('VPM_Con','i')):0.093,(('MOp_Ips','i'),('VPM_Con','e')):0.019,(('MOp_Ips','i'),('VPM_Con','i')):0.019,(('MOp_Ips','e'),('SSs_Con','e')):0.001,(('MOp_Ips','e'),('SSs_Con','i')):0.000,(('MOp_Ips','i'),('SSs_Con','e')):0.000,(('MOp_Ips','i'),('SSs_Con','i')):0.000,(('MOp_Ips','e'),('SSp-m_Con','e')):0.078,(('MOp_Ips','e'),('SSp-m_Con','i')):0.039,(('MOp_Ips','i'),('SSp-m_Con','e')):0.008,(('MOp_Ips','i'),('SSp-m_Con','i')):0.008,(('MOp_Ips','e'),('LGv_Ips','e')):0.001,(('MOp_Ips','e'),('LGv_Ips','i')):0.001,(('MOp_Ips','i'),('LGv_Ips','e')):0.000,(('MOp_Ips','i'),('LGv_Ips','i')):0.000,(('MOp_Ips','e'),('VPM_Ips','e')):0.185,(('MOp_Ips','e'),('VPM_Ips','i')):0.093,(('MOp_Ips','i'),('VPM_Ips','e')):0.019,(('MOp_Ips','i'),('VPM_Ips','i')):0.019,(('MOp_Ips','e'),('MOp_Ips','e')):0.005,(('MOp_Ips','e'),('MOp_Ips','i')):0.002,(('MOp_Ips','i'),('MOp_Ips','e')):0.000,(('MOp_Ips','i'),('MOp_Ips','i')):0.000,(('MOp_Ips','e'),('MOp_Con','e')):0.028,(('MOp_Ips','e'),('MOp_Con','i')):0.014,(('MOp_Ips','i'),('MOp_Con','e')):0.003,(('MOp_Ips','i'),('MOp_Con','i')):0.003,(('MOp_Ips','e'),('VPMpc_Con','e')):0.000,(('MOp_Ips','e'),('VPMpc_Con','i')):0.000,(('MOp_Ips','i'),('VPMpc_Con','e')):0.000,(('MOp_Ips','i'),('VPMpc_Con','i')):0.000,(('MOp_Ips','e'),('SSp-m_Ips','e')):0.011,(('MOp_Ips','e'),('SSp-m_Ips','i')):0.006,(('MOp_Ips','i'),('SSp-m_Ips','e')):0.001,(('MOp_Ips','i'),('SSp-m_Ips','i')):0.001,(('MOp_Ips','e'),('LGd_Con','e')):0.000,(('MOp_Ips','e'),('LGd_Con','i')):0.000,(('MOp_Ips','i'),('LGd_Con','e')):0.000,(('MOp_Ips','i'),('LGd_Con','i')):0.000,(('MOp_Ips','e'),('LGd_Ips','e')):0.139,(('MOp_Ips','e'),('LGd_Ips','i')):0.070,(('MOp_Ips','i'),('LGd_Ips','e')):0.014,(('MOp_Ips','i'),('LGd_Ips','i')):0.014,(('MOp_Ips','e'),('LGv_Con','e')):0.185,(('MOp_Ips','e'),('LGv_Con','i')):0.093,(('MOp_Ips','i'),('LGv_Con','e')):0.019,(('MOp_Ips','i'),('LGv_Con','i')):0.019,(('VPMpc_Ips','e'),('VPMpc_Ips','e')):0.387,(('VPMpc_Ips','e'),('VPMpc_Ips','i')):0.194,(('VPMpc_Ips','i'),('VPMpc_Ips','e')):0.039,(('VPMpc_Ips','i'),('VPMpc_Ips','i')):0.039,(('VPMpc_Ips','e'),('SSs_Ips','e')):0.000,(('VPMpc_Ips','e'),('SSs_Ips','i')):0.000,(('VPMpc_Ips','i'),('SSs_Ips','e')):0.000,(('VPMpc_Ips','i'),('SSs_Ips','i')):0.000,(('VPMpc_Ips','e'),('VPM_Con','e')):11.712,(('VPMpc_Ips','e'),('VPM_Con','i')):5.856,(('VPMpc_Ips','i'),('VPM_Con','e')):1.171,(('VPMpc_Ips','i'),('VPM_Con','i')):1.171,(('VPMpc_Ips','e'),('SSs_Con','e')):0.000,(('VPMpc_Ips','e'),('SSs_Con','i')):0.000,(('VPMpc_Ips','i'),('SSs_Con','e')):0.000,(('VPMpc_Ips','i'),('SSs_Con','i')):0.000,(('VPMpc_Ips','e'),('SSp-m_Con','e')):30.516,(('VPMpc_Ips','e'),('SSp-m_Con','i')):15.258,(('VPMpc_Ips','i'),('SSp-m_Con','e')):3.052,(('VPMpc_Ips','i'),('SSp-m_Con','i')):3.052,(('VPMpc_Ips','e'),('LGv_Ips','e')):0.000,(('VPMpc_Ips','e'),('LGv_Ips','i')):0.000,(('VPMpc_Ips','i'),('LGv_Ips','e')):0.000,(('VPMpc_Ips','i'),('LGv_Ips','i')):0.000,(('VPMpc_Ips','e'),('VPM_Ips','e')):0.000,(('VPMpc_Ips','e'),('VPM_Ips','i')):0.000,(('VPMpc_Ips','i'),('VPM_Ips','e')):0.000,(('VPMpc_Ips','i'),('VPM_Ips','i')):0.000,(('VPMpc_Ips','e'),('MOp_Ips','e')):0.005,(('VPMpc_Ips','e'),('MOp_Ips','i')):0.002,(('VPMpc_Ips','i'),('MOp_Ips','e')):0.000,(('VPMpc_Ips','i'),('MOp_Ips','i')):0.000,(('VPMpc_Ips','e'),('MOp_Con','e')):0.000,(('VPMpc_Ips','e'),('MOp_Con','i')):0.000,(('VPMpc_Ips','i'),('MOp_Con','e')):0.000,(('VPMpc_Ips','i'),('MOp_Con','i')):0.000,(('VPMpc_Ips','e'),('VPMpc_Con','e')):0.005,(('VPMpc_Ips','e'),('VPMpc_Con','i')):0.002,(('VPMpc_Ips','i'),('VPMpc_Con','e')):0.000,(('VPMpc_Ips','i'),('VPMpc_Con','i')):0.000,(('VPMpc_Ips','e'),('SSp-m_Ips','e')):0.021,(('VPMpc_Ips','e'),('SSp-m_Ips','i')):0.010,(('VPMpc_Ips','i'),('SSp-m_Ips','e')):0.002,(('VPMpc_Ips','i'),('SSp-m_Ips','i')):0.002,(('VPMpc_Ips','e'),('LGd_Con','e')):0.000,(('VPMpc_Ips','e'),('LGd_Con','i')):0.000,(('VPMpc_Ips','i'),('LGd_Con','e')):0.000,(('VPMpc_Ips','i'),('LGd_Con','i')):0.000,(('VPMpc_Ips','e'),('LGd_Ips','e')):0.236,(('VPMpc_Ips','e'),('LGd_Ips','i')):0.118,(('VPMpc_Ips','i'),('LGd_Ips','e')):0.024,(('VPMpc_Ips','i'),('LGd_Ips','i')):0.024,(('VPMpc_Ips','e'),('LGv_Con','e')):0.013,(('VPMpc_Ips','e'),('LGv_Con','i')):0.006,(('VPMpc_Ips','i'),('LGv_Con','e')):0.001,(('VPMpc_Ips','i'),('LGv_Con','i')):0.001,(('LGv_Ips','e'),('VPMpc_Ips','e')):0.350,(('LGv_Ips','e'),('VPMpc_Ips','i')):0.175,(('LGv_Ips','i'),('VPMpc_Ips','e')):0.035,(('LGv_Ips','i'),('VPMpc_Ips','i')):0.035,(('LGv_Ips','e'),('SSs_Ips','e')):0.000,(('LGv_Ips','e'),('SSs_Ips','i')):0.000,(('LGv_Ips','i'),('SSs_Ips','e')):0.000,(('LGv_Ips','i'),('SSs_Ips','i')):0.000,(('LGv_Ips','e'),('VPM_Con','e')):3.562,(('LGv_Ips','e'),('VPM_Con','i')):1.781,(('LGv_Ips','i'),('VPM_Con','e')):0.356,(('LGv_Ips','i'),('VPM_Con','i')):0.356,(('LGv_Ips','e'),('SSs_Con','e')):0.000,(('LGv_Ips','e'),('SSs_Con','i')):0.000,(('LGv_Ips','i'),('SSs_Con','e')):0.000,(('LGv_Ips','i'),('SSs_Con','i')):0.000,(('LGv_Ips','e'),('SSp-m_Con','e')):0.008,(('LGv_Ips','e'),('SSp-m_Con','i')):0.004,(('LGv_Ips','i'),('SSp-m_Con','e')):0.001,(('LGv_Ips','i'),('SSp-m_Con','i')):0.001,(('LGv_Ips','e'),('LGv_Ips','e')):0.004,(('LGv_Ips','e'),('LGv_Ips','i')):0.002,(('LGv_Ips','i'),('LGv_Ips','e')):0.000,(('LGv_Ips','i'),('LGv_Ips','i')):0.000,(('LGv_Ips','e'),('VPM_Ips','e')):0.003,(('LGv_Ips','e'),('VPM_Ips','i')):0.002,(('LGv_Ips','i'),('VPM_Ips','e')):0.000,(('LGv_Ips','i'),('VPM_Ips','i')):0.000,(('LGv_Ips','e'),('MOp_Ips','e')):0.007,(('LGv_Ips','e'),('MOp_Ips','i')):0.004,(('LGv_Ips','i'),('MOp_Ips','e')):0.001,(('LGv_Ips','i'),('MOp_Ips','i')):0.001,(('LGv_Ips','e'),('MOp_Con','e')):0.000,(('LGv_Ips','e'),('MOp_Con','i')):0.000,(('LGv_Ips','i'),('MOp_Con','e')):0.000,(('LGv_Ips','i'),('MOp_Con','i')):0.000,(('LGv_Ips','e'),('VPMpc_Con','e')):0.002,(('LGv_Ips','e'),('VPMpc_Con','i')):0.001,(('LGv_Ips','i'),('VPMpc_Con','e')):0.000,(('LGv_Ips','i'),('VPMpc_Con','i')):0.000,(('LGv_Ips','e'),('SSp-m_Ips','e')):0.006,(('LGv_Ips','e'),('SSp-m_Ips','i')):0.003,(('LGv_Ips','i'),('SSp-m_Ips','e')):0.001,(('LGv_Ips','i'),('SSp-m_Ips','i')):0.001,(('LGv_Ips','e'),('LGd_Con','e')):0.000,(('LGv_Ips','e'),('LGd_Con','i')):0.000,(('LGv_Ips','i'),('LGd_Con','e')):0.000,(('LGv_Ips','i'),('LGd_Con','i')):0.000,(('LGv_Ips','e'),('LGd_Ips','e')):0.017,(('LGv_Ips','e'),('LGd_Ips','i')):0.009,(('LGv_Ips','i'),('LGd_Ips','e')):0.002,(('LGv_Ips','i'),('LGd_Ips','i')):0.002,(('LGv_Ips','e'),('LGv_Con','e')):0.359,(('LGv_Ips','e'),('LGv_Con','i')):0.180,(('LGv_Ips','i'),('LGv_Con','e')):0.036,(('LGv_Ips','i'),('LGv_Con','i')):0.036,(('SSs_Ips','e'),('VPMpc_Ips','e')):0.253,(('SSs_Ips','e'),('VPMpc_Ips','i')):0.127,(('SSs_Ips','i'),('VPMpc_Ips','e')):0.025,(('SSs_Ips','i'),('VPMpc_Ips','i')):0.025,(('SSs_Ips','e'),('SSs_Ips','e')):0.000,(('SSs_Ips','e'),('SSs_Ips','i')):0.000,(('SSs_Ips','i'),('SSs_Ips','e')):0.000,(('SSs_Ips','i'),('SSs_Ips','i')):0.000,(('SSs_Ips','e'),('VPM_Con','e')):2.923,(('SSs_Ips','e'),('VPM_Con','i')):1.461,(('SSs_Ips','i'),('VPM_Con','e')):0.292,(('SSs_Ips','i'),('VPM_Con','i')):0.292,(('SSs_Ips','e'),('SSs_Con','e')):0.000,(('SSs_Ips','e'),('SSs_Con','i')):0.000,(('SSs_Ips','i'),('SSs_Con','e')):0.000,(('SSs_Ips','i'),('SSs_Con','i')):0.000,(('SSs_Ips','e'),('SSp-m_Con','e')):0.001,(('SSs_Ips','e'),('SSp-m_Con','i')):0.000,(('SSs_Ips','i'),('SSp-m_Con','e')):0.000,(('SSs_Ips','i'),('SSp-m_Con','i')):0.000,(('SSs_Ips','e'),('LGv_Ips','e')):0.001,(('SSs_Ips','e'),('LGv_Ips','i')):0.000,(('SSs_Ips','i'),('LGv_Ips','e')):0.000,(('SSs_Ips','i'),('LGv_Ips','i')):0.000,(('SSs_Ips','e'),('VPM_Ips','e')):0.001,(('SSs_Ips','e'),('VPM_Ips','i')):0.000,(('SSs_Ips','i'),('VPM_Ips','e')):0.000,(('SSs_Ips','i'),('VPM_Ips','i')):0.000,(('SSs_Ips','e'),('MOp_Ips','e')):0.009,(('SSs_Ips','e'),('MOp_Ips','i')):0.004,(('SSs_Ips','i'),('MOp_Ips','e')):0.001,(('SSs_Ips','i'),('MOp_Ips','i')):0.001,(('SSs_Ips','e'),('MOp_Con','e')):0.000,(('SSs_Ips','e'),('MOp_Con','i')):0.000,(('SSs_Ips','i'),('MOp_Con','e')):0.000,(('SSs_Ips','i'),('MOp_Con','i')):0.000,(('SSs_Ips','e'),('VPMpc_Con','e')):0.002,(('SSs_Ips','e'),('VPMpc_Con','i')):0.001,(('SSs_Ips','i'),('VPMpc_Con','e')):0.000,(('SSs_Ips','i'),('VPMpc_Con','i')):0.000,(('SSs_Ips','e'),('SSp-m_Ips','e')):0.012,(('SSs_Ips','e'),('SSp-m_Ips','i')):0.006,(('SSs_Ips','i'),('SSp-m_Ips','e')):0.001,(('SSs_Ips','i'),('SSp-m_Ips','i')):0.001,(('SSs_Ips','e'),('LGd_Con','e')):0.000,(('SSs_Ips','e'),('LGd_Con','i')):0.000,(('SSs_Ips','i'),('LGd_Con','e')):0.000,(('SSs_Ips','i'),('LGd_Con','i')):0.000,(('SSs_Ips','e'),('LGd_Ips','e')):0.030,(('SSs_Ips','e'),('LGd_Ips','i')):0.015,(('SSs_Ips','i'),('LGd_Ips','e')):0.003,(('SSs_Ips','i'),('LGd_Ips','i')):0.003,(('SSs_Ips','e'),('LGv_Con','e')):0.272,(('SSs_Ips','e'),('LGv_Con','i')):0.136,(('SSs_Ips','i'),('LGv_Con','e')):0.027,(('SSs_Ips','i'),('LGv_Con','i')):0.027,(('VPM_Con','e'),('VPMpc_Ips','e')):7.322,(('VPM_Con','e'),('VPMpc_Ips','i')):3.661,(('VPM_Con','i'),('VPMpc_Ips','e')):0.732,(('VPM_Con','i'),('VPMpc_Ips','i')):0.732,(('VPM_Con','e'),('SSs_Ips','e')):0.002,(('VPM_Con','e'),('SSs_Ips','i')):0.001,(('VPM_Con','i'),('SSs_Ips','e')):0.000,(('VPM_Con','i'),('SSs_Ips','i')):0.000,(('VPM_Con','e'),('VPM_Con','e')):0.001,(('VPM_Con','e'),('VPM_Con','i')):0.000,(('VPM_Con','i'),('VPM_Con','e')):0.000,(('VPM_Con','i'),('VPM_Con','i')):0.000,(('VPM_Con','e'),('SSs_Con','e')):0.000,(('VPM_Con','e'),('SSs_Con','i')):0.000,(('VPM_Con','i'),('SSs_Con','e')):0.000,(('VPM_Con','i'),('SSs_Con','i')):0.000,(('VPM_Con','e'),('SSp-m_Con','e')):0.000,(('VPM_Con','e'),('SSp-m_Con','i')):0.000,(('VPM_Con','i'),('SSp-m_Con','e')):0.000,(('VPM_Con','i'),('SSp-m_Con','i')):0.000,(('VPM_Con','e'),('LGv_Ips','e')):0.000,(('VPM_Con','e'),('LGv_Ips','i')):0.000,(('VPM_Con','i'),('LGv_Ips','e')):0.000,(('VPM_Con','i'),('LGv_Ips','i')):0.000,(('VPM_Con','e'),('VPM_Ips','e')):0.001,(('VPM_Con','e'),('VPM_Ips','i')):0.000,(('VPM_Con','i'),('VPM_Ips','e')):0.000,(('VPM_Con','i'),('VPM_Ips','i')):0.000,(('VPM_Con','e'),('MOp_Ips','e')):0.001,(('VPM_Con','e'),('MOp_Ips','i')):0.000,(('VPM_Con','i'),('MOp_Ips','e')):0.000,(('VPM_Con','i'),('MOp_Ips','i')):0.000,(('VPM_Con','e'),('MOp_Con','e')):0.000,(('VPM_Con','e'),('MOp_Con','i')):0.000,(('VPM_Con','i'),('MOp_Con','e')):0.000,(('VPM_Con','i'),('MOp_Con','i')):0.000,(('VPM_Con','e'),('VPMpc_Con','e')):0.000,(('VPM_Con','e'),('VPMpc_Con','i')):0.000,(('VPM_Con','i'),('VPMpc_Con','e')):0.000,(('VPM_Con','i'),('VPMpc_Con','i')):0.000,(('VPM_Con','e'),('SSp-m_Ips','e')):0.000,(('VPM_Con','e'),('SSp-m_Ips','i')):0.000,(('VPM_Con','i'),('SSp-m_Ips','e')):0.000,(('VPM_Con','i'),('SSp-m_Ips','i')):0.000,(('VPM_Con','e'),('LGd_Con','e')):0.000,(('VPM_Con','e'),('LGd_Con','i')):0.000,(('VPM_Con','i'),('LGd_Con','e')):0.000,(('VPM_Con','i'),('LGd_Con','i')):0.000,(('VPM_Con','e'),('LGd_Ips','e')):0.502,(('VPM_Con','e'),('LGd_Ips','i')):0.251,(('VPM_Con','i'),('LGd_Ips','e')):0.050,(('VPM_Con','i'),('LGd_Ips','i')):0.050,(('VPM_Con','e'),('LGv_Con','e')):0.000,(('VPM_Con','e'),('LGv_Con','i')):0.000,(('VPM_Con','i'),('LGv_Con','e')):0.000,(('VPM_Con','i'),('LGv_Con','i')):0.000,(('LGd_Con','e'),('VPMpc_Ips','e')):0.141,(('LGd_Con','e'),('VPMpc_Ips','i')):0.071,(('LGd_Con','i'),('VPMpc_Ips','e')):0.014,(('LGd_Con','i'),('VPMpc_Ips','i')):0.014,(('LGd_Con','e'),('SSs_Ips','e')):0.000,(('LGd_Con','e'),('SSs_Ips','i')):0.000,(('LGd_Con','i'),('SSs_Ips','e')):0.000,(('LGd_Con','i'),('SSs_Ips','i')):0.000,(('LGd_Con','e'),('VPM_Con','e')):1.157,(('LGd_Con','e'),('VPM_Con','i')):0.579,(('LGd_Con','i'),('VPM_Con','e')):0.116,(('LGd_Con','i'),('VPM_Con','i')):0.116,(('LGd_Con','e'),('SSs_Con','e')):0.000,(('LGd_Con','e'),('SSs_Con','i')):0.000,(('LGd_Con','i'),('SSs_Con','e')):0.000,(('LGd_Con','i'),('SSs_Con','i')):0.000,(('LGd_Con','e'),('SSp-m_Con','e')):0.000,(('LGd_Con','e'),('SSp-m_Con','i')):0.000,(('LGd_Con','i'),('SSp-m_Con','e')):0.000,(('LGd_Con','i'),('SSp-m_Con','i')):0.000,(('LGd_Con','e'),('LGv_Ips','e')):0.000,(('LGd_Con','e'),('LGv_Ips','i')):0.000,(('LGd_Con','i'),('LGv_Ips','e')):0.000,(('LGd_Con','i'),('LGv_Ips','i')):0.000,(('LGd_Con','e'),('VPM_Ips','e')):0.003,(('LGd_Con','e'),('VPM_Ips','i')):0.002,(('LGd_Con','i'),('VPM_Ips','e')):0.000,(('LGd_Con','i'),('VPM_Ips','i')):0.000,(('LGd_Con','e'),('MOp_Ips','e')):0.026,(('LGd_Con','e'),('MOp_Ips','i')):0.013,(('LGd_Con','i'),('MOp_Ips','e')):0.003,(('LGd_Con','i'),('MOp_Ips','i')):0.003,(('LGd_Con','e'),('MOp_Con','e')):0.005,(('LGd_Con','e'),('MOp_Con','i')):0.002,(('LGd_Con','i'),('MOp_Con','e')):0.000,(('LGd_Con','i'),('MOp_Con','i')):0.000,(('LGd_Con','e'),('VPMpc_Con','e')):0.076,(('LGd_Con','e'),('VPMpc_Con','i')):0.038,(('LGd_Con','i'),('VPMpc_Con','e')):0.008,(('LGd_Con','i'),('VPMpc_Con','i')):0.008,(('LGd_Con','e'),('SSp-m_Ips','e')):0.018,(('LGd_Con','e'),('SSp-m_Ips','i')):0.009,(('LGd_Con','i'),('SSp-m_Ips','e')):0.002,(('LGd_Con','i'),('SSp-m_Ips','i')):0.002,(('LGd_Con','e'),('LGd_Con','e')):0.000,(('LGd_Con','e'),('LGd_Con','i')):0.000,(('LGd_Con','i'),('LGd_Con','e')):0.000,(('LGd_Con','i'),('LGd_Con','i')):0.000,(('LGd_Con','e'),('LGd_Ips','e')):0.378,(('LGd_Con','e'),('LGd_Ips','i')):0.189,(('LGd_Con','i'),('LGd_Ips','e')):0.038,(('LGd_Con','i'),('LGd_Ips','i')):0.038,(('LGd_Con','e'),('LGv_Con','e')):0.065,(('LGd_Con','e'),('LGv_Con','i')):0.033,(('LGd_Con','i'),('LGv_Con','e')):0.007,(('LGd_Con','i'),('LGv_Con','i')):0.007,(('SSp-m_Con','e'),('VPMpc_Ips','e')):0.038,(('SSp-m_Con','e'),('VPMpc_Ips','i')):0.019,(('SSp-m_Con','i'),('VPMpc_Ips','e')):0.004,(('SSp-m_Con','i'),('VPMpc_Ips','i')):0.004,(('SSp-m_Con','e'),('SSs_Ips','e')):0.000,(('SSp-m_Con','e'),('SSs_Ips','i')):0.000,(('SSp-m_Con','i'),('SSs_Ips','e')):0.000,(('SSp-m_Con','i'),('SSs_Ips','i')):0.000,(('SSp-m_Con','e'),('VPM_Con','e')):0.002,(('SSp-m_Con','e'),('VPM_Con','i')):0.001,(('SSp-m_Con','i'),('VPM_Con','e')):0.000,(('SSp-m_Con','i'),('VPM_Con','i')):0.000,(('SSp-m_Con','e'),('SSs_Con','e')):0.000,(('SSp-m_Con','e'),('SSs_Con','i')):0.000,(('SSp-m_Con','i'),('SSs_Con','e')):0.000,(('SSp-m_Con','i'),('SSs_Con','i')):0.000,(('SSp-m_Con','e'),('SSp-m_Con','e')):0.000,(('SSp-m_Con','e'),('SSp-m_Con','i')):0.000,(('SSp-m_Con','i'),('SSp-m_Con','e')):0.000,(('SSp-m_Con','i'),('SSp-m_Con','i')):0.000,(('SSp-m_Con','e'),('LGv_Ips','e')):0.001,(('SSp-m_Con','e'),('LGv_Ips','i')):0.000,(('SSp-m_Con','i'),('LGv_Ips','e')):0.000,(('SSp-m_Con','i'),('LGv_Ips','i')):0.000,(('SSp-m_Con','e'),('VPM_Ips','e')):0.002,(('SSp-m_Con','e'),('VPM_Ips','i')):0.001,(('SSp-m_Con','i'),('VPM_Ips','e')):0.000,(('SSp-m_Con','i'),('VPM_Ips','i')):0.000,(('SSp-m_Con','e'),('MOp_Ips','e')):0.000,(('SSp-m_Con','e'),('MOp_Ips','i')):0.000,(('SSp-m_Con','i'),('MOp_Ips','e')):0.000,(('SSp-m_Con','i'),('MOp_Ips','i')):0.000,(('SSp-m_Con','e'),('MOp_Con','e')):0.007,(('SSp-m_Con','e'),('MOp_Con','i')):0.003,(('SSp-m_Con','i'),('MOp_Con','e')):0.001,(('SSp-m_Con','i'),('MOp_Con','i')):0.001,(('SSp-m_Con','e'),('VPMpc_Con','e')):0.000,(('SSp-m_Con','e'),('VPMpc_Con','i')):0.000,(('SSp-m_Con','i'),('VPMpc_Con','e')):0.000,(('SSp-m_Con','i'),('VPMpc_Con','i')):0.000,(('SSp-m_Con','e'),('SSp-m_Ips','e')):0.000,(('SSp-m_Con','e'),('SSp-m_Ips','i')):0.000,(('SSp-m_Con','i'),('SSp-m_Ips','e')):0.000,(('SSp-m_Con','i'),('SSp-m_Ips','i')):0.000,(('SSp-m_Con','e'),('LGd_Con','e')):0.000,(('SSp-m_Con','e'),('LGd_Con','i')):0.000,(('SSp-m_Con','i'),('LGd_Con','e')):0.000,(('SSp-m_Con','i'),('LGd_Con','i')):0.000,(('SSp-m_Con','e'),('LGd_Ips','e')):0.019,(('SSp-m_Con','e'),('LGd_Ips','i')):0.010,(('SSp-m_Con','i'),('LGd_Ips','e')):0.002,(('SSp-m_Con','i'),('LGd_Ips','i')):0.002,(('SSp-m_Con','e'),('LGv_Con','e')):0.000,(('SSp-m_Con','e'),('LGv_Con','i')):0.000,(('SSp-m_Con','i'),('LGv_Con','e')):0.000,(('SSp-m_Con','i'),('LGv_Con','i')):0.000,(('MOp_Con','e'),('VPMpc_Ips','e')):0.047,(('MOp_Con','e'),('VPMpc_Ips','i')):0.024,(('MOp_Con','i'),('VPMpc_Ips','e')):0.005,(('MOp_Con','i'),('VPMpc_Ips','i')):0.005,(('MOp_Con','e'),('SSs_Ips','e')):0.000,(('MOp_Con','e'),('SSs_Ips','i')):0.000,(('MOp_Con','i'),('SSs_Ips','e')):0.000,(('MOp_Con','i'),('SSs_Ips','i')):0.000,(('MOp_Con','e'),('VPM_Con','e')):1.312,(('MOp_Con','e'),('VPM_Con','i')):0.656,(('MOp_Con','i'),('VPM_Con','e')):0.131,(('MOp_Con','i'),('VPM_Con','i')):0.131,(('MOp_Con','e'),('SSs_Con','e')):0.001,(('MOp_Con','e'),('SSs_Con','i')):0.000,(('MOp_Con','i'),('SSs_Con','e')):0.000,(('MOp_Con','i'),('SSs_Con','i')):0.000,(('MOp_Con','e'),('SSp-m_Con','e')):0.011,(('MOp_Con','e'),('SSp-m_Con','i')):0.005,(('MOp_Con','i'),('SSp-m_Con','e')):0.001,(('MOp_Con','i'),('SSp-m_Con','i')):0.001,(('MOp_Con','e'),('LGv_Ips','e')):0.001,(('MOp_Con','e'),('LGv_Ips','i')):0.000,(('MOp_Con','i'),('LGv_Ips','e')):0.000,(('MOp_Con','i'),('LGv_Ips','i')):0.000,(('MOp_Con','e'),('VPM_Ips','e')):0.001,(('MOp_Con','e'),('VPM_Ips','i')):0.001,(('MOp_Con','i'),('VPM_Ips','e')):0.000,(('MOp_Con','i'),('VPM_Ips','i')):0.000,(('MOp_Con','e'),('MOp_Ips','e')):0.001,(('MOp_Con','e'),('MOp_Ips','i')):0.000,(('MOp_Con','i'),('MOp_Ips','e')):0.000,(('MOp_Con','i'),('MOp_Ips','i')):0.000,(('MOp_Con','e'),('MOp_Con','e')):0.000,(('MOp_Con','e'),('MOp_Con','i')):0.000,(('MOp_Con','i'),('MOp_Con','e')):0.000,(('MOp_Con','i'),('MOp_Con','i')):0.000,(('MOp_Con','e'),('VPMpc_Con','e')):0.001,(('MOp_Con','e'),('VPMpc_Con','i')):0.000,(('MOp_Con','i'),('VPMpc_Con','e')):0.000,(('MOp_Con','i'),('VPMpc_Con','i')):0.000,(('MOp_Con','e'),('SSp-m_Ips','e')):22.848,(('MOp_Con','e'),('SSp-m_Ips','i')):11.424,(('MOp_Con','i'),('SSp-m_Ips','e')):2.285,(('MOp_Con','i'),('SSp-m_Ips','i')):2.285,(('MOp_Con','e'),('LGd_Con','e')):153.347,(('MOp_Con','e'),('LGd_Con','i')):76.673,(('MOp_Con','i'),('LGd_Con','e')):15.335,(('MOp_Con','i'),('LGd_Con','i')):15.335,(('MOp_Con','e'),('LGd_Ips','e')):0.029,(('MOp_Con','e'),('LGd_Ips','i')):0.015,(('MOp_Con','i'),('LGd_Ips','e')):0.003,(('MOp_Con','i'),('LGd_Ips','i')):0.003,(('MOp_Con','e'),('LGv_Con','e')):0.246,(('MOp_Con','e'),('LGv_Con','i')):0.123,(('MOp_Con','i'),('LGv_Con','e')):0.025,(('MOp_Con','i'),('LGv_Con','i')):0.025,(('VPMpc_Con','e'),('VPMpc_Ips','e')):45.826,(('VPMpc_Con','e'),('VPMpc_Ips','i')):22.913,(('VPMpc_Con','i'),('VPMpc_Ips','e')):4.583,(('VPMpc_Con','i'),('VPMpc_Ips','i')):4.583,(('VPMpc_Con','e'),('SSs_Ips','e')):0.000,(('VPMpc_Con','e'),('SSs_Ips','i')):0.000,(('VPMpc_Con','i'),('SSs_Ips','e')):0.000,(('VPMpc_Con','i'),('SSs_Ips','i')):0.000,(('VPMpc_Con','e'),('VPM_Con','e')):0.107,(('VPMpc_Con','e'),('VPM_Con','i')):0.053,(('VPMpc_Con','i'),('VPM_Con','e')):0.011,(('VPMpc_Con','i'),('VPM_Con','i')):0.011,(('VPMpc_Con','e'),('SSs_Con','e')):0.000,(('VPMpc_Con','e'),('SSs_Con','i')):0.000,(('VPMpc_Con','i'),('SSs_Con','e')):0.000,(('VPMpc_Con','i'),('SSs_Con','i')):0.000,(('VPMpc_Con','e'),('SSp-m_Con','e')):0.000,(('VPMpc_Con','e'),('SSp-m_Con','i')):0.000,(('VPMpc_Con','i'),('SSp-m_Con','e')):0.000,(('VPMpc_Con','i'),('SSp-m_Con','i')):0.000,(('VPMpc_Con','e'),('LGv_Ips','e')):0.001,(('VPMpc_Con','e'),('LGv_Ips','i')):0.001,(('VPMpc_Con','i'),('LGv_Ips','e')):0.000,(('VPMpc_Con','i'),('LGv_Ips','i')):0.000,(('VPMpc_Con','e'),('VPM_Ips','e')):0.002,(('VPMpc_Con','e'),('VPM_Ips','i')):0.001,(('VPMpc_Con','i'),('VPM_Ips','e')):0.000,(('VPMpc_Con','i'),('VPM_Ips','i')):0.000,(('VPMpc_Con','e'),('MOp_Ips','e')):0.001,(('VPMpc_Con','e'),('MOp_Ips','i')):0.000,(('VPMpc_Con','i'),('MOp_Ips','e')):0.000,(('VPMpc_Con','i'),('MOp_Ips','i')):0.000,(('VPMpc_Con','e'),('MOp_Con','e')):324.692,(('VPMpc_Con','e'),('MOp_Con','i')):162.346,(('VPMpc_Con','i'),('MOp_Con','e')):32.469,(('VPMpc_Con','i'),('MOp_Con','i')):32.469,(('VPMpc_Con','e'),('VPMpc_Con','e')):37.727,(('VPMpc_Con','e'),('VPMpc_Con','i')):18.864,(('VPMpc_Con','i'),('VPMpc_Con','e')):3.773,(('VPMpc_Con','i'),('VPMpc_Con','i')):3.773,(('VPMpc_Con','e'),('SSp-m_Ips','e')):0.005,(('VPMpc_Con','e'),('SSp-m_Ips','i')):0.003,(('VPMpc_Con','i'),('SSp-m_Ips','e')):0.001,(('VPMpc_Con','i'),('SSp-m_Ips','i')):0.001,(('VPMpc_Con','e'),('LGd_Con','e')):0.000,(('VPMpc_Con','e'),('LGd_Con','i')):0.000,(('VPMpc_Con','i'),('LGd_Con','e')):0.000,(('VPMpc_Con','i'),('LGd_Con','i')):0.000,(('VPMpc_Con','e'),('LGd_Ips','e')):0.006,(('VPMpc_Con','e'),('LGd_Ips','i')):0.003,(('VPMpc_Con','i'),('LGd_Ips','e')):0.001,(('VPMpc_Con','i'),('LGd_Ips','i')):0.001,(('VPMpc_Con','e'),('LGv_Con','e')):0.003,(('VPMpc_Con','e'),('LGv_Con','i')):0.001,(('VPMpc_Con','i'),('LGv_Con','e')):0.000,(('VPMpc_Con','i'),('LGv_Con','i')):0.000,(('LGv_Con','e'),('VPMpc_Ips','e')):7.186,(('LGv_Con','e'),('VPMpc_Ips','i')):3.593,(('LGv_Con','i'),('VPMpc_Ips','e')):0.719,(('LGv_Con','i'),('VPMpc_Ips','i')):0.719,(('LGv_Con','e'),('SSs_Ips','e')):0.001,(('LGv_Con','e'),('SSs_Ips','i')):0.000,(('LGv_Con','i'),('SSs_Ips','e')):0.000,(('LGv_Con','i'),('SSs_Ips','i')):0.000,(('LGv_Con','e'),('VPM_Con','e')):0.001,(('LGv_Con','e'),('VPM_Con','i')):0.001,(('LGv_Con','i'),('VPM_Con','e')):0.000,(('LGv_Con','i'),('VPM_Con','i')):0.000,(('LGv_Con','e'),('SSs_Con','e')):0.000,(('LGv_Con','e'),('SSs_Con','i')):0.000,(('LGv_Con','i'),('SSs_Con','e')):0.000,(('LGv_Con','i'),('SSs_Con','i')):0.000,(('LGv_Con','e'),('SSp-m_Con','e')):0.000,(('LGv_Con','e'),('SSp-m_Con','i')):0.000,(('LGv_Con','i'),('SSp-m_Con','e')):0.000,(('LGv_Con','i'),('SSp-m_Con','i')):0.000,(('LGv_Con','e'),('LGv_Ips','e')):0.001,(('LGv_Con','e'),('LGv_Ips','i')):0.000,(('LGv_Con','i'),('LGv_Ips','e')):0.000,(('LGv_Con','i'),('LGv_Ips','i')):0.000,(('LGv_Con','e'),('VPM_Ips','e')):0.001,(('LGv_Con','e'),('VPM_Ips','i')):0.000,(('LGv_Con','i'),('VPM_Ips','e')):0.000,(('LGv_Con','i'),('VPM_Ips','i')):0.000,(('LGv_Con','e'),('MOp_Ips','e')):0.004,(('LGv_Con','e'),('MOp_Ips','i')):0.002,(('LGv_Con','i'),('MOp_Ips','e')):0.000,(('LGv_Con','i'),('MOp_Ips','i')):0.000,(('LGv_Con','e'),('MOp_Con','e')):0.000,(('LGv_Con','e'),('MOp_Con','i')):0.000,(('LGv_Con','i'),('MOp_Con','e')):0.000,(('LGv_Con','i'),('MOp_Con','i')):0.000,(('LGv_Con','e'),('VPMpc_Con','e')):38.386,(('LGv_Con','e'),('VPMpc_Con','i')):19.193,(('LGv_Con','i'),('VPMpc_Con','e')):3.839,(('LGv_Con','i'),('VPMpc_Con','i')):3.839,(('LGv_Con','e'),('SSp-m_Ips','e')):0.000,(('LGv_Con','e'),('SSp-m_Ips','i')):0.000,(('LGv_Con','i'),('SSp-m_Ips','e')):0.000,(('LGv_Con','i'),('SSp-m_Ips','i')):0.000,(('LGv_Con','e'),('LGd_Con','e')):0.000,(('LGv_Con','e'),('LGd_Con','i')):0.000,(('LGv_Con','i'),('LGd_Con','e')):0.000,(('LGv_Con','i'),('LGd_Con','i')):0.000,(('LGv_Con','e'),('LGd_Ips','e')):0.512,(('LGv_Con','e'),('LGd_Ips','i')):0.256,(('LGv_Con','i'),('LGd_Ips','e')):0.051,(('LGv_Con','i'),('LGd_Ips','i')):0.051,(('LGv_Con','e'),('LGv_Con','e')):0.000,(('LGv_Con','e'),('LGv_Con','i')):0.000,(('LGv_Con','i'),('LGv_Con','e')):0.000,(('LGv_Con','i'),('LGv_Con','i')):0.000,(('SSs_Con','e'),('VPMpc_Ips','e')):0.022,(('SSs_Con','e'),('VPMpc_Ips','i')):0.011,(('SSs_Con','i'),('VPMpc_Ips','e')):0.002,(('SSs_Con','i'),('VPMpc_Ips','i')):0.002,(('SSs_Con','e'),('SSs_Ips','e')):0.000,(('SSs_Con','e'),('SSs_Ips','i')):0.000,(('SSs_Con','i'),('SSs_Ips','e')):0.000,(('SSs_Con','i'),('SSs_Ips','i')):0.000,(('SSs_Con','e'),('VPM_Con','e')):0.333,(('SSs_Con','e'),('VPM_Con','i')):0.167,(('SSs_Con','i'),('VPM_Con','e')):0.033,(('SSs_Con','i'),('VPM_Con','i')):0.033,(('SSs_Con','e'),('SSs_Con','e')):0.001,(('SSs_Con','e'),('SSs_Con','i')):0.000,(('SSs_Con','i'),('SSs_Con','e')):0.000,(('SSs_Con','i'),('SSs_Con','i')):0.000,(('SSs_Con','e'),('SSp-m_Con','e')):0.000,(('SSs_Con','e'),('SSp-m_Con','i')):0.000,(('SSs_Con','i'),('SSp-m_Con','e')):0.000,(('SSs_Con','i'),('SSp-m_Con','i')):0.000,(('SSs_Con','e'),('LGv_Ips','e')):0.000,(('SSs_Con','e'),('LGv_Ips','i')):0.000,(('SSs_Con','i'),('LGv_Ips','e')):0.000,(('SSs_Con','i'),('LGv_Ips','i')):0.000,(('SSs_Con','e'),('VPM_Ips','e')):0.023,(('SSs_Con','e'),('VPM_Ips','i')):0.011,(('SSs_Con','i'),('VPM_Ips','e')):0.002,(('SSs_Con','i'),('VPM_Ips','i')):0.002,(('SSs_Con','e'),('MOp_Ips','e')):0.000,(('SSs_Con','e'),('MOp_Ips','i')):0.000,(('SSs_Con','i'),('MOp_Ips','e')):0.000,(('SSs_Con','i'),('MOp_Ips','i')):0.000,(('SSs_Con','e'),('MOp_Con','e')):0.029,(('SSs_Con','e'),('MOp_Con','i')):0.014,(('SSs_Con','i'),('MOp_Con','e')):0.003,(('SSs_Con','i'),('MOp_Con','i')):0.003,(('SSs_Con','e'),('VPMpc_Con','e')):0.025,(('SSs_Con','e'),('VPMpc_Con','i')):0.013,(('SSs_Con','i'),('VPMpc_Con','e')):0.003,(('SSs_Con','i'),('VPMpc_Con','i')):0.003,(('SSs_Con','e'),('SSp-m_Ips','e')):0.002,(('SSs_Con','e'),('SSp-m_Ips','i')):0.001,(('SSs_Con','i'),('SSp-m_Ips','e')):0.000,(('SSs_Con','i'),('SSp-m_Ips','i')):0.000,(('SSs_Con','e'),('LGd_Con','e')):0.000,(('SSs_Con','e'),('LGd_Con','i')):0.000,(('SSs_Con','i'),('LGd_Con','e')):0.000,(('SSs_Con','i'),('LGd_Con','i')):0.000,(('SSs_Con','e'),('LGd_Ips','e')):0.003,(('SSs_Con','e'),('LGd_Ips','i')):0.002,(('SSs_Con','i'),('LGd_Ips','e')):0.000,(('SSs_Con','i'),('LGd_Ips','i')):0.000,(('SSs_Con','e'),('LGv_Con','e')):0.001,(('SSs_Con','e'),('LGv_Con','i')):0.000,(('SSs_Con','i'),('LGv_Con','e')):0.000,(('SSs_Con','i'),('LGv_Con','i')):0.000,}

    conn_weights = {
        'e': .175*1e-4*2.5,
        'i': -.7*1e-4*2.5
    }
    
    position_dict = {
        ('SSp-m_Ips', 'e'): (0,0,13),
        ('SSp-m_Ips', 'i'): (0,1,13),
        ('SSp-m_Con', 'e'): (0,0,12),
        ('SSp-m_Con', 'i'): (0,1,12),
        ('SSs_Ips', 'e'): (0,0,11),
        ('SSs_Ips', 'i'): (0,1,11),
        ('SSs_Con', 'e'): (0,0,10),
        ('SSs_Con', 'i'): (0,1,10),
        ('MOp_Ips', 'e'): (0,0,9),
        ('MOp_Ips', 'i'): (0,1,9),
        ('MOp_Con', 'e'): (0,0,8),
        ('MOp_Con', 'i'): (0,1,8),
        ('LGv_Ips', 'e'): (0,0,7),
        ('LGv_Ips', 'i'): (0,1,7),
        ('LGv_Con', 'e'): (0,0,6),
        ('LGv_Con', 'i'): (0,1,6),
        ('LGd_Ips', 'e'): (0,0,5),
        ('LGd_Ips', 'i'): (0,1,5),
        ('LGd_Con', 'e'): (0,0,4),
        ('LGd_Con', 'i'): (0,1,4),
        ('VPM_Ips', 'e'): (0,0,3),
        ('VPM_Ips', 'i'): (0,1,3),
        ('VPM_Con', 'e'): (0,0,2),
        ('VPM_Con', 'i'): (0,1,2),
        ('VPMpc_Ips', 'e'): (0,0,1),
        ('VPMpc_Ips', 'i'): (0,1,1),
        ('VPMpc_Con', 'e'): (0,0,0),
        ('VPMpc_Con', 'i'): (0,1,0)
    }
    
    internal_population_settings = {'v_min': -.03, 
                                    'v_max':.015,
                                    'dv':dv,
                                    'update_method':'gmres',
                                    'tau_m':.01,
                                    'tol':1e-7,
                                    'record':True}
    
    # Create populations:
    background_population_dict = {}
    internal_population_dict = {}
    for layer, celltype in itertools.product(['SSp-m_Ips','SSs_Ips','MOp_Ips','VPM_Ips','VPMpc_Ips','LGd_Ips','LGv_Ips','SSp-m_Con','SSs_Con','MOp_Con','VPM_Con','VPMpc_Con','LGd_Con','LGv_Con'], ['e', 'i']):
        background_population_dict[layer, celltype] = ExternalPopulation('Heaviside(t)*%s' % background_firing_rate, record=True, metadata={'layer':layer, 'celltype':celltype})
        curr_population_settings = copy.copy(internal_population_settings)
        x_pos, y_pos, z_pos = position_dict[layer, celltype]
        metadata={'layer':layer, 'celltype':celltype, 'x':x_pos, 'y':y_pos, 'z':z_pos,}
        curr_population_settings.update({'metadata':metadata})
        internal_population_dict[layer, celltype] = InternalPopulation(**curr_population_settings)
    
    # Create background connections:
    connection_list = []
    for layer, celltype in itertools.product(['SSp-m_Ips','SSs_Ips','MOp_Ips','VPM_Ips','VPMpc_Ips','LGd_Ips','LGv_Ips','SSp-m_Con','SSs_Con','MOp_Con','VPM_Con','VPMpc_Con','LGd_Con','LGv_Con'], ['e', 'i']):
        source_population = background_population_dict[layer, celltype]
        target_population = internal_population_dict[layer, celltype]
        if celltype == 'e':
            background_delay = .005
        else:
            background_delay = 0.
        curr_connection = Connection(source_population, target_population, nsyn_background[layer, celltype], weights=conn_weights['e'], delays=background_delay) 
        connection_list.append(curr_connection)
    
    # Create recurrent connections:
    for source_layer, source_celltype in itertools.product(['SSp-m_Ips','SSs_Ips','MOp_Ips','VPM_Ips','VPMpc_Ips','LGd_Ips','LGv_Ips','SSp-m_Con','SSs_Con','MOp_Con','VPM_Con','VPMpc_Con','LGd_Con','LGv_Con'], ['e', 'i']):
        for target_layer, target_celltype in itertools.product(['SSp-m_Ips','SSs_Ips','MOp_Ips','VPM_Ips','VPMpc_Ips','LGd_Ips','LGv_Ips','SSp-m_Con','SSs_Con','MOp_Con','VPM_Con','VPMpc_Con','LGd_Con','LGv_Con'], ['e', 'i']):
            source_population = internal_population_dict[source_layer, source_celltype]
            target_population = internal_population_dict[target_layer, target_celltype]
            nsyn = connection_probabilities[(source_layer, source_celltype), (target_layer, target_celltype)]*internal_population_sizes[source_layer, source_celltype]
            weight = conn_weights[source_celltype]
            curr_connection = Connection(source_population, target_population, nsyn, weights=weight, delays=0)
            connection_list.append(curr_connection)
    
    # Create simulation:
    population_list = list(background_population_dict.values()) + list(internal_population_dict.values())

    def f(n):
        print('t:', n.t)
        # if n.t%.001 < 1e-10:
        #     print 't:', n.t
    network = Network(population_list, connection_list, update_callback=f)
    
    return network
    
def example(show=False, save=False, network=None):
    
    # Simulation settings:
    t0 = 0.
    dt = .0002
    tf = .1
    dv = .0002
    
    if network is None:
        network = get_network(dv)
    
    internal_population_dict = {}
    for p in network.population_list:
        if isinstance(p, InternalPopulation):
            layer = p.metadata['layer']
            celltype = p.metadata['celltype']
            internal_population_dict[layer, celltype] = p
    
    # Run simulation:
    simulation_configuration = SimulationConfiguration(dt, tf, t0=t0)
    simulation = Simulation(network=network, simulation_configuration=simulation_configuration)
    simulation.run()
    print('Run Time:', network.run_time)
    
    # Visualize:
    y_label_dict = {'SSp-m_Ips':'SSp-m_Ips', 'SSs_Ips':'SSs_Ips', 'MOp_Ips':'MOp_Ips', 'VPM_Ips':'VPM_Ips', 'VPMpc_Ips':'VPMpc_Ips', 'LGd_Ips':'LGd_Ips', 'LGv_Ips':'LGv_Ips'}

    result_dict = {}
    for row_ind, layer in enumerate(['SSp-m_Ips','SSs_Ips','MOp_Ips','VPM_Ips','VPMpc_Ips','LGd_Ips','LGv_Ips']):
        for plot_color, celltype in zip(['r', 'b'],['e', 'i']):
            curr_population = internal_population_dict[layer, celltype]
            result_dict[layer, celltype] = curr_population.firing_rate_record[-1]

    if show == True:  # pragma: no cover

        fig, axes = plt.subplots(nrows=8, ncols=1, **{'figsize': (4, 8)})
        for row_ind, layer in enumerate(['SSp-m_Ips','SSs_Ips','MOp_Ips','VPM_Ips','VPMpc_Ips','LGd_Ips','LGv_Ips']):
            for plot_color, celltype in zip(['r', 'b'], ['e', 'i']):
                curr_population = internal_population_dict[layer, celltype]
                axes[row_ind].plot(curr_population.t_record, curr_population.firing_rate_record, plot_color)


            axes[row_ind].set_xlim([0,tf])
            axes[row_ind].set_ylim(ymin=0)
            axes[row_ind].set_ylabel('Layer %s\nfiring rate (Hz)' % y_label_dict[layer])
            if layer == 'VPM_Ips': axes[row_ind].legend(['Excitatory', 'Inhibitory'], prop={'size':10}, loc=4)

        axes[3].set_xlabel('Time (seconds)')
        fig.tight_layout()

        if save == True: plt.savefig('./TH-Ctx_loop.png')

        plt.show()  # pragma: no cover

    return result_dict, simulation
    
if __name__ == "__main__":
    result_dict, simulation = example(show=True)        # pragma: no cover