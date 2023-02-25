from math import ceil
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

    def compute_wc_rt(self, comps_idx: int):
        # worst-case response time
        rt: float = self.get_wt(comps_idx)
        if rt == 0:
            # non-schedulable
            print("ERROR: non-schedulable")
            return -1
        rt += self.comps[comps_idx].trans_time
        # print(f'{comps_idx:2d} : rt = {rt}')
        print(f'{rt}')
        return rt

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


# DEBUG_MODE = True
DEBUG_MODE = False
file_name = 'input.dat'
# file_name = 'input_1.dat'


def main():
    can: CAN
    can, comps_num = read_dat(file_name, DEBUG_MODE)

    ## print CAN and the Components ##
    if DEBUG_MODE:
        can.print()

    for i in range(comps_num):
        can.compute_wc_rt(i)
    return


if __name__ == '__main__':
    main()
