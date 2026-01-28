class AutoFeatureManager:
    def __init__(self, owner=False):
        self.owner = owner

    def activate_all(self, owner=False):
        if not owner:
            return
        print("[AUTO FEATURE] All proposed features activated")

    def check_proposals(self, owner=False):
        if not owner:
            return
        print("[AUTO FEATURE] Feature proposals checked")
