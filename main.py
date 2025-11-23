from PetriNet import PetriNet
from BFS import bfs_reachable
from DFS import dfs_reachable
from BDD import bdd_reachable


def main():
    # 1. Task 1: đọc PNML -> PetriNet
    pn = PetriNet.from_pnml("SimpleMutex.pnml")
    print("=== Loaded Petri Net ===")
    print(pn)  # in I, O, M0 để kiểm tra

    # 2. Task 2: Explicit reachability (BFS + DFS)
    print("\n=== Task 2: Explicit BFS ===")
    reachable_bfs = bfs_reachable(pn)
    print("BFS reachable markings:")
    for m in reachable_bfs:
        print(m)
    print("Total BFS:", len(reachable_bfs))

    print("\n=== Task 2: Explicit DFS ===")
    reachable_dfs = dfs_reachable(pn)
    print("DFS reachable markings:")
    for m in reachable_dfs:
        print(m)
    print("Total DFS:", len(reachable_dfs))

    # 3. Task 3: BDD-based reachability
    print("\n=== Task 3: BDD Reachability ===")
    bdd, count = bdd_reachable(pn)
    print("Number of reachable markings (via BFS inside BDD):", count)
    # nếu muốn xem size BDD:
    try:
        print("BDD DAG size:", bdd.dag_size)
    except AttributeError:
        pass
    print("Done.")


if __name__ == "__main__":
    main()
