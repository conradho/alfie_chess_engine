from typing import Optional


def process_line(line: str) -> Optional[str]:
    if line == "uci":
        return "id name Alfie\nid author Conrad\nuciok"
    elif line == "isready":
        return "readyok"
    elif line.startswith("debug "):
        # debug [ on | off ]
        pass
    elif line.startswith("setoption "):
        # setoption name  Selectivity value 3
        pass
    elif line.startswith("position "):
        pass
    elif line.startswith("go "):
        # do a bunch of stuff, once we figure out best move
        # for go infinite, this "blocks" and returns when "stop" is called
        return "info depth 99 score cp 64\nbestmove"
    return None
