import os


class SolverBased:
    graph = None

    def convert_variabl2array(self, solved_prob):
        return []

    def read_file(self, file_name):
        """
        用于读取存储于dataset文件夹下的数据集文件
        @param file_name: 文件名，无需输入路径，会自动补充
        @return: 返回一个规格化后的数据
        """

        with open("../dataset/" + file_name, encoding='utf-8') as file_obj:
            contents = file_obj.read()
            points = contents.split("\n")
            print(points)
            self.graph = contents

    def run(self, file_name):
        self.read_file(file_name)


if __name__ == "__main__":
    runner = SolverBased()
    runner.run("data1")
