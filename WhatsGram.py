from selenium import webdriver
import os
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pyperclip
import telebot



class zapbot:
    # O local de execução do nosso script
    dir_path = os.getcwd()
    # O caminho do chromedriver
    chromedriver = os.path.join(dir_path, "chromedriver.exe")
    # Caminho onde será criada pasta profile
    profile = 'user-data-dir=C:\\Users\\Thiago\\AppData\\Local\\Google\\Chrome\\User Data'

    def __init__(self):
        self.options = webdriver.ChromeOptions()
        # Configurando a pasta profile, para mantermos os dados da seção
        self.options.add_argument(self.profile)
        # Inicializa o webdriver
        self.driver = webdriver.Chrome(
            self.chromedriver, chrome_options=self.options)
        # Abre o whatsappweb
        self.driver.get("https://web.whatsapp.com/")
        # Aguarda alguns segundos para validação manual do QrCode
        self.driver.implicitly_wait(15)

    def ultima_msg(self, chave, mensagens, update):
        """ Captura a ultima mensagem da conversa """
        try:
            update = False

            dataHoraMessageList = self.driver.find_elements_by_xpath("//*[@data-pre-plain-text]")
            dataHoraMessageObj = dataHoraMessageList[len(dataHoraMessageList)-1]
            dataHoraMessage = dataHoraMessageObj.get_attribute('data-pre-plain-text')

            if chave in dataHoraMessageObj.text:
                pyperclip.copy(dataHoraMessageObj.text)

                if dataHoraMessage not in mensagens.keys():
                    mensagens.update({dataHoraMessage: dataHoraMessageObj.text})
                    update = True

            return update

        except Exception as e:
            print("Erro ao ler msg, tentando novamente!")

    def envia_msg(self):
        """ Envia uma mensagem para a conversa aberta """
        try:
            sleep(1)
            self.caixa_de_mensagem = self.driver.switch_to.active_element
            self.caixa_de_mensagem.send_keys(Keys.CONTROL + 'v')
            self.caixa_de_mensagem.send_keys(Keys.ENTER)
            sleep(1)
        except Exception as e:
            print("Erro ao enviar msg", e)

    def envia_media(self, fileToSend):
        """ Envia media """
        try:
            # Clica no botão adicionar
            self.driver.find_element_by_css_selector("span[data-icon='clip']").click()
            # Seleciona input
            attach = self.driver.find_element_by_css_selector("input[type='file']")
            # Adiciona arquivo
            attach.send_keys(fileToSend)
            sleep(3)
            # Seleciona botão enviar
            send = self.driver.find_element_by_xpath("//div[contains(@class, 'yavlE')]")
            # Clica no botão enviar
            send.click()
        except Exception as e:
            print("Erro ao enviar media", e)

    def abre_conversa(self, contato):
        """ Abre a conversa com um contato especifico """
        try:
            # Seleciona a caixa de pesquisa de conversa
            # self.caixa_de_pesquisa = self.driver.find_element_by_t("_357i8")
            self.caixa_de_pesquisa = self.driver.find_element(By.XPATH,'//span[text()="'+contato+'"]')
            self.caixa_de_pesquisa.click()

            # # Digita o nome ou numero do contato
            # self.caixa_de_pesquisa.send_keys(contato)
            # sleep(2)
            # # Seleciona o contato
            # self.contato = self.driver.find_element_by_xpath("//span[@title = '{}']".format(contato))
            # # Entra na conversa
            # self.contato.click()
        except Exception as e:
            raise e


configuracao_Texto = open('config.config', 'r')
line = configuracao_Texto.readline()
dic = {line.split(';')[0] : [line.split(';')[1], line.split(';')[2]]}

botTelegram = telebot.TeleBot("1149802329:AAFlQb4pdqtlS9K6YfwdDRqdK5OR1GMQkV8")
botTelegram._start()

bot = zapbot()
bot.abre_conversa("Teste grupo bot")

mensagens = {}
update = False
msg = ""
while msg != "/quit":
    sleep(1)
    
    for i in dic.keys():
        try:
            update = bot.ultima_msg(i, mensagens, update)
            
            if update:
                tipoBot = dic[i][0]
                idGroup = dic[i][1]

                if(len(tipoBot.split(',')) > 1):
                    msg = pyperclip.paste()
                    botTelegram.send_message(idGroup.split(',')[1], msg)

                    bot.abre_conversa(idGroup.split(',')[0])
                    bot.envia_msg()
                else:
                    if tipoBot == '1':
                        bot.abre_conversa(idGroup)
                        bot.envia_msg()
                    else:
                        msg = pyperclip.paste()
                        botTelegram.send_message(idGroup, msg)

        except Exception as e:
            pass



    bot.abre_conversa("Teste grupo bot")


