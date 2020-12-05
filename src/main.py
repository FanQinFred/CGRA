from src.solver import Solver


for i in range(2, 42):
    runner = Solver()
    print("========================================================")
    print(i.__str__() + "begin  :: ")
    runner.run("../dataset/raw_datas/g" + i.__str__())
