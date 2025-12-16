from dataclasses import dataclass
from typing import Any


@dataclass()
class GameReportingGroup:
    id: str
    name: str
    created_at: str
    created_by: str
    updated_at: Any
    updated_by: Any

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            created_at=data.get('createdAt'),
            created_by=data.get('createdBy'),
            updated_at=data.get('updatedAt'),
            updated_by=data.get('updatedBy')
        )


class GameReportingGroupsList(list[GameReportingGroup]):
    @classmethod
    def from_dict(cls, data: dict):
        items = [GameReportingGroup.from_dict(gr) for gr in data.get('items', [])]
        return cls(items)
