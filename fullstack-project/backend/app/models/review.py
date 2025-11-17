class Review:
    def __init__(self, content):
        self.content = content
        self.views = 0

    def editReview(self, new_content):
        self.content = new_content

    def incrementViews(self):
        self.views += 1
