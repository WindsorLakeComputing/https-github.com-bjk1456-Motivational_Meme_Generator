
import subprocess

from QuoteEngine.ingestor_interface import ingestor_interface


class txt_ingestor(ingestor_interface):

    def can_ingest(self, path: str):
        p = subprocess.run(['file', path], stdout=subprocess.PIPE).stdout.decode('utf-8').split(' ')
        last_2_words = ' '.join(p[len(p)-2:])
        if(last_2_words == ("ASCII text")):
            return True
        else:
            return False

    def parse(self, path: str):
        with open(path, 'r') as f:
            for line in f:
                if(len(line.strip())):
                    print(f"line is {line}")

if __name__ == "__main__":
    _txt = txt_ingestor()
    _txt.can_ingest("/home/kelbenj/Udacity/src/_data/SimpleLines/SimpleLines.txt")
    if(_txt):
        _txt.parse("/home/kelbenj/Udacity/src/_data/SimpleLines/SimpleLines.txt")