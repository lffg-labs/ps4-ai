# ps4-ai/initial-decision-tree
# this code is horrific, but it apparently serve its purpose

from decimal import *
from collections import defaultdict, Counter
from typing import Optional
from dataclasses import dataclass, field
import csv


DEBUG = True
CSV_DELIMITER = ";"


def log2(n: Decimal) -> Decimal:
    return n.ln() / Decimal(2).ln()


@dataclass
class AttrValInfo:
    total: int = field(default_factory=lambda: 0)
    classes: Counter[str] = field(default_factory=Counter)

    def add_class(self, class_val: str) -> str:
        self.total += 1
        self.classes[class_val] += 1


# entropy
def S_simple(counter: Counter[str]) -> Decimal:
    s = Decimal(0)
    for _, count in counter.items():
        d = Decimal(count) / Decimal(counter.total())
        lg = log2(d)
        if lg.is_infinite():
            continue
        s += -d * lg
    return s


# entropy for attribute
def S_attr(instance_count: int, attr_info_map: dict[str, AttrValInfo]) -> Decimal:
    s = Decimal(0)
    total = Decimal(instance_count)
    for info in attr_info_map.values():
        prob = Decimal(info.total) / total
        s_simple = S_simple(info.classes)
        s += prob * s_simple
    return s


def read_raw_data(path: str) -> dict[str, list[str]]:
    cols = defaultdict(list)
    with open(path, newline="") as file:
        reader = csv.DictReader(file, delimiter=";")
        for entry in reader:
            for k, v in entry.items():
                cols[k].append(v)
    return dict(cols)


def compute_attr_map(
    raw_data: dict[str, list[str]], instance_name: str, class_name: str
) -> dict[str, dict[str, AttrValInfo]]:
    cl = raw_data[class_name]  # the class
    attr_map: dict[str, dict[str, AttrValInfo]] = defaultdict(
        lambda: defaultdict(AttrValInfo)
    )
    for attr_name, attr_vals in raw_data.items():
        if attr_name in {instance_name, class_name}:
            continue

        attr_info_map = attr_map[attr_name]
        for instance_index, attr_val in enumerate(attr_vals):
            class_val = cl[instance_index]  # get corresponding class value
            attr_info_map[attr_val].add_class(class_val)

    return attr_map


def find_attr_with_max_gain(
    instance_count: int,
    class_entropy: Decimal,
    attr_map: dict[str, dict[str, AttrValInfo]],
) -> tuple[str, Decimal]:
    max: Optional[tuple[str, Decimal]] = None  # (attr_name, attr_gain)
    for attr_name, attr_info_map in attr_map.items():
        dbg_attr_info_map(attr_name, attr_info_map)
        attr_entropy = S_attr(instance_count, attr_info_map)
        attr_gain = class_entropy - attr_entropy
        dbg("attr entropy is", attr_entropy)
        dbg("   attr gain is", attr_gain)
        if not max or attr_gain > max[1]:
            dbg("  (new max!)")
            max = (attr_name, attr_gain)
        dbg()
    return max


def filter_raw_data(
    attr_name: str, expected_attr_val: str, old: dict[str, list[str]]
) -> dict[str, list[str]]:
    guide = old[attr_name]
    l = len(guide)
    new = defaultdict(list)
    for i in range(0, l):
        for key, values in old.items():
            if guide[i] != expected_attr_val:
                continue
            new[key].append(values[i])
    return dict(new)


def dbg_attr_info_map(attr_name: str, attr_info_map: dict[str, AttrValInfo]):
    if not DEBUG:
        return
    print(f"===== {attr_name} =====")
    for attr_val, attr_val_info in attr_info_map.items():
        print(f"[{attr_val}] (total = {attr_val_info.total})")
        for class_name, class_count in attr_val_info.classes.items():
            print(f"    [{class_name}] ({class_count})")


def dbg(*args):
    if not DEBUG:
        return
    print(*args)


def analyze_level(
    attr_name: str,
    raw_data: dict[str, list[str]],
    levels: int,
    current_level: int,
    instance_name: str,
    class_name: str,
):
    if current_level > levels:
        return
    dbg(f"@@@@@@@ level {current_level} for [{attr_name}] @@@@@@@")

    cl = raw_data[class_name]
    instance_count = len(cl)

    level_class_entropy = S_simple(Counter(cl))
    dbg("class entropy for current level is:", level_class_entropy, "\n")

    attr_map = compute_attr_map(raw_data, instance_name, class_name)
    best_name, best_gain = find_attr_with_max_gain(
        instance_count, level_class_entropy, attr_map
    )
    best_attr_info_map = attr_map[best_name]

    dbg(f"at level {current_level}, best is [{best_name}] with gain of {best_gain}")

    attr_val_queue = []
    for attr_val, attr_info in best_attr_info_map.items():
        if len(attr_info.classes) == 1:
            dbg(f"  finished for [{best_name}]#[{attr_val}] (leaf)")
            continue
        dbg(f"  will recur on [{best_name}]#[{attr_val}]")
        attr_val_queue.append(attr_val)

    dbg(f"finished level {current_level} for [{attr_name}]\n\n\n")

    for attr_val in attr_val_queue:
        new_raw_data = filter_raw_data(best_name, attr_val, raw_data)
        analyze_level(
            f"[{best_name}]#[{attr_val}]",
            new_raw_data,
            levels,
            current_level + 1,
            instance_name,
            class_name,
        )


def analyze(path: str, levels: int, instance_name: str, class_name: str):
    initial_raw_data = read_raw_data(path)
    analyze_level("$root", initial_raw_data, levels, 0, instance_name, class_name)


if __name__ == "__main__":
    analyze(path="rest.csv", levels=1, instance_name="Exemplo", class_name="Resultado")
