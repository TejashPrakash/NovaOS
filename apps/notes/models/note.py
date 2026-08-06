from dataclasses import dataclass


@dataclass
class Note:

    id: int

    title: str

    content: str

    created_at: str

    updated_at: str

    # =====================================

    @classmethod
    def from_dict(cls, data):

        return cls(
            id=data["id"],
            title=data["title"],
            content=data["content"],
            created_at=data["created_at"],
            updated_at=data["updated_at"]
        )

    # =====================================

    def to_dict(self):

        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }