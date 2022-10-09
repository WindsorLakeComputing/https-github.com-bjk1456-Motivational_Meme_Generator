from abc import ABC, abstractmethod
import subprocess
#p = subprocess.run(['emoj', 'dog'], stdout=subprocess.PIPE)
#emoji = p.stdout.decode('utf-8').split(' ')


class ingestor_interface(ABC):

    @abstractmethod
    def can_ingest(self, cls, path: str):
        pass

    def parse(self, path: str, file_delim: str):
        quotes = []
        print("In sup????")

        with open(path, 'r') as f:
            for line in f:
                if(len(line.strip())):
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

    def parse(self, path: str, file_delim: str):
        super().parse(path, file_delim)

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
        super().parse(new_file, file_delim)




if __name__ == "__main__":
    _pdf = pdf_ingestor()
    _pdf.can_ingest("/home/kelbenj/Udacity/src/_data/DogQuotes/DogQuotesPDF.pdf")
    if(_pdf):
        _pdf.parse("/home/kelbenj/Udacity/src/_data/DogQuotes/DogQuotesPDF.pdf")
