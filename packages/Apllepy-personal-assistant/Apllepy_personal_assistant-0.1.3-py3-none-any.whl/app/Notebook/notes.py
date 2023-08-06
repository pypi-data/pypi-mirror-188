from datetime import datetime
from os import path
from .notesclass import Tag, Note, Notebook
import time

#file_name = "notes.txt"
notebook = Notebook()

# add note
def add_note(*args):
    note = (' '.join(str(p) for p in args))
    if len(note) > 1000:
        return "Number of symbol > 1000, must be less"
    else:
        note = Note(note)    
        result = notebook.add_note(note)
        return result


# def delete_by_tags(tag): #видаляємо нотатки за тегом. Їх може бути декілька
#     tag = Tag(tag)
#     list_by_tag = notebook.search_by_tag(tag)
#     if len(list_by_tag) > 1:
#         user_input = input("More than 1 note found for this tag. Do you want to continue? (y/n): ")
#         if user_input == 'y':
#             for item in list_by_tag:
#                 notebook.del_note(item.number)
#         elif user_input == 'n':
#             return
#         else:
#             raise IndexError
#     elif len(list_by_tag) == 1:
#         notebook.del_note(list_by_tag[0].number)
#     return "There is no such tag"


def edit_note(number): #редагування нотатки
    if int(number) in notebook.keys():
        ch_note = notebook[int(number)]
        user_input = input(f' Input new text >>')
        notebook[int(number)] = Note(user_input)
        ch_note.change_note(user_input)
        #notebook[int(number)] = 
        # print(notebook[int(number_note)])
        print(ch_note)
    else:
        raise IndexError

# add tag to note. You need to know 'number'. You can do some shearch and see number
def add_tags(number, tag):
    tag = Tag(tag)
    notebook[int(number)].add_tag(tag)
    return "ok"

# delete note tag. You need to know 'number'. You can do some shearch and see number
def del_tag(number, tag):
    tag = Tag(tag)
    ch_note = notebook[int(number)]
    ch_note.delete_tag(tag)

# delete note by number. You need to know 'number'. You can do some shearch and see number
def del_note(number):
    number = int(number)
    return notebook.pop(number)

def search_by_tag(tag):
    tag = Tag(tag)
    note_list = notebook.search_by_tag(tag)
    return '\n'.join(repr(p) for p in note_list)   
    

def search_by_text(word):
    result = notebook.search_by_word_in_note(word)
    if not result:
        return 'No notes found with this phrase'
    return '\n'.join(repr(p) for p in result)   

def search_by_date(date):
    print('Date have to be in format %Y-%m-%d')
    date_for_search = datetime.strptime(date, '%Y-%m-%d')    
    result = notebook.search_by_date(date_for_search)
    if not result:
        return 'No notes found with this date'
    return '\n'.join(repr(p) for p in result)   

# notes sorting for date
def sort_by_date():
    pr = ''
    result = notebook.sort_by_date()  
    for p in  result:
        pr = pr + '\n' + p.note_date.strftime('%Y-%m-%d') + "|| " + repr(p)
    return  pr #'\n'.join(repr(p) for p in result)  

# notes sorting for first tag
def sort_by_tag():
    pr = ''
    result = notebook.sort_by_tag()  
    for p in  result:
        if not p.tags:
            str_tag  = 'empty'
        else:
            str_tag =  str(p.tags[0])  
        pr = pr + '\n' + '{:<20}'.format(str_tag) + "|| " + repr(p)
    return  pr # '\n'.join(repr(p) for p in result)  


# show all existing dates
def show_all_dates():
    return notebook.show_all_dates()

# show all existing tags
def show_all_tags():
    print(repr(notebook.show_all_tags()))
    return "Ok"

def show_one_note(number):
    print(f'Full information: {repr(notebook[int(number)])}')
    print(f'Only text: {str(notebook[int(number)])}')
    return "Ok"

# show all existing tags  
def show_all_notes():
    for key in notebook.keys():
        #num = key
        print(f'Note: {repr(notebook[key])}')
        #print(num)
    return 'Ok'

def save_notebook(path = 'notebook.txt'):
    save_status = notebook.serializer(path)
    return save_status

def save_notebook_with_ques(path = 'notebook.txt'):
    user_input = input('Do you want to save notes? (y/n)>>>')
    if user_input not in ('y', 'n'):
        return "Try once more"
    elif user_input == 'y':
        save_status = notebook.serializer(path)
        return save_status
    else:
        return


def load_notebook(path = 'notebook.txt'):
    return notebook.deserializer(path)
    
    
def help(*args):
    print("I know these commands:  add_note, del_note_tag, edit, add_tag, del_note, search_tag, search_text, search_date, sort_by_date, sort_by_tag, show_dates, show_tags,  show_notes, show_single, save, help")


COMMANDS = {
    "add_note": add_note,
#    'del_note_tag': delete_by_tags,
    "edit": edit_note,
    "add_tag": add_tags,
    "del_note": del_note,
    "search_tag": search_by_tag,
    "search_text": search_by_text,
    "search_date": search_by_date,
    "sort_by_date": sort_by_date,
    "sort_by_tag": sort_by_tag,
    "show_dates": show_all_dates,
    "show_tags": show_all_tags,
    "show_notes": show_all_notes,
    "show_single": show_one_note,
    "save": save_notebook,
    "help": help 
}


# def command_parser(u_input: str):
#     for command, key_words in COMMANDS.items():
#         if u_input.startswith(key_words):
#             return command, u_input.replace(key_words, "").strip().split(" ")
#     return None, None

def command_parser(user_input):
    key_word, *args = user_input.split()
    command = None
    key_word = key_word.lower()
   
    #while key_word  not in COMMANDS:
        # if args:
        #     command = command + ' ' + args[0].lower()
        #     args = args[1:]    
        # else:
    #       break
    if key_word   not in COMMANDS:
        return
    command = COMMANDS.get(key_word)
    return command, *args

def notepad():
    print("Notebook is opened")
    
    load_status = load_notebook('notebook.txt')
    print(load_status)

    while True:
        u_input = input(">>>")
        u_input = u_input.lower()
        if u_input in [".", "good bye", "close", "exit", "/", ]:
            print(save_notebook_with_ques())
            print("Good bye!")
            time.sleep(1.5)
            break
        command, *data = command_parser(u_input)
        if not command:
            result = "Enter command or choose 'help'"
        else:
            result = command(*data)
        print(result)    

   


# if __name__ == '__main__':
#     notepad()
