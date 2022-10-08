from abc import ABC, abstractmethod
import subprocess
#p = subprocess.run(['emoj', 'dog'], stdout=subprocess.PIPE)
#emoji = p.stdout.decode('utf-8').split(' ')


class ingestor_interface(ABC):

    @abstractmethod
    def can_ingest(self, cls, path: str):
        pass

    @abstractmethod
    def parse(self, cls, path: str):
        pass


class txt_ingestor(ingestor_interface):

    def can_ingest(self, path: str):
        p = subprocess.run(['file', path], stdout=subprocess.PIPE).stdout.decode('utf-8').split(' ')
        last_2_words = ' '.join(p[len(p)-2:])
        if(last_2_words == ("ASCII text")):
            return True
        else:
            return False

    def parse(self, path: str):
        quotes = []
        with open(path, 'r') as f:
            for line in f:
                if(len(line.strip())):
                    body, author = line.replace('"','').split(" - ")
                    print(f"line is {line}")
                    print(f"body is {body}")
                    print(f"author is {author}")
                    quotes.append((body, author.rstrip()))
        print("END!!!")
        for q in quotes:
            print(f"q is {q}")
        return quotes


if __name__ == "__main__":
    _txt = txt_ingestor()
    _txt.can_ingest("/home/kelbenj/Udacity/src/_data/SimpleLines/SimpleLines.txt")
    if(_txt):
        _txt.parse("/home/kelbenj/Udacity/src/_data/SimpleLines/SimpleLines.txt")
