import os.path


class Folder:
    def __init__(self, path):
        self.__path = path

    def get_path(self):
        return self.__path

    def listdir(self, filters=None):
        path = self.get_path()
        filters_ = None
        if filters:
            filters_ = filters.split(';')

        files = os.listdir(path)
        if not filters_:
            return files

        results = []
        for file in files:
            filename, extension = os.path.splitext(os.path.join(path, file))
            if extension in filters_:
                results.append(file)
        return results
