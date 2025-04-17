import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import os
import time

os.makedirs("capturas", exist_ok=True)
imagenes = []

@pytest.fixture
def driver():  
    servicio = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=servicio)
    driver.maximize_window()
    yield driver
    driver.quit()

def esperar(segundos):
    time.sleep(segundos)

def guardar_captura(driver, nombre):
    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta = f"capturas/{nombre}_{fecha}.png"
    driver.save_screenshot(ruta)
    print(f"Captura tomada: {ruta}")
    imagenes.append((nombre, ruta))

def crear_reporte(resultado_final):
    color = "#d4edda" if resultado_final == "SUCCESS" else "#f8d7da"
    texto_color = "#155724" if resultado_final == "SUCCESS" else "#721c24"

    html = f"""
    <html>
    <head>
        <title>Reporte Selenium - Parqueo</title>
        <style>
            .resultado {{
                background-color: {color};
                color: {texto_color};
                padding: 15px;
                border-radius: 10px;
                font-weight: bold;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <h1>Prueba Selenium - Sistema de Parqueo</h1>
        <p>Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <div class='resultado'>Resultado Final: {resultado_final}</div>
    """
    for titulo, ruta in imagenes:
        html += f"<h2>{titulo}</h2><img src='{ruta}' width='700'><br><br>"

    html += "</body></html>"
    with open("reporte.html", "w", encoding="utf-8") as archivo:
        archivo.write(html)
    print("Reporte generado: reporte.html")

def test_sistema_parqueo(driver):  
    resultado_final = "SUCCESS"
    try:
        driver.get("file:///C:/Users/kevin/OneDrive/Desktop/ApiFrontendFinal/login.html")
       
        driver.find_element(By.XPATH, "//a[@href='ticket.html']").click()
       
        driver.find_element(By.ID, "btnMostrarDatos").click() 
        esperar(2)
        driver.execute_script("window.scrollBy(0, 300);")
        guardar_captura(driver, "01_Mostrar_Disponibilidad")

        campo_tipo = driver.find_element(By.ID, "tipo")
        campo_tipo.clear()  
        campo_tipo.send_keys("Carro")  

        driver.find_element(By.ID, "btnCrearTicket").click()  
        esperar(2)
        guardar_captura(driver, "02_Crear_Ticket")

        ticket_id = driver.find_element(By.ID, "ticketId").text
        print(f"ID capturado: {ticket_id}")

        campo_id = driver.find_element(By.ID, "ticketIdInput")
        campo_id.clear()
        campo_id.send_keys(ticket_id)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        esperar(2)

        driver.find_element(By.ID, "btnCalcularCosto").click()
        esperar(2)
        guardar_captura(driver, "03_Calcular_Costo")
        driver.execute_script("window.scrollBy(0, 1000);")

  

        WebDriverWait(driver, 5).until
        EC.presence_of_element_located((By.ID, "usuario"))
        esperar(2)

        driver.find_element(By.XPATH, "//a[@href='login.html']").click()
        esperar(2)      

        driver.find_element(By.ID, "usuario").send_keys("usuario_invalido")
        driver.find_element(By.ID, "clave").send_keys("1234")
        driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

        WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "ajs-error"))
)
        guardar_captura(driver, "04_Login_Incorrecto")
    
        esperar(2)
        driver.find_element(By.ID, "usuario").clear()
        driver.find_element(By.ID, "clave").clear()
        driver.find_element(By.ID, "usuario").send_keys("kevin")
        driver.find_element(By.ID, "clave").send_keys("1234")
        driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
        WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, '//button[text()="Guardar"]'))
)       
        esperar(2)
        guardar_captura(driver, "05_Login_Exitoso")

        driver.find_element(By.ID, "tipo").send_keys("Nave")
        driver.find_element(By.ID, "total").send_keys("100")
        driver.find_element(By.ID, "tarifa").send_keys("50")
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = Alert(driver)
        alert.accept() 

        esperar(1)
        driver.execute_script("window.scrollBy(0, 300);")

        esperar(2)
        guardar_captura(driver, "06_Agregar_Vehiculo")

        botones_editar = driver.find_elements(By.ID, "btn-editar")
        botones_editar[-1].click()
               
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        esperar(2)


        campo_tipo = driver.find_element(By.ID, "updateTipo")
        campo_tipo.clear()
        campo_tipo.send_keys("Nave Espacial")

        campo_total = driver.find_element(By.ID, "updateTotal")
        campo_total.clear()
        campo_total.send_keys("150")

        campo_tarifa = driver.find_element(By.ID, "updateTarifa")
        campo_tarifa.clear()
        campo_tarifa.send_keys("5")


        driver.find_element(By.ID, "boton-guardar").click()

       

        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = Alert(driver)
        alert.accept()  

        driver.execute_script("window.scrollBy(0, -1250);")

        esperar(2)
        guardar_captura(driver, "07_Editar_Vehiculo")

        
        botones_eliminar = driver.find_elements(By.CSS_SELECTOR, ".btn-danger")
        botones_eliminar[-1].click()
       

        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = Alert(driver)
        alert.accept()

        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = Alert(driver)
        alert.accept()

        esperar(2)
        guardar_captura(driver, "08_Eliminar_Vehiculo")

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        esperar(2)
        guardar_captura(driver, "09_EEliminar_Ticket_prueba")

        botones_eliminarTickets = driver.find_elements(By.CSS_SELECTOR, ".btn-primary")

        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botones_eliminarTickets[-1])
        esperar(1)

        botones_eliminarTickets[-1].click()

        esperar(2)
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        Alert(driver).accept()

        esperar(2)        
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        Alert(driver).accept()

        esperar(2)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        esperar(2)
        guardar_captura(driver, "09_Eliminar_Ticket")

        driver.find_element(By.CLASS_NAME, "btn-light").click()

        esperar(2)
        driver.find_element(By.ID, "registrarse").click()    
      
        esperar(2)   
        driver.find_element(By.ID, "nombre_usuario").send_keys("Steve")
        driver.find_element(By.ID, "contra_usuario").send_keys("12345")
        driver.find_element(By.ID, "rol_usuario").send_keys("Administrador") 

        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        Alert(driver).accept()
       
        esperar(2)
        guardar_captura(driver, "10_Crear_Usuario")


        botones_editar = driver.find_elements(By.ID, "btn-cambios")
        botones_editar[-1].click()

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        esperar(2)

        campo_nombre = driver.find_element(By.ID, "updateNombre")
        campo_nombre.clear()
        campo_nombre.send_keys("Kevin Ortega")

        campo_clave = driver.find_element(By.ID, "updateContra")
        campo_clave.clear() 
        campo_clave.send_keys("Contraseña")
    
        driver.find_element(By.ID, "guardar-cambios").click()       

        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = Alert(driver)
        alert.accept()  

        esperar(2)
        guardar_captura(driver, "11_Editar_Usuario")     

        botones_eliminar_usuario = driver.find_elements(By.CSS_SELECTOR, ".btn-danger")
        botones_eliminar_usuario[-1].click()
       
        esperar(2)
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = Alert(driver)
        alert.accept()

        esperar(2)
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = Alert(driver)
        alert.accept()

        esperar(2)
        guardar_captura(driver, "12_Eliminar_Usuario")
 


    except Exception as e:
        print("Error:", e)
        guardar_captura(driver, "ERROR")
        resultado_final = "FAIL"
        raise AssertionError("Prueba fallida: " + str(e))
    finally:
        crear_reporte(resultado_final)



if __name__ == "__main__":
    pytest.main([__file__, "--html=resultado_pytest.html"])