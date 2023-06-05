import json


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
                break
            elif flag == "1":
                self.notes[index]["content"] = input("Enter new text --> ")
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
        self.notes.sort(key = lambda note: note["timestamp"])
        self.show_notebook()