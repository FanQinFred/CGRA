from src.solver import Solver

runner = Solver()
for i in range(1, 42):
    print("========================================================")
    print(i.__str__() + "begin  :: ")
    runner.run("../dataset/raw_datas/g" + i.__str__())
