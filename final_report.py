class FinalReport:
    def __init__(self):
        self.steps = []

    def add_step(self, step_details):
        self.steps.append(step_details)

    def generate_report(self, file_path):
        with open(file_path, "w") as f:
            for step in self.steps:
                f.write(step + "\n")
