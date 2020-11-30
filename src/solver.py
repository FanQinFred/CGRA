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

    def add_aim_function(self, N, parameter_lists, model):
        # 目标函数的权重系数
        belta = 2
        nins = 0
        Npe = 0
        x = parameter_lists["X"]
        y = parameter_lists["Y"]
        z = parameter_lists["Z"]
        for i in range(len(x[0])):
            for j in range(len(x)):
                nins = x[i][j] + y[i][j] + z[i][j]
        nins -= len(x[0])
        max_Npe = 0
        for i in range(len(x[0])):
            for j in range(len(x)):
                temp_value = x[i][j] + y[i][j] + z[i][j]
            if temp_value > max_Npe:
                max_Npe = temp_value
        Npe = max_Npe
        model += belta * nins - Npe

    """
    @author: QinFan@cqu.edu.cn
    """

    def reduct_graph(self, solved_prob):
        parameter_solved_lists = self.convert_variabl2array(solved_prob)
        return parameter_solved_lists

    """
    @param col_number 传入节点所在的列号
    @param X 返转后且重新编号后的调度表格 
    @author: QinFan@cqu.edu.cn
    """

    def get_time_step(self, col_number, X):
        for i in range(len(X[col_number])):
            if (X[col_number][i] == 1):
                return i + 1

    """
    @author: QinFan@cqu.edu.cn
    """

    def get_node_type(self):
        pass

    """
    @author: QinFan@cqu.edu.cn
    """

    def get_son_node(self):
        pass

    """
    @author: QinFan@cqu.edu.cn
    """

    def get_first_one_raw_num(self, resolved_xyz, i):
        a = -1
        raw_num = len(resolved_xyz[0])
        for j in range(raw_num):
            if (resolved_xyz[j][i] == 1):
                a = j
                break
        return a

    """
    @author: QinFan@cqu.edu.cn
    @param resolved_xyz 是已经求解出值了的大表格
    @param time_steps 每个节点的最早时间步，最晚时间步，最晚路由时间步
    @param relies 节点间的依赖关系,
                  格式如：((x1, y1), (x2, y2), (x3, y3), ...)，
                  其中(x1, y1)表示有一条从x1出发指向y1的边
    """

    def pre_print_answer_table(self, resolved_xyz, time_steps, relies):
        resolved_xyz["X"] = self.two_dim_array_reverse_interface(resolved_xyz["X"])
        resolved_xyz["Y"] = self.two_dim_array_reverse_interface(resolved_xyz["Y"])
        resolved_xyz["Z"] = self.two_dim_array_reverse_interface(resolved_xyz["Z"])
        resolved_xyz_merged = resolved_xyz["X"] + resolved_xyz["Y"] + resolved_xyz["Z"]
        relies_list = []
        for i in range(len(relies)):
            bridge = []
            for j in range(len(relies[0])):
                bridge.append(relies[i][j])
            relies_list.append(bridge)
        self.print_answer_table(resolved_xyz_merged, time_steps, relies_list)

    """
    @author: QinFan@cqu.edu.cn
    """

    def print_answer_table(self, resolved_xyz, time_steps, relies):
        # 保留原始的resolved_xyz
        old_resolved_xyz = []
        for i in range(len(resolved_xyz)):
            bridge = []
            for j in range(len(resolved_xyz[0])):
                bridge.append(resolved_xyz[i][j])
            old_resolved_xyz.append(bridge)
        # 定义额外的参数
        node_cnt = len(resolved_xyz[0])  # 原始图中算子的数量
        old_node_cnt = node_cnt
        # 获取变化前列数
        col_num = len(resolved_xyz[0])
        # 获取行数
        raw_num = len(resolved_xyz)
        # 给出i，j返回新的一个节点的编号
        new_node_number_record = [[-1 for i in range(col_num)] for j in range(raw_num)]
        # 统计resolved_xyz中1的个数
        one_number_in_src_resolved_xyz = 0
        for i in range(len(resolved_xyz)):
            for j in range(len(resolved_xyz[0])):
                if resolved_xyz[i][j] == 1:
                    one_number_in_src_resolved_xyz += 1
        # print(one_number_in_src_resolved_xyz," lalalalalla")
        node_original_node_number = [-1 for x in range(one_number_in_src_resolved_xyz)]
        # 节点类型
        node_type = []
        # for i in range(len(resolved_xyz[0])):
        for i in range(one_number_in_src_resolved_xyz):
            node_type.append(-1)
        # 遍历每一列的每一个1
        for i in range(col_num):
            # 处理插入路由节点后依赖的改变
            a = -1  # 最晚的1所在的时间步，时间步从0开始算起
            for j in range(raw_num):
                if (resolved_xyz[j][i] == 1):
                    a = j
            # 存在问题
            b = time_steps[i][1]  # i列对应的节点的最晚时间步
            if (b >= a):
                pass
                # 用节点a所形成的新的编号更新节点间的依赖关系
            else:
                # 用最晚时间步对应的新的节点编号更新依赖关系
                pass
            # 处理插入的路由节点
            for j in range(raw_num):
                if j == self.get_first_one_raw_num(old_resolved_xyz, i):
                    new_node_number_record[j][i] = i + 1  # 将列号作为节点的新的编号
                    node_type[i] = 0  # 为之前的路由算子，将类型记录为0
                    node_original_node_number[i] = i + 1
                if resolved_xyz[j][i] == 1 and j != self.get_first_one_raw_num(old_resolved_xyz, i):
                    # 将其剥离，以将表格形成one-hot形式
                    resolved_xyz[j][i] = 0
                    # 剥离后放到表格最后一列去
                    node_cnt += 1  # 节点数加一，因为加入了新的节点
                    node_type[node_cnt - 1] = 1  # 为新插入的路由算子，将类型记录为1
                    # 给出i，j返回新的一个节点的编号
                    new_node_number_record[j][i] = node_cnt
                    node_original_node_number[node_cnt - 1] = i + 1  # 比如10号结点的下标为9
                    for ii in range(raw_num):
                        resolved_xyz[ii].append(1 if ii == j else 0)

        # 处理节点的时间步
        scheduled_time_steps = [-1 for x in range(len(resolved_xyz[0]))]  # 先全部初始化为-1
        for i in range(len(resolved_xyz[0])):  # 列
            a = self.get_first_one_raw_num(resolved_xyz, i)
            scheduled_time_steps[i] = a
        # 子节点
        for i in range(len(old_resolved_xyz[0])):  # 列
            for j in range(len(old_resolved_xyz) - 1):
                if old_resolved_xyz[j][i] == 1 and old_resolved_xyz[j + 1][i] == 1:
                    # print("something")
                    rely = []
                    rely.append(new_node_number_record[j][i])
                    rely.append(new_node_number_record[j + 1][i])
                    # print(rely,"rely")
                    relies.append(rely)  # 添加加入新的路由算子后的新的依赖
        # 开始输出table
        result_table = []
        for i in range(len(resolved_xyz[0])):
            result_table.append([])
        # 一行一行的输出
        for i in range(len(resolved_xyz[0])):  # 一列对应一个节点，一个节点对应一行
            # 节点新的编号
            result_table[i].append(i + 1)
            # 节点的时间步
            result_table[i].append(scheduled_time_steps[i])
            # 子节点1,2,3,4
            son_node_cnt = 0
            for ii in range(len(relies)):
                if (relies[ii][0] == i + 1):
                    son_node_cnt += 1
                    result_table[i].append(relies[ii][1])
            # print("son_node_cnt= ",son_node_cnt)
            if son_node_cnt > 4:
                print("子节点数大于4，错误")
                exit(0)
            if son_node_cnt < 4:
                for _ in range(4 - son_node_cnt):
                    result_table[i].append(0)
            # 节点类型
            if (i > old_node_cnt - 1):  # 新节点
                result_table[i].append(1)
            else:
                result_table[i].append(0)
            # 节点原节点编号：路由节点传递的原始节点的编号
            # print(i)
            # print(node_original_node_number[i])
            result_table[i].append(node_original_node_number[i])
        # 节点编号 时间步 子节点1 子节点2 子节点3 子节点4 节点类型 源节点编号
        # 打印出table查看
        for i in range(len(result_table)):
            if (len(result_table[i]) != 8):
                print("存在某一行长度不为8")
                exit(0)
            # print("第",i+1,"行的长度：",len(result_table[i]))
            for j in range(len(result_table[i])):
                print(result_table[i][j], end=' ')
            print()
