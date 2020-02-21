import math
from pprint import pprint
import timeit

#######PROCESSING#############

class Library(object):
    def __init__(self, library_id, signup_time, books, books_per_day):
        self.library_id = library_id
        self.signup_time = signup_time
        self.books = books
        self.book_amount = len(self.books)
        self.books_per_day = books_per_day

    def __repr__(self):
        return 'Library: {} \n Signup Time: {} \n Amount of books: {} \n Books per day: {} \n Books: {} \n Time to ' \
               'completion: {}'.format(
            self.library_id, self.signup_time, self.book_amount, self.books_per_day, ', '.join(map(str,self.books)),
            self.time_to_completion()
        )

    def time_to_completion(self, start_time=0):
        return start_time + self.signup_time + math.ceil(
            self.book_amount / self.books_per_day)


def get_input(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        total_counts = lines[0]
        amount_of_books, amount_of_libraries, days_for_scanning = map(
            int, total_counts.split(' '))

        book_scores_line = lines[1]
        book_scores = {}
        for index, value in enumerate(book_scores_line.split(' ')):
            book_scores[index] = value

        return_value = []
        for i in range(amount_of_libraries):
            lib_stats = lines[2 + 2 * i]
            lib_books = lines[2 + 2 * i + 1]
            books_in_library, signup_time, shippings_per_day = map(
                int, lib_stats.split(' '))
            books = list(map(int, lib_books.split(' ')))
            return_value.append(
                Library(i, signup_time, books, shippings_per_day))
        return return_value, book_scores, days_for_scanning

########SOLVING###########
def solve(map_, out_file_name):
    with open("Output/" +out_file_name, 'w+') as out_file:
        len_ = str(len(map_))
        out_file.write(len_ + "\n")
        for key, value in map_.items():
            first_line = str(key)
            second_line = ""
            counter = 0
            for ll in value:
                for l in ll:
                    counter += 1
                    second_line += " " + str(l)
            first_line += " " + str(counter)

            out_file.write(first_line + "\n")
            out_file.write(second_line.strip() + "\n")

def main():
    input_files = [
        'b_read_on.txt', 'c_incunabula.txt', 'd_tough_choices.txt',
        'e_so_many_books.txt', 'f_libraries_of_the_world.txt'
    ]
    out_files = ['b.txt', 'c.txt', 'd.txt', 'e.txt', 'f.txt']

    counter = 0
    for input_file in input_files:

        _, ext = input_file.split('.')
        libraries, book_scores, days_for_scanning = get_input("Input/" + input_file)

        sorted_lib = sort_libraries(libraries)
        for l in sorted_lib:
            sort_books(l.books, book_scores)

        elapsed_days = 0
        scanned = set()

        current_lib = sorted_lib.pop()
        currently_processing = [] #Queue

        library_map = dict()
        while elapsed_days < days_for_scanning:
            if current_lib.signup_time > 0:
                current_lib.signup_time -= 1
            else:
                currently_processing.append(current_lib)
                if len(sorted_lib) > 0:
                    current_lib = sorted_lib.pop()

            process_library_queue(currently_processing, library_map, scanned)
            elapsed_days += 1

            if elapsed_days >= days_for_scanning:
                process_library_queue(currently_processing, library_map,
                                      scanned)

        solve(library_map, out_files[counter])
        counter += 1

def process_library_queue(currently_processing, library_map, scanned):
    for l in currently_processing:
        result, _ = process_books(l, scanned)
        if len(result):
            if l.library_id in library_map:
                library_map[l.library_id].append(result)
            else:
                library_map[l.library_id] = []
                library_map[l.library_id].append(result)
        else:
            currently_processing.remove(l)


def process_books(l, scanned):
    result = []
    for i in range(l.books_per_day):
        if len(l.books):
            selected = l.books.pop()
            while len(l.books) and selected in scanned:
                selected = l.books.pop()
            result.append(selected)
            scanned.add(selected)
        else:
            return result, True

    return result, False

def lib_sorter(l):
    return (l.book_amount * l.books_per_day) / l.signup_time

def sort_libraries(libraries):
    return sorted(libraries,
                  key= lib_sorter)


def sort_books(list_books, book_scores):
    list_books.sort(key=lambda x: (book_scores[x]),reverse=True)


if __name__ == "__main__":
    import timeit
    start = timeit.default_timer()
    main()
    stop = timeit.default_timer()
    print('Time: ', stop - start)  