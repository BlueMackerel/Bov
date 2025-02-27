import sys

RED = "\033[91m"    # 빨간색 (오류)
GREEN = "\033[92m"  # 초록색 (성공)
RESET = "\033[0m"   # 색상 초기화




if __name__=="__main__":
    try:
        import os
        import requests
        import json
        from sys import argv
        
        # 기본 설정 데이터
        defaultdata = {"Loader": "Crawler"}
        
        # Launch.json 파일 체크 및 생성
        launch_file = "Launch.json"
        if not os.path.exists(launch_file):
            with open(launch_file, "w", encoding="utf-8") as f:
                json.dump(defaultdata, f, ensure_ascii=False, indent=2)

        # JSON 파일 로드
        with open(launch_file, "r", encoding="utf-8") as f:
            text = json.load(f)

        # ANSI 색상 코드
        RED = "\033[91m"    # 빨간색 (오류)
        GREEN = "\033[92m"  # 초록색 (성공)
        RESET = "\033[0m"   # 색상 초기화

        # 옵션 확인
        if len(argv) < 2:
            print(f"{RED} ERROR: No option provided. Use 'install <filename>'. {RESET}")
            exit(1)


        loader=text.get("Loader")
        option = argv[1]

        if option == "install":
            if loader=="Crawler":

                if len(argv) < 3:
                    print(f"{RED} ERROR: No file name provided. {RESET}")
                    exit(1)

                file_name = argv[2]
                repo_url = "https://raw.githubusercontent.com/BlueMackerel/Bov/master/Lib"
                download_url = f"{repo_url}/{file_name}"

                # 파일 존재 여부 확인
                response = requests.head(download_url)
                if response.status_code == 404:
                    #Page Not Found
                    print(f"{RED}ERROR: NOT NAMED PACKAGE: {file_name}{RESET}")
                    exit(1)

                # 다운로드 진행
                try:
                    response = requests.get(download_url, stream=True)
                    response.raise_for_status()

                    # 다운로드 경로 설정
                    install_path = r"C:\Program Files\Bov\Lib"
                    os.makedirs(install_path, exist_ok=True)
                    file_path = os.path.join(install_path, file_name)

                    # 파일 저장
                    with open(file_path, "wb") as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)

                    print(f"\033[32m SUCCESS: {file_name} successfully installed. {RESET}")

                except requests.RequestException as e:
                    print(f"{RED}ERROR: {file_name} download failed - {e}{RESET}")

                except PermissionError:
                    print(f"{RED}You need to run this program as an administrator.{RESET}")

            elif loader=="Downloader":
                import os
                import time
                import shutil
                import requests
                from selenium import webdriver
                from selenium.webdriver.chrome.service import Service
                from selenium.webdriver.common.by import By
                from selenium.webdriver.support.ui import WebDriverWait
                from selenium.webdriver.support import expected_conditions as EC
                from webdriver_manager.chrome import ChromeDriverManager
                from sys import argv
                file_name = argv[2]
                repo_url = "https://github.com/BlueMackerel/Bov/tree/master/Lib"
                download_page_url = f"{repo_url}/{file_name}"

                # 다운로드 버튼의 XPath
                xpath = """//button[@aria-label='Download raw content']"""

                # 다운로드 폴더 (Chrome의 기본 다운로드 경로)
                download_dir = os.path.expanduser("~\\Downloads")
                destination_dir = r"C:\Program Files\Bov\Lib"

                # Selenium WebDriver 설정
                service = Service(ChromeDriverManager().install())
                options = webdriver.ChromeOptions()
                options.add_experimental_option("prefs", {"download.default_directory": download_dir})
                downloader = webdriver.Chrome(service=service, options=options)

                # GitHub 파`일 페이지 열기
                downloader.get(download_page_url)

                try:
                    # 페이지 로드 대기
                    WebDriverWait(downloader, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

                    # 404 페이지 감지
                    if "File not found" in downloader.title or "File not found" in downloader.page_source:
                        print(f"{RED}ERROR: NOT NAMED PACKAGE: {file_name}{RESET}")
                    else:
                        # 다운로드 버튼 클릭
                        download_button = downloader.find_element(By.XPATH, xpath)
                        download_button.click()
                        print(f"{GREEN}Downloading {file_name}...{RESET}")

                        # 다운로드 완료 대기 (파일이 다운로드될 때까지 반복 체크)
                        downloaded_file = os.path.join(download_dir, file_name)
                        timeout = 30  # 최대 30초 대기
                        while timeout > 0:
                            if os.path.exists(downloaded_file):
                                break
                            time.sleep(1)
                            timeout -= 1

                        if os.path.exists(downloaded_file):
                            # 다운로드된 파일을 이동
                            os.makedirs(destination_dir, exist_ok=True)
                            shutil.move(downloaded_file, os.path.join(destination_dir, file_name))
                            print(f"{GREEN}SUCCESS: {file_name} successfully installed in {destination_dir}.{RESET}")
                        else:
                            print(f"{RED}ERROR: Download timed out. {file_name} not found.{RESET}")

                except Exception as e:
                    print(f"{RED}FATAL ERROR: {e}{RESET}")

                finally:
                    downloader.quit()  # 브라우저 종료
        import os
    finally:
        import os
        os.system("pause")