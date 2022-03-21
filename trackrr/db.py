from tinydb import TinyDB, where


class TrackDatabase(TinyDB):
    """Subclass of TinyDB that adds some validation checking"""

    def insert_item(self, item: dict):
        """Inserts item in the database but runs validation checks beforehand"""
        if not self._is_unique(item["name"]):
            raise NotUnique(item["name"])

        self.insert(item)

    def _is_unique(self, name: str) -> bool:
        """Checks if an item with the same name already exists in the database"""
        return not self.search(where("name") == name)


class NotUnique(Exception):
    """Execption used whenever there is conflict with non unique attributes"""

    def __init__(self, name: str):
        super().__init__(f"{name} already exists in the database!")
