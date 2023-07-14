import numpy as np
import torch
import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib as mpl
import argparse

import physo.benchmark.FeynmanDataset.FeynmanProblem as Feyn
import physo
# todo: Make noize

# Parallel config
PARALLEL_MODE_DEFAULT = False
N_CPUS_DEFAULT        = 1

# ---------------------------------------------------- SCRIPT ARGS -----------------------------------------------------
parser = argparse.ArgumentParser (description     = "Runs a Feynman problem job.",
                                  formatter_class = argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-i", "--equation", default = 0,
                    help = "Equation number in the set (e.g. 0 to 99 for bulk eqs and 100 to 119 for bonus eqs).")
parser.add_argument("-t", "--trial", default = 0,
                    help = "Trial number (sets seed accordingly).")
parser.add_argument("-n", "--noize", default = 0.,
                    help = "Noize level fraction.")
parser.add_argument("-p", "--parallel_mode", default = PARALLEL_MODE_DEFAULT,
                    help = "Should parallel mode be used.")
parser.add_argument("-ncpus", "--ncpus", default = N_CPUS_DEFAULT,
                    help = "Nb. of CPUs to use")
config = vars(parser.parse_args())

# Feynman problem number
I_FEYN  = int(config["equation"])
# Trial number
N_TRIAL = int(config["trial"])
# Noize level
NOIZE_LEVEL = float(config["noize"])
# Parallel config
PARALLEL_MODE = bool(config["parallel_mode"])
N_CPUS        = int(config["ncpus"])
# ---------------------------------------------------- SCRIPT ARGS -----------------------------------------------------

if __name__ == '__main__':

    # ----- HYPERPARAMS : CONSTANTS -----
    # Since physical constants (G, c etc.) are treated as input variables taking a range of values, two dimensionless
    # free constants + a fixed constant (1.) should be enough for most cases
    # Even 1 dimensionless free constant + 2 fixed constants (1. and pi) could be enough
    dimensionless_units = np.zeros(Feyn.FEYN_UNITS_VECTOR_SIZE)
    FIXED_CONSTS       = [1.]
    FIXED_CONSTS_UNITS = [dimensionless_units]
    FREE_CONSTS_NAMES  = ["c1", "c2"]
    FREE_CONSTS_UNITS  = [dimensionless_units, dimensionless_units]

    # ----- HYPERPARAMS : DATA -----
    # SRBench uses 100k data points https://arxiv.org/abs/2107.14351
    N_SAMPLES = int(1e5)

    # ----- HYPERPARAMS : CONFIG -----
    CONFIG = physo.config.config1.config1

    # ----- HYPERPARAMS : MAX NUMBER OF EVALUATIONS -----
    # 1M evaluation maximum allowed in SRBench https://arxiv.org/abs/2107.14351
    MAX_N_EVALUATIONS = int(1e6) + 1
    # Also setting the nb. of epochs for safety
    N_EPOCHS = int(MAX_N_EVALUATIONS/CONFIG["learning_config"]["batch_size"])

    # Fixing seed accordingly with attempt number
    seed = N_TRIAL
    np.random.seed(seed)
    torch.manual_seed(seed)

    # Paths
    RUN_NAME       = "FR_%i_%i_%f"%(I_FEYN, N_TRIAL, NOIZE_LEVEL)
    PATH_DATA      = "%s_data.csv"%(RUN_NAME)
    PATH_DATA_PLOT = "%s_data.png"%(RUN_NAME)

    # Making a directory for this run and run in it
    if not os.path.exists(RUN_NAME):
        os.makedirs(RUN_NAME)
    os.chdir(os.path.join(os.path.dirname(__file__), RUN_NAME,))

    # Copying .py this script to the directory
    # shutil.copy2(src = __file__, dst = os.path.join(os.path.dirname(__file__), RUN_NAME))

    # MONITORING CONFIG TO USE
    get_run_logger     = lambda : physo.learn.monitoring.RunLogger(
                                          save_path = 'SR.log',
                                          do_save   = True)
    get_run_visualiser = lambda : physo.learn.monitoring.RunVisualiser (
                                               epoch_refresh_rate = 1,
                                               save_path = 'SR_curves.png',
                                               do_show   = False,
                                               do_prints = True,
                                               do_save   = True, )

    # Loading Feynman problem
    pb = Feyn.FeynmanProblem(I_FEYN)

    # Generate data
    X, y = pb.generate_data_points (n_samples = N_SAMPLES)
    # Save data
    df = pd.DataFrame(data    = np.concatenate((y[np.newaxis,:], X), axis=0).transpose(),
                      columns = [pb.y_name] + pb.X_names.tolist())
    df.to_csv(PATH_DATA, sep=";")

    # Plot data
    mpl.rcParams.update(mpl.rcParamsDefault)
    n_dim = X.shape[0]
    fig, ax = plt.subplots(n_dim, 1, figsize=(10, n_dim * 4))
    for i in range(n_dim):
        curr_ax = ax if n_dim == 1 else ax[i]
        curr_ax.plot(X[i], y, 'k.', )
        curr_ax.set_xlabel("%s" % (pb.X_names[i]))
        curr_ax.set_ylabel("%s" % (pb.y_name))
    # Save plot
    fig.savefig(PATH_DATA_PLOT)

    # Printing start
    print("%s : Starting SR task"%(RUN_NAME))

    # Running SR task
    expression, logs = physo.SR(X, y,
                # Giving names of variables (for display purposes)
                X_names = pb.X_names,
                # Giving units of input variables
                X_units = pb.X_units,
                # Giving name of root variable (for display purposes)
                y_name  = pb.y_name,
                # Giving units of the root variable
                y_units = pb.y_units,
                # Fixed constants
                fixed_consts       = FIXED_CONSTS,
                # Units of fixed constants
                fixed_consts_units = FIXED_CONSTS_UNITS,
                # Free constants names (for display purposes)
                free_consts_names = FREE_CONSTS_NAMES,
                # Units of free constants
                free_consts_units = FREE_CONSTS_UNITS,
                # Run config
                run_config = CONFIG,
                # Run monitoring
                get_run_logger     = get_run_logger,
                get_run_visualiser = get_run_visualiser,
                # Stopping condition
                max_n_evaluations = MAX_N_EVALUATIONS,
                epochs            = N_EPOCHS,
                # Parallel mode
                parallel_mode = PARALLEL_MODE,
                n_cpus        = N_CPUS,
        )

    # Printing end
    print("%s : SR task finished"%(RUN_NAME))