import src.solver_based as solver_based

"""
@author: QinFan@cqu.edu.cn
"""


class Solver(solver_based.SolverBased):
    """
    向模型中添加目标函数
    @param N 一共有N个点
    @param parameter_lists: 参数列表，一个字典，{"X":[[], [], ...], "Y":[[], [], ...], "Z":[[], [], ...], }， 每个键值对代表一个表， 表中的每一个元素
                            是一个PuLP的约束变量，添加到模型中的约束应由变量和运算构成
    @param model 表示传进来的PuLP模型，添加的约束直接在模型上进行添加即可
    @author: QinFan@cqu.edu.cn
    """

    def add_aim_function(self, N, parameter_lists, routing_points, static_points, npe, model):
        """
        需要被重载的函数，向模型中添加目标函数
        @param N 一共有N个点
        @param parameter_lists: 参数列表，一个三维数组，表示xnij (self.N * self.T * self.T)
        @param routing_points: ((node_id, earliest_time_step, lastest_time_step, lastest_routing_time_step),  ... )其中node_id表示点的数量
        @param static_points: ((node_id, earliest_time_step),  ... )其中node_id表示点的数量
        @param model 表示传进来的PuLP模型，添加的约束直接在模型上进行添加即可
        """
        X = parameter_lists
        belta = 1
        nins = 0
        for n in range(N):
            earliest_time_step, lastest_time_step, lastest_routing_time_step = self.get_earliest_time_step_lastest_time_step_lastest_routing_time_step(
                n + 1, routing_points, static_points)
            for i in range(earliest_time_step, lastest_routing_time_step + 1):
                for j in range(i, lastest_routing_time_step + 1):
                    nins += X[n][i][j]
        model += belta * npe - nins
        pass

    def get_earliest_time_step_lastest_time_step_lastest_routing_time_step(self, node_id, routing_points,
                                                                           static_points):
        for ii in range(len(routing_points)):
            if routing_points[ii][0] == node_id:
                #print(routing_points[ii][1], routing_points[ii][2], routing_points[ii][3])
                return routing_points[ii][1], routing_points[ii][2], routing_points[ii][3]
        for ii in range(len(static_points)):
            if static_points[ii][0] == node_id:
                #print(static_points[ii][1], static_points[ii][1], static_points[ii][1])
                return static_points[ii][1], static_points[ii][1], static_points[ii][1]

    def is_routing_point(self, node_id, routing_points, static_points):
        for ii in range(len(routing_points)):
            if routing_points[ii][0] == node_id:
                return 1
        for ii in range(len(static_points)):
            if static_points[ii][0] == node_id:
                return 0
        return 0

    def generate_constraints(self, N, T, relies, parameter_lists, routing_points, static_points, npe, model):
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

        X = parameter_lists
        # print(routing_points)

        # 唯一性，仅可在表中选一列
        for n in range(N):  # 选择节点 节点编号为ii+1
            # 对所有的算子，可调度算子个非可调度算子
            earliest_time_step, lastest_time_step, lastest_routing_time_step = \
                self.get_earliest_time_step_lastest_time_step_lastest_routing_time_step(n + 1, routing_points,
                                                                                        static_points)
            sum_xnii = 0
            for i in range(earliest_time_step, lastest_routing_time_step + 1):
                sum_xnii += X[n][i][i]
            model += (sum_xnii == 1)

        # 排他性
        # 对所有的算子，可调度算子个非可调度算子
        for n in range(N):  # 选择节点 节点编号为ii+1
            for kk in range(T):
                for pp in range(T):
                    if kk != pp:
                        for jj in range(T):
                            model += X[n][kk][kk] + X[n][pp][jj] <= 1

        for static_point in static_points:
            for i in range(T):
                for j in range(T):
                    if i == j and i == static_point[1]:
                        model += (X[static_point[0] - 1][i][j] == 1)
                    else:
                        model += (X[static_point[0] - 1][i][j] == 0)

        # 依赖约束——1
        """
        for rely_idx in range(len(relies)):
            father = relies[rely_idx][0]
            son = relies[rely_idx][1]
            earliest_time_step, lastest_time_step, lastest_routing_time_step = self.get_earliest_time_step_lastest_time_step_lastest_routing_time_step(
                son, routing_points, static_points)
            i2_sum = 0
            for i2 in range(earliest_time_step, lastest_routing_time_step + 1):
                i2_sum += i2 * X[son - 1][i2][i2]
            for i1 in range(T):
                i1_sum = 0
                for j1 in range(T):
                    i1_sum += i1 * X[father - 1][i1][j1]
                model += i1_sum -i2_sum + 1 <= 0
        """

        for rely_idx in range(len(relies)):
            n1 = relies[rely_idx][0]
            n2 = relies[rely_idx][1]
            for i2 in range(1, T):
                sum_n1_i1_i2s1 = 0
                for i1 in range(T):
                    sum_n1_i1_i2s1 += X[n1 - 1][i1][i2 - 1]
                model += X[n2 - 1][i2][i2] - sum_n1_i1_i2s1 <= 0

        # 依赖约束——2
        """
        for rely_idx in range(len(relies)):
            father = relies[rely_idx][0]
            son = relies[rely_idx][1]
            earliest_time_step, lastest_time_step, lastest_routing_time_step = self.get_earliest_time_step_lastest_time_step_lastest_routing_time_step(
                son, routing_points, static_points)
            i2_sum = 0
            for i2 in range(earliest_time_step, lastest_routing_time_step + 1):
                i2_sum += X[son - 1][i2][i2]
            for i1 in range(T):
                i1_sum = 0
                for j1 in range(T):
                    i1_sum += j1 * X[father - 1][i1][j1]
                model += i1_sum - i2_sum + 1 <= 0
        """
        # PE资源约束
        for j in range(T):
            sum_ij = 0
            for n in range(N):
                earliest_time_step, lastest_time_step, lastest_routing_time_step = self.get_earliest_time_step_lastest_time_step_lastest_routing_time_step(
                    n + 1, routing_points, static_points)
                for i in range(earliest_time_step, lastest_routing_time_step + 1):
                    sum_ij += X[n][i][j]
            model += sum_ij <= npe
