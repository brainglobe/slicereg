from dataclasses import dataclass
import xmltodict

from slicereg.io.utils import split_keyvalue_string


@dataclass
class QuickNiiData:
    ox: float
    oy: float 
    oz: float
    ux: float 
    uy: float
    uz: float
    vx: float 
    vy: float
    vz: float
    first: int
    last: int
    name: str
    filename: str
    height: int
    width: int
    nr: int
    

def read_quicknii_xml(filename: str):
    with open(filename, mode='rb') as f:
        metadata = xmltodict.parse(f)
    
    series = metadata['series']
    slice = series['slice']
    coords = split_keyvalue_string(slice['@anchoring'], sep1="&", sep2="=")

    data = QuickNiiData(
        ox=coords['ox'], oy=coords['oy'], oz=coords['oz'], 
        ux=coords['ux'], uy=coords['uy'], uz=coords['uz'], 
        vx=coords['vx'], vy=coords['vy'], vz=coords['vz'],
        first=int(series['@first']), 
        last=int(series['@last']),
        name=series['@name'], 
        filename=slice['@filename'],
        height=int(slice['@height']), 
        width=int(slice['@width']), 
        nr=int(slice['@nr'])
    )
    return data


