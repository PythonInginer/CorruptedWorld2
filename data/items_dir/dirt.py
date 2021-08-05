from data.system_dir.standard_item import Item


class Dirt(Item):
    def __init__(self,
                 filename="data/textures_dir/items/dirt.png",
                 item_id=1):
        super().__init__(filename, item_id)
