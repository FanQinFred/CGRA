def generate_constraints(N, T, relies, parameter_lists, routing_points, static_points, model):
    """
    用于向模型中添加约束
    @param N: 一共有N个点
    @param T: 一共有T个回合
    @param relies: 依赖集合，格式如：((x1, y1), (x2, y2), (x3, y3), ...)， 其中(x1, y1)表示有一条从x1出发指向y1的边
    @param parameter_lists: 参数列表，一个字典，{"X":[[], [], ...], "Y":[[], [], ...], "Z":[[], [], ...], }， 每个键值对代表一个表， 表中的每一个元素
                            是一个PuLP的约束变量，添加到模型中的约束应由变量和运算构成
    @param routing_points: ((node_id, earliest_time_step, lastest_time_step, lastest_routing_time_step),  ... )其中node_id表示点的数量
    @param static_points: ((node_id, earliest_time_step),  ... )其中node_id表示点的数量
    @param model: 表示传进来的PuLP模型，添加的约束直接在模型上进行添加即可
    """

    prob = model

    x = parameter_lists['X']
    print(x)
    y = parameter_lists['Y']
    z = parameter_lists['Z']

    for i in range(len(static_points)):
        for t in range(T):
            if t != static_points[i][1]:
                prob += x[i][t] == 0

    for i in range(N):
        for t in range(T):
            prob += x[i][t] + y[i][t] + z[i][t] <= 1

    for i in range(1, N):
        for t in range(T):
            print(abs(-1))
            if (x[i][t] - x[i - 1][t])<0:
                prob += (x[i - 1][t]-x[i][t]) <= 2
            else:
                prob += (x[i][t] - x[i - 1][t]) <= 2

    for i in range(len(relies)):
        for t in range(T):
            prob += x[relies[i][1]][t] * (x[relies[i][1]][t] - x[relies[i][1]][t]) <= x[relies[i][1] - 1][t] + z[
                relies[i][1] - 1]

    for t in range(T):
        tot = 0
        for i in range(N):
            tot = tot + x[i][t]
        prob += tot <= 4

    y_sum = 0
    z_sum = 0
    for i in range(len(parameter_lists['X'])):
        y_sum = y_sum + sum(y[i])
        z_sum - z_sum + sum(z[i])
    prob += y_sum <= 1
    prob += z_sum <= 1

    temp = 0
    for t in range(T):
        for i in range(1, N):
            temp = temp + (z[i + 1][t] - z[i][t]) * i - (y[i + 1][t] - y[i][t]) * i
        opora = temp + temp + 1
        prob += temp * opora + 1 >= T

    for i in range(len(routing_points)):
        t_count = 0
        for t in range(T):
            t_count = t_count + x[routing_points[i][0]][t] + y[routing_points[i][0]][t] + z[routing_points[i][0]][t]
    prob += t_count <= routing_points[i][2] - routing_points[i][1] + 1


    prob.solve()

    pass