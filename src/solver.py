import src.solver_based as solver_based


class Solver(solver_based.SolverBased):
    """
    用于求解的类，继承于SolverBased
    """
    def add_aim_function(self, N, parameter_lists, model):
        """
        向模型中添加目标函数
        @param N 一共有N个点
        @param parameter_lists: 参数列表，一个字典，{"X":[[], [], ...], "Y":[[], [], ...], "Z":[[], [], ...], }， 每个键值对代表一个表， 表中的每一个元素
                               是一个PuLP的约束变量，添加到模型中的约束应由变量和运算构成
        @param model 表示传进来的PuLP模型，添加的约束直接在模型上进行添加即可
        """
        pass

    def reduct_graph(self, solved_prob):
        parameter_lists = self.convert_variabl2array(solved_prob)

    def print_answer_table(self, parameter_lists, relies):
        """
        @param relies 依赖集合，格式如：((x1, y1), (x2, y2), (x3, y3), ...)， 其中(x1, y1)表示有一条从x1出发指向y1的边
        @param parameter_lists: 参数列表，一个字典，{"X":[[], [], ...], "Y":[[], [], ...], "Z":[[], [], ...], }， 每个键值对代表一个表， 表中的每一个元素
                               是一个PuLP的约束变量，添加到模型中的约束应由变量和运算构成
        """
        pass
