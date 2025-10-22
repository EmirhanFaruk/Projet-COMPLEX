# TODO: MAKE FUNCS HERE TO SAVE THE GRAPHS AND RESULTS
from pathlib import Path
from typing import Any


def toStringGraph(graph: Any) -> str:
    nodes = list(graph.nodes())
    edges = list(graph.edges())
    res = "Nombre de sommets\n"
    res += f"{len(nodes)}\n"
    res += "Sommets\n"
    for node in nodes:
        res += f"{node}\n"
    res += "Nombre d aretes\n"
    res += f"{len(edges)}\n"
    res += "Aretes\n"
    for edge in edges:
        res += f"{edge[0]} {edge[1]}\n"
    return res


def saveGraphToFile(graph: Any, filename: str) -> None:
    out_dir = Path("graphs")
    out_dir.mkdir(parents=True, exist_ok=True)
    p = out_dir / filename
    # Use Path.open for better portability
    with p.open("w", encoding="utf-8") as f:
        f.write(toStringGraph(graph))
    print(f"Graph saved to {p}")