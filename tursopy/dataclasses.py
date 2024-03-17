from dataclasses import dataclass, asdict, fields
from typing import List, Type, TypeVar, Any, Dict

T = TypeVar('T')


@dataclass
class BaseDataClass:
    def to_dict(self):
        return asdict(self)

    @classmethod
    def load(cls: Type[T], data: Dict[str, Any]) -> T:
        field_names = {f.name for f in fields(cls)}
        reduced_data = {k: v for k, v in data.items() if k in field_names}
        return cls(**reduced_data)


#############################################################
#                   PLATFORM API TOKENS                     #
#############################################################
@dataclass
class PlatformTokenRead(BaseDataClass):
    id: str
    name: str


@dataclass
class PlatformTokenCreated(BaseDataClass):
    id: str
    name: str
    token: str


#############################################################
#                        DATABASES                          #
#############################################################
@dataclass
class DatabaseRead(BaseDataClass):
    Name: str
    DbId: str
    Hostname: str
    is_schema: bool
    schema: str
    block_reads: bool
    block_writes: bool
    allow_attach: bool
    regions: List[str]
    primaryRegion: str
    type: str
    hostname: str
    version: str
    group: str
    sleeping: bool


@dataclass
class DatabaseCreated(BaseDataClass):
    DbId: str
    Hostname: str
    Name: str
    IssuedCertCount: int
    IssuedCertLimit: int
