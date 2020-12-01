from src.graph import Graph
import pulp
import math


class SolverBased:
    graph = Graph()
    x_variable_array = []
    N = 0
    T = 0
    model = pulp.LpProblem()

    def add_aim_function(self, N, parameter_lists, routing_points, static_points, model):
        """
        需要被重载的函数，向模型中添加目标函数
        @param N 一共有N个点
        @param parameter_lists: 参数列表，一个三维数组，表示xnij (self.N * self.T * self.T)
        @param routing_points: ((node_id, earliest_time_step, lastest_time_step, lastest_routing_time_step),  ... )其中node_id表示点的数量
        @param static_points: ((node_id, earliest_time_step),  ... )其中node_id表示点的数量
        @param model 表示传进来的PuLP模型，添加的约束直接在模型上进行添加即可
        """
        pass

    def generate_constraints(self, N, T, relies, parameter_lists, routing_points, static_points, model):
        """
        需要被重写的函数，用于向模型中添加约束
        @author: wangsaiyu@cqu.edu.cn
        @param N: 一共有N个点
        @param T: 一共有T个回合
        @param relies: 依赖集合，格式如：((x1, y1), (x2, y2), (x3, y3), ...)， 其中(x1, y1)表示有一条从x1出发指向y1的边
        @param parameter_lists: 参数列表，一个字典，{"X":[[], [], ...], "Y":[[], [], ...], "Z":[[], [], ...], }， 每个键值对代表一个表， 表中的每一个元素
                                是一个PuLP的约束变量，添加到模型中的约束应由变量和运算构成
        @param routing_points: ((node_id, earliest_time_step, lastest_time_step, lastest_routing_time_step),  ... )其中node_id表示点的数量
        @param static_points: ((node_id, earliest_time_step),  ... )其中node_id表示点的数量
        @param model: 表示传进来的PuLP模型，添加的约束直接在模型上进行添加即可
        """
        pass

    def __init__(self):
        graph = Graph()

    def read_file(self, file_name):
        """
        用于读取存储于dataset文件夹下的数据集文件
        @param file_name: 文件名，无需输入路径，会自动补充
        @return: 返回一个规格化后的数据
        @author: wangsaiyu@cqu.edu.cn
        """
        with open("../dataset/" + file_name, encoding='utf-8') as file_obj:
            contents = file_obj.read()
            for line in contents.split("\n"):
                line_items = line.split()
                self.graph.add_node(line_items[0], line_items[11], line_items[9], line_items[10])
                for edge in range(4):
                    self.graph.add_edge(line_items[0], line_items[1 + edge * 2], line_items[2 + edge * 2])

        print(self.graph)  # 测试当前图

    def get_latest_routing_time_step(self, node_id):
        """
        获取当前节点的最长路由时间步， 使用了深度优先搜索的方法， 每个点的最晚路由时间步为所有子节点的最晚路由时间步 - 1
        @param node_id: 想要获取最长路由时间步的节点的编号
        @return: 返回当前节点的最长路由时间步，如果是一个普通点，那么就返回当前点的最晚时间步
        @author: wangsaiyu@cqu.edu.cn
        """
        cur_node = self.graph.nodes[node_id]
        if not cur_node.is_changeable:
            return cur_node.latest_time_step
        elif cur_node.latest_routing_time_step != 0:
            return cur_node.latest_routing_time_step
        else:  # 都不是的话，则需要遍历图去进行查询
            cur_latest_routing_time_step = 0
            cur_edge_id = self.graph.adjacency_list[node_id]
            while cur_edge_id != 0:  # 遍历所有子节点，取最大
                cur_edge = self.graph.edges[cur_edge_id]
                cur_latest_routing_time_step = max(cur_latest_routing_time_step,
                                                   self.get_latest_routing_time_step(cur_edge.to_point_id) - 1)
                cur_edge_id = cur_edge.next_edge_id

            # 更新时间步
            cur_node.latest_routing_time_step = cur_latest_routing_time_step
            return cur_latest_routing_time_step

    def get_maneuver_nodes_range(self):
        """
        获取图中的机动点的机动范围， 值得注意的是，在进行该步骤的同时，会统计点的数量以及最高回合数
        @author: wangsaiyu@cqu.edu.cn
        """
        for node_id in self.graph.nodes:
            cur_node = self.graph.nodes[node_id]
            self.N += 1
            self.T = max(self.T, cur_node.latest_time_step + 1)
            if cur_node.is_changeable:  # 如果当前点是机动点，那么就进行查找
                self.get_latest_routing_time_step(node_id)

        print(self.graph)

    def init_model(self):
        """
        创建一个基础模型，并且创建基础参数列表， 参数列表为：
        x_variable_array: 表示PE节点
        @author: wangsaiyu@cqu.edu.cn
        """
        self.model = pulp.LpProblem("prob", pulp.LpMinimize)  # 新建问题
        self.x_variable_array = []
        for point in range(self.N):
            new_x_array = []
            for turn in range(self.T):
                new_x_line = []
                for sub_turn in range(self.T):
                    extend_name = "," + str(point) + "," + str(turn) + "," + str(sub_turn)
                    new_x_line.append(pulp.LpVariable("x" + extend_name, lowBound=0, upBound=1, cat=pulp.LpInteger))
                new_x_array.append(new_x_line)
            self.x_variable_array.append(new_x_array)

    def generate_param_table(self):
        """
        根据模型生成参数列表
        生成参数列表
        """
        res_list = [[[0 for i in range(self.T)] for k in range(self.T)] for j in range(self.N)]
        for variable in self.model.variables():
            if variable.name != "__dummy":
                _, node_id, st_turn, cur_turn = variable.name.split(",")
                node_id, st_turn, cur_turn = int(node_id), int(st_turn), int(cur_turn)
                res_list[node_id][st_turn][cur_turn] = math.floor(variable.varValue + 0.5)
        return res_list

    def show_answer(self):
        """
        用于模型求解后展示答案，直接与自身的模型进行交互即可
        @author: wangsaiyu@cqu.edu.cn
        """
        param_list = self.generate_param_table()  # 获取模型中每个点的值
        # 统计每个时间点，每个点之间的依赖关系，对点之间的依赖关系进行统计后，重新编号，并且输出
        rename_node_counter = self.N
        for try_time in range(self.T - 1):
            for try_node_from in range(self.N):
                node_from_rely_nodes = []
                for try_node_to in range(self.N):  # 遍历有依赖关系的点
                    if self.graph.have_edge(try_node_from + 1, try_node_to + 1):  # 如果有从to到from的依赖
                        for try_from_node_begin_time in range(try_time + 1):  # 如果在本步中有点，那么就继续探查
                            if param_list[try_node_from][try_from_node_begin_time][try_time] == 0:
                                # 本步中没有点，那么就直接跳过本步，继续探测
                                continue
                            # 本步中有点，那么就探查to_node在本步中是否是起点
                            if param_list[try_node_to][try_time + 1][try_time + 1]:  # 如果本步是依赖点的起点，那么就添加边
                                node_from_rely_nodes.append(try_node_to + 1)
                # 当前点的所有到达点试探完毕，进行输出
                if len(node_from_rely_nodes) == 0 and not self.graph.is_origin_node(try_node_from + 1):
                    # 如果没有被依赖，或者在本回合没有给其他点传递，那么就跳过
                    continue
                print("node id {} (node type is {}, origin node id is {}), time step {}, nex node list :: ".format(
                    rename_node_counter, self.graph.get_node_type(try_node_from + 1), try_node_from + 1, try_time
                ))
                rename_node_counter += 1
                for to_node in node_from_rely_nodes:
                    print(to_node, end=", ")

    def run(self, file_name):
        self.read_file(file_name)
        self.get_maneuver_nodes_range()
        self.init_model()
        self.generate_constraints(
            self.N, self.T,  # N, T
            self.graph.generate_relies(),  # relies
            self.x_variable_array,
            self.graph.generate_routing_points_description(),
            self.graph.generate_static_points_description(),
            self.model,  # model
        )
        self.add_aim_function(
            self.N, self.x_variable_array,
            self.graph.generate_routing_points_description(),
            self.graph.generate_static_points_description(),
            self.model,
        )
        self.model.solve()
        self.show_answer()


if __name__ == "__main__":
    runner = SolverBased()
    runner.run("data1")
