from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from datetime import datetime

monthsPassed = int(input("Verificar quantos meses anteriores? "))
driver = webdriver.Chrome()

driver.get("https://siap.educacao.go.gov.br/login.aspx?ReturnUrl=%2fdefault.aspx")

chrome_options = Options()

seletorX = lambda link: driver.find_element(By.XPATH, link)

def clickSeq(*args, slp=0.1):
    for i in args:
        sleep(slp)
        seletorX(i).click()

def login():
    # Coloque os dados
    userData = {"login": "89034058115", "password": "o9979EqH"}
    # userData = {"login": input("Login SIAP: "), "password": input("Senha SIAP: ")}
    seletorX('//*[@id="txtLogin"]').send_keys(userData["login"])
    seletorX('//*[@id="txtSenha"]').send_keys(userData["password"])

    # Preencha o código de verificação
    seletorX('//*[@id="txtCaptcha"]').send_keys(seletorX('//*[@id="lblCaptcha"]').text)

    # Clique para realizar o login
    seletorX('//*[@id="btnLogon"]').click()

diaMes = datetime.now().day
mesAtual = datetime.now().month

def executeClass(td):
    td.click()
    sleep(1)
    clickSeq('//*[@id="cphFuncionalidade_cphCampos_grdPlanejado_Button1_0"]','//*[@id="cphFuncionalidade_btnAlterar"]','//*[@id="cphFuncionalidade_cphCampos_LstAulasDiaSelecionado"]', slp=2)
    try:
        seletorX('//*[@id="cphFuncionalidade_cphCampos_LstAulasDiaSelecionado"]/option[2]').click()
        clickSeq('//*[@id="cphFuncionalidade_cphCampos_grdPlanejado_Button1_0"]','//*[@id="cphFuncionalidade_btnAlterar"]', slp=2)
    except:
        pass

def executeFreq(td):
    td.click()
    sleep(1)
    seletorX('//*[@id="cphFuncionalidade_btnAlterar"]').click()

def acessExec(idx):
    for mes in range(mesAtual-monthsPassed, mesAtual+1):
        clickSeq('//*[@id="selectMesCalendarioMensal"]', f'//*[@id="selectMesCalendarioMensal"]/option[{mes}]')
        for line in range(1, 6):
            for col in range([3,5][idx==1], 6):
                try:  
                    actDay = int(seletorX(f'//*[@id="cphFuncionalidade_cphCampos_CalendarioMensal"]/div/table/tbody/tr[{line}]/td[{col}]/div').text)
                except:
                    continue
                # Verifica se o dia não é maior
                if (mes==mesAtual and actDay < diaMes) or mes<mesAtual:
                    # print(f"\033[1;35mPASSOU AQUI PELO MENOS - dia {actDay}\033[m")
                    actTd = seletorX(f'//*[@id="cphFuncionalidade_cphCampos_CalendarioMensal"]/div/table/tbody/tr[{line}]/td[{col}]')
                    # Verifica se o dia atual de fato tem aula (se não é feriado ou outra coisa)
                    if ('dialog' in actTd.get_attribute('class').split() and 'letivo' in actTd.get_attribute('class').split()):
                        # Verifica se está planejado
                        if actTd.get_attribute('data-planejado')=="True":
                            # Verifica se já foi executado
                            if actTd.get_attribute('data-executado')=="False":
                                print(f'Aula do dia {actDay}/{mesAtual} \033[34melegível para ser executada\033[m.')
                                executeClass(actTd)
                            else:
                                print(f'Aula do dia {actDay}/{mesAtual} \033[32mjá executada\033[m.')
                        else: 
                            print(f'Aula do dia {actDay}/{mesAtual} \033[31mnão planejada\033[m.')

def accessFreq(idx):
    seletorX('//*[@id="cphFuncionalidade_cphCampos_BtnFrequencia"]').click()
    sleep(1)

    for mes in range(mesAtual-monthsPassed, mesAtual+1):
        clickSeq('//*[@id="selectMesCalendarioMensal"]', f'//*[@id="selectMesCalendarioMensal"]/option[{mes}]')
        for line in range(1, 6):
            for col in range([3,5][idx==1], 6):
                try:  
                    actDay = int(seletorX(f'//*[@id="cphFuncionalidade_cphCampos_CalendarioMensal"]/div/table/tbody/tr[{line}]/td[{col}]/div').text)
                except:
                    continue
                # Verifica se o dia não é maior
                if (mes==mesAtual and actDay < diaMes) or mes<mesAtual:
                    actTd = seletorX(f'//*[@id="cphFuncionalidade_cphCampos_CalendarioMensal"]/div/table/tbody/tr[{line}]/td[{col}]')
                    # Verifica se o dia atual de fato tem aula (se não é feriado ou outra coisa)
                    if ('dialog' in actTd.get_attribute('class').split() and 'letivo' in actTd.get_attribute('class').split()):
                        # Verifica se já a frequência já foi executada
                        if actTd.get_attribute('data-executado')=="False":
                            print(f'Frequência do dia {actDay}/{mesAtual} \033[34melegível para ser executada\033[m.')
                            executeFreq(actTd)
                        else:
                            print(f'Frequência do dia {actDay}/{mesAtual} \033[32mjá executada\033[m.')

login()

for i in range(1, 5):
    driver.get('https://siap.educacao.go.gov.br/DiarioEscolarListagem.aspx')
    clickSeq('//*[@id="cphFuncionalidade_cphCampos_ddlComposicao"]', '//*[@id="cphFuncionalidade_cphCampos_ddlComposicao"]/option[3]',
             '//*[@id="cphFuncionalidade_cphCampos_ddlBimestre"]', '//*[@id="cphFuncionalidade_cphCampos_ddlBimestre"]/option[4]',
             '//*[@id="cphFuncionalidade_cphCampos_ddlTurno"]', '//*[@id="cphFuncionalidade_cphCampos_ddlTurno"]/option[2]',
             '//*[@id="cphFuncionalidade_btnListar"]', slp=0.2)
    print('\033[33mTurma '+seletorX(f'//*[@id="cphFuncionalidade_gdvListagem"]/tbody/tr[{i+1}]/td[8]').text+'\033[m')
    clickSeq(f'//*[@id="cphFuncionalidade_gdvListagem"]/tbody/tr[{i+1}]', '//*[@id="cphFuncionalidade_btnAuxiliar1"]', slp=2)
    
    acessExec(i)
    accessFreq(i)

input("Ação concluída. Clique para finalizar.")
