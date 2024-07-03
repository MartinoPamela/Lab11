import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []

    def fillDD(self):

        dailySalesList = self._model.getYears()
        productsList = self._model.getColors()

        for n in dailySalesList:
            if n.Date.year not in self._listYear:
                self._listYear.append(n._Date.year)

        self._listYear.sort()

        for a in self._listYear:
            self._view._ddyear.options.append(ft.dropdown.Option(a))

        for n in productsList:
            if n._Product_color not in self._listColor:
                self._listColor.append(n._Product_color)

        for a in self._listColor:
            self._view._ddcolor.options.append(ft.dropdown.Option(a))

        self._view._page.update()

    def handle_graph(self, e):
        color = self._view._ddcolor.value
        anno = self._view._ddyear.value
        self._model.buildGraph(color, anno)
        self.fillDDProduct()

        self._view.txtOut.controls.clear()
        self._view.txtOut.controls.append(ft.Text(f"Numero di vertici: {self._model.getNumNodi()} "
                                                  f"Numero di archi: {self._model.getNumArchi()}"))

        freq = {}
        for edge in self._model.get_sorted_edges()[:3]:
            self._view.txtOut.controls.append(ft.Text(f"Arco da {edge[0]._Product_number} a "
                                                      f"{edge[1]._Product_number}, peso={edge[2]['weight']}"))

            if edge[0]._Product_number not in freq:
                freq[edge[0]._Product_number] = 1
            else:
                freq[edge[0]._Product_number] += 1

            if edge[1]._Product_number not in freq:
                freq[edge[1]._Product_number] = 1
            else:
                freq[edge[1]._Product_number] += 1

        # n_repeated = [k for (k,v) in freq.items() if v > 1]
        n_repeated = []
        for (k, v) in freq.items():
            if v > 1:
                n_repeated.append(k)
        self._view.txtOut.controls.append(ft.Text(f"I nodi ripetuti sono: {n_repeated}"))

        self._view._page.update()

    def fillDDProduct(self):
        for n in self._model.get_nodes():
            self._view._ddnode.options.append(ft.dropdown.Option(n._Product_number))

        self._view._page.update()


    def handle_search(self, e):
        self._model.bestPath(self._model.getObjFromId(int(self._view._ddnode.value)))
        self._view.txtOut2.controls.clear()
        self._view.txtOut2.controls.append(ft.Text(f"Numero archi percorso più lungo: {len(self._model._solBest)}"))
        self._view._page.update()
