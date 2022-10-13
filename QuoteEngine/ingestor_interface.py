from abc import ABC, abstractmethod
import subprocess
import re
#p = subprocess.run(['emoj', 'dog'], stdout=subprocess.PIPE)
#emoji = p.stdout.decode('utf-8').split(' ')


class ingestor_interface(ABC):

    @abstractmethod
    def can_ingest(self, cls, path: str):
        pass

    def parse(self, path: str, file_delim: str):
        quotes = []
        print("In sup????")

        with open(path, 'r', encoding='utf-8-sig') as f:
            for line in f:
                if(len(line.strip())):
                    if(line.strip() == "body,author"):
                        continue

                    if(line[0] == "\""):
                        body = re.search('\".*\"', line)
                        print(f"HERE INSIDE THE LINE is {line}")
                        #print(f"line {body.group(1)}")
                        body_no_quotes = body.group(0).replace("\"","")
                        print(f"new_str is {body_no_quotes}")
                        author = line.split(file_delim)[-1].strip()
                        print(f"f the author is {author}")
                        quotes.append((body_no_quotes, author))
                        continue




                    #body, author = line.replace('"','').split(" - ")
                    body, author = line.replace('"','').split(file_delim)
                    print(f"line is {line}")
                    print(f"body is {body}")
                    print(f"author is {author}")
                    quotes.append((body, author.rstrip()))
        print("END!!!")
        for q in quotes:
            print(f"q is {q}")
        return quotes


class txt_ingestor(ingestor_interface):

    def can_ingest(self, path: str):
        p = subprocess.run(['file', path], stdout=subprocess.PIPE).stdout.decode('utf-8').split(' ')
        last_2_words = ' '.join(p[len(p)-2:])
        if(last_2_words == ("ASCII text")):
            return True
        else:
            return False

    def parse(self, path: str):
        file_delim = " - "
        return super().parse(path, file_delim)

class pdf_ingestor(ingestor_interface):

    def can_ingest(self, path: str):
        file_type = subprocess.run(['file', path], stdout=subprocess.PIPE).stdout.decode('utf-8').split(' ')[1]
        if(file_type == "PDF"):
            return True
        else:
            return False

    def parse(self, path: str):
        file_delim = " - "
        print(f"the path is {path}")
        new_file = path.replace(".pdf",".txt")
        old_filename = path.split("/")[-1]
        print(f"the filename is {old_filename}")
        print(f"the new file is {new_file}")
        call = subprocess.run(['pdftotext', path, new_file])
        return super().parse(new_file, file_delim)

class docx_ingestor(ingestor_interface):

    def can_ingest(self, path: str):
        file_type = subprocess.run(['file', path], stdout=subprocess.PIPE).stdout.decode('utf-8').split(': ')[1].rstrip()
        print(f"the file_type {file_type}")

        if(file_type == "Microsoft Word 2007+"):
            return True
        else:
            return False

    def parse(self, path: str):
        file_delim = " - "
        print(f"the path is {path}")
        new_file = path.replace(".docx",".txt")
        old_filename = path.split("/")[-1]
        print(f"the filename is {old_filename}")
        print(f"the new file is {new_file}")
        call = subprocess.run(['docx2txt', path, new_file])
        return super().parse(new_file, file_delim)

class csv_ingestor(ingestor_interface):

    def can_ingest(self, path: str):
        filename = path.split("/")[-1]
        file_suffix = filename[-3:].rstrip()
        print(f"the filename is {filename}")
        print(f"the file_suffix is {file_suffix}")

        file_type = subprocess.run(['file', path], stdout=subprocess.PIPE).stdout.decode('utf-8').split(': ')[1].rstrip()
        print(f"the file_type {file_type}")

        if((file_suffix == "csv") and ("ASCII text" in file_type)):
            return True
        else:
            return False

    def parse(self, path: str):
        print("YEEEHAW")
        file_delim = ","
        return super().parse(path, file_delim)




if __name__ == "__main__":
    _csv = csv_ingestor()
    if(_csv.can_ingest("/home/kelbenj/Udacity/src/_data/DogQuotes/DogQuotesCSV.csv")):
        _csv.parse("/home/kelbenj/Udacity/src/_data/DogQuotes/DogQuotesCSV.csv")
