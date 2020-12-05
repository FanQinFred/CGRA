import pandas as pd


def read_dataset(_from, _to):
    excel = pd.read_excel(_from)
    node_index = excel["kernel name:"][5:]
    to_node1 = excel["Unnamed: 1"][5:]
    to_node2 = excel["Unnamed: 2"][5:]
    to_node3 = excel["Unnamed: 3"][5:]
    to_node4 = excel["Unnamed: 4"][5:]
    e_t_s = excel["Unnamed: 5"][5:]
    l_t_s = excel["Unnamed: 6"][5:]
    is_movable = excel["Unnamed: 7"][5:]
    have_father = excel["Unnamed: 8"][5:]

    with open(_to, "w") as file:
        for i in range(len(node_index)):
            print("{} {} 0 {} 0 {} 0 {} 0 {} {} {} {}".format(
                node_index[i + 5], to_node1[i + 5], to_node2[i + 5], to_node3[i + 5], to_node4[i + 5],
                e_t_s[i + 5], l_t_s[i + 5], is_movable[i + 5], have_father[i + 5]
            ), end="" if i == len(node_index) - 1 else "\n", file=file)
    return excel


if __name__ == "__main__":

    import os

    path = "../dataset/tables/"
    for file in os.listdir(path):
        if file.split(".")[1] != "xls" and file.split(".")[1] != "xlsx":
            continue
        temp = read_dataset(path + file, "../dataset/raw_datas/" + file.split(".")[0])
