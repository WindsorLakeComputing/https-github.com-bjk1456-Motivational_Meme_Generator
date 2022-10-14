from abc import ABC, abstractmethod
import subprocess
import re
from docx import Document
from pathlib import Path

class ingestor_interface(ABC):

    @abstractmethod
    def can_ingest(self, cls, path: str):
        pass

    def parse(self, path: str, file_delim: str):
        quotes = []
        with open(path, 'r', encoding='utf-8-sig') as f:
            for line in f:
                if(len(line.strip())):
                    if(line.strip() == "body,author"):
                        continue

                    if(line[0] == "\""):
                        body = re.search('\".*\"', line)
                        body_no_quotes = body.group(0).replace("\"","")
                        author = line.split(file_delim)[-1].strip()
                        quotes.append((body_no_quotes, author))
                        continue
                    body, author = line.replace('"','').split(file_delim)
                    quotes.append((body, author.rstrip()))
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
        new_file = path.replace(".pdf",".txt")
        old_filename = path.split("/")[-1]
        call = subprocess.run(['pdftotext', path, new_file])
        return super().parse(new_file, file_delim)

class docx_ingestor(ingestor_interface):

    def can_ingest(self, path: str):
        file_type = subprocess.run(['file', path], stdout=subprocess.PIPE).stdout.decode('utf-8').split(': ')[1].rstrip()
        if(file_type == "Microsoft Word 2007+"):
            return True
        else:
            return False

    def parse(self, path: str):
        file_delim = " - "
        new_file = path.replace(".docx",".txt")
        docx = Document(path)
        txt_fle = Path(new_file)
        txt_fle.touch(exist_ok=True)
        docx_lines = []
        for p in docx.paragraphs:
            docx_lines.append(p.text)

        with open(txt_fle, 'w+') as outfile:
            for l in docx_lines:
                outfile.write(l)
                outfile.write('\n')

        return super().parse(new_file, file_delim)

class csv_ingestor(ingestor_interface):

    def can_ingest(self, path: str):
        filename = path.split("/")[-1]
        file_suffix = filename[-3:].rstrip()
        file_type = subprocess.run(['file', path], stdout=subprocess.PIPE).stdout.decode('utf-8').split(': ')[1].rstrip()
        if((file_suffix == "csv") and ("ASCII text" in file_type)):
            return True
        else:
            return False

    def parse(self, path: str):
        file_delim = ","
        return super().parse(path, file_delim)
