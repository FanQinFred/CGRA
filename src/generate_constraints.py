
"""
用于向模型中添加约束
@param N 一共有N个点
@param T 一共有T个回合
@param relies 依赖集合，格式如：((x1, y1), (x2, y2), (x3, y3), ...)， 其中(x1, y1)表示有一条从x1出发指向y1的边
@param parameter_lists 参数列表，一个字典，{"X":[[], [], ...], "Y":[[], [], ...], "Z":[[], [], ...], }， 每个键值对代表一个表， 表中的每一个元素
                       是一个PuLP的约束变量，添加到模型中的约束应由变量和运算构成
@param routing_points ((node_id, earliest_time_step, lastest_time_step, lastest_routing_time_step),  ... )其中node_id表示点的数量
@param model 表示传进来的PuLP模型，添加的约束直接在模型上进行添加即可
"""
def generate_constraints(N, T, relies, parameter_lists, routing_points, model):
    pass;

