import vismet.scripts.xavier as xavier
import vismet.scripts.inmet as inmet
import vismet.scripts.ana as ana
import vismet.scripts.categories as categories
import vismet.scripts.pixel as pixel
import vismet.scripts.city as city

def run():
    categories.LoadCategories()
    xavier.LoadXavierStations()
    inmet.LoadINMETStations()
    ana.LoadANAStations()
    ana.LoadANAStations2()
    pixel.LoadPixels()
    city.LoadCities()

    print("\n\nTodas os elementos foram carregados.")
