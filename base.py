class baseModel:
    __instances = {}
    __err = {}

    def getInstance(self,cls):
        if(cls not in self.__instances):
            self.__instances[cls]=cls()
            return self.__instances[cls]
        return self.__instances[cls]

    def setError(self, errno, error):
        self.__err["errno"] = errno
        self.__err["error"] = error
        return self.__err

    def getError(self):
        return self.__err

    def check(self):
        if("errno" in self.__err.keys()):
            return true
        if("error" in self.__err.keys()):
            return true
        return false