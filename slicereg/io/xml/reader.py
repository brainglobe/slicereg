from dataclasses import dataclass
from _pytest.monkeypatch import V
import xmltodict


@dataclass
class QuickNiiResult:
    ox: float
    oy: float 
    oz: float
    ux: float 
    uy: float
    uz: float
    vx: float 
    vy: float
    vz: float
    

def read_quicknii_xml(filename: str):
    with open(filename, mode='rb') as f:
        metadata = xmltodict.parse(f)
    anchoring = metadata['series']['slice']['@anchoring']
    coords = {(kv := pair.split('='))[0]: float(kv[1]) for pair in anchoring.split('&')}
    data = QuickNiiResult(
        ox=coords['ox'], oy=coords['oy'], oz=coords['oz'], 
        ux=coords['ux'], uy=coords['uy'], uz=coords['uz'], 
        vx=coords['vx'], vy=coords['vy'], vz=coords['vz'],
    )
    return data