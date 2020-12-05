class Node:
    """
    用于描述一个图中的节点，描述节点类型、开始、结束、路由时间步
    最后， is_changeable记录了该节点是否有机动性
    """
    is_changeable = False  # 表示当前点是否有机动性，若为0则无机动性
    earliest_time_step = 0  # 最早时间步
    latest_time_step = 0  # 最晚时间步
    latest_routing_time_step = 0  # 路由事件步

    def __init__(self, is_changeable, earliest_time_step, latest_time_step):
        """
        构造函数，给出点的一些基本信息，构造一个点
        @param is_changeable: 表示当前点是否是一个机动点
        @param earliest_time_step: 当前点的最早时间步
        @param latest_time_step: 当前点的最晚时间步
        """
        self.is_changeable = True if is_changeable != 0 else False
        self.earliest_time_step = earliest_time_step
        self.latest_time_step = latest_time_step

    def __str__(self):
        return "is_changeable: \t" + str(self.is_changeable) + \
               "\t, earliest_time_step: \t" + str(self.earliest_time_step) + \
               "\t, latest_time_step: \t" + str(self.latest_time_step) + \
               "\t, latest_routing_time_step: \t" + str(self.latest_routing_time_step)