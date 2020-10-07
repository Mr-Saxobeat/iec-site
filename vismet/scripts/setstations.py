import vismet.scripts.xavier as xavier
import vismet.scripts.inmet as inmet
import vismet.scripts.ana as ana
import vismet.scripts.categories as categories

def run():
    categories.LoadCategories()
    xavier.LoadXavierStations()
    inmet.LoadINMETStations()
    ana.LoadANAStations()

    print("\n\nTodas as estações foram carregadas.")
