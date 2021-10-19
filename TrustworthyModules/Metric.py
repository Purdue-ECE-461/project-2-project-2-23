class Metric:
    def __init__(self, priority, module_name):
        self.priority = priority
        self.submetric_weights = 0
        self.score = 0
        self.name = module_name

