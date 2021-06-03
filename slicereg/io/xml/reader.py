from dataclasses import dataclass
import xmltodict

from slicereg.io.utils import split_keyvalue_string


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
    coords = split_keyvalue_string(anchoring, sep1="&", sep2="=")
    data = QuickNiiResult(
        ox=coords['ox'], oy=coords['oy'], oz=coords['oz'], 
        ux=coords['ux'], uy=coords['uy'], uz=coords['uz'], 
        vx=coords['vx'], vy=coords['vy'], vz=coords['vz'],
    )
    return data


