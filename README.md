# Meme Generator

The goal of this project is to build a "meme generator" – a multimedia application to dynamically generate memes, including an image with an overlaid quote. The content team spent countless hours writing quotes in a variety of filetypes. A solution is included to load quotes from each file that will show off my fancy new Python skills. 
## Overview

This application will:

    Interact with a variety of complex filetypes. This emulates the kind of data encountered in a data engineering role.
    Load quotes from a variety of filetypes (PDF, Word Documents, CSVs, Text files).
    Load, manipulate, and save images.
    Accept dynamic user input through a command-line tool and a web service. This emulates the kind of work encountered as a full stack developer.

This project demonstrates:

    Object-oriented thinking in Python, including abstract classes, class methods, and static methods.
    DRY (don’t repeat yourself) principles of class and method design.
    Working with modules and packages in Python.

Quote Engine

The Quote Engine module is responsible for ingesting many types of files that contain quotes. For our purposes, a quote contains a body and an author:

"This is a quote body" - Author

This module is composed of many classes that demonstrate complex inheritance, abstract classes, classmethods, strategy objects and other fundamental programming principles.
Quote Format

Example quotes are provided in a variety of files. Take a moment to review the file formats in ./_data/SimpleLines and ./_data/DogQuotes. Your task is to design a system to extract each quote line-by-line from these files.
Ingestors

An abstract base class, IngestorInterface should define two methods with the following class method signatures:

def can_ingest(cls, path: str) -> boolean
def parse(cls, path: str) -> List[QuoteModel]

Separate strategy objects realize IngestorInterface for each file type (csv, docx, pdf, txt).


Meme Engine Module

The Meme Engine Module is responsible for manipulating and drawing text onto images. It reinforces object-oriented thinking while demonstrating skill using a more advanced third party library for image manipulation.
