# flask_app/models.py
class Document:
    def __init__(self, title, content):
        self.title = title
        self.content = content

    def __repr__(self):
        return f"<Document {self.title}>"
