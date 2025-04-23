from dataclasses import dataclass

@dataclass
class Error:
    field: str
    message: str

    def __repr__(self):
        return f"<Error field={self.field}, message={self.message}>"
