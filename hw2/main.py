import random
from math import ceil, exp
from pathlib import Path


class Component():
    ## Component ##
    # priority
    priority: int
    # transmission time
    trans_time: float
    # period
    period: int

    def __init__(self, priority: int, trans_time: float, period: int):
        self.priority = int(priority)
        self.trans_time = float(trans_time)
        self.period = int(period)
        return

    def __init__(self, comp_tmp: list[int, float, int]):
        self.priority = int(comp_tmp[0])
        self.trans_time = float(comp_tmp[1])
        self.period = int(comp_tmp[2])
        return

    def print(self) -> None:
        print(
            f"priority = {self.priority:2d}, trans_time = {self.trans_time:.3f},",
            f"period = {self.period:4d}.")
        return


class CAN():
    ## Controller Area Network ##
    # transmission of one bit
    tau: float
    # Components
    comps: list[Component] = []

    def __init__(self, tau: float):
        self.tau = tau
        return

    def add(self, comp: Component) -> None:
        self.comps.append(comp)
        return

    def append(self, comps: list[Component]) -> None:
        self.comps += comps
        return

    def get_long_bt(self, comps_idx: int):
        # blocking time of the longest lower or same priority message
        long_bt: float = 0
        c_comp_priority = self.comps[comps_idx].priority
        for comp in self.comps:
            if comp.priority >= c_comp_priority:
                if long_bt == 0:
                    long_bt = comp.trans_time
                elif long_bt < comp.trans_time:
                    long_bt = comp.trans_time
        return long_bt

    def get_wt(self, comps_idx: int):
        long_bt = self.get_long_bt(comps_idx)
        # waiting time: current Q_i
        wt: float = long_bt
        # rhs
        rhs: float = 0
        c_comp_priority = self.comps[comps_idx].priority
        while True:
            ## compute ##
            rhs = long_bt
            for comp in self.comps:
                if comp.priority < c_comp_priority:
                    rhs += comp.trans_time * ceil(
                        (wt + self.tau) / comp.period)
            ## compare  ##
            if ((rhs + self.comps[comps_idx].trans_time) >
                (self.comps[comps_idx].period)):
                # rhs + C_i > T_i
                # constraint violation (the system is not schedulable)
                return 0
            elif wt == rhs:
                # Q_i == rhs
                # compute successfully
                return wt
            else:
                # otherwise
                wt = rhs
                continue

    def compute_single_wc_rt(self, comps_idx: int, b_print:bool = False):
        # worst-case response time
        rt: float = self.get_wt(comps_idx)
        if rt == 0:
            # non-schedulable
            if b_print:
                print("ERROR: non-schedulable")
            return -1
        rt += self.comps[comps_idx].trans_time
        if b_print:
            # print(f'{comps_idx:2d} : rt = {rt}')
            print(rt)
        return rt

    def compute_wc_rt(self, b_print:bool = False):
        total_wc_rt, non_sched_n = 0, 0
        for idx in range(len(self.comps)):
            tmp = self.compute_single_wc_rt(idx, b_print)
            if tmp < 0:
                non_sched_n += 1
            else:
                total_wc_rt += tmp
        if b_print:
            print(total_wc_rt)
            # print(total_wc_rt, non_sched_n)
        return total_wc_rt, non_sched_n

    def get_cost(self, seq:list[int] = None, penalty = 0, b_print:bool = False):
        if seq != None:
            self.do_seq(seq)
        wc_rt, non_sched_n = self.compute_wc_rt(b_print)
        wc_rt += non_sched_n * penalty
        good = True
        if non_sched_n > 0:
            good = False
        return wc_rt, good

    def do_seq(self, seq:list[int]):
        for comp, p in zip(self.comps, seq):
            comp.priority = p
        return

    def swap(self, f_idx, s_idx):
        if f_idx == s_idx:
            return
        tmp_priority = self.comps[f_idx].priority
        self.comps[f_idx].priority = self.comps[s_idx].priority
        self.comps[s_idx].priority = tmp_priority
        return

    def sort(self):
        self.comps = sorted(self.comps, key= lambda comp: comp.priority)
        return

    def print(self) -> None:
        print('tau =', self.tau)
        for comp in self.comps:
            comp.print()
        return


def read_dat(filename: Path, pri: bool = False) -> None:
    # Component: priority, transmission time, period.
    comp_list: list[int, float, int] = []
    ## read file ##
    with open(filename, 'r') as f:
        # Component Number
        comp_num: int = int(f.readline().splitlines()[0])
        # transmission of one bit
        tau: float = float(f.readline().splitlines()[0])
        # class
        can = CAN(tau)
        for i in range(comp_num):
            comp_tmp = (f.readline().splitlines()[0]).strip()
            comp_tmp = comp_tmp.split()
            comp_list.append(comp_tmp)
            can.add(Component(comp_tmp))
    ## print parse ##
    if pri:
        print('com_num =', comp_num)
        print('tau =', tau)
        print('com_list =', comp_list)
    return can, comp_num


def get_two_diff_randint(n_min, n_max):
    a = random.randint(n_min, n_max)
    b = a
    while b == a:
        b = random.randint(n_min, n_max)
    return a, b


def swapping(seq, a, b):
    r_seq = list(seq) # list copy
    tmp = r_seq[a]
    r_seq[a] = r_seq[b]
    r_seq[b] = tmp
    return r_seq


# Simulated Annealing
def SA(can:CAN, n_comp:int, T_start:int, T_frozen:int, ratio:float):
    print("CAN SA starting...")
    print(f"SA | Temp start: {T_start}, frozen: {T_frozen}, ratio: {ratio}")

    # SA value
    constant = 100000
    penalty = 150
    T_current = T_start

    # start sequence
    s = []
    for comp in can.comps:
        s.append(comp.priority)
    s_star = s

    while T_current > T_frozen:
        # pick a neighbor p_prime of p
        a, b = get_two_diff_randint(0, n_comp - 1)
        s_prime = swapping(s, a, b)

        # compute cost
        cost_s, _ = can.get_cost(seq=s, penalty=penalty)
        cost_s_prime, good = can.get_cost(seq=s_prime, penalty=penalty)
        cost_s_star, _ = can.get_cost(seq=s_star, penalty=penalty)

        # checker
        # print(f"Temp | c: {T_current}, f: {T_frozen}")
        # print(f"cost | s*: {cost_s_star}, s: {cost_s}, s': {cost_s_prime, good}")
        print(f"\rcost | s*: {cost_s_star}", end='')

        # compute cost difference
        cost_diff = cost_s_prime - cost_s

        if good and (cost_s_prime < cost_s_star):
            s_star = s_prime

        if cost_diff <= 0:
            s = s_prime
        else:
            prob = random.uniform(0, 1)
            if constant * prob < prob * exp(-1 * cost_diff / T_current):
                s = s_prime

        # Annealing
        T_current *= ratio
    print()
    print("CAN SA was done")
    if not can.get_cost(seq=s_star)[1]:
        print("ERROR: non-schedulable, potential fail in SA.")
    print()
    return s_star


# DEBUG_MODE = True
DEBUG_MODE = False
file_name = 'input.dat'

def main():
    can: CAN
    can, comps_num = read_dat(file_name, DEBUG_MODE)

    ## print CAN and the Components ##
    if DEBUG_MODE:
        can.print()

    print(f"original cost: {can.get_cost()[0]}")

    p = SA(can, comps_num, 2, 1, ratio = 0.999)

    can.do_seq(p)
    can.sort()
    # can.compute_wc_rt(True)
    can.get_cost(b_print=True)

    print()
    can.print()
    print(p)

    return

## result ##
# original cost: 208.56
#  my bast cost: 204.12     (given 2, 1 0.999)
#  my bast cost: 204.12     (given 2, 1 0.9999)

if __name__ == '__main__':
    main()
