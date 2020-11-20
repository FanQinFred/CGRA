from src.graph import Graph
from src.generate_constraints import generate_constraints
import pulp
import math


class SolverBased:
    graph = Graph()
    x_variable_array = []
    y_variable_array = []
    z_variable_array = []
    N = 0
    T = 0
    model = pulp.LpProblem()

    def __init__(self):
        graph = Graph()

    def convert_variabl2array(self, solved_prob):
        """
        根据给出的解，生成x，y，z数据表
        @param solved_prob: 运行后的解
        @return: 返回一个字典，其中可通过下标x_variable_array, y_variable_array, z_variable_array访问三个表格
        """
        res_x_variable_array = [[0 for i in range(self.T)] for j in range(self.N)]
        res_y_variable_array = [[0 for i in range(self.T)] for j in range(self.N)]
        res_z_variable_array = [[0 for i in range(self.T)] for j in range(self.N)]

        # 定义不同的ref应当写入那个数组
        write_goal = {
            "x": res_x_variable_array,
            "y": res_y_variable_array,
            "z": res_z_variable_array,
        }

        for variable in solved_prob.variables():
            if variable.name != "__dummy":
                ref, node_id, turn_id = variable.name.split(",")
                node_id, turn_id = int(node_id), int(turn_id)
                write_goal[ref][node_id][turn_id] = math.floor(variable.varValue + 0.5)

        return {
            "X": res_x_variable_array,
            "Y": res_y_variable_array,
            "Z": res_z_variable_array,
        }

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
        y_variable_array: 表示向内存存储
        z_variable_array: 表示向内存读取
        @author: wangsaiyu@cqu.edu.cn
        """
        self.model = pulp.LpProblem("prob", pulp.LpMinimize)  # 新建问题
        self.x_variable_array, self.y_variable_array, self.z_variable_array = [], [], []
        for point in range(self.N):
            new_x_line, new_y_line, new_z_line = [], [], []
            for turn in range(self.T):
                extend_name = "," + str(point) + "," + str(turn)
                new_x_line.append(pulp.LpVariable("x" + extend_name, lowBound=0, upBound=21, cat=pulp.LpInteger))
                new_y_line.append(pulp.LpVariable("y" + extend_name, lowBound=0, upBound=21, cat=pulp.LpInteger))
                new_z_line.append(pulp.LpVariable("z" + extend_name, lowBound=0, upBound=21, cat=pulp.LpInteger))
            self.x_variable_array.append(new_x_line)
            self.y_variable_array.append(new_y_line)
            self.z_variable_array.append(new_z_line)

    def add_aim_function(self, N, parameter_lists, model):
        """
            需要被重载的函数，向模型中添加目标函数
            @param N 一共有N个点
            @param parameter_lists: 参数列表，一个字典，{"X":[[], [], ...], "Y":[[], [], ...], "Z":[[], [], ...], }， 每个键值对代表一个表， 表中的每一个元素
                                   是一个PuLP的约束变量，添加到模型中的约束应由变量和运算构成
            @param model 表示传进来的PuLP模型，添加的约束直接在模型上进行添加即可
        """
        pass

    def pre_print_answer_table(self, resolved_xyz, time_steps, relies):
        """
        需要被重写的函数
        @author: wangsaiyu@cqu.edu.cn
        @param resolved_xyz 是已经求解出值了的大表格
        @param time_steps 每个节点的最早时间步，最晚时间步，最晚路由时间步
        @param relies 节点间的依赖关系,
                     格式如：((x1, y1), (x2, y2), (x3, y3), ...)，
                     其中(x1, y1)表示有一条从x1出发指向y1的边
        """
        print("ERROR :: NO DUO TAI")
        pass

    def two_dim_array_reverse_interface(self, array):

        new_array = [[0 for i in range(len(array))] for j in range(len(array[0]))]
        for i in range(len(new_array)):
            for j in range(len(new_array[0])):
                new_array[i][j] = array[j][i]

        return new_array

    def run(self, file_name, II=None):
        self.read_file(file_name)
        self.get_maneuver_nodes_range()
        self.init_model()
        generate_constraints(
            self.N, self.T,  # N, T
            self.graph.generate_relies(),  # relies
            {"X": self.x_variable_array, "Y": self.y_variable_array, "Z": self.z_variable_array},  # param_lists
            self.graph.generate_routing_points_description(),
            self.graph.generate_static_points_description(),
            self.model,  # model
        )
        self.add_aim_function(
            self.N, {"X": self.x_variable_array, "Y": self.y_variable_array, "Z": self.z_variable_array}, self.model,
        )
        self.model.solve()

        #print(pulp.LpStatus[self.model.status])
        #print(self.convert_variabl2array(self.model))
        self.pre_print_answer_table(
            self.convert_variabl2array(self.model),
            self.graph.generate_all_points_description(),
            self.graph.generate_relies()
        )


if __name__ == "__main__":
    runner = SolverBased()
    runner.run("data1")
