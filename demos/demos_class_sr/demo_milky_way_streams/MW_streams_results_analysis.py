import os
import pandas as pd
import time
import argparse
import numpy as np
import sympy
import platform
# Internal imports
from physo.benchmark.utils import symbolic_utils as su
import physo.benchmark.utils.timeout_unix as timeout_unix
from benchmarking import utils as bu
import physo


# ---------------------------------------------------- SCRIPT ARGS -----------------------------------------------------
parser = argparse.ArgumentParser (description     = "Analyzes MW streams results folder (works on ongoing benchmarks) "
                                                    "and produces .csv files containing results and a summary.",
                                  formatter_class = argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-p", "--path", default = ".",
                    help = "Paths to results folder.")
parser.add_argument("-u", "--list_unfinished", default = 1,
                    help = "Save a list of unfinished runs.")
config = vars(parser.parse_args())

RESULTS_PATH    = str(config["path"])
SAVE_UNFINISHED = bool(int(config["list_unfinished"]))
# ---------------------------------------------------- SCRIPT ARGS -----------------------------------------------------


# ------------------------------- PATHS -------------------------------
# Path where to save the results
PATH_RESULTS_SAVE = os.path.join(RESULTS_PATH, "MW_streams_results_detailed.csv")
# Path where to save jobfile to relaunch unfinished jobs
PATH_UNFINISHED_JOBFILE          = os.path.join(RESULTS_PATH, "jobfile_unfinished")
PATH_UNFINISHED_BUSINESS_JOBFILE = os.path.join(RESULTS_PATH, "jobfile_unfinished_business")


#

@timeout_unix.timeout(2) # Max 20s wrapper (works on unix only)
def timed_compare_expr(trial_expr, target_expr):
    return su.compare_expression(
                        trial_expr              = trial_expr,
                        target_expr             = target_expr,
                        handle_trigo            = True,
                        prevent_zero_frac       = True,
                        prevent_inf_equivalence = True,
                        round_decimal           = 2,
                        verbose                 = True, )

def untimed_compare_expr(trial_expr, target_expr):
    return
def compare_expr(trial_expr, target_expr):
    if platform.system() == "Windows":
        return untimed_compare_expr(trial_expr, target_expr)
    else:
        return timed_compare_expr(trial_expr, target_expr)


# ------------------------------- TARGET EXPRESSION -------------------------------

# todo: add same with opposite in log to get around protected logabs
# Target expression
target_expr_str = np.array([
	   " -2.25433197869809  + 3.77705922384934 * log( 1.0000075063141 *r + 1.0 ) / r ",
       " -2.41436719312905  + 3.77705922384934 * log( 1.0000075063141 *r + 1.0 ) / r ",
       " -2.2447343815812   + 3.77705922384934 * log( 1.0000075063141 *r + 1.0 ) / r ",
       " -1.5859020918779   + 3.77705922384934 * log( 1.0000075063141 *r + 1.0 ) / r ",
       " -2.5645735964909   + 3.77705922384934 * log( 1.0000075063141 *r + 1.0 ) / r ",
       " -1.62503655452927  + 3.77705922384934 * log( 1.0000075063141 *r + 1.0 ) / r ",
       " -2.15162507988352  + 3.77705922384934 * log( 1.0000075063141 *r + 1.0 ) / r ",
       " -1.35017082006533  + 3.77705922384934 * log( 1.0000075063141 *r + 1.0 ) / r ",
       " -1.34999371983704  + 3.77705922384934 * log( 1.0000075063141 *r + 1.0 ) / r ",
       " -0.886739103968145 + 3.77705922384934 * log( 1.0000075063141 *r + 1.0 ) / r ",
       " -1.4852048039817   + 3.77705922384934 * log( 1.0000075063141 *r + 1.0 ) / r ",
       " -1.93110067461651  + 3.77705922384934 * log( 1.0000075063141 *r + 1.0 ) / r ",
       " -2.27868502863944  + 3.77705922384934 * log( 1.0000075063141 *r + 1.0 ) / r ",
       " -1.90140528126145  + 3.77705922384934 * log( 1.0000075063141 *r + 1.0 ) / r ",
       " -1.79236813095344  + 3.77705922384934 * log( 1.0000075063141 *r + 1.0 ) / r ",
       " -2.0266623875962   + 3.77705922384934 * log( 1.0000075063141 *r + 1.0 ) / r ",
       " -1.76631299530485  + 3.77705922384934 * log( 1.0000075063141 *r + 1.0 ) / r ",
       " -1.62558963183134  + 3.77705922384934 * log( 1.0000075063141 *r + 1.0 ) / r ",
       " -2.31576548893306  + 3.77705922384934 * log( 1.0000075063141 *r + 1.0 ) / r ",
       " -1.41578671710615  + 3.77705922384934 * log( 1.0000075063141 *r + 1.0 ) / r ",
       " -1.17092711945236  + 3.77705922384934 * log( 1.0000075063141 *r + 1.0 ) / r ",
       " -1.48716147657053  + 3.77705922384934 * log( 1.0000075063141 *r + 1.0 ) / r ",
       " -1.51377591474388  + 3.77705922384934 * log( 1.0000075063141 *r + 1.0 ) / r ",
       " -1.9125453150739   + 3.77705922384934 * log( 1.0000075063141 *r + 1.0 ) / r ",
       " -1.07822521728563  + 3.77705922384934 * log( 1.0000075063141 *r + 1.0 ) / r ",
       " -1.29561794758918  + 3.77705922384934 * log( 1.0000075063141 *r + 1.0 ) / r ",
       " -1.56992178190473  + 3.77705922384934 * log( 1.0000075063141 *r + 1.0 ) / r ",
       " -2.05315490058432  + 3.77705922384934 * log( 1.0000075063141 *r + 1.0 ) / r ",
       " -1.68884448806975  + 3.77705922384934 * log( 1.0000075063141 *r + 1.0 ) / r ",
       " -2.25433197869809  + 3.77705922384934 * log( - (1.0000075063141 *r + 1.0 ) ) / r ",
       " -2.41436719312905  + 3.77705922384934 * log( - (1.0000075063141 *r + 1.0 ) ) / r ",
       " -2.2447343815812   + 3.77705922384934 * log( - (1.0000075063141 *r + 1.0 ) ) / r ",
       " -1.5859020918779   + 3.77705922384934 * log( - (1.0000075063141 *r + 1.0 ) ) / r ",
       " -2.5645735964909   + 3.77705922384934 * log( - (1.0000075063141 *r + 1.0 ) ) / r ",
       " -1.62503655452927  + 3.77705922384934 * log( - (1.0000075063141 *r + 1.0 ) ) / r ",
       " -2.15162507988352  + 3.77705922384934 * log( - (1.0000075063141 *r + 1.0 ) ) / r ",
       " -1.35017082006533  + 3.77705922384934 * log( - (1.0000075063141 *r + 1.0 ) ) / r ",
       " -1.34999371983704  + 3.77705922384934 * log( - (1.0000075063141 *r + 1.0 ) ) / r ",
       " -0.886739103968145 + 3.77705922384934 * log( - (1.0000075063141 *r + 1.0 ) ) / r ",
       " -1.4852048039817   + 3.77705922384934 * log( - (1.0000075063141 *r + 1.0 ) ) / r ",
       " -1.93110067461651  + 3.77705922384934 * log( - (1.0000075063141 *r + 1.0 ) ) / r ",
       " -2.27868502863944  + 3.77705922384934 * log( - (1.0000075063141 *r + 1.0 ) ) / r ",
       " -1.90140528126145  + 3.77705922384934 * log( - (1.0000075063141 *r + 1.0 ) ) / r ",
       " -1.79236813095344  + 3.77705922384934 * log( - (1.0000075063141 *r + 1.0 ) ) / r ",
       " -2.0266623875962   + 3.77705922384934 * log( - (1.0000075063141 *r + 1.0 ) ) / r ",
       " -1.76631299530485  + 3.77705922384934 * log( - (1.0000075063141 *r + 1.0 ) ) / r ",
       " -1.62558963183134  + 3.77705922384934 * log( - (1.0000075063141 *r + 1.0 ) ) / r ",
       " -2.31576548893306  + 3.77705922384934 * log( - (1.0000075063141 *r + 1.0 ) ) / r ",
       " -1.41578671710615  + 3.77705922384934 * log( - (1.0000075063141 *r + 1.0 ) ) / r ",
       " -1.17092711945236  + 3.77705922384934 * log( - (1.0000075063141 *r + 1.0 ) ) / r ",
       " -1.48716147657053  + 3.77705922384934 * log( - (1.0000075063141 *r + 1.0 ) ) / r ",
       " -1.51377591474388  + 3.77705922384934 * log( - (1.0000075063141 *r + 1.0 ) ) / r ",
       " -1.9125453150739   + 3.77705922384934 * log( - (1.0000075063141 *r + 1.0 ) ) / r ",
       " -1.07822521728563  + 3.77705922384934 * log( - (1.0000075063141 *r + 1.0 ) ) / r ",
       " -1.29561794758918  + 3.77705922384934 * log( - (1.0000075063141 *r + 1.0 ) ) / r ",
       " -1.56992178190473  + 3.77705922384934 * log( - (1.0000075063141 *r + 1.0 ) ) / r ",
       " -2.05315490058432  + 3.77705922384934 * log( - (1.0000075063141 *r + 1.0 ) ) / r ",
       " -1.68884448806975  + 3.77705922384934 * log( - (1.0000075063141 *r + 1.0 ) ) / r ",
       ])
target_expr = np.array([sympy.parse_expr(expr) for expr in target_expr_str])

# ------------------------------- RUN FOLDER DETAILS -------------------------------
# Run folders
run_folder_prefix = "StreamsSR_0_"
folders = os.listdir(RESULTS_PATH)

# ------------------------------- ANALYSIS -------------------------------
t00 = time.time()

# Results lines of dict list
run_results = []
# Unfinished jobs list
unfinished_jobs          = []
# Unfinished + target not recovered job list
unfinished_business_jobs = []

for folder in folders:
    # If folder is a run folder
    if folder.startswith(run_folder_prefix):

        # try:
        run_name = folder[len(run_folder_prefix):]
        i_trial   = int   (run_name.split("_")[0])
        noise     = float (run_name.split("_")[1])
        frac_real = float (run_name.split("_")[2])

        print("--------------------")
        print("Analyzing run :")
        print("i_trial   : %d"%(i_trial))
        print("noise     : %f"%(noise))
        print("frac_real : %f"%(frac_real))


        run_result = {}

        run_result.update(
            {
                "i_trial"   : i_trial,
                "noise"     : noise,
                "frac_real" : frac_real,
            }
        )

        # Pareto expressions pkl
        path_pareto_pkl = os.path.join(RESULTS_PATH, folder, "run_curves_pareto.pkl")
        pareto_expressions = physo.load_pareto_pkl(path_pareto_pkl)

        # Pareto expressions df
        path_pareto_csv = os.path.join(RESULTS_PATH, folder, "run_curves_pareto.csv")
        pareto_expressions_df = pd.read_csv(path_pareto_csv)

        run_result.update(
            {
                "r2"     : pareto_expressions_df.iloc[-1]["r2"],
                "reward" : pareto_expressions_df.iloc[-1]["reward"],
            }
        )

        # Run log
        path_run_log = os.path.join(RESULTS_PATH, folder, "run_curves_data.csv")
        run_log_df = pd.read_csv(path_run_log)

        n_evals = run_log_df["n_rewarded"].sum()
        is_finished = n_evals >= 240_000 # 250k - batch size
        run_result.update(
            {
            "n_evals"     : n_evals,
            "is_finished" : is_finished,
            }
        )

        # --------- Assessing symbolic equivalence ---------

        # Last expression in pareto front
        # (n_realizations,) size as there is one free const value set per realization
        trial_expr = pareto_expressions[-1].get_infix_sympy(evaluate_consts=True)     # (n_realizations,)
        # todo: whole pareto front

        # Comparing any expression found to target expression (with any constants)
        expr = trial_expr[0]
        for texpr in target_expr:
            try:
                expr  = su.clean_sympy_expr(expr, round_decimal=3)
                texpr = su.clean_sympy_expr(texpr, round_decimal=3)
                is_equivalent, report = compare_expr(trial_expr=expr, target_expr=texpr)
            except:
                is_equivalent = False
            if is_equivalent:
                print("Found equivalent expression, breaking.")
                break

        run_result.update(
            {
                "symbolic_solution": is_equivalent,
                "expression"       : su.clean_sympy_expr(trial_expr[0], round_decimal=4),

            }
        )

        # ----- Results .csv -----
        run_results.append(run_result)
        df = pd.DataFrame(run_results)
        df.to_csv(PATH_RESULTS_SAVE, index=False)

        # ----- Listing unfinished jobs -----

        # If job was not finished let's put it in the joblist of runs to be re-started.

        if SAVE_UNFINISHED and (not is_finished):
            command = "python MW_streams_run.py --trial %i --noise %f --frac_real %f"%(i_trial, noise, frac_real)
            unfinished_jobs.append(command)
            bu.make_jobfile_from_command_list(PATH_UNFINISHED_JOBFILE, unfinished_jobs)

        if SAVE_UNFINISHED and (not is_finished) and (not is_equivalent):
            command = "python MW_streams_run.py --trial %i --noise %f --frac_real %f"%(i_trial, noise, frac_real)
            unfinished_business_jobs.append(command)
            bu.make_jobfile_from_command_list(PATH_UNFINISHED_BUSINESS_JOBFILE, unfinished_business_jobs)
        # except:
        #     print("Unable to process folder %s (ignoring it)."%(folder))

# Saving results one last time with sorted lines
df.sort_values(by=["noise", "frac_real", "i_trial",], inplace=True)
df.to_csv(PATH_RESULTS_SAVE, index=False)

t01 = time.time()
print("Total time : %f s"%(t01 - t00))

print(None)