import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceTeam = None


    def handleCreaGrafo(self, e):
        self._model.creaGrafo()
        n, m = self._model.getGraphDetails()
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato! "
                    f"Il grafo è costituito di {n} nodi ed {m} archi"))

        self._view.update_page()


    def handleDettagli(self, e):
        pass

    def handlePercorso(self, e):
        pass

    def fillDDyears(self):
        years= self._model.getAllYears()

        # yearsDD =[]
        # for year in years:
        #     yearsDD.append(ft.dropdown.Option(year))

        yearsDD = list(map(lambda x: ft.dropdown.Option(x), years))
        self._view.ddAnno.options= yearsDD
        self._view.update_page()

    def handleYearSelecton(self):
        #questo metodo viene usato quando qualcuno ha selezionato un anno, deve recuperare tutti i
        # team che hanno giocato quell'anno, stamparli nel textfield, e riempire il dd sotto

        if self._view.ddAnno.value is None:
            self._view._txtOutSquadre.controls.clear()
            self._view._txtOutSquadre.controls.append("selezionare un anno dal menu")

        teams = self._model.getTeamsOfYear(self._view.ddAnno.value)
        self._view._txtOutSquadre.controls.clear()
        self._view._txtOutSquadre.controls.append(ft.Text(f"Per il {self._view.ddAnno.value} sono iscritte al campionato"
                                                          f" {len(teams)} squadre "))
        for t in teams:
            self._view._txtOutSquadre.controls.append(ft.Text(t))
            self._view._ddSquadra.options.append(
                ft.dropdown.Option(
                    data = t,
                    text = t.name,
                    on_click= self.readDDTeams
                )
            )
        self._view.update_page

    def readDDTeams(self, e):
        if e.control.data is None:
            self._choiceTeam = None
        else:
            self._choiceTeam = e.control.data
        print(f"Selezionato il team {self._choiceTeam}")