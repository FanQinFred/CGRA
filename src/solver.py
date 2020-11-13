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
        z=0 # z为模拟的目标函数
        model += z
        solved_prob = model.solve()
        return solved_prob
    
    def reduct_graph(self, solved_prob):
        parameter_lists = self.convert_variabl2array(solved_prob)
        return parameter_lists
     


    def get_time_step():
        pass
    def get_node_type():
        pass
    def get_son_node():
        pass
    def print_answer_table(self, parameter_lists, relies):
        """
        @param relies 依赖集合，格式如：((x1, y1), (x2, y2), (x3, y3), ...)， 其中(x1, y1)表示有一条从x1出发指向y1的边
        @param parameter_lists: 参数列表，一个字典，{"X":[[], [], ...], "Y":[[], [], ...], "Z":[[], [], ...], }， 每个键值对代表一个表， 表中的每一个元素
                               是一个PuLP的约束变量，添加到模型中的约束应由变量和运算构成
        """
        #进行每列的分离，此时会产生更多的节点编号
        X=parameter_lists['X']
        Y=parameter_lists['Y']
        Z=parameter_lists['Z']
        X_Revert=[]
        Y_Revert=[]
        Z_Revert=[]
        x_col_len=len(X[0])  #列数
        y_col_len=len(Y[0])
        z_col_len=len(Z[0])
        x_row_len=len(X)  #行数
        y_row_len=len(Y)
        z_row_len=len(Z)
        #反转
        for i in range(x_col_len):
            for j in range(x_row_len):
                temp=[]
                temp.append(X[i][j])
            X_Revert.append(temp)

        for i in range(x_row_len):
            for j in range(x_col_len):
               if(X_Revert[i][j]==1):
                   X_Revert[i][j]==0
                   temp=[0 for x in range(0,x_col_len)]
                   temp[j]=1
                   X_Revert.append(temp)
                   j=0
                   continue 

        node_num=len(X_Revert)  #输出格式行数为node_num  列数为8
        table=[0 for x in range(0,node_num)]
        for i in range(node_num):
            temp=[0,0,0,0,0,0,0,0]
            temp[0]=i+1  #节点编号
            temp[1]=get_time_step()
            temp[2:5]=get_son_node()
            temp[6]=get_node_type()
            temp[7]=get_src_number()
            table.append(temp)
        
        for i in len(table):
            for j in len(table[i]):
                print(table[i][j],end=" ")