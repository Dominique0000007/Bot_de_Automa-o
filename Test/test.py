# Importar módulos
import os
import shutil
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configurar logging
logging.basicConfig(filename='test_log.log', level=logging.INFO)

# Caminho padrão de downloads
download_path = os.path.expanduser("~/Downloads")
filename = "atividade.txt"

# Inicializar navegador
nav = webdriver.Chrome()  # adicione executable_path se necessário
wait = WebDriverWait(nav, 10)  # espera de até 10 segundos

# Abrir site
nav.get("https://happy-wave-0b04a110f.6.azurestaticapps.net/")

# Preencher login
email_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))
password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
email_field.send_keys("Fiona123@gmail.com")
password_field.send_keys("Fiona5510@")

# Submeter login
login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
login_button.click()

# Navegar para Global e Local
nav.get("https://happy-wave-0b04a110f.6.azurestaticapps.net/global")
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Global')]"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Local')]"))).click()

logging.info("Login e navegação para Global/Local concluídos.")
print("Login e navegação para Global/Local concluídos.")

# Biblioteca / Atividades
nav.get("https://happy-wave-0b04a110f.6.azurestaticapps.net/library")
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Atividades')]"))).click()

# Verificar atividades
activities = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'activity')]")))
if activities:
    logging.info("Atividades encontradas.")
    print("Atividades encontradas.")
else:
    logging.warning("Nenhuma atividade encontrada.")
    print("Nenhuma atividade encontrada.")

# Interagir com atividades
for activity in activities:
    wait.until(EC.element_to_be_clickable(activity)).click()

# Gerar arquivos
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Gerar Atividade')]"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Gerar TXT')]"))).click()

# Esperar arquivo .txt e renomear
downloaded_files = [f for f in os.listdir(download_path) if f.endswith('.txt')]
if downloaded_files:
    latest_file = max([os.path.join(download_path, f) for f in downloaded_files], key=os.path.getctime)
    new_file_path = os.path.join(download_path, filename)
    shutil.move(latest_file, new_file_path)
    logging.info(f"Arquivo baixado e renomeado para {filename}.")
else:
    logging.warning("Arquivo .txt não encontrado para renomear.")
    print("Arquivo .txt não encontrado para renomear.")

# Carregar arquivo
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Carregar')]"))).click()
file_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
file_input.send_keys(os.path.join(download_path, filename))

# Entregar atividade
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Entregar')]"))).click()

# Verificar carregamento
try:
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'activity-detail')]")))
    logging.info("Atividade carregada com sucesso.")
    print("Atividade carregada com sucesso.")
except:
    logging.warning("Falha ao carregar a atividade.")
    print("Falha ao carregar a atividade.")

# Fechar navegador
nav.quit()

#finalizar o script
logging.info("Teste concluído.")
print("Teste concluído.")