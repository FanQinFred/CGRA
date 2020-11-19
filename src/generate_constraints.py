def generate_constraints(N, T, relies, parameter_lists, routing_points, static_points, model):
    """
    用于向模型中添加约束
    @param N: 一共有N个点
    @param T: 一共有T个回合
    @param relies: 依赖集合，格式如：((x1, y1), (x2, y2), (x3, y3), ...)， 其中(x1, y1)表示有一条从x1出发指向y1的边
    @param parameter_lists: 参数列表，一个字典，{"X":[[], [], ...], "Y":[[], [], ...], "Z":[[], [], ...], }， 每个键值对代表一个表， 表中的每一个元素
                           是一个PuLP的约束变量，添加到模型中的约束应由变量和运算构成
    @param routing_points: ((node_id, earliest_time_step, lastest_time_step, lastest_routing_time_step),  ... )其中node_id表示点的数量
    @param static_points: [(node_id, earliest_time_step)]
    @param model: 表示传进来的PuLP模型，添加的约束直接在模型上进行添加即可
    """
    print("generate_constraints")

    for i in range(N):
        for j in range(T):
            model += parameter_lists["X"][i][j] <= 1
            model += parameter_lists["Y"][i][j] <= 1
            model += parameter_lists["Z"][i][j] <= 1
            model += parameter_lists["X"][i][j] >= 0
            model += parameter_lists["Y"][i][j] >= 0
            model += parameter_lists["Z"][i][j] >= 0

    """
    prob = model


    for i in range(len(parameter_lists['X'])):
        prob += parameter_lists['X'][i] + parameter_lists['Y'][i] + parameter_lists['Z'][i] <= 1

    for i in range(len(parameter_lists['X']) - 1):
        prob += abs(parameter_lists['x'][i + 1] - parameter_lists['x'][i]) <= 2

    for i in range(len(parameter_lists['X']) - 1):
        prob += parameter_lists['X'][i + 1] * (parameter_lists['X'][i + 1] - parameter_lists['X'][i]) <= \
                parameter_lists['X'][i + 1 + ll] + parameter_lists['Z'][i + 1 + ll]

    for t in range(T):  # t means clock time  这个不会改
        tot = 0;
        for son in range(get_list):
            tot = tot + x[son][t]
        prob += tot <= 4

    y_sum = 0
    z_sum = 0
    for i in range(len(parameter_lists['X'])):
        y_sum = y_sum + parameter_lists['Y'][i]
        z_sum - z_sum + parameter_lists['Z'][i]
    prob += y_sum <= 1
    pron += z_sum <= 1

    temp = 0
    for i in range(len(parameter_lists['X']) - 1):
        temp = temp + (parameter_lists['Z'][i + 1] - parameter_lists['Z'][i]) * i - (
                    parameter_lists['Y'][i + 1] - parameter_lists['Y'][i]) * i
    opora = temp % 2 + (temp + 1) % 2
    prob += (ll + temp * opora) % ll + 1 >= T

    for t in range(T):
        t_count = 0
        for i in range(x_row):
            t_count = t_count + parameter_lists['X'][i] + parameter_lists['Y'][i] + parameter_lists['Z'][i]
        prob += t_count <= routing_points['node_id']

    pass
    """