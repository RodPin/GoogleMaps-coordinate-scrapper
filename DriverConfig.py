import platform
from selenium.webdriver.chrome.options import Options


class DriverConfig:

    @staticmethod
    def get_system_driver():
        """
        Checa o tipo de sistema e retorna o path do arquivo correspondente ou uma string vazia caso o sistema não seja reconhecido.

        :return: String
        """
        driver_path = ""
        if platform.system() == "Windows":
            driver_path = r"chromedriver_windows.exe"
        elif platform.system() == "Linux":
            driver_path = r"chromedriver"
        elif platform.system() == "Darwin":
            driver_path = r"chromedriver_mac"

        return driver_path

    @staticmethod
    def get_options():
        """
        Retorna configurações padrões das opções do driver

        :return: Options
        """
        options = Options()
        # options.add_argument("--headless")
        options.add_argument("window-size=1920,1080")
        return options
