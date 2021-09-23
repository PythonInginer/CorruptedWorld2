from data.system_dir.standard_item import Item


class Dirt(Item):
    def __init__(self,
                 filename="data/textures_dir/items/dirt_item3.png",
                 item_id=1):
        super().__init__(filename, item_id)
