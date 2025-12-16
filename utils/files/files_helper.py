import os


def file_read_binary(filename, src_dictionary):
    """
    Generuje plik binarny z przesłanego pliku graficznego.
    :param filename: Nazwa pliku graficznego znajdującego się w katalogu wskazanym przez 'src_dictionary'
    :param src_dictionary: Nazwa katalogu w folderze 'resources'.
    :return: (bytes) Plik w formacie bytes
    """
    path = os.path.join(os.path.dirname(__file__), "..", "resources", src_dictionary, filename)
    with open(path, "rb") as f:
        return f.read()
