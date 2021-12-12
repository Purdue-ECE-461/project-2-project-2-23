
class Contributor:
    def __init__(self, name, num_commits, weeks, uid):
        self.name = name
        self.num_commits = num_commits
        self.weeks = weeks
        self.uid = uid
        self.last_week = "--/--/--"
        self.most_recent_commit()

    def __str__(self):
        return f"{self.name} {self.num_commits} {self.last_week} {self.uid}"

    def most_recent_commit(self):
        for week in self.weeks:
            if week.c != 0:
                self.last_week = week.w.timestamp()
