import sys, getopt, subprocess
from datetime import datetime
import os
import configparser


def main(argv):
    max_round = 2000
    seedvalue = 1
    config = configparser.ConfigParser(allow_no_value=True)
    config.read("config.ini")
    scenario = config.get ("File", "scenario")

    solution = config.get("File", "solution")
    local_time = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')[:-1]
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
            solution = arg
        elif opt in ("-w", "--scenario"):
            scenario = arg
        elif opt in ("-r", "--seed"):
            seedvalue = int(arg)
        elif opt in ("-n", "--maxrounds"):
           max_round = int(arg)
    round=1
    dir = "./outputs/mulitple/" + str(local_time)+ \
          "_" + scenario + "_" + \
          solution
    if not os.path.exists(dir):
        os.makedirs(dir)
    out = open(dir+"/multiprocess.txt", "w")
    child_processes = []
    for seed in range(1, seedvalue+1):
        process ="python3.6", "run.py", "-w"+ scenario,"-s" + solution \
                 ,"-n" + str(max_round), "-m 1", "-d"+str(local_time),\
                              "-r" + str(seed), "-v" + str(0)
        p = subprocess.call(process, stdout=out, stderr=out)
        print("Round Nr. ", round ,"finished")
        child_processes.append(p)
        round += 1
    #
    # for cp in child_processes:
    #     cp.wait()


    fout=open(dir+"/all_aggregates.csv","w+")
    # first file:
    for line in open(dir+"/"+str(1)+"/aggregate_rounds.csv"):
        fout.write(line)
    # now the rest:
    for seed in range(2, seedvalue+1):
        f = open(dir+"/"+str(seed)+"/aggregate_rounds.csv")
        f.__next__() # skip the header
        for line in f:
             fout.write(line)
        f.close() # not really needed
    fout.close()
if __name__ == "__main__":
    main(sys.argv[1:])
