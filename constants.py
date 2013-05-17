class Constants(object):
    """
    This class is meant to add an easy way to dynamically scale zoom, center area size, etc
    """
    def __init__(self):
        self.refresh_interval_millis = 75
        self.mouse_offset = -5
        self.display_image_pxs = 140
        self.capture_image_pxs = 15
        self.sub_image_pxs = 10
        self.set_dependent_values()

    def set_dependent_values(self):
        self.sub_image_anchor_px = self.display_image_pxs / 2 - self.sub_image_pxs / 2
        self.display_image_edge_pxs = self.display_image_pxs - 1
