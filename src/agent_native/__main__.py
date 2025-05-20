from .ide import IDE
from .view import IDEApp

if __name__ == "__main__":
    text = ["print('hello')", "print('world')"]
    ide = IDE(initial_text=text)
    app = IDEApp(ide)
    app.run()