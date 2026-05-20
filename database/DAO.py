from database.DB_connect import DBConnect
from model.team import Team


class DAO():
    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT distinct(t.year)
                   from teams t
                   where t.year >= 1980"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["year"]) #sono numeri, posso salvarli cosi

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getTeamsOfYear(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * 
                    from teams t  
                     where t.year = %s"""

        cursor.execute(query, (year,))

        for row in cursor:
            result.append(Team(**row))

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getSalariesTeam(year, idMapTeams):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t.ID , t.teamCode , sum(s.salary) as totSalary
                    from salaries s , teams t , appearances a 
                    where s.`year`  = t.`year` and t.`year` = a.`year`  and a.`year` = %s
                    and t.ID = a.teamID and a.playerID =s.playerID 
                    group by t.ID, t.teamCode 
                    
                    """
        #creo e riempio un idmap
        cursor.execute(query, (year,))
        mapSalary= {}
        for row in cursor:
            mapSalary[ idMapTeams[row["ID"]]] = row["totSalary"]

        # #mi arriva un id e un salario, posso usare un id map per recuperare l'oggetto team partendo dal suo id
        # for row in cursor:
        #     result.append((idMapTeams(row["ID"], row["Totsalary"])))

        cursor.close()
        conn.close()
        return result