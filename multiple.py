import sys, getopt, subprocess
from datetime import datetime




def main(argv):
    max_round = 100
    seedvalue = 5
    nTime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')[:-1]
    try:
        opts, args = getopt.getopt(argv, "hs:w:r:n:v:", ["solution=", "world="])
    except getopt.GetoptError:
        print('Error: multiple.py -r <randomeSeed> -s <solution> -w <world> -n <maxRounds>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('multiple.py -r <randomeSeed> -s <solution> -w <world> -n <maxRounds>')
            sys.exit()
        elif opt in ("-s", "--solution"):
            solution_file = arg
        elif opt in ("-w", "--world"):
            world_file = arg
        elif opt in ("-r", "--seed"):
            seedvalue = int(arg)
        elif opt in ("-n", "--maxrounds"):
           max_round = int(arg)

    for seed in range(1, seedvalue+1):
        subprocess.call(["python3.6", "run.py", "-n"+ str(max_round), "-m 1", "-d"+str(nTime), "-r"+ str(seed), "-v 0"] )




    fout=open("./outputs/mulitple/"+str(nTime)+"/all_aggregates.csv","a")
    # first file:
    for line in open("./outputs/mulitple/"+str(nTime)+"/"+str(1)+"/aggregate_rounds.csv"):
        fout.write(line)
    # now the rest:
    for seed in range(2, seedvalue+1):
        f = open("./outputs/mulitple/"+str(nTime)+"/"+str(seed)+"/aggregate_rounds.csv")
        f.__next__() # skip the header
        for line in f:
             fout.write(line)
        f.close() # not really needed
    fout.close()
if __name__ == "__main__":
    main(sys.argv[1:])
