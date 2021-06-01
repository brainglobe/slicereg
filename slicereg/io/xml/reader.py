from dataclasses import dataclass


@dataclass
class QuickNiiResult:
    ox: float
    # oy: float 
    # oz: float
    # ux: float 
    # uy: float
    # uz: float
    # vx: float 
    # vy: float
    # vz: float
    

def read_quicknii_xml(filename: str):
    data = QuickNiiResult(ox=475.8982543945312)
    return data