from domain.alias import Alias


class AliasDNS(Alias):

    def alias_is_available(self):
        return self.name not in self.open_data

    def create_alias(self):
        if self.alias_is_available():
            self.open_data.append(self.name)
