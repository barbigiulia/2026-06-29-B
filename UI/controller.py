import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    # =====================================================================================================

    def handleCreaGrafo(self, e):
        self._model.buildGraph()
        self._view._txt_result.clean()
        self._view._txt_result.controls.append(ft.Text("Grafo creato correttamente", color="green"))
        self._view._txt_result.controls.append(ft.Text(f"Numero di nodi: {self._model.getNumNodi()}", color="green"))
        self._view._txt_result.controls.append(ft.Text(f"Numero di archi: {self._model.getNumArchi()}", color="green"))
        self._view._btnStampaInfo.disabled= False

        self._view._ddAlbum.options = self.fillAlbum()
        self._view.update_page()
# ================================================================
    def fillAlbum(self):
        res = []
        for a in self._model.fillAlbum():
            res.append(ft.dropdown.Option(text=a.Title, key=str(a.AlbumId)))
        return res

# ================================================================
    def handleStampaInfo(self,e):
        num, piuGrande = self._model.compConnesse()
        if int(num) == 0:
            self._view._txt_result.controls.append(
                ft.Text(f"Il grafo non ha componenti connesse", color="red"))
            self._view.update_page()
            return

        self._view._txt_result.controls.append(ft.Text(f"Numero di componenti connesse: {num}", color="blue"))
        self._view._txt_result.controls.append(ft.Text(f"Dimensione della componente connessa più grande: {piuGrande[1]} album", color="purple"))
        lista=[]
        for a in piuGrande[0]:
            lista.append(a)
        lista.sort(key=lambda a: a.Title)
        for a in lista:
            self._view._txt_result.controls.append(ft.Text(f"--> {str(a)} : numero di brani {len(a.listaBrani)}", color="pink"))
        self._view.update_page()
# =====================================================================================================
    def handleSelezione(self,e):
        self._view._txt_result.clean()

        albumId = self._view._ddAlbum.value
        if albumId is None:
            self._view._txt_result.controls.append(ft.Text("Selezionare un album di partenza", color="red"))
            self._view.update_page()
            return

        nStr = self._view._txtInN.value
        if nStr is None or nStr.strip() == "":
            self._view._txt_result.controls.append(ft.Text("Inserire il numero di album N", color="red"))
            self._view.update_page()
            return

        try:
            n = int(nStr)
        except ValueError:
            self._view._txt_result.controls.append(ft.Text("N deve essere un numero intero", color="red"))
            self._view.update_page()
            return

        if n <= 0:
            self._view._txt_result.controls.append(ft.Text("N deve essere maggiore di 0", color="red"))
            self._view.update_page()
            return

        nodoStart = self._model.getAlbumById(albumId)
        if nodoStart is None:
            self._view._txt_result.controls.append(ft.Text("Album non trovato", color="red"))
            self._view.update_page()
            return

        try:
            selezione, totBrani = self._model.trovaSelezione(nodoStart, n)
        except Exception as ex:
            self._view._txt_result.controls.append(
                ft.Text(f"Errore durante il calcolo della selezione: {ex}", color="red"))
            self._view.update_page()
            return

        if selezione is None:
            self._view._txt_result.controls.append(
                ft.Text(f"Non esiste una selezione valida di {n} album (componenti connesse insufficienti)",
                        color="red"))
            self._view.update_page()
            return

        selezione.sort(key=lambda a: a.Title)

        for a in selezione:
            generi = set()
            for t in a.listaBrani:
                generi.add(t.GenreId)
            self._view._txt_result.controls.append(
                ft.Text(f"--> {a.Title}  | ID generi: {sorted(generi)}  | Numero di brani: {len(a.listaBrani)}",
                        color="pink"))

        self._view._txt_result.controls.append(
            ft.Text(f"Numero totale di album selezionati: {len(selezione)}", color="blue"))
        self._view._txt_result.controls.append(ft.Text(f"Numero complessivo di brani: {totBrani}", color="blue"))
        self._view.update_page()