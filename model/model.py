from database.DAO import DAO


class Model:
    def __init__(self):
        pass

    def getTeamsOfYear(self):
        return DAO.getTeamsOfYear()

    def getAllYears(self):
        return DAO.getAllYears()