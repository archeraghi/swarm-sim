import sys, getopt, subprocess
from datetime import datetime
import os
import configparser
import multiprocessing
import concurrent.futures

def runflac(idx, out, max_round, nTime ):
    """Use the flac(1) program to convert a music file to FLAC format.

    Arguments:
        idx: track index (starts from 0)
        data: album data dictionary

    Returns:
        A tuple containing the track index and return value of flac.
    """

    num = idx + 1
    process = "python3.6", "run.py", "-n" + str(max_round), "-m 1", "-d" + str(nTime), \
                                 "-r"+ str(num), "-v" + str(0)
    #     #p = subprocess.Popen(process, stdout=out, stderr=out)

    rv = subprocess.call(process, stdout=out, stderr=out)
    return (idx, rv)

def main(argv):
    max_round = 1700
    seed_start = 15
    seed_end = 20
    config = configparser.ConfigParser(allow_no_value=True)
    config.read("config.ini")
    try:
        scenario_file = config.get ("File", "scenario")
    except (configparser.NoOptionError) as noe:
        scenario_file = "init_scenario.py"

    try:
        solution_file = config.get("File", "solution")
    except (configparser.NoOptionError) as noe:
        solution_file = "solution.py"
    nTime = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')[:-1]
    try:
        opts, args = getopt.getopt(argv, "hs:w:r:n:v:", ["scenaro=", "solution="])
    except getopt.GetoptError:
        print('Error: multiple.py -r <randomeSeed> -w <scenario> -s <solution> -n <maxRounds>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('multiple.py -r <randomeSeed> -w <scenario> -s <solution>  -n <maxRounds>')
            sys.exit()
        elif opt in ("-s", "--solution"):
            solution_file = arg
        elif opt in ("-w", "--scenario"):
            sim_file = arg
        elif opt in ("-r", "--seed"):
            seedvalue = int(arg)
        elif opt in ("-n", "--maxrounds"):
           max_round = int(arg)
    round=1
    dir = "./outputs/mulitple/" + str(nTime) + "_" + scenario_file.rsplit('.', 1)[0] + "_" + \
          solution_file.rsplit('.', 1)[0]
    if not os.path.exists(dir):
        os.makedirs(dir)
    out = open(dir + "/multiprocess.txt", "w")
    child_processes = []
    #idx=1
    # with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as tp:
    #     print(os.cpu_count() )
    #     for idx in range(seedvalue):
    #         tp.map(runflac, idx, out, max_round, nTime)
    round = 0
    round_cnt=0
    for seed in range(seed_start, seed_end+1):
        process ="python3.6", "run.py", "-n"+ str(max_round), "-m 1", "-d"+str(nTime),\
                              "-r"+ str(seed), "-v" + str(0)
        if round == os.cpu_count():
            for cp in child_processes:
                cp.wait()
            round = 0
        p = subprocess.Popen(process, stdout=out, stderr=out)
        #p = multiprocessing.Process(target=process)
        round += 1
        round_cnt += 1
        print("Round Nr. ", round_cnt ,"started")
        child_processes.append(p)


    for cp in child_processes:
        cp.wait()


    fout=open(dir+"/all_aggregates.csv","w+")
    # first file:
    for line in open(dir+"/"+str(seed_start)+"/aggregate_rounds.csv"):
        fout.write(line)
    # now the rest:
    for seed in range(seed_start+1, seed_end+1):
        f = open(dir+"/"+str(seed)+"/aggregate_rounds.csv")
        f.__next__() # skip the header
        for line in f:
             fout.write(line)
        f.close() # not really needed
    fout.close()
if __name__ == "__main__":
    main(sys.argv[1:])
