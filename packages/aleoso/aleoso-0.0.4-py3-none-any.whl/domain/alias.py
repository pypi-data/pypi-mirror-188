from dataclasses import dataclass

@dataclass
class Alias:
    name: str = ""
    open_data: list[str] = list

    def alias_is_available(self):
        pass

    def create_alias(self):
        pass

# comment