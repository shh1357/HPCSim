'''
Created on 2020/08/17

@author: smallcat
'''

#assume half of ports for intra-rack and the other half for inter-rack
def generate_edge_file(sws, ports, nodes, racks):
    fn = "edges/cpo_s" + str(sws) + "_p" + str(ports) + "_n" + str(nodes) + "_r" + str(racks) + ".edge"
    rack_groups = racks/(ports/2)
    with open(fn, "w") as f:
        f.write("# 0-" + str(sws*racks-1) + ": switches, " + str(sws*racks) + "-: hosts\n")
        for sw in range(sws*racks):
            rack = sw/sws
            rack_group = rack/(ports/2)
        for sw in range(sws*racks/rack_groups):
            for n

generate_edge_file(4, 64, 64, 64)