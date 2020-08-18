'''
Created on 2020/08/17

@author: smallcat
'''

#assume half of ports for intra-rack and the other half for inter-rack
def generate_edge_file(sws, ports, nodes, racks):
    fn = "edges/cpo_s" + str(sws) + "_p" + str(ports) + "_n" + str(nodes) + "_r" + str(racks) + ".edge"
    racks_in_group = ports/2 #racks_in_group == nodes_in_group
    rack_groups = racks/racks_in_group
    node_groups = nodes/racks_in_group
    node_num_begin = sws*racks
    with open(fn, "w") as f:
        f.write("# 0-" + str(node_num_begin-1) + ": switches, " + str(node_num_begin) + "-: hosts\n")
        for sw in range(sws*racks):
            rack = sw/sws
            rack_group = rack/racks_in_group
            sw_num = sw%sws
            sw_group_by_rack = sw_num/(sws/rack_groups) #sw_groups == rack_groups, sw_group <-> link rack_group
            sw_group_by_node = sw_num/(sws/node_groups) #sw_groups == node_groups, sw_group <-> link node_group
            #inter-rack sw-sw
            rack_begin = racks_in_group * sw_group_by_rack
            rack_end = rack_begin + racks_in_group 
            for rack_link in range(rack+1, rack_end):
                sw_link = rack_link * sws + sw_num
                f.write(str(sw) + " " + str(sw_link) + "\n")
            #intra-rack sw-node
            node_begin = node_num_begin + rack * nodes
            node_end = node_begin + nodes
            node_link_begin = node_begin + racks_in_group * sw_group_by_node
            node_link_end = node_begin + racks_in_group * sw_group_by_node + racks_in_group
            for node_link in range(node_link_begin, node_link_end):
                f.write(str(sw) + " " + str(node_link) + "\n")
    #check sw port
    sw_port = [0] * node_num_begin
    with open(fn, "r") as f:
        f.readline()
        line = f.readline().split(" ")
        left = int(line[0])
        right = int(line[1].replace('\n',''))
        if left < node_num_begin:
            sw_port[left] += 1
        if right < node_num_begin:
            sw_port[right] += 1
    for i in range(node_num_begin):
        print i, ": ", sw_port[i]

generate_edge_file(4, 64, 64, 64)