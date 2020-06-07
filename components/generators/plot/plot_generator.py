import subprocess
import pandas as pd


def plot_generator(directory):
    data = pd.read_csv(directory+"/rounds.csv")
    i = 1
    plot = subprocess.Popen(['gnuplot', '--persist'], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            universal_newlines=True)
    plot.stdin.write("set datafile separator ',' \n")

    plot.stdin.write('set xlabel "Rounds" \n')
    for bla in data.columns:
        if i >= 5:
            plot.stdin.write('set ylabel "%s" \n' % (bla))
            plot.stdin.write("set outputs '" + directory + "/rounds_%s.png' \n" % (bla))
            plot.stdin.write("set term png giant size 800,600 font 'Helvetica,20' \n")
            plot.stdin.write(
                "plot '" + directory + "/rounds.csv' using 2:" + str(i) + " title '" + bla + "' with lines axis x1y1 smooth unique \n")
            plot.stdin.write("set terminal pdf monochrome font 'Helvetica,10' \n")
            plot.stdin.write("set outputs '" + directory + "/rounds_%s.pdf' \n" % (bla))
            plot.stdin.write("replot \n")
        i += 1

    data = pd.read_csv(directory+"/agent.csv")
    i = 1
    plot = subprocess.Popen(['gnuplot', '--persist'], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            universal_newlines=True)
    plot.stdin.write("set datafile separator ',' \n")

    plot.stdin.write('set xlabel "Agent" \n')
    for bla in data.columns:
        if i >= 3 :
            plot.stdin.write('set ylabel "%s" \n' % (bla))
            plot.stdin.write("set term png giant size 800,600 font 'Helvetica,20' \n")
            plot.stdin.write("set outputs '" + directory + "/agent_%s.png' \n" % (bla))
            plot.stdin.write(
                "plot '" + directory + "/agent.csv' using 2:" + str(
                    i) + " title '" + bla + "' with lines axis x1y1 smooth unique \n")
            plot.stdin.write("set terminal pdf monochrome font 'Helvetica,10' \n")
            plot.stdin.write("set outputs '" + directory + "/agent_%s.pdf' \n" % (bla))
            plot.stdin.write("replot \n")
        i += 1

    plot.stdin.write('quit\n')

