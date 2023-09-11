
class CorruptedSaveFileError(Exception): #class for the exception object used when loading a corrupted savefile

    def __init__(self, message): #initializes error and sets message
        super(CorruptedSaveFileError, self).__init__(message)


class CorruptedLevelError(Exception): #class for the exception object used when loading a corrupted level file

    def __init__(self, message): #initializes error and sets message
        super(CorruptedLevelError, self).__init__(message)
