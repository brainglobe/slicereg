from dataclasses import dataclass
import xmltodict
from pathlib import Path

from slicereg.io.utils import split_keyvalue_string

# https://www.nitrc.org/plugins/mwiki/index.php?title=quicknii:Coordinate_systems
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
    name: Path
    filename: Path
    height: int
    width: int
    nr: int
    path: Path

    def __post_init__(self):
        if self.name != self.filename:
            raise ValueError('xml name and filename fields should match')

    @property
    def image_path(self) -> Path:
        return self.path / self.name
    

def read_quicknii_xml(filename: str) -> QuickNiiData:

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
        name=Path(series['@name']),
        filename=Path(slice['@filename']),
        height=int(slice['@height']), 
        width=int(slice['@width']), 
        nr=int(slice['@nr']),
        path=Path(filename).parent,
    )
    return data


