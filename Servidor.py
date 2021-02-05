import requests
import pandas as pd
#from datetime import datetime
import time
import git
import datetime

def Disponibilidad(url):
    r = requests.get(url)
    if(r.status_code == 200):
        return True
    return False

def DisponibilidadNombre(url):
    if(Disponibilidad(url)):
        return "Disponible"
    return "No Disponible"

def ultimoElemento(nombre):
    dataAux = pd.read_csv("https://github.com/Sud-Austral/Monitoreo/raw/main/Disponibilidad.csv")
    return dataAux[dataAux["URL"] == nombre].sort_values("Fecha",ascending=False).iloc[0]
    
def UltimoDisponible(nombre,estado):
    ultimoRegistro = ultimoElemento(nombre)
    if(estado != ultimoRegistro["Disponibilidad"]):
        return datetime.now()
    return None

def DiccionarioLink(link):
    return {"Nombre":link[0],"URL":link[1],"Disponibilidad":DisponibilidadNombre(link[1]),"Ultimo":UltimoDisponible(link[1],DisponibilidadNombre(link[1]))}


def URLCriticas():
    urlCriticas = [
    ["Odoo","https://www.dataintelligence-group.com/"],
    [ "Blackbox","https://serviciodashboard.azurewebsites.net/"],
    ["PowerBI","https://powerbi.microsoft.com/es-es/"],
    ["Dropbox","https://www.dropbox.com/"],
    ["Odoo","https://dataintelligence.store/"],
    ["GEE","https://app-data-i.users.earthengine.app/"],
    ["UtilidadesOdoo", "https://odooutil.azurewebsites.net/"],
    ["Filtros Dashboard", "https://filtradordashboard.azurewebsites.net/"],
    ["MapStore", "https://ide.dataintelligence-group.com/mapstore/#/"],
    ["GeoServer", "https://ide.dataintelligence-group.com/geoserver/web/?0"],
    ["Tomcat","https://ide.dataintelligence-group.com/"],
    ["Shiny","https://rpubs.com/dataintelligence/"],
    ["Github","https://github.com/Sud-Austral/"],
    ["EZ Exporter","https://ezexporter.highviewapps.com/exports/export-profile/"]
    ]
    return urlCriticas

def Update():
    salida = []

    for i in URLCriticas():
        salida.append(DiccionarioLink(i).copy())

    data = pd.DataFrame(salida)
    data["Fecha"] = datetime.datetime.now()
    dataGeneral = pd.read_excel("Disponibilidad.xlsx")
    dataGeneral = pd.concat([dataGeneral,data])
    dataGeneral.to_excel("Disponibilidad.xlsx", index=False)
    dataGeneral.to_csv("Disponibilidad.csv",index=False)
    dataActualizado = dataGeneral.tail(len(URLCriticas()) * 3)[::-1]
    dataActualizado.to_excel("DisponibilidadActualizado.xlsx", index=False)
    dataActualizado.to_csv("DisponibilidadActualizado.csv",index=False)
    return

def guardarRepositorio():
    repoLocal = git.Repo(r'C:\Users\datos\Documents\GitHub\Monitoreo')
    try:
        for remote in repoLocal.remotes:
            remote.fetch()

        for remote in repoLocal.remotes:
            remote.pull()
        repoLocal.git.add(".")
        repoLocal.git.commit(m='Update automatico via Actualizar ' + datetime.datetime.now().strftime("%m-%d-%Y %H-%M-%S"))
        origin = repoLocal.remote(name='origin')
        origin.push()
    except:
        print("Error de GITHUB")

    return

def Ciclo():
    print("Comienza el Ciclo...")
    Update()
    guardarRepositorio()
    time.sleep(60 * 30)
    Ciclo()
