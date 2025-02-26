import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from sys import argv

RED = "\033[91m"  # 빨간색 출력
GREEN = "\033[92m"  # 초록색 출력 (성공 메시지)
RESET = "\033[0m"  # 기본 색상 복귀

option = argv[1]

if option == "install":
    print("Installing...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    repo_url = "https://github.com/BlueMackerel/Bov/tree/master/Lib"
    file_name = argv[2]
    url = f"{repo_url}/{file_name}"

    driver.get(url)

    try:
        # GitHub의 페이지가 완전히 로드될 때까지 기다림 (최대 10초)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # 404 페이지 감지
        if "File not found" in driver.title or "Page not found" in driver.page_source:
            print(f"{RED}ERROR: NOT NAMED PACKAGE: {file_name}{RESET}")
        else:
            # 다운로드 URL 추출
            download_url = f"https://raw.githubusercontent.com/BlueMackerel/Bov/master/Lib/{file_name}"
            
            # 파일 다운로드
            response = requests.get(download_url)
            import os
            os.chdir("..\\Lib")
            if response.status_code == 200:
                with open(f"{file_name}", "wb") as f:
                    f.write(response.content)
                print(f"{GREEN}SUCCESS: {file_name}: Successfully installed.{RESET}")
            else:
                print(f"{RED}ERROR: {file_name}(HTTP {response.status_code}){RESET}")

    except Exception as e:
        print(f"{RED}FATAL ERROR: {e}{RESET}")

    finally:
        driver.quit()  # 브라우저 종료
