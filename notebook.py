import json
from datetime import datetime as dt


class notebook:

    def __init__(self, from_file=False):
        if not from_file:
            self.notes = []
            self.notes_count = 0
        else:
            with open("notebook.json", "r") as file:
                data = json.load(file)
                self.notes = data["notes"]
                self.notes_count = data["notes_count"]


    def save(self):
        with open("notebook.json", "w") as file:
            data = {
                "notes_count": self.notes_count,
                "notes": self.notes
            }
            json.dump(data, file)
        print("Notebook saved succesfully")


    def add(self):
        title = input("Enter a title --> ")
        content = input("Enter a note --> ")
        id = self.notes_count
        timestamp = dt.now().timestamp()

        note = {
            "id": id,
            "title": title,
            "content": content,
            "timestamp": timestamp
        }

        self.notes.append(note)
        self.notes_count += 1
        print("Note saved succesfully")


    def edit(self, id):
        index = -1
        for i in range(len(self.notes)):
            if self.notes[i]["id"] == id:
                index = i
                break
        if index == -1:
            print("Note with this id is not found")
            return

        while (True):
            flag = input('Enter "0" if you want to change the title\n\t"1" if you want to change text --> ')
            if flag == "0":
                self.notes[index]["title"] = input("Enter a new title --> ")
                self.notes[index]["timestamp"] = dt.now().timestamp()
                break
            elif flag == "1":
                self.notes[index]["content"] = input("Enter new text --> ")
                self.notes[index]["timestamp"] = dt.now().timestamp()
                break
            else:
                print("Invalid input, try again")
        print("Note updated succesfully")


    def remove(self, id):
        self.notes = [note for note in self.notes if note["id"] != id]
        # Счётчик заметок не обновляем для корректной генерации
        # идентификаторов
        print("Book updated succesfully")
        
    
    def show_note(self, id):
        found = [note for note in self.notes if note["id"] == id]
        if len(found) == 0:
            print("Note with this id is not found")
            return
        
        for note in found:
            date = dt.fromtimestamp(note["timestamp"])
            print(f'{date}; id: {note["id"]:>5d}; title: {note["title"]};\ntext: {note["content"]}')


    def show_notebook(self):
        for note in self.notes:
            date = dt.fromtimestamp(note["timestamp"])
            print(f'{date}; id: {note["id"]:>5d}; title: {note["title"]};')


    def choose_relevant(self, hours_num):
        current = dt.now()
        for note in self.notes:
            date = dt.fromtimestamp(note["timestamp"])
            delta = current - date
            if delta.seconds/3600 <= hours_num:
                print(f'{date}; id: {note["id"]:>5d}; title: {note["title"]};')


    def sort_by_date(self):
        self.notes.sort(key = lambda note: note["timestamp"], reverse=True)
        self.show_notebook()



def main():
    print('Enter initial command or "/help" to see initial command list')
    while True:
        cmd = input("--> ")
        if cmd == "/help":
            print("/fromfile - load notebook from file")
            print("/new - create new notebook")
        elif cmd == "/new":
            book = notebook(from_file=False)
            break
        elif cmd == "/fromfile":
            try:
                book = notebook(from_file=True)
                break
            except Exception:
                print("File not found or damaged")
        else:
            print(f"Unknown command '{cmd}'")

    print('Enter proccession command or "/help" to see proccession command list')
    while True:
        cmd = input("--> ")
        words = cmd.split()
        if cmd == "/help":
            print("/add - add new note to the book")
            print("/edit <id> - edit note with ID <id>")
            print("/remove <id> - remove note with ID <id>")
            print("/print <id> - print note with ID <id>")
            print("/show - show whole book")
            print("/relevant <hrs> - show notes made <hrs> hours ago and later")
            print("/save - save notebook to the file")
            print("/exit - exit the program")
            print("/timesort - sort notebook by date")

        elif cmd == "/add":
            book.add()

        elif cmd == "/timesort":
            book.sort_by_date()

        elif cmd == "/exit":
            break

        elif cmd == "/save":
            book.save()

        elif cmd == "/show":
            book.show_notebook()

        elif (len(words) == 2):
            try:
                param = int(words[1])
                if words[0] == "/edit":
                    book.remove(param)
                elif words[0] == "/print":
                    book.show_note(param)
                elif words[0] == "/remove":
                    book.remove(param)
                elif words[0] == "/relevant":
                    book.choose_relevant(param)
                else:
                    print(f"Unknown command {cmd}")
            except Exception:
                print(f"Invalid parameter {words[1]}")

        else:
            print(f"Unknown command {cmd}")


if __name__ == '__main__':
    main()