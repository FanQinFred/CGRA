from src.node import Node
from src.edge import Edge


class Graph:
    nodes = {}
    edges = []
    adjacency_list = {}
    number_of_nodes = 0
    number_of_edges = 1

    def __init__(self):
        """
        构造函数，构造一个空的图
        @author: wangsaiyu@cqu.edu.cn
        """
        self.nodes = {}
        self.edges = [Edge(0, 0, 0, 0)]  # 初始情况下有一个为空的
        self.adjacency_list = {}
        self.number_of_nodes = 0

    def add_node(self, point_id, is_changeable, earliest_time_step, latest_time_step):
        """
        向当前图中加入一个节点
        @param point_id: 结点的编号
        @param is_changeable: 表示当前点是否是一个机动点
        @param earliest_time_step: 当前点的最早时间步
        @param latest_time_step: 当前点的最晚时间步
        @author: wangsaiyu@cqu.edu.cn
        """
        point_id, is_changeable, earliest_time_step, latest_time_step = int(point_id), int(is_changeable), int(
            earliest_time_step), int(latest_time_step)
        self.nodes[point_id] = Node(is_changeable, earliest_time_step, latest_time_step)
        self.adjacency_list[point_id] = 0
        self.number_of_nodes += 1

    def add_edge(self, from_point_id, to_point_id, edge_type):
        """
        向图中添加一条边，如果边的起点或终点为0，那么将不执行添加操作
        @param from_point_id: 起点的点id
        @param to_point_id: 终点的点id
        @param edge_type: 边的类型，如果该值为1， 那么就代表迭代间依赖，否则表示迭代内依赖
        @author: wangsaiyu@cqu.edu.cn
        """
        if from_point_id == "0" or to_point_id == "0":  # 若起点或终点为0就直接结束
            return
        from_point_id, to_point_id, edge_type = int(from_point_id), int(to_point_id), int(edge_type)
        self.edges.append(Edge(from_point_id, to_point_id, edge_type, self.adjacency_list[from_point_id]))
        self.adjacency_list[from_point_id] = self.number_of_edges  # 将当前边的前一条边加入
        self.number_of_edges += 1

    def __str__(self):
        return_string = ""
        for node in self.nodes:
            return_string += str(node) + "::" + str(self.nodes[node]) + "\n"
        for i in range(len(self.edges)):
            return_string += str(i) + "::" + str(self.edges[i]) + "\n"
        for st_node_id in self.adjacency_list:
            return_string += str(st_node_id) + "::" + str(self.adjacency_list[st_node_id]) + "\n"

        return return_string
