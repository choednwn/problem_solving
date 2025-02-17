import glob
import os

websites = list()


def main():
    Website("Baekjoon")
    Website("LeetCode")
    Website("AdventOfCode")

    Markdown()


class Website:
    def __init__(self, folder_name):
        self.folder_name = folder_name
        self.files = list()
        self.lang_count = dict()  # count of solutions per language
        self.recent = str()  # most recent solution

        self.ignored_exts = [".txt", ".a", ".o", ".out", ".DS_Store"]

        # actions
        global websites
        websites.append(self)
        self.scan_count()
        self.find_recent()

    def scan_count(self):
        for dir in os.walk(self.folder_name):
            for file in dir[2]:
                if not file.startswith(".") and file.find(".") != 1:
                    file_extension = file[file.find("."):]

                    if file_extension not in self.ignored_exts:
                        path = str()
                        fmt_dir: str = dir[0].replace(
                            "\\", "/") + "/"

                        if fmt_dir == "/":
                            path = file
                        else:
                            path = fmt_dir + file

                        # add file to self.files
                        self.files.append(path)

                        # increment count
                        if file_extension in self.lang_count.keys():
                            self.lang_count[file_extension] += 1
                        else:
                            self.lang_count[file_extension] = 1

    def find_recent(self):
        self.recent = max(self.files, key=os.path.getmtime).removeprefix(
            self.folder_name + "/")

    def get_stats(self) -> tuple:
        total_count = 0
        for count in self.lang_count.values():
            total_count += count

        most_used_lang = max(self.lang_count, key=(
            lambda key: self.lang_count[key]))
        match most_used_lang:
            case ".c":
                most_used_lang = "C"
            case ".cpp":
                most_used_lang = "C++"
            case ".cs" | ".csx":
                most_used_lang = "C#"
            case ".py":
                most_used_lang = "Python"
            case ".java":
                most_used_lang = "Java"
            case ".js":
                most_used_lang = "JavaScript"
            case ".ts":
                most_used_lang = "TypeScript"
            case ".rs":
                most_used_lang = "Rust"
            case _:
                most_used_lang = "Other"

        # folder_name, total_count, most_used_lang, recent
        return self.folder_name, total_count, most_used_lang, self.recent


class Markdown:
    def __init__(self):
        self.file = "README.md"
        self.updated_text = list()

        global websites
        self.websites = websites

        self.update_md()
        self.write_md()

    def update_md(self):
        # non-replacing text
        with open(self.file, "r", encoding="utf-8") as md:
            lines = md.readlines()
            deletion_start_line = len(lines)

            # find starting line for replacing
            for ln, text in enumerate(lines):
                if text.startswith("|"):
                    deletion_start_line = ln
                    break

            # adds non-replacing content to self.updated_text
            for ln, line in enumerate(lines):
                if ln < deletion_start_line:
                    self.updated_text.append(line)
        md.close()

        # replaced text
        self.updated_text.append(
            "| Website | Solved | Most used language | Recent |\n")
        self.updated_text.append("|-|-|-|:-|\n")

        for site in websites:
            name, total_count, most_used_lang, recent = site.get_stats()
            self.updated_text.append(
                f"|[{name}]({name})|{total_count}|{most_used_lang}|[{
                    recent}]({name}/{recent.replace(' ', '%20')})|\n"
            )

    def write_md(self):
        with open(self.file, "w") as md:
            md.writelines(self.updated_text)
        md.close()


if __name__ == "__main__":
    main()
