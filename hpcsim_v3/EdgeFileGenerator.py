'''
Created on 2020/08/17

@author: smallcat
'''


# assume half of ports for intra-rack and the other half for inter-rack
def generate_edge_file(sws, ports, nodes, racks):
    fn = "edges/cpo_s" + str(sws) + "_p" + str(ports) + "_n" + str(nodes) + "_r" + str(racks) + ".edge"
    racks_in_group = ports / 2  # racks_in_group == nodes_in_group
    if racks % racks_in_group != 0 or nodes % racks_in_group != 0:
        print("check input (ports, nodes, racks)")
        return
    rack_groups = racks / racks_in_group  # require racks%racks_in_group == 0
    node_groups = nodes / racks_in_group  # require nodes%racks_in_group == 0
    if sws % rack_groups != 0 or (sws / rack_groups) % node_groups != 0:  # or sws%node_groups != 0
        print("check input (sws)")
        return
    node_num_begin = sws * racks
    with open(fn, "w") as f:
        f.write("# 0-" + str(node_num_begin - 1) + ": switches, " + str(node_num_begin) + "-: hosts\n")
        for sw in range(sws * racks):
            rack = sw / sws
            rack_group = rack / racks_in_group
            sw_num = sw % sws
            sw_group_by_rack = sw_num / (
                    sws / rack_groups)  # sw_groups == rack_groups, sw_group <-> link rack_group #require sws%rack_groups == 0
            #             sw_group_by_node = sw_num/(sws/node_groups) #sw_groups == node_groups, sw_group <-> link node_group #require sws%node_groups == 0
            sw_group_by_node = sw_num % node_groups  # sw_groups == node_groups, sw <-> link node_group #require (sws/rack_groups)%node_groups == 0
            # inter-rack sw-sw
            rack_begin = racks_in_group * sw_group_by_rack
            rack_end = rack_begin + racks_in_group
            rack_link_begin = rack_begin if rack_begin > rack else rack + 1  # avoid duplex links
            rack_link_end = rack_end
            for rack_link in range(rack_link_begin, rack_link_end):
                # sw_link = rack_link * sws + sw_num
                sw_link = rack_link * sws + rack_group * (sws / rack_groups) + sw_num % (
                        sws / rack_groups)  # rack offset + sw_group offset + sw offset
                f.write(str(sw) + " " + str(sw_link) + "\n")
            # intra-rack sw-node
            node_begin = node_num_begin + rack * nodes
            node_end = node_begin + nodes
            node_link_begin = node_begin + racks_in_group * sw_group_by_node
            node_link_end = node_link_begin + racks_in_group
            for node_link in range(node_link_begin, node_link_end):
                f.write(str(sw) + " " + str(node_link) + "\n")
            # intra-rack sw-sw
            if sw_group_by_rack == rack_group:
                if sw_num % (sws / rack_groups) < sws / rack_groups / 2:
                    f.write(str(sw) + " " + str(sw - sw_num % (sws / rack_groups) + sws / rack_groups - 1 - sw_num % (
                            sws / rack_groups)) + "\n")
    print("racks_in_group: ", racks_in_group)
    print("rack_groups: ", rack_groups)
    print("node_groups: ", node_groups)
    print("node_num_begin: ", node_num_begin)
    # check sw port
    sw_port = [0] * node_num_begin
    with open(fn, "r") as f:
        lines = f.readlines()[1:]
        for line in lines:
            left = int(line.split(" ")[0])
            right = int(line.split(" ")[1].replace('\n', ''))
            if left < node_num_begin:
                sw_port[left] += 1
            if right < node_num_begin:
                sw_port[right] += 1
    for i in range(node_num_begin):
        print(i, ": ", sw_port[i])

# generate_edge_file(sws, ports, nodes, racks)
# generate_edge_file(4, 64, 64, 64)
# generate_edge_file(4, 128, 64, 128)
# generate_edge_file(4, 64, 32, 64)
# generate_edge_file(4, 64, 32, 128)
# generate_edge_file(2, 64, 32, 64)
# generate_edge_file(2, 128, 64, 128)
