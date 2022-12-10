# free_ver :                            매핑서포터 + 중복단어 제거 추가한 버전
# individual_ver :                      개별 tmg number를 입력한 버전. 카테고리 분류 (/,&,및) 추가함.
# individual_ver :                      로그인 실패 시 크롬을 꺼지도록 하였음. 다른 사람에게 프로그램을 빌려줄 때 아이디, 비번을 공개하게 하는 부담을 지게 됨. 허나 아이디,비번을 공개한다면 다른 아이디 사용가능한 허점이 존재.
# fortified_individual_ver :            불러오기 시 URL을 가져와 tmg number을 검사하여 맞는 번호가 아닐 시 프로그램 종료 기능 추가 버전. 이제 아이디를 빌려줄 수 없게 되었음. tmg 번호 부분을 Label에서 line edit로 바꿈.
# hide_sellerlife_mapping_ver :         셀러라이프 창이 안뜨도록 변화시킴. label에 셀러라이프라는 단어 제거.
# license_ver :                         라이센스 코드를 입력해야지 실행되도록 만든 버전.
# add_search_ver :                      마켓카테고리 전체검색 기능을 추가한 버전.
# Version 1.0.0 :                       라이센스 인증시 오류가 있어 오류 수정하고 Class밖에서 라이센스를 인증하고 진입하는 방식으로 변경. 중복단어 기능에 단어 앞뒤공백제거 기능 추가.라이센스창에 구매링크 추가.

from unicodedata import category
from PyQt5.QtWidgets import *
from PyQt5 import uic
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from posixpath import split
from ntpath import join
from collections import Counter
from webdriver_manager.chrome import ChromeDriverManager
import sys, os, time, requests, webbrowser, pyautogui, threading, getmac, subprocess, ast
from pprint import pprint
import datetime as dt
from cryptography.fernet import Fernet
from tkinter import filedialog

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UI_PATH = "mango_supporter.ui"

class MainDialog(QDialog) :
    def __init__(self) :
        QDialog.__init__(self, None)
        uic.loadUi(os.path.join(BASE_DIR, UI_PATH), self)

        self.client_id_edit.setText('')
        self.client_sr_edit.setText('')
        self.cate_load_and_autoinput_btn.setText("불러오기\n\nand\n\n자동입력")
        self.input_license_btn.setText("라이센스 키\n입력/수정")
        self.smartstore_btn.setText("라이센스\n구매링크")
        self.forbidden_keyword_save_btn.setText('키워드 금지어\n저장')
        self.forbidden_keyword_label.setText('키워드\n금지어')
        self.update_tab_divider_btn.setText('업데이트 창 나누기\n\nand\n\n상품업데이트\n\n마켓전송시작 ')
        self.mapping_login_btn.setText('로그인 창\n열기')
        self.update_tab_divider_two_radioButton.setChecked(True)
        self.translation_word = None
        self.first_category_radioButton.setChecked(True)
        self.tabWidget.setTabEnabled(0,True)
        self.tabWidget.setTabEnabled(1,False)
        self.tabWidget.setTabEnabled(2,False)
        self.tabWidget.setTabEnabled(3,False)
        self.tabWidget.setTabEnabled(4,True)

        self.chrome_driver_fname = 'chromedriver.exe'

        self.Alignment_info_list = []

        self.decryptography()

        self.file_path_info_read()

        self.forbidden_keyword_read()

        self.Alignment_info_file_read()

        #################매핑서포터 탭##################################
        # 매핑서포터 로그인 버튼 (매핑서포터 로그인 함수 실행)
        self.mapping_login_btn.clicked.connect(self.mapping_login)

        # 불러오기/자동입력 버튼 (카테고리 불러오기 함수 실행)
        self.cate_load_and_autoinput_btn.clicked.connect(self.category_load)
        
        # 검색/키워드입력 버튼 (셀러라이프 자동검색/입력 함수 실행)
        self.keyword_search_btn.clicked.connect(self.auto_keyword)
        self.sellerlife_search_edit.returnPressed.connect(self.auto_keyword)

        # 키워드 금지어 설정 버튼 (키워드 금지어 설정 함수 실행)
        self.forbidden_keyword_save_btn.clicked.connect(self.forbidden_keyword_save)

        # 키워드입력 버튼 (키워드 입력 함수 실행)
        self.keyword_input_btn.clicked.connect(self.keyword_input)

        # 검색 버튼 (더망고 카테고리 검색 함수)
        self.mango_cate_search_btn.clicked.connect(self.mango_cate_search)
        self.mango_cate_search_lineEdit.returnPressed.connect(self.mango_cate_search)

        # 카테고리 설정저장 버튼(카테고리 설정저장 클릭 함수)
        self.category_save_btn.clicked.connect(self.category_save)

        # 테스트 버튼 (테스트 버튼 함수)
        self.papago_test_btn.clicked.connect(self.test_btn)

        # 번역 사용 체크박스 (번역 사용 체크박스 함수)
        self.used_transrator_checkbox.stateChanged.connect(self.used_transrator)

        # 키워드 금지어 사용 체크박스 ()
        self.forbidden_keyword_Check_Box.stateChanged.connect(self.used_forbidden_keyword_Check_Box)

        # 검색 카테고리 선택 라디오 버튼 (검색 카테고리 출력 함수)
        self.first_category_radioButton.toggled.connect(self.search_category)
        self.second_category_radioButton.toggled.connect(self.search_category)

        # 검색 마켓 선택 콤보박스 버튼 (해외/국내 콤보박스 활성화/비활성화 함수)
        self.search_select_comboBox.currentTextChanged.connect(self.search_select)

        ####################라이센스키 입력 탭###########################
        # 중복키워드 제거 버튼(중복키워드 제거 함수 실행)
        self.Removed_duplicate_word_btn.clicked.connect(self.Removed_duplicate_word)

        # 라이센스 키 입력/수정 버튼(라이센스 입력 함수 실행)
        self.input_license_btn.clicked.connect(self.input_license)

        # 라이센스 구매링크 버튼(스마트스토어 구매 링크 함수 실행)
        self.smartstore_btn.clicked.connect(self.smartstore)

        # 망고서포터 사용법 버튼(망고서포터 사용법 블로그 링크 함수 실행)
        self.mango_supporter_manual_btn.clicked.connect(self.mango_supporter_manual_blog)

        # 파일 정보 저장 버튼 (파일 위치 정보 저장 함수 실행)
        self.file_path_info_save_btn.clicked.connect(self.file_path_info_save)

        ####################자동 창정렬 탭###############################
        # 자동 창 정렬 로그인 엔터(자동 창 정렬 로그인 함수 실행)
        self.Alignmenter_login_btn.clicked.connect(self.Alignmenter_login)

        # 마우스 좌표 버튼 (마우스 좌표 보기 함수 실행)
        self.mouse_position_btn.clicked.connect(self.mouse_position)

        # 크롬드라이버 파일찾기 버튼(크롬드라이버 파일찾기 함수 실행)
        self.ExpressVPN_path_btn.clicked.connect(self.search_ExpressVPN)

        # 크롬 파일찾기 버튼 (크롬 파일찾기 함수 실행)
        self.chrome_path_btn.clicked.connect(self.search_chrome)

        # 창 정렬 버튼 (창 정렬 함수 실행)
        self.Alignment_ctrl_btn.clicked.connect(self.Alignment)

        # 자동 정렬 버튼 (자동 정렬 함수 실행)
        self.auto_Alignment_ctrl_btn.clicked.connect(self.auto_Alignment)

        # 업데이트 창 나누기 실행 버튼 (업데이트 창 나누기 함수 실행)
        self.update_tab_divider_btn.clicked.connect(self.update_tab_divider_and_send)

        # 정렬 정보 콤보 박스 (정렬 정보 읽기 함수)
        self.Alignment_info_list_comboBox.activated[str].connect(self.Alignment_info_read)

        # 정렬 정보 저장 버튼 (정렬 정보 파일 저장 함수)
        self.Alignment_info_file_save_btn.clicked.connect(self.Alignment_info_file_save)

        # 정렬 정보 삭제 버튼 (정렬 정보 파일 삭제 함수)
        self.Alignment_info_file_delete_btn.clicked.connect(self.Alignment_info_file_delete)

        ####################VPN 자동 ON/OFF 탭################################
        self.VPN_auto_btn.clicked.connect(self.Period_VPN_thread)

########################매핑 서포터 함수###################################
    # 매핑서포터 로그인 함수
    def mapping_login(self) :
        self.mapping_clear_status()

        # tmg번호, 아이디, 비밀번호 불러와서 변수에 저장하는 코드.
        tmg_num = self.mapping_decry_tmg_edit.text()

        # 브라우저 꺼짐 방지
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)

        # 불필요한 에러 메시지 없애기 (꼭 필요한 코드는 아님. 없어도됨. 다만 이상한 오류코드가 발생하기에 그거 없애려고 추가하는 것)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

        service = Service(executable_path=ChromeDriverManager().install())
        self.mapping_driver = webdriver.Chrome(service=service, options=chrome_options)

        # 웹페이지가 로딩 될때까지 5초는 기다림
        self.mapping_driver.implicitly_wait(5)

        # 화면 최대화
        self.mapping_driver.maximize_window()

        # 개인 cafe24 주소로 이동
        self.mapping_driver.get(f"https://tmg{tmg_num}.cafe24.com/mall/admin/admin_login.php")
        time.sleep(1)

    # 미매핑 설정 함수
    def no_mapping(self) : 
        # 옥션 미매핑
        try :
            if self.aution_checkbox.isChecked() == 1 :
                self.mapping_driver.find_element(By.CSS_SELECTOR, "#category_B_AUC > a.defbtn_med.dtype4").click()
        except :
            pass

        # 지마켓 미매핑
        try :
            if self.gmarket_checkbox.isChecked() == 1 :
                self.mapping_driver.find_element(By.CSS_SELECTOR, "#category_B_GMK > a.defbtn_med.dtype4").click()
        except :
            pass
        
        # 11번가 미매핑
        try :
            if self.elevenst_checkbox.isChecked() == 1 :
                self.mapping_driver.find_element(By.CSS_SELECTOR, "#category_B_11ST > a.defbtn_med.dtype4").click()
        except :
            pass

        # 인터파크 미매핑
        try : 
            if self.interpark_checkbox.isChecked() == 1 :
                self.mapping_driver.find_element(By.CSS_SELECTOR, "#category_B_INTER > a.defbtn_med.dtype4").click()
        except :
            pass

        # 스마트스토어 미매핑
        try : 
            if self.smartstore_checkbox.isChecked() == 1 :
                self.mapping_driver.find_element(By.CSS_SELECTOR, "#category_B_SMART > a.defbtn_med.dtype4").click()
        except :
            pass

        # 쿠팡 미매핑
        try :
            if self.coupang_checkbox.isChecked() == 1 :
                self.mapping_driver.find_element(By.CSS_SELECTOR, "#category_B_COUP > a.defbtn_med.dtype4").click()
        except :
            pass

        # 위메프 미매핑
        try : 
            if self.wemape_checkbox.isChecked() == 1 :
                self.mapping_driver.find_element(By.CSS_SELECTOR, "#category_B_WMP > a.defbtn_med.dtype4").click()
        except :
            pass

        # 티몬 미매핑
        try :
            if self.tmon_checkbox.isChecked() == 1 :
                self.mapping_driver.find_element(By.CSS_SELECTOR, "#category_B_TMON > a.defbtn_med.dtype4").click()
        except :
            pass

        # 롯데온 미매핑
        try :
            if self.lotteon_checkbox.isChecked() == 1 :
                self.mapping_driver.find_element(By.CSS_SELECTOR, "#category_B_LTON > a.defbtn_med.dtype4").click()
        except :
            pass

        # SSG 미매핑
        try :
            if self.ssg_checkbox.isChecked() == 1 :
                self.mapping_driver.find_element(By.CSS_SELECTOR, "#category_B_SSG > a.defbtn_med.dtype4").click()
        except :
            pass

        # LFMall 미매핑
        try:
            if self.lfmall_checkbox.isChecked() == 1 :
                self.mapping_driver.find_element(By.CSS_SELECTOR, "#category_B_LFMALL > a.defbtn_med.dtype4").click()
        except :
            pass

        # 멸치쇼핑 미매핑
        try :
            if self.melchi_checkbox.isChecked() == 1 :
                self.mapping_driver.find_element(By.CSS_SELECTOR, "#category_B_MELCHI > a.defbtn_med.dtype4").click()
        except :
            pass

        # 머스트잇 미매핑
        try :
            if self.mustit_checkbox.isChecked() == 1 :
                self.mapping_driver.find_element(By.CSS_SELECTOR, "#category_B_MUSTIT > a.defbtn_med.dtype4").click()
        except :
            pass

        # 리본즈 미매핑
        try :
            if self.REEBONZ_checkbox.isChecked() == 1 :
                self.mapping_driver.find_element(By.CSS_SELECTOR, "#category_B_REEBONZ > a.defbtn_med.dtype4").click()
        except :
            pass

        # 발란 미매핑
        try :
            if self.balaan_checkbox.isChecked() == 1 :
                self.mapping_driver.find_element(By.CSS_SELECTOR, "#category_B_BALAAN > a.defbtn_med.dtype4").click()
        except :
            pass
        

    # 카테고리 불러오기 함수
    def category_load(self) :
        self.mapping_clear_status()
        self.mapping_status_label_2.setText('카테고리 불러오기 진행 중')
        QApplication.processEvents()

        try :
            # 새탭으로 드라이버 전환
            all_windows = self.mapping_driver.window_handles         # 드라이버가 제어하고 있는 모든 크롬 윈도우를 all_windows 변수에 넣어 
            self.mapping_driver.switch_to.window(all_windows[1])     # all_winddows[1]을 선택하여 2번째 탭으로 전환.
            time.sleep(1)

            # tmg num 사이트 접근 검증 함수.
            guardian = self.mapping_guardian()
            if guardian == False :
                return 0

            # 카테고리 이름 찾기
            category_full_name = self.mapping_driver.find_element(By.CSS_SELECTOR, "body > form > table:nth-child(10) > tbody > tr:nth-child(1) > td:nth-child(2)").text

            # 전체 카테고리명 출력
            self.category_full_name_label.setText(category_full_name)
            QApplication.processEvents()

            # [ > ]를 기준으로 텍스트를 나눠 리스트 형태로 저장
            category_full_name_list = category_full_name.split(' > ')
            category_last_name = category_full_name_list[-1]

            # 최하위 카테고리명 출력
            self.category_last_name_label.setText(category_last_name)
            QApplication.processEvents()

            # 검색 카테고리 출력 함수 실행
            self.search_category()

            # 번역 사용 체크박스 선택 시 번역 카테고리명 출력
            if self.used_transrator_checkbox.isChecked() == 1 :
                self.papago(self.search_category_name_label.text())

            # 셀러라이프 자동검색/입력 함수 실행
            # 프로그램 검색어창에 최하 카테고리 변수명 입력
            # 번역 사용 체크박스 미선택시
            if self.used_transrator_checkbox.isChecked() == 0 :
                self.sellerlife_search_edit.setText(self.search_category_name_label.text())
            # 번역 사용 체크박스 선택시
            elif self.used_transrator_checkbox.isChecked() == 1 :
                self.sellerlife_search_edit.setText(self.category_transration_name_label.text())
            QApplication.processEvents()
            self.auto_keyword()

            # 검색시에 사용할 카테고리 이름 변수 생성 및 입력
            # 번역 사용 체크박스 미선택시
            if self.used_transrator_checkbox.isChecked() == 0 :
                self.mango_cate_search_lineEdit.setText(self.search_category_name_label.text())
            # 번역 사용 체크박스 선택시
            elif self.used_transrator_checkbox.isChecked() == 1 :
                self.mango_cate_search_lineEdit.setText(self.category_transration_name_label.text())
            # 더망고 카테고리 검색 함수 실행
            self.mango_cate_search()

            # 미매핑 설정 함수 실행
            self.no_mapping()

            self.mapping_status_label_2.setText('카테고리 불러오기, 키워드 입력, 카테고리 검색 완료')

        except Exception as e:
            self.mapping_status_label_1.setText('카테고리탭 인식 실패 : ' + str(e))
            self.mapping_status_label_2.setText('1. 크롬브라우저가 띄워져 있는지 확인해주세요')
            self.mapping_status_label_3.setText('2. 카테고리탭이 2번째 탭에 띄워져 있는지 확인해주세요.')

    # 셀러라이프 검색 함수
    def sellerlife_search(self) :
        self.mapping_clear_status()
        self.mapping_status_label_2.setText('키워드 가져오기 진행 중')
        QApplication.processEvents()

        try : 
            if self.sellerlife_search_edit.text() == '' :
                self.keyword_amount_label.setText('카테고리를 불러오지 않었거나 검색어를 입력하지 않았습니다.')

            else :    
                # 셀러라이프로 이동
                self.mapping_driver.execute_script('window.open("https://sellerlife.co.kr/keyword");')

                # 새탭으로 드라이버 전환
                all_windows = self.mapping_driver.window_handles                 # 드라이버가 제어하고 있는 모든 크롬 윈도우를 all_windows 변수에 넣어 
                self.mapping_driver.switch_to.window(all_windows[-1])           # all_winddows[-1]을 선택하여 마지막 탭으로 전환.
                time.sleep(1)

                # 검색창 찾기
                search_window = self.mapping_driver.find_element(By.CSS_SELECTOR, "#search > .input-group > input")

                # 검색창에 sellerlife_search_edit의 검색어 입력
                search_window.send_keys(self.sellerlife_search_edit.text())

                # 검색 버튼 클릭
                # self.mapping_driver.find_element(By.CSS_SELECTOR, "#keyword-search-btn").click()
                self.mapping_driver.find_element(By.CSS_SELECTOR, "#keyword-search-btn").send_keys(Keys.ENTER)
                time.sleep(1)

                # 키워드 추천 버튼 클릭
                # self.mapping_driver.find_element(By.CSS_SELECTOR, "#keyword-recommend").click()
                self.mapping_driver.find_element(By.CSS_SELECTOR, "#keyword-recommend").send_keys(Keys.ENTER)

                # 40개 추천 버튼 클릭
                # self.mapping_driver.find_element(By.CSS_SELECTOR, "#select-keyword > div > div:nth-child(1) > div > ul > li:nth-child(3) > a").click()
                self.mapping_driver.find_element(By.CSS_SELECTOR, "#select-keyword > div > div:nth-child(1) > div > ul > li:nth-child(3) > a").send_keys(Keys.ENTER)

                keyword = self.mapping_driver.find_element(By.CSS_SELECTOR, ".form-control.p-3").get_attribute('value')

                # keyword를 프로그램 키워드창(keyword_plainTextEdit)으로 출력
                self.keyword_plainTextEdit.setPlainText(keyword)

                # 키워드 개수 카운트
                keyword_amount_num = keyword.count(',') + 1

                # 키워드 개수 출력
                self.keyword_amount_label.setText(str(keyword_amount_num))

                # 새 탭 닫기
                self.mapping_driver.close()

                # all_winddows[0]을 선택하여 1번째 탭으로 전환.
                self.mapping_driver.switch_to.window(all_windows[0]) 

                self.mapping_status_label_2.setText('키워드 가져오기 완료')

        except Exception as e:
            self.keyword_amount_label.setText('셀러라이프 검색 실패')
            pyautogui.alert(f'오류코드 : {str(e)}')

    # 키워드 입력 함수
    def keyword_input(self) :
        self.mapping_clear_status()
        self.mapping_status_label_2.setText('키워드 입력 중')
        QApplication.processEvents()
        try : 
            # 키워드 변수에 키워드 text 넣기.
            keyword = self.keyword_plainTextEdit.toPlainText()

            # 새탭으로 드라이버 전환
            all_windows = self.mapping_driver.window_handles            # 드라이버가 제어하고 있는 모든 크롬 윈도우를 all_windows 변수에 넣어 
            self.mapping_driver.switch_to.window(all_windows[1])        # all_winddows[1]을 선택하여 2번째 탭으로 전환.
            time.sleep(1)

            # tmg num 사이트 접근 검증 함수.
            guardian = self.mapping_guardian()
            if guardian == False :
                return 0

            # 태그설정란 클릭
            tag_wingdow = self.mapping_driver.find_element(By.CSS_SELECTOR, "#text_searchtag_")
            tag_wingdow.click()
            tag_wingdow.send_keys(Keys.CONTROL, 'a')
            tag_wingdow.send_keys(keyword)

            # 미매핑 설정 함수 실행
            self.no_mapping()

            self.mapping_status_label_2.setText('키워드 입력 완료')

        except : 
            self.mapping_status_label_1.setText('키워드 입력 실패')
            self.mapping_status_label_2.setText('1. 크롬브라우저가 띄워져 있는지 확인해주세요')
            self.mapping_status_label_3.setText('2. 카테고리탭이 2번째 탭에 띄워져 있는지 확인해주세요.')

    # 셀러라이프 자동검색/입력 함수
    def auto_keyword(self) : 
        # 셀러라이프 검색 함수 실행
        self.sellerlife_search()
        # 키워드 금지어 제거 함수 실행
        if self.forbidden_keyword_Check_Box.isChecked() == 1 :
            self.forbidden_keyword_remover()
        # 키워드 입력 함수 실행
        self.keyword_input()
        self.mapping_status_label_2.setText('키워드 가져오기 및 입력 완료')

    # 키워드 금지어사용여부 체크박스 함수
    def used_forbidden_keyword_Check_Box(self) :
        if self.forbidden_keyword_Check_Box.isChecked() == 1 :
            self.forbidden_keyword_num_label.setText('제거된 키워드 개수 : ')
            self.forbidden_keyword_plainTextEdit.setEnabled(True)
            self.forbidden_keyword_save_btn.setEnabled(True)
            self.forbidden_keyword_label.setEnabled(True)

        elif self.forbidden_keyword_Check_Box.isChecked() == 0 :
            self.forbidden_keyword_num_label.setText('')
            self.removed_keyword_amount_label.setText('')
            self.forbidden_keyword_plainTextEdit.setEnabled(False)
            self.forbidden_keyword_save_btn.setEnabled(False)
            self.forbidden_keyword_label.setEnabled(False)

    # 키워드 금지어 설정 함수
    def forbidden_keyword_save(self) :
        forbidden_keyword_txt = self.forbidden_keyword_plainTextEdit.toPlainText()
        if forbidden_keyword_txt == None :
            return 0
        with open(f'forbidden_keyword.txt', mode='w') as file :            # txt 파일 생성 및 저장
            file.write(forbidden_keyword_txt)
        self.forbidden_keyword_plainTextEdit.setPlainText(forbidden_keyword_txt)
        self.mapping_status_label_2.setText('금지어 저장 완료')

    # 키워드 금지어 읽기 함수
    def forbidden_keyword_read(self) :
        forbidden_keyword_file_existence = os.path.isfile(f'forbidden_keyword.txt')      # 라이센스 파일 존재 유무 확인.    존재할 경우 True, 비존재할경우 False 반환.

        if forbidden_keyword_file_existence == True :                              # 라이센스 파일이 존재할 경우 실행.
            with open(f'forbidden_keyword.txt', mode='r') as file :                       # txt 파일 읽어오기
                forbidden_keyword = file.read()
            self.forbidden_keyword_plainTextEdit.setPlainText(forbidden_keyword)
        elif forbidden_keyword_file_existence == False :                                       # 라이센스 파일이 존재하지 않을 경우 실행.
            return 0

    # 키워드 금지어 제거 함수
    def forbidden_keyword_remover(self) :
        self.mapping_clear_status()
        self.mapping_status_label_2.setText('키워드 금지어 제거 중.')
        QApplication.processEvents()

        keyword = self.keyword_plainTextEdit.toPlainText()
        forbidden_keyword = self.forbidden_keyword_plainTextEdit.toPlainText()

        keyword_list = keyword.split(',')
        forbidden_keyword_list = forbidden_keyword.split(',')

        Removed_keywords_num = 0
        Removed_keywords_list = []
        for value in keyword_list : 
            if value not in forbidden_keyword_list :
                Removed_keywords_list.append(value)
            elif value in forbidden_keyword_list :
                Removed_keywords_num += 1

        self.removed_keyword_amount_label.setText(str(Removed_keywords_num))

        Removed_keywords = ','.join(Removed_keywords_list)

        # 키워드란에 제거된 키워드 출력
        self.keyword_plainTextEdit.setPlainText(Removed_keywords)

        # 키워드 개수 카운트
        keyword_amount_num = Removed_keywords.count(',') + 1

        # 키워드 개수 출력
        self.keyword_amount_label.setText(str(keyword_amount_num))

        self.mapping_status_label_2.setText('키워드 금지어 제거 완료')

    # 더망고 카테고리 검색 함수
    def mango_cate_search(self) :
        self.mapping_clear_status()
        self.mapping_status_label_2.setText('카테고리 검색어 입력 중')
        QApplication.processEvents()
        
        try :
            # 새탭으로 드라이버 전환
            all_windows = self.mapping_driver.window_handles         # 드라이버가 제어하고 있는 모든 크롬 윈도우를 all_windows 변수에 넣어
            self.mapping_driver.switch_to.window(all_windows[1])     # all_winddows[1]을 선택하여 2번째 탭으로 전환.
            time.sleep(1)

            # tmg num 사이트 접근 검증 함수.
            guardian = self.mapping_guardian()
            if guardian == False :
                return 0

            category_last_name = self.mango_cate_search_lineEdit.text()
            
            # 더망고 검색 라디오 버튼 선택시 함수 실행
            if self.search_select_comboBox.currentText() == '더망고 검색' :
                # 검색창 찾기
                search_window = self.mapping_driver.find_element(By.CSS_SELECTOR, "#category_search_text")
                # 국내/해외 설정
                if self.domestic_foreign_comboBox.currentText() == '해외' :
                    self.mapping_driver.find_element(By.CSS_SELECTOR, "#select_category_type > option:nth-child(1)").click()
                elif self.domestic_foreign_comboBox.currentText() == '국내' :
                    self.mapping_driver.find_element(By.CSS_SELECTOR, "#select_category_type > option:nth-child(2)").click()


            # 마켓별 검색 라디오 버튼 선택 시 함수 실행
            elif self.search_select_comboBox.currentText() == '마켓별 검색' :
                    search_window = self.mapping_driver.find_element(By.CSS_SELECTOR, "#openmarket_category_search_text")

            # 검색창 클릭
            search_window.click()
            # 검색창에 있는 문자 모두선택
            search_window.send_keys(Keys.CONTROL, 'a')
            # 검색창에 최하위 카테고리 이름 입력
            search_window.send_keys(category_last_name)

            # 더망고 검색 라디오 버튼 선택시 함수 실행
            if self.search_select_comboBox.currentText() == '더망고 검색' :
                # 더망고 카테고리 검색버튼 클릭.
                self.mapping_driver.find_element(By.CSS_SELECTOR, "body > form > table:nth-child(21) > tbody > tr:nth-child(1) > td:nth-child(2) > a.defbtn_med.dtype5").click()

            # 마켓별 검색 라디오 버튼 선택 시 함수 실행
            elif self.search_select_comboBox.currentText() == '마켓별 검색' :
                # 마켓별 카테고리 검색버튼 클릭.
                self.mapping_driver.find_element(By.CSS_SELECTOR, "body > form > table:nth-child(21) > tbody > tr:nth-child(2) > td:nth-child(2) > a").click()

            time.sleep(1)

            # 미매핑 설정 함수 실행
            self.no_mapping()

            self.mapping_status_label_2.setText('카테고리 검색어 입력 완료')
        
        except Exception as e :
            self.mapping_status_label_1.setText('카테고리 검색 실패')
            self.mapping_status_label_2.setText('1. 크롬브라우저가 띄워져 있는지 확인해주세요')
            self.mapping_status_label_3.setText('2. 카테고리탭이 2번째 탭에 띄워져 있는지 확인해주세요.')

    # 더망고 카테고리 설정저장 클릭 함수
    def category_save(self) :
        self.mapping_clear_status()
        try :
            # 새탭으로 드라이버 전환
            all_windows = self.mapping_driver.window_handles         # 드라이버가 제어하고 있는 모든 크롬 윈도우를 all_windows 변수에 넣어 
            self.mapping_driver.switch_to.window(all_windows[1])     # all_winddows[1]을 선택하여 2번째 탭으로 전환.
            time.sleep(1)

            # tmg num 사이트 접근 검증 함수.
            guardian = self.mapping_guardian()
            if guardian == False :
                return 0

            # 미매핑 설정 함수 실행
            self.no_mapping()

            # 카테고리 설정저장 클릭
            self.mapping_driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(13) > a.defbtn_lar.dtype2").click()

        except : 
            self.mapping_status_label_1.setText('카테고리 설정저장 실패')
            self.mapping_status_label_2.setText('1. 크롬브라우저가 띄워져 있는지 확인해주세요')
            self.mapping_status_label_3.setText('2. 카테고리탭이 2번째 탭에 띄워져 있는지 확인해주세요.')

    # 파파고 번역 함수
    def papago(self, en_text) :
        client_id = self.client_id_edit.text()
        client_sr = self.client_sr_edit.text()

        data = {'text' : en_text,
            'source' : 'en',
            'target': 'ko'}

        url = "https://openapi.naver.com/v1/papago/n2mt"

        header = {"X-Naver-Client-Id":client_id,
                "X-Naver-Client-Secret":client_sr}

        response = requests.post(url, headers=header, data= data)
        rescode = response.status_code

        if(rescode==200):
            t_data = response.json()
            self.translation_word = t_data['message']['result']['translatedText']
            self.category_transration_name_label.setText(self.translation_word)
            self.trasrator_status_label.setText('번역성공')

        else:
            if rescode == 400 :
                self.trasrator_status_label.setText('err 400 - 번역내용 없음')
            elif rescode == 401 :
                self.trasrator_status_label.setText('err 401 - API인증실패')
            elif rescode == 429 :
                self.trasrator_status_label.setText('err 429 - 일일 번역량 초과')
            elif rescode == 500 :
                self.trasrator_status_label.setText('err 500 - 서버 오류')

    # 파파고 테스트 버튼
    def test_btn(self) :
        if self.used_transrator_checkbox.isChecked() == 1 :
            self.search_category_name_label.setText('hi')
            self.papago('hi')

        elif self.used_transrator_checkbox.isChecked() == 0 : 
            self.trasrator_status_label.setText('[번역 사용]을 체크 표시해주세요')

    # 번역 사용 체크박스
    def used_transrator(self) :
        if self.used_transrator_checkbox.isChecked() == 1 :
            self.category_transration_name_label2.setText('번역 카테고리 : ')
            self.category_transration_name_label.setText(self.translation_word)

        elif self.used_transrator_checkbox.isChecked() == 0 :
            self.category_transration_name_label2.setText('')
            self.category_transration_name_label.setText('')

    # 해외/국내 콤보박스 활성화/비활성화 함수
    def search_select(self) :
        if self.search_select_comboBox.currentText() == '더망고 검색' :
            self.domestic_foreign_comboBox.setEnabled(True)
        elif self.search_select_comboBox.currentText() == '마켓별 검색' :
            self.domestic_foreign_comboBox.setEnabled(False)

    # 상태창 초기화
    def mapping_clear_status(self) :
        self.mapping_status_label_1.setText('')
        self.mapping_status_label_2.setText('')
        self.mapping_status_label_3.setText('')
        QApplication.processEvents()

    # 검색 카테고리 출력 함수
    def search_category(self) : 
        # 최하 카테고리에 '/'가 있을 시에 앞 또는 뒤 카테고리 출력.
        category_last_name = self.category_last_name_label.text()
        category_last_name_list = list(category_last_name)      # 최하 카테고리의 모든 문자를 리스트 변수에 넣음.
        if '/' in category_last_name_list :                      # cate_last_name_list에 '/'가 포함되어 있다면 if문 실행
            categorized_categories = category_last_name.split('/')  # 최하 카테고리의 /를 기준으로 문자를 나눔. 
            first_category = categorized_categories[0]              # /로 나눠진 첫번째 카테고리는 first_category 변수에 저장.
            second_category = categorized_categories[1]               # /로 나눠진 두번째 카테고리는 second_category 변수에 저장.
            third_category = categorized_categories[-1]               # /로 나눠진 세번째 카테고리는 second_category 변수에 저장.

            # 카테고리 앞/뒤 버튼 선택에 따른 검색 카테고리 출력
            if self.first_category_radioButton.isChecked() == 1 :
                # 검색 카테고리에 first_category 출력
                self.search_category_name_label.setText(first_category)

            elif self.second_category_radioButton.isChecked() == 1 :
                # 검색 카테고리에 second_category 출력
                self.search_category_name_label.setText(second_category)

            elif self.third_category_radioButton.isChecked() == 1 :
                # 검색 카테고리에 second_category 출력
                self.search_category_name_label.setText(third_category)
        
        elif '&' in category_last_name_list :                      # cate_last_name_list에 '&'가 포함되어 있다면 if문 실행
            category_last_name = category_last_name.replace(' &', '&')
            category_last_name = category_last_name.replace('& ', '&')
            categorized_categories = category_last_name.split('&')  # 최하 카테고리의 &를 기준으로 문자를 나눔. 
            first_category = categorized_categories[0]              # &로 나눠진 첫번째 카테고리는 first_category 변수에 저장.
            second_category = categorized_categories[1]               # &로 나눠진 두번째 카테고리는 second_category 변수에 저장.
            third_category = categorized_categories[-1]               # &로 나눠진 세번째 카테고리는 second_category 변수에 저장.

            # 카테고리 앞/뒤 버튼 선택에 따른 검색 카테고리 출력
            if self.first_category_radioButton.isChecked() == 1 :
                # 검색 카테고리에 first_category 출력
                self.search_category_name_label.setText(first_category)

            elif self.second_category_radioButton.isChecked() == 1 :
                # 검색 카테고리에 second_category 출력
                self.search_category_name_label.setText(second_category)

            elif self.third_category_radioButton.isChecked() == 1 :
                # 검색 카테고리에 second_category 출력
                self.search_category_name_label.setText(third_category)

        elif '및' in category_last_name_list :                      # cate_last_name_list에 '및'이 포함되어 있다면 if문 실행
            category_last_name = category_last_name.replace(' 및', '및')
            category_last_name = category_last_name.replace('및 ', '및')
            categorized_categories = category_last_name.split('및')  # 최하 카테고리의 및를 기준으로 문자를 나눔. 
            first_category = categorized_categories[0]              # 및으로 나눠진 첫번째 카테고리는 first_category 변수에 저장.
            second_category = categorized_categories[1]               # 및으로 나눠진 두번째 카테고리는 second_category 변수에 저장.
            third_category = categorized_categories[-1]               # 및으로 나눠진 세번째 카테고리는 second_category 변수에 저장.

            # 카테고리 앞/뒤 버튼 선택에 따른 검색 카테고리 출력
            if self.first_category_radioButton.isChecked() == 1 :
                # 검색 카테고리에 first_category 출력
                self.search_category_name_label.setText(first_category)

            elif self.second_category_radioButton.isChecked() == 1 :
                # 검색 카테고리에 second_category 출력
                self.search_category_name_label.setText(second_category)

            elif self.third_category_radioButton.isChecked() == 1 :
                # 검색 카테고리에 second_category 출력
                self.search_category_name_label.setText(third_category)

        else :
            self.search_category_name_label.setText(category_last_name)

        QApplication.processEvents()

    # tmg num 사이트 접근 검증 함수
    def mapping_guardian(self) :
        # 로그인 했던 tmg 번호만 허용됨. 크롬에서 다른 tmg 번호로 접속할 경우 접속 종료 실행.
        # 현재 접속한 사이트에서 tmg 번호 추출.
        tmg_num = self.mapping_decry_tmg_edit.text()
        current_url = self.mapping_driver.current_url
        A_list = current_url.split('.')
        B_list = A_list[0].split('g')
        extracted_tmg_num = B_list[1]

        if tmg_num != extracted_tmg_num :
            self.mapping_status_label_1.setText('로그인한 tmg 번호와')
            self.mapping_status_label_2.setText('사이트에서 접근한 tmg 번호가 다릅니다.')
            self.mapping_status_label_3.setText('비정상적인 접근으로 크롬을 종료합니다.')
            self.mapping_driver.quit()
            return False

##################################중복키워드 제거 함수############################################
    # 중복키워드 제거 함수
    def Removed_duplicate_word(self) :
        Banned_word = self.Banned_word_input_window.toPlainText()
        if Banned_word == "" :
            self.status.setText("금지어를 입력해 주세요.")
            return 0

        self.status.setText("입력한 금지어 개수와 중복 횟수를 분석 중 입니다.")
        QApplication.processEvents()

        # 입력받은 금지어의 \n를 ;로 변환
        Banned_word = Banned_word.replace('\n', ';')

        # 단어 앞 뒤 공백 제거 체크박스 선택시 실행
        if self.gap_removal_checkBox.isChecked() == True :
            Banned_word = Banned_word.replace(' ;', ';')
            Banned_word = Banned_word.replace('; ', ';')

        # 금지어 단어 개수 출력
        semicolon_num = Banned_word.count(';')
        Banned_word_num = str(semicolon_num)
        self.Banned_word_num_status.setText(Banned_word_num)

        # ;를 기준으로 나눠서 리스트 형태로 저장
        Banned_word_list = Banned_word.split(';')

        # 리스트의 각 인덱스의 중복횟수를 세어줌. 딕셔너리 형태로 저장하고 그 값을 출력
        counter_list = []
        counter = Counter(Banned_word_list).most_common         # Counter 모듈이 괄호안에 있는 리스트 변수의 중복횟수를 리스트명을 key에, 중복횟수를 value에 저장하여 딕셔너리 형태로 저장.
        for key, value in counter() :
            if value == 1 :
                continue
            counter_list.append(f'{key} : {value}')             # value가 1 이상인 것들만 따로 리스트 형태로 counter_list라는 리스트에 저장

        sum_counter_list = '\n'.join(counter_list)              # counter_list 리스트 변수의 안에 있는 인덱스들을 하나의 텍스트로 저장. 각 인덱스들을 sum_counter_list라는 하나의 텍스트변수에 저장하는데 인덱스마다 (\n)띄어쓰기로 구분하여 저장.
        self.Duplicate_words_num.setText(sum_counter_list)      # 문자열과 그 문자열의 중복횟수를 정보를 가지고 있는 sub_counter_list 변수 출력.
        

        # for문을 이용한 중복 키워드 제거, 중복이 없는 단어들만을 추출하여 Removed_duplicate_words_list라는 리스트에 저장.
        self.status.setText("중복키워드를 제거 중 입니다.")
        QApplication.processEvents()

        Removed_duplicate_words_num = 0
        Removed_duplicate_words_list = []
        for value in Banned_word_list : 
            if value not in Removed_duplicate_words_list :
                Removed_duplicate_words_list.append(value)
            elif value in Removed_duplicate_words_list :
                Removed_duplicate_words_num += 1

        # 중복키워드제거 리스트를 다시 하나로 합침. 모든 인덱스의 뒤에 ;를 붙임.
        Removed_duplicate_words= ';'.join(Removed_duplicate_words_list)

        # 중복키워드제거 변수 출력.
        self.Result_window_of_removed_duplicate_word.setPlainText(Removed_duplicate_words)

        # 제거된 단어 개수 출력
        self.Removed_duplicate_word_num_status.setText(str(Removed_duplicate_words_num))

        # 중복 단어 제거 결과 창 단어 개수 출력
        Result_semicolon_num = Removed_duplicate_words.count(';')
        semicolon_num = Banned_word.count(';')
        self.Result_of_removed_duplicate_word_num.setText(str(Result_semicolon_num))

        self.status.setText("금지어 분석 및 중복 키워드 제거가 완료되었습니다.")

##################################자동 창 정렬 함수################################################
    # 얼라인먼터 로그인 함수
    def Alignmenter_login(self) :
        self.alignmenter_clear_status()

        # tmg번호, 아이디, 비밀번호 불러와서 변수에 저장하는 코드.
        tmg_num = self.alignmenter_decry_tmg_edit.text()

        # 브라우저 꺼짐 방지
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)

        # 불필요한 에러 메시지 없애기 (꼭 필요한 코드는 아님. 없어도됨. 다만 이상한 오류코드가 발생하기에 그거 없애려고 추가하는 것)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

        service = Service(executable_path=ChromeDriverManager().install())
        self.alignmenter_driver = webdriver.Chrome(service=service, options=chrome_options)

        # 웹페이지가 로딩 될때까지 5초는 기다림
        self.alignmenter_driver.implicitly_wait(5)

        # 쿠팡 access denied 안나게 하는 코드
        self.alignmenter_driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) """})

        # 웹페이지가 로딩 될때까지 5초는 기다림
        self.alignmenter_driver.implicitly_wait(5)

        # 화면 최대화
        self.alignmenter_driver.maximize_window()

        # 개인 cafe24 주소로 이동
        self.alignmenter_driver.get(f"https://tmg{tmg_num}.cafe24.com/mall/admin/admin_login.php")
        time.sleep(1)


    # 업데이트 창 나누기 & 상품업데이트 & 마켓전송 시작 함수
    def update_tab_divider_and_send(self) :
        self.update_tab_divider()
        self.update_and_market_send()

    # 업데이트 창 나누기 함수
    def update_tab_divider(self) :
        self.alignmenter_clear_status()
        try :
            all_windows = self.alignmenter_driver.window_handles

            self.alignmenter_driver.switch_to.window(all_windows[0])

            current_url = self.alignmenter_driver.current_url

            A_list = current_url.split('.')
            if A_list[2] != 'com/mall/admin/admin_goods_update' :
                self.alignmenter_status_label_2.setText('첫 페이지를 상품업데이트&마켓전송 페이지로 열어놓고,')
                self.alignmenter_status_label_3.setText('업데이트 및 전송마켓을 설정 후 다시 시도해 주세요.')
                return 0
            
            self.alignmenter_status_label_2.setText('상품업데이트&마켓전송 창 분할 중')

            try :   
                item_amount_num_str = self.alignmenter_driver.find_element(By.CSS_SELECTOR, "#span_total_count").text           # 총 상품 개수 추출
                item_amount_num_str_list = item_amount_num_str.split(',')
                item_amount_num = int(''.join(item_amount_num_str_list))

            except :
                item_amount_num_str_org = self.alignmenter_driver.find_element(By.CSS_SELECTOR, "#sp_limit_info").text           # 총 상품 개수 추출
                item_amount_num_str = item_amount_num_str_org[6:12]
                item_amount_num_str_list = item_amount_num_str.split(',')
                item_amount_num = int(''.join(item_amount_num_str_list))

            if self.update_tab_divider_two_radioButton.isChecked() == 1 :
                tab_num = 2
                item_amount_num_share = item_amount_num // tab_num

                for i in range(tab_num) : 
                    all_windows = self.alignmenter_driver.window_handles
                    tab_front = (item_amount_num_share * i) + 1
                    if i < tab_num - 1 :
                        tab_back = (item_amount_num_share * (i+1))
                    elif i == tab_num - 1 :
                        tab_back = item_amount_num

                    self.alignmenter_driver.switch_to.window(all_windows[i])
                    try :
                        self.alignmenter_driver.find_element(By.CSS_SELECTOR, "#sp_limit_btn > a > span").click()
                    except :
                        pass
                    start_limit = self.alignmenter_driver.find_element(By.CSS_SELECTOR, "#start_limit")
                    start_limit.click()
                    start_limit.send_keys(Keys.CONTROL, 'a')
                    start_limit.send_keys(tab_front)

                    end_limit = self.alignmenter_driver.find_element(By.CSS_SELECTOR, "#end_limit")
                    end_limit.click()
                    end_limit.send_keys(Keys.CONTROL, 'a')
                    end_limit.send_keys(tab_back)
                
                    if i < tab_num - 1 :
                        self.alignmenter_driver.execute_script(f'window.open("{current_url}")')

            elif self.update_tab_divider_three_radioButton.isChecked() == 1 :
                tab_num = 3
                item_amount_num_share = item_amount_num // tab_num

                for i in range(tab_num) : 
                    all_windows = self.alignmenter_driver.window_handles
                    tab_front = (item_amount_num_share * i) + 1
                    if i < tab_num - 1 :
                        tab_back = (item_amount_num_share * (i+1))
                    elif i == tab_num - 1 :
                        tab_back = item_amount_num

                    self.alignmenter_driver.switch_to.window(all_windows[i])
                    try :
                        self.alignmenter_driver.find_element(By.CSS_SELECTOR, "#sp_limit_btn > a > span").click()
                    except :
                        pass
                    start_limit = self.alignmenter_driver.find_element(By.CSS_SELECTOR, "#start_limit")
                    start_limit.click()
                    start_limit.send_keys(Keys.CONTROL, 'a')
                    start_limit.send_keys(tab_front)

                    end_limit = self.alignmenter_driver.find_element(By.CSS_SELECTOR, "#end_limit")
                    end_limit.click()
                    end_limit.send_keys(Keys.CONTROL, 'a')
                    end_limit.send_keys(tab_back)
                
                    if i < tab_num - 1 :
                        self.alignmenter_driver.execute_script(f'window.open("{current_url}")')

            elif self.update_tab_divider_four_radioButton.isChecked() == 1 :
                tab_num = 4
                item_amount_num_share = item_amount_num // tab_num

                for i in range(tab_num) : 
                    all_windows = self.alignmenter_driver.window_handles
                    tab_front = (item_amount_num_share * i) + 1
                    if i < tab_num - 1 :
                        tab_back = (item_amount_num_share * (i+1))
                    elif i == tab_num - 1 :
                        tab_back = item_amount_num

                    self.alignmenter_driver.switch_to.window(all_windows[i])
                    try :
                        self.alignmenter_driver.find_element(By.CSS_SELECTOR, "#sp_limit_btn > a > span").click()
                    except :
                        pass
                    start_limit = self.alignmenter_driver.find_element(By.CSS_SELECTOR, "#start_limit")
                    start_limit.click()
                    start_limit.send_keys(Keys.CONTROL, 'a')
                    start_limit.send_keys(tab_front)

                    end_limit = self.alignmenter_driver.find_element(By.CSS_SELECTOR, "#end_limit")
                    end_limit.click()
                    end_limit.send_keys(Keys.CONTROL, 'a')
                    end_limit.send_keys(tab_back)
                
                    if i < tab_num - 1 :
                        self.alignmenter_driver.execute_script(f'window.open("{current_url}")')

            elif self.update_tab_divider_five_radioButton.isChecked() == 1 :
                tab_num = 5
                item_amount_num_share = item_amount_num // tab_num

                for i in range(tab_num) : 
                    all_windows = self.alignmenter_driver.window_handles
                    tab_front = (item_amount_num_share * i) + 1
                    if i < tab_num - 1 :
                        tab_back = (item_amount_num_share * (i+1))
                    elif i == tab_num - 1 :
                        tab_back = item_amount_num

                    self.alignmenter_driver.switch_to.window(all_windows[i])
                    try :
                        self.alignmenter_driver.find_element(By.CSS_SELECTOR, "#sp_limit_btn > a > span").click()
                    except :
                        pass
                    start_limit = self.alignmenter_driver.find_element(By.CSS_SELECTOR, "#start_limit")
                    start_limit.click()
                    start_limit.send_keys(Keys.CONTROL, 'a')
                    start_limit.send_keys(tab_front)

                    end_limit = self.alignmenter_driver.find_element(By.CSS_SELECTOR, "#end_limit")
                    end_limit.click()
                    end_limit.send_keys(Keys.CONTROL, 'a')
                    end_limit.send_keys(tab_back)
                
                    if i < tab_num - 1 :
                        self.alignmenter_driver.execute_script(f'window.open("{current_url}")')

            self.alignmenter_status_label_2.setText('상품업데이트&마켓전송 창 분할 완료')

        except :
            self.alignmenter_status_label_1.setText('상품업데이트&마켓전송 페이지이외에')
            self.alignmenter_status_label_2.setText('다른 페이지가 검출됩니다.')
            self.alignmenter_status_label_3.setText('상품업데이트&마켓전송 탭 이외의 모든 페이지는 닫아주세요.')

            return 0

    # 상품업데이트 & 마켓전송 시작 함수
    def update_and_market_send(self) :
        self.alignmenter_clear_status()
        try :
            if self.update_tab_divider_two_radioButton.isChecked() == 1 :
                tab_max_num = 2
            elif self.update_tab_divider_three_radioButton.isChecked() == 1 :
                tab_max_num = 3
            elif self.update_tab_divider_four_radioButton.isChecked() == 1 :
                tab_max_num = 4
            elif self.update_tab_divider_five_radioButton.isChecked() == 1 :
                tab_max_num = 5
            all_windows = self.alignmenter_driver.window_handles

            for i in range(tab_max_num) :
                self.alignmenter_driver.switch_to.window(all_windows[i])
                self.alignmenter_driver.find_element(By.CSS_SELECTOR, "#update_start_limit > span").click()

            self.alignmenter_status_label_2.setText('상품업데이트&마켓전송 시작')

        except :
            self.alignmenter_status_label_1.setText('상품업데이트&마켓전송 페이지이외에')
            self.alignmenter_status_label_2.setText('다른 페이지가 검출됩니다.')
            self.alignmenter_status_label_3.setText('상품업데이트&마켓전송 탭 이외의 모든 페이지는 닫아주세요.')

    # 정렬 정보 파일 저장 함수
    def Alignment_info_file_save(self) :
        self.alignmenter_clear_status()
        Alignment_info_name = self.Alignment_info_name_edit.text()
        if Alignment_info_name == '' :
            self.alignmenter_status_label_2.setText('정렬 정보 저장의 제목을 입력해주세요')
            return 0

        self.Alignment_info_list_comboBox.addItem(Alignment_info_name)
        Alignment_info = [Alignment_info_name,self.window_width_spinBox.text(),self.window_height_spinBox.text(),self.window_column_amount_spinBox.text(),self.alignment_period_spinBox.text(),self.window_width_gap_spinBox.text(),self.window_height_gap_spinBox.text(),self.window_x_position_spinBox.text(),self.window_y_position_spinBox.text()]
        self.Alignment_info_list.append(Alignment_info)

        with open(f'Alignment_info.txt', mode='w') as file :            # txt 파일 생성 및 저장
            file.write(str(self.Alignment_info_list))
        self.alignmenter_status_label_2.setText('정렬 정보 저장 완료')

    # 정렬 정보 파일 읽기 함수
    def Alignment_info_file_read(self) :
        Alignment_info_file_existence = os.path.isfile(f'Alignment_info.txt')               # 라이센스 파일 존재 유무 확인.    존재할 경우 True, 비존재할경우 False 반환.

        if Alignment_info_file_existence == True :                                          # 라이센스 파일이 존재할 경우 실행.
            with open(f'Alignment_info.txt', mode='r') as file :                            # txt 파일 읽어오기
                Alignment_info = file.read()
            try :
                self.Alignment_info_list = ast.literal_eval(Alignment_info)                 # 괄호안에 든 문자열을 그대로 읽는 기능. 리스트형태로 문자가 되어있는데, 이것을 변수에 저장할때는 리스트형태의 문자가 그대로 문자로 저장되어 버리는데 ast.literal_eval을 쓰면 리스트 형태로 저장되어짐.
            except :
                self.Alignment_info_list = []

            Alignment_info_list_len = len(self.Alignment_info_list)

            for i in range(Alignment_info_list_len) :
                self.Alignment_info_list_comboBox.addItem(self.Alignment_info_list[i][0])

        elif Alignment_info_file_existence == False :                                       # 라이센스 파일이 존재하지 않을 경우 실행.
            return 0

    # 정렬 정보 읽기 함수
    def Alignment_info_read(self) :
        index = self.Alignment_info_list_comboBox.currentIndex()
        self.window_width_spinBox.setValue(int(self.Alignment_info_list[index][1]))
        self.window_height_spinBox.setValue(int(self.Alignment_info_list[index][2]))
        self.window_column_amount_spinBox.setValue(int(self.Alignment_info_list[index][3]))
        self.alignment_period_spinBox.setValue(int(self.Alignment_info_list[index][4]))
        self.window_width_gap_spinBox.setValue(int(self.Alignment_info_list[index][5]))
        self.window_height_gap_spinBox.setValue(int(self.Alignment_info_list[index][6]))
        self.window_x_position_spinBox.setValue(int(self.Alignment_info_list[index][7]))
        self.window_y_position_spinBox.setValue(int(self.Alignment_info_list[index][8]))

    # 정렬 정보 삭제 함수
    def Alignment_info_file_delete(self) :
        self.alignmenter_clear_status()
        del self.Alignment_info_list[self.Alignment_info_list_comboBox.currentIndex()]
        self.Alignment_info_list_comboBox.removeItem(self.Alignment_info_list_comboBox.currentIndex())
        with open(f'Alignment_info.txt', mode='w') as file :                                            # txt 파일 생성 및 저장
            file.write(str(self.Alignment_info_list))
        self.alignmenter_status_label_2.setText('정렬 정보 삭제 완료')

    # 창 정렬 함수
    def Alignment(self) :
        self.alignmenter_clear_status()
        Alignment = threading.Thread(target=self.Alignment_thread)
        Alignment.daemon=True
        Alignment.start()

    # 창 정렬 쓰레드 함수    
    def Alignment_thread(self) :
        self.auto_alignment_time_listWidget.insertItem(0,str(dt.datetime.now()))
        try : 
            all_windows = self.alignmenter_driver.window_handles         # 드라이버가 제어하고 있는 모든 크롬 윈도우를 all_windows 변수에 넣어.
        except :
            self.alignmenter_status_label_1.setText('로그인하여 브라우저를 열어주세요.')
            self.alignmenter_status_label_2.setText('자동정렬이 활성화 되어 있으면 자동정렬을')
            self.alignmenter_status_label_3.setText('중지하고 다음 작업을 진행해주세요.')
            QApplication.processEvents()
            return 0
        time.sleep(1)

        # 창 정렬 정보 받기
        window_width = int(self.window_width_spinBox.text())
        window_height = int(self.window_height_spinBox.text())
        window_column_amount = int(self.window_column_amount_spinBox.text())
        window_amount = len(all_windows)-1
        window_width_gap = int(self.window_width_gap_spinBox.text())
        window_height_gap = int(self.window_height_gap_spinBox.text())
        window_x_position = int(self.window_x_position_spinBox.text())
        window_y_position = int(self.window_y_position_spinBox.text())

        row = 0
        column = 0
        num = 0

        while(True) :
            if num > window_amount :
                break
            # 새탭으로 드라이버 전환
            self.alignmenter_driver.switch_to.window(all_windows[num])
            guardian = self.alignmenter_guardian()
            if guardian == False :
                return 0
            current_url = self.alignmenter_driver.current_url
            current_url_list = current_url.split('.')
            if len(current_url_list) == 1 :
                current_url_list.append('')
            cafe24_check = current_url_list[1]
            if cafe24_check != 'cafe24' :
                position_x = window_x_position+(window_width+window_width_gap)*(column)
                position_y = window_y_position+(window_height+window_height_gap)*(row)
                self.alignmenter_driver.set_window_rect(position_x,position_y,window_width,window_height)
                column += 1
                if column == window_column_amount : 
                    column = 0
                    row += 1
            num += 1

    # 자동 정렬 시작/중지 select 함수
    def auto_Alignment(self) :
        if self.auto_Alignment_ctrl_btn.text() == '자동 정렬 시작' :
            self.auto_Alignment_ctrl_btn.setText('자동 정렬 중지')
            self.alignmenter_status_label_2.setText('자동 정렬 진행중!')
            QApplication.processEvents()
            self.exit = False
            auto_Alignment = threading.Thread(target=self.auto_Alignment_thread)
            auto_Alignment.daemon=True
            auto_Alignment.start()
        elif self.auto_Alignment_ctrl_btn.text() == '자동 정렬 중지' :
            self.auto_Alignment_ctrl_btn.setText('자동 정렬 시작')
            self.alignmenter_status_label_1.setText('')
            self.alignmenter_status_label_2.setText('자동 정렬 중지!')
            self.alignmenter_status_label_3.setText('')
            self.exit = True

    # 자동 정렬 쓰레드 함수
    def auto_Alignment_thread(self) :
        while True :
            self.alignmenter_status_label_2.setText('자동 정렬 진행중!')
            if self.exit == True :
                return
            self.Alignment_thread()
            time.sleep(int(self.alignment_period_spinBox.text())-2)

    # 마우스 좌표 보기 함수
    def mouse_position(self) :
        pyautogui.mouseInfo()

    # 상태창 초기화
    def alignmenter_clear_status(self) :
        self.alignmenter_status_label_1.setText('')
        self.alignmenter_status_label_2.setText('')
        self.alignmenter_status_label_3.setText('')
        QApplication.processEvents()

    # tmg num 사이트 접근 검증 함수
    def alignmenter_guardian(self) :
        # 로그인 했던 tmg 번호만 허용됨. 크롬에서 다른 tmg 번호로 접속할 경우 접속 종료 실행.
        # 현재 접속한 사이트에서 tmg 번호 추출.
        current_url = self.alignmenter_driver.current_url
        A_list = current_url.split('.')
        B_list = A_list[0].split('g')
        if B_list[0] == 'https://tm' : 
            extracted_tmg_num = B_list[1]
            tmg_num = self.alignmenter_decry_tmg_edit.text()

            if tmg_num != extracted_tmg_num :
                self.alignmenter_status_label_1.setText('로그인한 tmg 번호와')
                self.alignmenter_status_label_2.setText('사이트에서 접근한 tmg 번호가 다릅니다.')
                self.alignmenter_status_label_3.setText('비정상적인 접근으로 크롬을 종료합니다.')
                self.alignmenter_driver.quit()
                return False

#########################자동 VPN ON/OFF 함수##########################################################
    # VPN 스케쥴 함수 쓰레드 실행 함수
    def Period_VPN_thread(self) :
        if self.VPN_auto_btn.text() == 'VPN 자동 ON/OFF 시작' :
            self.period_VPN_status_label.setText('VPN 자동 ON/OFF 진행중..')
            self.VPN_auto_btn.setText('VPN 자동 ON/OFF 중지')
            self.Period_VPN_status = True
            Period_VPN = threading.Thread(target=self.Period_VPN_schedule)
            Period_VPN.daemon=True
            Period_VPN.start()
        elif self.VPN_auto_btn.text() == 'VPN 자동 ON/OFF 중지' :
            self.period_VPN_status_label.setText('VPN 자동 ON/OFF 중지됨')
            self.VPN_auto_btn.setText('VPN 자동 ON/OFF 시작')
            self.Period_VPN_status = False
            
    # VPN 스케쥴 자동실행 함수
    def Period_VPN_schedule(self) :
        while self.Period_VPN_status == True :
            if self.Period_VPN_status == False :
                return
            Priod_minute = (int(self.Period_minute_spinBox.text())*60)-6
            self.Period_VPN()
            time.sleep(Priod_minute)

    # VPN 자동 ON,OFF 함수
    def Period_VPN(self) :
        try :
            subprocess.call("C:\Program Files (x86)\ExpressVPN\expressvpn-ui\ExpressVPN.exe")       # VPN 실행
            time.sleep(1)
            OFF_click = pyautogui.locateOnScreen("OFF.png", confidence=0.7)                      # 이미지의 70%만 같아도 이미지를 위치를 호출.
            pyautogui.click(OFF_click)                                                           # OFF 이미지 클릭
            time.sleep(3)
            subprocess.call("C:\Program Files (x86)\ExpressVPN\expressvpn-ui\ExpressVPN.exe")       # VPN 실행
            time.sleep(1)
            ON_click = pyautogui.locateOnScreen("ON.png", confidence=0.7)                        # 이미지의 70%만 같아도 이미지를 위치를 호출.
            pyautogui.click(ON_click)
            self.rerun_time_listWidget.insertItem(0,str(dt.datetime.now()))
        except Exception as e:
            self.rerun_time_listWidget.insertItem(0,'오류 발생- 코드 : ' + str(e))

###########################라이센스 관련 함수####################################################
    # 라이센스 입력 함수
    def input_license(self) :
        with open(f'license_key.txt', mode='w') as file :            # txt 파일 읽어오기
            license_key = self.decry_license_text_line_edit.text()
            file.write(license_key)
        self.license_status.setText('라이센스 입력이 완료되었습니다.')
        QApplication.processEvents()
        self.decryptography()
        return

    # 복호화 함수
    def decryptography(self) :      
        # MS)820,2022-04-09//ALIGN:820,2022-04-09/PEV)12:12:12:12:12:12,2022-04-09
        # MS)DISABLE/ALIGN)DISABLE/PEV)DISABLE
        # 라이센스 파일 존재 유무 확인.
        license_file_existence = os.path.isfile(f'license_key.txt')      # 라이센스 파일 존재 유무 확인.    존재할 경우 True, 비존재할경우 False 반환.

        if license_file_existence == True :                              # 라이센스 파일이 존재할 경우 실행.
            with open(f'license_key.txt', mode='r') as file :            # txt 파일 읽어오기
                license_key = file.read()
                self.decry_license_text_line_edit.setText(license_key)
        elif license_file_existence == False :                                       # 라이센스 파일이 존재하지 않을 경우 실행.
            self.license_status.setText('다른 기능을 사용하려면 라이센스 키를 입력하세요.\n프로그램이 설치된 경로내에 라이센스키가 들어있는 메모장이 생성됩니다.')
            return

        key_code = "0rKTqtZ4GQJlecUE8zRfU1B-metwX61_2Iz6B66B5eo="
        key_code = key_code.encode('utf-8')
        fernet = Fernet(key_code)

        today = dt.datetime.today()

        # 복호화 성공 시 실행
        try :
            decry_text = fernet.decrypt(license_key.encode('utf-8'))           # license를 인코딩하여 바이너리형태로 만들고, 복호화 하여 decry_text에 저장
            decry_text = decry_text.decode('utf-8')                             # decry_text를 디코딩하여 str형태로 변형.

            decry_text_list = decry_text.split('/')                             # decry_text를 /로 나눠 각 메뉴 탭들에 필요한 데이터로 나눔.

            mapping_decry_data = decry_text_list[0]
            alignmenter_decry_data = decry_text_list[1]
            period_VPN_decry_data = decry_text_list[2]

            mapping_decry_data_list = mapping_decry_data.split(')')
            alignmenter_decry_data_list = alignmenter_decry_data.split(')')
            period_VPN_decry_data_list = period_VPN_decry_data.split(')')

            mapping_available_status = mapping_decry_data_list[1]
            alignmenter_available_status = alignmenter_decry_data_list[1]
            period_VPN_available_status = period_VPN_decry_data_list[1]

            if mapping_available_status == 'DISABLE' :
                self.mapping_decry_tmg_status_2.setText('사용불가')
                self.mapping_decry_expiration_status_2.setText('사용불가')
                self.mapping_decry_service_period_status_2.setText('사용불가')
                self.tabWidget.setTabEnabled(1,False)
            elif mapping_available_status != 'DISABLE' :
                mapping_decry_tmg = mapping_available_status.split(',')[0]
                mapping_decry_expiration = mapping_available_status.split(',')[1]
                mapping_decry_expiration_date_list = mapping_decry_expiration.split('-')            # mapping_decry_expiration을 -로 나눠 연,월,일로 나눔.
                mapping_decry_expiration_year = int(mapping_decry_expiration_date_list[0])          # 연 정보가 입력된 str 데이터를 int로 변형.
                mapping_decry_expiration_monce = int(mapping_decry_expiration_date_list[1])         # 월 정보가 입력된 str 데이터를 int로 변형.
                mapping_decry_expiration_day = int(mapping_decry_expiration_date_list[2])         # 일 정보가 입력된 str 데이터를 int로 변형.
                mapping_decry_expiration_dt = dt.datetime(mapping_decry_expiration_year,mapping_decry_expiration_monce,mapping_decry_expiration_day)    # 날짜 계산을 위해 연,월,일 정보를 합하여 datetime 데이터로 변형함.

                mapping_decry_service_period = mapping_decry_expiration_dt - today             # [만기일 - 현재일 = 서비스 기간] 식을 만들어 줌.
                mapping_decry_service_period_days = str(int(mapping_decry_service_period.days)+1)

                if mapping_decry_tmg == 'open' :
                    self.mapping_decry_tmg_edit.setEnabled(True)
                    self.mapping_decry_tmg_status_2.setText('ALL')
                elif mapping_decry_tmg != 'open' :
                    self.mapping_decry_tmg_edit.setEnabled(False)
                    self.mapping_decry_tmg_edit.setText(mapping_decry_tmg)
                    self.mapping_decry_tmg_status_2.setText(mapping_decry_tmg)

                self.mapping_decry_expiration_status.setText(mapping_decry_expiration)
                self.mapping_decry_expiration_status_2.setText(mapping_decry_expiration)
                self.mapping_decry_service_period_status.setText(f'{mapping_decry_service_period_days}일')    # label에 서비스 기간 출력.
                self.mapping_decry_service_period_status_2.setText(f'{mapping_decry_service_period_days}일')

                # 복호화 성공 후 서비스 기한이 양수인 경우 True 반환``
                if int(mapping_decry_service_period_days) >= 0 :
                    self.tabWidget.setTabEnabled(1,True)
                # 복호화 성공 후 서비스 기한이 음수인 경우 종료일을 보여주기 위해 종료 기한 날짜 반환.
                elif int(mapping_decry_service_period_days) < 0 :
                    self.tabWidget.setTabEnabled(1,False)
                    self.mapping_decry_service_period_status_2.setText('사용기한 초과')


            if alignmenter_available_status == 'DISABLE' :
                self.alignmenter_decry_tmg_status_2.setText('사용불가')
                self.alignmenter_decry_expiration_status_2.setText('사용불가')
                self.alignmenter_decry_service_period_status_2.setText('사용불가')
                self.tabWidget.setTabEnabled(2,False)
            elif alignmenter_available_status != 'DISABLE' :
                alignmenter_decry_tmg = alignmenter_available_status.split(',')[0]
                alignmenter_decry_expiration = alignmenter_available_status.split(',')[1]
                alignmenter_decry_expiration_date_list = alignmenter_decry_expiration.split('-')            # mapping_decry_expiration을 -로 나눠 연,월,일로 나눔.
                alignmenter_decry_expiration_year = int(alignmenter_decry_expiration_date_list[0])          # 연 정보가 입력된 str 데이터를 int로 변형.
                alignmenter_decry_expiration_monce = int(alignmenter_decry_expiration_date_list[1])         # 월 정보가 입력된 str 데이터를 int로 변형.
                alignmenter_decry_expiration_day = int(alignmenter_decry_expiration_date_list[2])         # 일 정보가 입력된 str 데이터를 int로 변형.
                alignmenter_decry_expiration_dt = dt.datetime(alignmenter_decry_expiration_year,alignmenter_decry_expiration_monce,alignmenter_decry_expiration_day)    # 날짜 계산을 위해 연,월,일 정보를 합하여 datetime 데이터로 변형함.

                alignmenter_decry_service_period = alignmenter_decry_expiration_dt - today             # [만기일 - 현재일 = 서비스 기간] 식을 만들어 줌.
                alignmenter_decry_service_period_days = str(int(alignmenter_decry_service_period.days)+1)

                if alignmenter_decry_tmg == 'open' :
                    self.alignmenter_decry_tmg_edit.setEnabled(True)
                    self.alignmenter_decry_tmg_status_2.setText('ALL')
                elif alignmenter_decry_tmg != 'open' :
                    self.alignmenter_decry_tmg_edit.setEnabled(False)
                    self.alignmenter_decry_tmg_edit.setText(alignmenter_decry_tmg)
                    self.alignmenter_decry_tmg_status_2.setText(alignmenter_decry_tmg)

                self.alignmenter_decry_expiration_status.setText(alignmenter_decry_expiration)
                self.alignmenter_decry_expiration_status_2.setText(alignmenter_decry_expiration)
                self.alignmenter_decry_service_period_status.setText(f'{alignmenter_decry_service_period_days}일')    # label에 서비스 기간 출력.
                self.alignmenter_decry_service_period_status_2.setText(f'{alignmenter_decry_service_period_days}일')

                # 복호화 성공 후 서비스 기한이 양수인 경우 True 반환
                if int(alignmenter_decry_service_period_days) >= 0 :
                    self.tabWidget.setTabEnabled(2,True)
                # 복호화 성공 후 서비스 기한이 음수인 경우 종료일을 보여주기 위해 종료 기한 날짜 반환.
                elif int(alignmenter_decry_service_period_days) < 0 :
                    self.tabWidget.setTabEnabled(2,False)
                    self.alignmenter_decry_service_period_status_2.setText('사용기한 초과')


            if period_VPN_available_status == 'DISABLE' :
                self.period_VPN_decry_mac_status_2.setText('사용불가')
                self.this_mac_status.setText(getmac.get_mac_address())
                self.period_VPN_decry_expiration_status_2.setText('사용불가')
                self.period_VPN_decry_service_period_status_2.setText('사용불가')
                self.tabWidget.setTabEnabled(3,False)
            elif period_VPN_available_status != 'DISABLE' :
                period_VPN_decry_mac = period_VPN_available_status.split(',')[0]
                period_VPN_decry_expiration = period_VPN_available_status.split(',')[1]
                period_VPN_decry_expiration_date_list = period_VPN_decry_expiration.split('-')            # mapping_decry_expiration을 -로 나눠 연,월,일로 나눔.
                period_VPN_decry_expiration_year = int(period_VPN_decry_expiration_date_list[0])          # 연 정보가 입력된 str 데이터를 int로 변형.
                period_VPN_decry_expiration_monce = int(period_VPN_decry_expiration_date_list[1])         # 월 정보가 입력된 str 데이터를 int로 변형.
                period_VPN_decry_expiration_day = int(period_VPN_decry_expiration_date_list[2])         # 일 정보가 입력된 str 데이터를 int로 변형.
                period_VPN_decry_expiration_dt = dt.datetime(period_VPN_decry_expiration_year,period_VPN_decry_expiration_monce,period_VPN_decry_expiration_day)    # 날짜 계산을 위해 연,월,일 정보를 합하여 datetime 데이터로 변형함.

                period_VPN_decry_service_period = period_VPN_decry_expiration_dt - today             # [만기일 - 현재일 = 서비스 기간] 식을 만들어 줌.
                period_VPN_decry_service_period_days = str(int(period_VPN_decry_service_period.days)+1)

                if period_VPN_decry_mac == 'open' :
                    self.period_VPN_decry_mac_status_2.setText('ALL')
                elif period_VPN_decry_mac != 'open' :
                    self.period_VPN_decry_mac_status_2.setText(period_VPN_decry_mac)
                self.this_mac_status.setText(getmac.get_mac_address())
                self.period_VPN_decry_expiration_status.setText(period_VPN_decry_expiration)
                self.period_VPN_decry_expiration_status_2.setText(period_VPN_decry_expiration)
                self.period_VPN_decry_service_period_status.setText(f'{period_VPN_decry_service_period_days}일')    # label에 서비스 기간 출력.
                self.period_VPN_decry_service_period_status_2.setText(f'{period_VPN_decry_service_period_days}일')

                if period_VPN_decry_mac != 'open' :
                    # 복호화 성공 후 서비스 기한이 양수인 경우 True 반환
                    if int(period_VPN_decry_service_period_days) >= 0 and period_VPN_decry_mac == getmac.get_mac_address():
                        self.tabWidget.setTabEnabled(3,True)
                    # 복호화 성공 후 서비스 기한이 음수인 경우 종료일을 보여주기 위해 종료 기한 날짜 반환.
                    elif int(period_VPN_decry_service_period_days) < 0 :
                        self.tabWidget.setTabEnabled(3,False)
                        self.period_VPN_decry_service_period_status_2.setText('사용기한 초과')

                    elif period_VPN_decry_mac != getmac.get_mac_address():
                        self.tabWidget.setTabEnabled(3,False)
                        self.period_VPN_decry_service_period_status_2.setText('허용되지 않은 맥주소')

                elif period_VPN_decry_mac == 'open' :
                    if int(period_VPN_decry_service_period_days) >= 0 :
                        self.tabWidget.setTabEnabled(3,True)
                    # 복호화 성공 후 서비스 기한이 음수인 경우 종료일을 보여주기 위해 종료 기한 날짜 반환.
                    elif int(period_VPN_decry_service_period_days) < 0 :
                        self.tabWidget.setTabEnabled(3,False)
                        self.period_VPN_decry_service_period_status_2.setText('사용기한 초과')

        # 복호화 실패 시 오류가 뜰 때 실행
        except :
            self.license_status.setText('허가되지않은 라이센스입니다.')

            self.mapping_decry_tmg_status_2.setText('사용불가')
            self.mapping_decry_expiration_status_2.setText('사용불가')
            self.mapping_decry_service_period_status_2.setText('사용불가')
            self.tabWidget.setTabEnabled(1,False)

            self.alignmenter_decry_tmg_status_2.setText('사용불가')
            self.alignmenter_decry_expiration_status_2.setText('사용불가')
            self.alignmenter_decry_service_period_status_2.setText('사용불가')
            self.tabWidget.setTabEnabled(2,False)

            self.period_VPN_decry_mac_status_2.setText('사용불가')
            self.this_mac_status.setText(getmac.get_mac_address())
            self.period_VPN_decry_expiration_status_2.setText('사용불가')
            self.period_VPN_decry_service_period_status_2.setText('사용불가')
            self.tabWidget.setTabEnabled(3,False)

    # 크롬 파일 찾기 함수
    def search_chrome(self)  :
        self.chrome_fname = filedialog.askopenfilename(initialdir="/", title = "크롬 베타버전 exe파일을 선택 해 주세요", filetypes = (("exe file","*.exe"),("all file","*.*")))
        self.chrome_path_textBrowser.setText(self.chrome_fname)

    # ExpressVPN 파일 찾기 함수
    def search_ExpressVPN(self) :
        self.ExpressVPN_fname = filedialog.askopenfilename(initialdir="/", title = "ExpressVPN.exe파일을 선택해 주세요", filetypes = (("exe file","*.exe"),("all file","*.*")))
        self.ExpressVPN_path_textBrowser.setText(self.ExpressVPN_fname)

    # 파일 위치 정보 저장 함수
    def file_path_info_save(self) :
        with open(f'chrome_path_info.txt', mode='w') as file :            # txt 파일 쓰기오기
            file.write(self.chrome_fname +'\n' + self.ExpressVPN_fname)
        self.alignmenter_status_label_2.setText('크롬 위치 정보입력이 완료되었습니다.')
        QApplication.processEvents()

    # 파일 위치 정보 읽기 함수
    def file_path_info_read(self) :
        file_path_info_file_existence = os.path.isfile(f'chrome_path_info.txt')      # 라이센스 파일 존재 유무 확인.    존재할 경우 True, 비존재할경우 False 반환.
        if file_path_info_file_existence == True :                              # 라이센스 파일이 존재할 경우 실행.
            with open(f'chrome_path_info.txt', mode='r') as file :            # txt 파일 쓰기오기
                self.chrome_fname = file.readline().replace('\n','')            # 한칸 띄움이 있어서 크롬이 안불러와져서 한칸띄움표시 제거.
                self.ExpressVPN_fname = file.readline()
                self.chrome_path_textBrowser.setText(self.chrome_fname)
                self.ExpressVPN_path_textBrowser.setText(self.ExpressVPN_fname)
        elif file_path_info_file_existence == False :                                       # 라이센스 파일이 존재하지 않을 경우 실행.
            return 0

    # 스마트스토어 구매 링크
    def smartstore(self) :
        webbrowser.open('https://smartstore.naver.com/ctmall_')
        return

    # 더망고 사용법 블로그 링크
    def mango_supporter_manual_blog(self) :
        webbrowser.open('https://blog.naver.com/awldnjs2')
        return

QApplication.setStyle("fusion")
app = QApplication(sys.argv)
main_dialog = MainDialog()
main_dialog.show()
sys.exit(app.exec_())


# pyinstaller --onefile --windowed PERIOD_EXPRESS_VPN.py
# Pyinstaller와 Python 3.9와 Opencv 3개 사이에 복잡하게 엮인 충돌로 작동이 안되는것 확인했습니다
# 모든 방법 다 실행해보다가 밑에 opencv 버전 다운그레이드 후 pyinstall 진행해서 성공했습니다 (조금 허무하네요..)
# pip uninstall opencv-python
# pip install opencv-python==4.5.3.56