class Edge:
    """
    描述图中节点的类，每个对象是一条有向边
    @author: wangsaiyu@cqu.edu.cn
    """
    from_point_id = None  # 起始点编号
    to_point_id = None  # 到达点编号
    edge_type = 0  # 若为0表示内依赖，若为1表示迭代间依赖
    next_edge_id = None  # 在邻接表中下一个边的序号

    def __init__(self, from_point_id, to_point_id, edge_type, next_edge_id):
        """
        新建一个边类型的对象
        @param from_point_id: 起点id
        @param to_point_id: 终点id
        @param edge_type: 边的类型，如果该值为1， 那么就代表迭代间依赖，否则表示迭代内依赖
        @param next_edge_id: 在邻接表中下一个边的序号
        @author: wangsaiyu@cqu.edu.cn
        """
        self.from_point_id = from_point_id
        self.to_point_id = to_point_id
        self.edge_type = edge_type
        self.next_edge_id = next_edge_id

    def __str__(self):
        return "from_point_id: \t" + str(self.from_point_id) + \
               "\t, to_point_id: \t" + str(self.to_point_id) + \
               "\t, edge_type: \t" + str(self.edge_type) + \
               "\t, next_edge_id: \t" + str(self.next_edge_id)
