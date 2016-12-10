class ProductionBlock(object):
    """"
    :param left - string por the left size
    :param right - list of productions (production is a list of strings (tokens or non-terminals))
                    list for a production can be empty - meaning an <epsilon> production
    """""
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

    def __str__(self, *args, **kwargs):
        if not hasattr(self, "left"):
            return "<no-init>"
        if not hasattr(self, "right"):
            return "<no valid productions>"
        result = ""
        left = self.left
        right = self.right
        for production in right:
            result += str(left) + " ->"
            for name in production:
                result += " " + str(name)
            result += "\n"
        return result