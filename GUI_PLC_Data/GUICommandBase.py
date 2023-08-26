import sqlite3 as sql
from datetime import datetime as dt


class GUICommandBase():

    def __init__(self):
        self.conn = sql.connect("../PLC_DataBase.sqlite")
        self.c = self.conn.cursor()

    def newFormatDate(self, date_input, actualFormat, newFormat):
        date = dt.strptime(date_input, actualFormat)
        new_format = date.strftime(newFormat)
        return new_format

    def deleteAllaData(self):
        self.c.execute(f"DELETE FROM Aktualne_poziomy")
        self.c.execute(f"UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = 'Aktualne_poziomy'")
        self.c.execute(f"DELETE FROM Aktualne_przepływy")
        self.c.execute(f"UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = 'Aktualne_przepływy'")
        self.c.execute(f"DELETE FROM Aktualne_sterowania")
        self.c.execute(f"UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = 'Aktualne_sterowania'")
        self.c.execute(f"DELETE FROM Wystąpienie_alarmu")
        self.c.execute(f"UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = 'Wystąpienie_alarmu'")
        self.c.execute(f"DELETE FROM Zadane_poziomy")
        self.c.execute(f"UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = 'Zadane_poziomy'")
        self.c.execute(f"DELETE FROM Zmiany_parametrów")
        self.c.execute(f"UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = 'Zmiany_parametrów'")
        self.conn.commit()

    def readDataForCharts(self, tank, dateFrom, dateTo):
        id_tank = 0
        if tank == "Zbiornik_1":
           id_tank = 1
        elif tank == "Zbiornik_2":
            id_tank = 2
        elif tank == "Zbiornik_3":
            id_tank = 3
        try:
            self.c.execute(f"SELECT * FROM Aktualne_poziomy WHERE ID_Zbiornika = '{id_tank}' "
                           f"AND Data_i_godzina >= '{dateFrom}' AND Data_i_godzina <= '{dateTo}'")
            currentLevel = self.c.fetchall()
        except Exception as error:
            print("Select CurrentLevel: " + error)

        try:
            self.c.execute(f"SELECT * FROM Aktualne_przepływy WHERE ID_Zbiornika = '{id_tank}'"
                           f"AND Data_i_godzina >= '{dateFrom}' AND Data_i_godzina <= '{dateTo}'")
            currentDisFlow = self.c.fetchall()

            self.c.execute(f"SELECT * FROM Aktualne_sterowania WHERE ID_Zbiornika = '{id_tank}'"
                           f"AND Data_i_godzina >= '{dateFrom}' AND Data_i_godzina <= '{dateTo}'")
            currentControl = self.c.fetchall()
        except Exception as error:
            print("Dis flow or control: " + error)



        try:
            self.c.execute(f"SELECT * FROM Zadane_poziomy WHERE ID_Zbiornika = '{id_tank}' "
                           f"AND Data_i_godzina >= '{dateFrom}' AND Data_i_godzina <= '{dateTo}'")
            setPoint = self.c.fetchall()
        except Exception as error:
            print("Select SetPoint: " + error)

        try:
            self.c.execute(f"SELECT * FROM Wystąpienie_alarmu INNER JOIN Alarmy ON Wystąpienie_alarmu.ID_Alarmu = "
                           f"Alarmy.ID_Alarmu WHERE Wystąpienie_alarmu.ID_Zbiornika = '{id_tank}' "
                           f"AND Wystąpienie_alarmu.ID_Alarmu = '{1}' AND Data_i_godzina >= '{dateFrom}' AND Data_i_godzina <= '{dateTo}' ")
            currentAlarms_1 = self.c.fetchall()

            self.c.execute(f"SELECT * FROM Wystąpienie_alarmu INNER JOIN Alarmy ON Wystąpienie_alarmu.ID_Alarmu = "
                           f"Alarmy.ID_Alarmu WHERE Wystąpienie_alarmu.ID_Zbiornika = '{id_tank}' "
                           f"AND Wystąpienie_alarmu.ID_Alarmu = '{2}' AND Data_i_godzina >= '{dateFrom}' AND Data_i_godzina <= '{dateTo}' ")
            currentAlarms_2= self.c.fetchall()

            self.c.execute(f"SELECT * FROM Wystąpienie_alarmu INNER JOIN Alarmy ON Wystąpienie_alarmu.ID_Alarmu = "
                           f"Alarmy.ID_Alarmu WHERE Wystąpienie_alarmu.ID_Zbiornika = '{id_tank}' "
                           f"AND Wystąpienie_alarmu.ID_Alarmu = '{3}' AND Data_i_godzina >= '{dateFrom}' AND Data_i_godzina <= '{dateTo}' ")
            currentAlarms_3 = self.c.fetchall()

            self.c.execute(f"SELECT * FROM Wystąpienie_alarmu INNER JOIN Alarmy ON Wystąpienie_alarmu.ID_Alarmu = "
                           f"Alarmy.ID_Alarmu WHERE Wystąpienie_alarmu.ID_Zbiornika = '{id_tank}' "
                           f"AND Wystąpienie_alarmu.ID_Alarmu = '{4}' AND Data_i_godzina >= '{dateFrom}' AND Data_i_godzina <= '{dateTo}' ")
            currentAlarms_4 = self.c.fetchall()

            self.c.execute(f"SELECT * FROM Wystąpienie_alarmu INNER JOIN Alarmy ON Wystąpienie_alarmu.ID_Alarmu = "
                           f"Alarmy.ID_Alarmu WHERE Wystąpienie_alarmu.ID_Zbiornika = '{id_tank}' "
                           f"AND Wystąpienie_alarmu.ID_Alarmu = '{5}' AND Data_i_godzina >= '{dateFrom}' AND Data_i_godzina <= '{dateTo}' ")
            currentAlarms_5 = self.c.fetchall()
        except Exception as error:
            print("Select Alarms: " + error)

        try:
            self.c.execute(f"SELECT * FROM Zmiany_parametrów INNER JOIN Parametry ON Zmiany_parametrów.ID_Parametru = "
                           f"Parametry.ID_Parametru WHERE Zmiany_parametrów.ID_Zbiornika = '{id_tank}'"
                           f"AND Data_i_godzina >= '{dateFrom}' AND Data_i_godzina <= '{dateTo}'")
            params = self.c.fetchall()
        except Exception as error:
            print("Select params: " + error)

        # if len is 0 that means no data is on this period
        if len(currentLevel) == 0:
            return [0]
        else:
            return [1, currentLevel, setPoint, currentAlarms_1,currentAlarms_2,
                    currentAlarms_3, currentAlarms_4, currentAlarms_5, params, currentDisFlow, currentControl]
        # print(currentDisFlow)
        # print(currentControl)
        # print(currentAlarms)
        # print(setPoint)
        # print(params)

