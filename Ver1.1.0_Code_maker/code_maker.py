from cryptography.fernet import Fernet
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QDate
import datetime as dt
import sys
import os
from posixpath import split

# MS)820,20220409/ALIGN)820,20220409/VPN)12:12:12:12:12:12
# MS)DISABLE/ALIGN)DISABLE/VPN)DISABLE

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UI_PATH = "code_maker.ui"

class MainDialog(QDialog) :
    def __init__(self) :
        QDialog.__init__(self, None)
        uic.loadUi(os.path.join(BASE_DIR, UI_PATH), self)
        
        # 클래스 속성
        ## 대칭키
        self.key_code = "0rKTqtZ4GQJlecUE8zRfU1B-metwX61_2Iz6B66B5eo="
        self.key_code = self.key_code.encode('utf-8')
        self.fernet = Fernet(self.key_code)
        ## 오늘 날짜 
        self.today = dt.datetime.today()
        ## 종료 날짜
        self.mapping_encry_expiration_dateEdit.setDate(QDate(self.today))
        self.alignmenter_encry_expiration_dateEdit.setDate(QDate(self.today))
        self.period_VPN_encry_expiration_dateEdit.setDate(QDate(self.today))
        # 라디오 버튼 체크
        self.mapping_disable_radioButton.setChecked(True)
        self.alignmenter_disable_radioButton.setChecked(True)
        self.period_VPN_disable_radioButton.setChecked(True)
        # 비활성화
        self.mapping_encry_tmg_line_edit.setEnabled(False)
        self.mapping_encry_expiration_dateEdit.setEnabled(False)
        self.alignmenter_encry_tmg_line_edit.setEnabled(False)
        self.alignmenter_encry_expiration_dateEdit.setEnabled(False)
        self.period_VPN_encry_expiration_dateEdit.setEnabled(False)
        self.period_VPN_mac_address_line_edit.setEnabled(False)

        # 동적 매서드
        self.encry_btn.clicked.connect(self.encryptography)                 # 암호화 시작 버튼(암호화 함수 실행)
        self.decry_btn.clicked.connect(self.decryptography)                 # 복호화 시작 버튼(복호화 함수 실행)
        self.mapping_able_radioButton.toggled.connect(self.able)            # 매핑서포터 라디오 버튼(활성화 함수 실행)
        self.mapping_openable_radioButton.toggled.connect(self.able)            # 매핑서포터 라디오 버튼(활성화 함수 실행)
        self.mapping_disable_radioButton.toggled.connect(self.able)            # 매핑서포터 라디오 버튼(활성화 함수 실행)
        self.alignmenter_able_radioButton.toggled.connect(self.able)        # 자동 창 정렬 라디오 버튼(활성화 함수 실행)
        self.alignmenter_openable_radioButton.toggled.connect(self.able)        # 자동 창 정렬 라디오 버튼(활성화 함수 실행)
        self.alignmenter_disable_radioButton.toggled.connect(self.able)        # 자동 창 정렬 라디오 버튼(활성화 함수 실행)
        self.period_VPN_able_radioButton.toggled.connect(self.able)         # 자동 VPN ON/OFF 라디오 버튼(활성화 함수 실행)
        self.period_VPN_openable_radioButton.toggled.connect(self.able)         # 자동 VPN ON/OFF 라디오 버튼(활성화 함수 실행)
        self.period_VPN_disable_radioButton.toggled.connect(self.able)         # 자동 VPN ON/OFF 라디오 버튼(활성화 함수 실행)

        self.mapping_encry_expiration_dateEdit.dateChanged.connect(self.service_period_calculator)  # 날짜 상하 조절버튼(암호화기 그룹박스 서비스기간 출력 함수 실행)
        self.alignmenter_encry_expiration_dateEdit.dateChanged.connect(self.service_period_calculator)  # 날짜 상하 조절버튼(암호화기 그룹박스 서비스기간 출력 함수 실행)
        self.period_VPN_encry_expiration_dateEdit.dateChanged.connect(self.service_period_calculator)  # 날짜 상하 조절버튼(암호화기 그룹박스 서비스기간 출력 함수 실행)

    # 활성화 함수
    def able(self) :
        if self.mapping_able_radioButton.isChecked() == True :
            self.mapping_encry_tmg_line_edit.setEnabled(True)
            self.mapping_encry_expiration_dateEdit.setEnabled(True)

        elif self.mapping_openable_radioButton.isChecked() == True :
            self.mapping_encry_tmg_line_edit.setText('open')
            self.mapping_encry_tmg_line_edit.setEnabled(False)
            self.mapping_encry_expiration_dateEdit.setEnabled(True)

        elif self.mapping_disable_radioButton.isChecked() == True :
            self.mapping_encry_tmg_line_edit.setEnabled(False)
            self.mapping_encry_expiration_dateEdit.setEnabled(False)





        if self.alignmenter_able_radioButton.isChecked() == True :
            self.alignmenter_encry_tmg_line_edit.setEnabled(True)
            self.alignmenter_encry_expiration_dateEdit.setEnabled(True)

        elif self.alignmenter_openable_radioButton.isChecked() == True :
            self.alignmenter_encry_tmg_line_edit.setText('open')
            self.alignmenter_encry_tmg_line_edit.setEnabled(False)
            self.alignmenter_encry_expiration_dateEdit.setEnabled(True)

        elif self.alignmenter_disable_radioButton.isChecked() == True :
            self.alignmenter_encry_tmg_line_edit.setEnabled(False)
            self.alignmenter_encry_expiration_dateEdit.setEnabled(False)




        if self.period_VPN_able_radioButton.isChecked() == True :
            self.period_VPN_mac_address_line_edit.setEnabled(True)
            self.period_VPN_encry_expiration_dateEdit.setEnabled(True)

        if self.period_VPN_openable_radioButton.isChecked() == True :
            self.period_VPN_mac_address_line_edit.setText('open')
            self.period_VPN_mac_address_line_edit.setEnabled(False)
            self.period_VPN_encry_expiration_dateEdit.setEnabled(True)

        elif self.period_VPN_disable_radioButton.isChecked() == True :
            self.period_VPN_mac_address_line_edit.setEnabled(False)
            self.period_VPN_encry_expiration_dateEdit.setEnabled(False)

    # 암호화 함수
    def encryptography(self) :
        self.service_period_calculator()                                    # 암호화기 그룹박스 서비스기간 출력 함수 실행.

        # 매핑서포터 암호화할 텍스트 만들기
        if self.mapping_able_radioButton.isChecked() == True :
            mapping_encry_tmg = str(self.mapping_encry_tmg_line_edit.text())            # int로 되어있는 TMG번호를 line_edit에서 str로 변환하여 tmg 번호를 가져옴.
            if mapping_encry_tmg == "" :
                self.encry_license_text_line_edit.setText('tmg 번호를 입력하여 주세요.')
                self.encry_text_status.setText('tmg 번호를 입력하여 주세요.')
                return 0
                
            mapping_encry_expiration = str(self.mapping_encry_expiration_dateEdit.text())       # 종료날짜 date_edit로 부터 str로 변환하여 종료날짜를 가져옴.
            mapping_encry_text = f'MS){mapping_encry_tmg},{mapping_encry_expiration}'

        elif self.mapping_openable_radioButton.isChecked() == True :
            mapping_encry_tmg = 'open'
            mapping_encry_expiration = str(self.mapping_encry_expiration_dateEdit.text())       # 종료날짜 date_edit로 부터 str로 변환하여 종료날짜를 가져옴.
            mapping_encry_text = f'MS){mapping_encry_tmg},{mapping_encry_expiration}'

        elif self.mapping_disable_radioButton.isChecked() == True :
            mapping_encry_text = "MS)DISABLE"

        # 자동 창 정렬 암호화할 텍스트 만들기
        if self.alignmenter_able_radioButton.isChecked() == True :
            alignmenter_encry_tmg = str(self.alignmenter_encry_tmg_line_edit.text())            # int로 되어있는 TMG번호를 line_edit에서 str로 변환하여 tmg 번호를 가져옴.
            if alignmenter_encry_tmg == "" :
                self.encry_license_text_line_edit.setText('tmg 번호를 입력하여 주세요.')
                self.encry_text_status.setText('tmg 번호를 입력하여 주세요.')
                return 0
            alignmenter_encry_expiration = str(self.alignmenter_encry_expiration_dateEdit.text())       # 종료날짜 date_edit로 부터 str로 변환하여 종료날짜를 가져옴.
            alignmenter_encry_text = f'ALIGN){alignmenter_encry_tmg},{alignmenter_encry_expiration}'

        elif self.alignmenter_openable_radioButton.isChecked() == True :
            alignmenter_encry_tmg = 'open'
            alignmenter_encry_expiration = str(self.alignmenter_encry_expiration_dateEdit.text())       # 종료날짜 date_edit로 부터 str로 변환하여 종료날짜를 가져옴.
            alignmenter_encry_text = f'ALIGN){alignmenter_encry_tmg},{alignmenter_encry_expiration}'

        elif self.alignmenter_disable_radioButton.isChecked() == True :
            alignmenter_encry_text = "ALIGN)DISABLE"

        # 자동 창 정렬 암호화할 텍스트 만들기
        if self.period_VPN_able_radioButton.isChecked() == True :
            period_VPN_mac_address = str(self.period_VPN_mac_address_line_edit.text())            # int로 되어있는 TMG번호를 line_edit에서 str로 변환하여 tmg 번호를 가져옴.
            if period_VPN_mac_address == "" :
                self.encry_license_text_line_edit.setText('mac 주소를 입력해 주세요.')
                self.encry_text_status.setText('mac 주소를 입력해 주세요.')
                return 0
            period_VPN_encry_expiration = str(self.period_VPN_encry_expiration_dateEdit.text())       # 종료날짜 date_edit로 부터 str로 변환하여 종료날짜를 가져옴.
            period_VPN_encry_text = f'VPN){period_VPN_mac_address},{period_VPN_encry_expiration}'

        elif self.period_VPN_openable_radioButton.isChecked() == True :
            period_VPN_mac_address = 'open'
            period_VPN_encry_expiration = str(self.period_VPN_encry_expiration_dateEdit.text())       # 종료날짜 date_edit로 부터 str로 변환하여 종료날짜를 가져옴.
            period_VPN_encry_text = f'VPN){period_VPN_mac_address},{period_VPN_encry_expiration}'

        elif self.period_VPN_disable_radioButton.isChecked() == True :
            period_VPN_encry_text = "VPN)DISABLE"


        # 암호화 텍스트 만들기 및 암호화 진행
        encry_text = f'{mapping_encry_text}/{alignmenter_encry_text}/{period_VPN_encry_text}'                      # TMG번호와 종료날짜를 조합하여 암호화 할 문자열 생성. string 형태
        self.encry_text_status.setText(encry_text)                          # 암호화할 문자열을 label에 출력. 

        license = self.fernet.encrypt(encry_text.encode('utf-8'))           # str로 되어있는 암호화할 문자열을 인코딩하여 binary형태로 만든 후 암호화하고 license에 저장
        license = license.decode('utf-8')                                   # binary 형태로 저장되어있는 license를 디코딩하여 str 형태로 변형.

        self.encry_license_text_line_edit.setText(license)                  # license를 line_edit에 출력.

    # 복호화 함수
    def decryptography(self) :                                              
        license = self.decry_license_text_line_edit.text()                  # line_edit에서 추출한 텍스트를 licence변수에 입력.
        if license == "" :
            self.decry_text_status.setText('라이센스키를 입력해주세요.')
            return 0

        try :
            decry_text = self.fernet.decrypt(license.encode('utf-8'))           # license를 인코딩하여 바이너리형태로 만들고, 복호화 하여 decry_text에 저장
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
                self.mapping_decry_tmg_status.setText('D/A')
                self.mapping_decry_expiration_status.setText('D/A')
                self.mapping_decry_service_period_status.setText('D/A')
            elif mapping_available_status != 'DISABLE' :
                mapping_decry_tmg = mapping_available_status.split(',')[0]
                mapping_decry_expiration = mapping_available_status.split(',')[1]
                mapping_decry_expiration_date_list = mapping_decry_expiration.split('-')            # mapping_decry_expiration을 -로 나눠 연,월,일로 나눔.
                mapping_decry_expiration_year = int(mapping_decry_expiration_date_list[0])          # 연 정보가 입력된 str 데이터를 int로 변형.
                mapping_decry_expiration_monce = int(mapping_decry_expiration_date_list[1])         # 월 정보가 입력된 str 데이터를 int로 변형.
                mapping_decry_expiration_day = int(mapping_decry_expiration_date_list[2])         # 일 정보가 입력된 str 데이터를 int로 변형.
                mapping_decry_expiration_dt = dt.datetime(mapping_decry_expiration_year,mapping_decry_expiration_monce,mapping_decry_expiration_day)    # 날짜 계산을 위해 연,월,일 정보를 합하여 datetime 데이터로 변형함.

                mapping_decry_service_period = mapping_decry_expiration_dt - self.today             # [만기일 - 현재일 = 서비스 기간] 식을 만들어 줌.

                self.mapping_decry_tmg_status.setText(mapping_decry_tmg)
                self.mapping_decry_expiration_status.setText(mapping_decry_expiration)
                self.mapping_decry_service_period_status.setText(str(int(mapping_decry_service_period.days)+1))    # label에 서비스 기간 출력.

            if alignmenter_available_status == 'DISABLE' :
                self.alignmenter_decry_tmg_status.setText('D/A')
                self.alignmenter_decry_expiration_status.setText('D/A')
                self.alignmenter_decry_service_period_status.setText('D/A')
            elif alignmenter_available_status != 'DISABLE' :
                alignmenter_decry_tmg = alignmenter_available_status.split(',')[0]
                alignmenter_decry_expiration = alignmenter_available_status.split(',')[1]
                alignmenter_decry_expiration_date_list = alignmenter_decry_expiration.split('-')            # mapping_decry_expiration을 -로 나눠 연,월,일로 나눔.
                alignmenter_decry_expiration_year = int(alignmenter_decry_expiration_date_list[0])          # 연 정보가 입력된 str 데이터를 int로 변형.
                alignmenter_decry_expiration_monce = int(alignmenter_decry_expiration_date_list[1])         # 월 정보가 입력된 str 데이터를 int로 변형.
                alignmenter_decry_expiration_day = int(alignmenter_decry_expiration_date_list[2])         # 일 정보가 입력된 str 데이터를 int로 변형.
                alignmenter_decry_expiration_dt = dt.datetime(alignmenter_decry_expiration_year,alignmenter_decry_expiration_monce,alignmenter_decry_expiration_day)    # 날짜 계산을 위해 연,월,일 정보를 합하여 datetime 데이터로 변형함.

                alignmenter_decry_service_period = alignmenter_decry_expiration_dt - self.today             # [만기일 - 현재일 = 서비스 기간] 식을 만들어 줌.

                self.alignmenter_decry_tmg_status.setText(alignmenter_decry_tmg)
                self.alignmenter_decry_expiration_status.setText(alignmenter_decry_expiration)
                self.alignmenter_decry_service_period_status.setText(str(int(alignmenter_decry_service_period.days)+1))    # label에 서비스 기간 출력.

            if period_VPN_available_status == 'DISABLE' :
                self.period_VPN_decry_mac_status.setText('D/A')
                self.period_VPN_decry_expiration_status.setText('D/A')
                self.period_VPN_decry_service_period_status.setText('D/A')
            elif period_VPN_available_status != 'DISABLE' :
                period_VPN_decry_mac = period_VPN_available_status.split(',')[0]
                period_VPN_decry_expiration = period_VPN_available_status.split(',')[1]
                period_VPN_decry_expiration_date_list = period_VPN_decry_expiration.split('-')            # mapping_decry_expiration을 -로 나눠 연,월,일로 나눔.
                period_VPN_decry_expiration_year = int(period_VPN_decry_expiration_date_list[0])          # 연 정보가 입력된 str 데이터를 int로 변형.
                period_VPN_decry_expiration_monce = int(period_VPN_decry_expiration_date_list[1])         # 월 정보가 입력된 str 데이터를 int로 변형.
                period_VPN_decry_expiration_day = int(period_VPN_decry_expiration_date_list[2])         # 일 정보가 입력된 str 데이터를 int로 변형.
                period_VPN_decry_expiration_dt = dt.datetime(period_VPN_decry_expiration_year,period_VPN_decry_expiration_monce,period_VPN_decry_expiration_day)    # 날짜 계산을 위해 연,월,일 정보를 합하여 datetime 데이터로 변형함.

                period_VPN_decry_service_period = period_VPN_decry_expiration_dt - self.today             # [만기일 - 현재일 = 서비스 기간] 식을 만들어 줌.

                self.period_VPN_decry_mac_status.setText(period_VPN_decry_mac)
                self.period_VPN_decry_expiration_status.setText(period_VPN_decry_expiration)
                self.period_VPN_decry_service_period_status.setText(str(int(period_VPN_decry_service_period.days)+1))    # label에 서비스 기간 출력.

            self.decry_text_status.setText(decry_text)                          # label에 복호화된 문자열 출력.

        except :
            self.decry_text_status.setText('복호화에 실패하였습니다.')

    # 암호화기 그룹박스 서비스기간 출력 함수
    def service_period_calculator(self) :
        mapping_encry_expiration_date = self.mapping_encry_expiration_dateEdit.text()   # 암호화기 종료날짜에서 날짜 데이터를 가져옴
        alignmenter_encry_expiration_date = self.alignmenter_encry_expiration_dateEdit.text()
        period_VPN_encry_expiration_date = self.period_VPN_encry_expiration_dateEdit.text()

        mapping_encry_expiration_date_list = mapping_encry_expiration_date.split('-')   # 날짜 데이터를 '-'로 나눠서 연,월,일 데이터를 리스트로 분리
        alignmenter_encry_expiration_date_list = alignmenter_encry_expiration_date.split('-')
        period_VPN_encry_expiration_date_list = period_VPN_encry_expiration_date.split('-')

        mapping_encry_expiration_year = int(mapping_encry_expiration_date_list[0])      # 연 정보가 입력된 str 데이터를 int로 변형
        alignmenter_encry_expiration_year = int(alignmenter_encry_expiration_date_list[0])
        period_VPN_encry_expiration_year = int(period_VPN_encry_expiration_date_list[0])

        mapping_encry_expiration_monce = int(mapping_encry_expiration_date_list[1])     # 월 정보가 입력된 str 데이터를 int로 변헝
        alignmenter_encry_expiration_monce = int(alignmenter_encry_expiration_date_list[1])
        period_VPN_encry_expiration_monce = int(period_VPN_encry_expiration_date_list[1])

        mapping_encry_expiration_day = int(mapping_encry_expiration_date_list[2])     # 일 정보가 입력된 str 데이터를 int로 변형
        alignmenter_encry_expiration_day = int(alignmenter_encry_expiration_date_list[2])
        period_VPN_encry_expiration_day = int(period_VPN_encry_expiration_date_list[2])

        mapping_encry_expiration = dt.datetime(mapping_encry_expiration_year,mapping_encry_expiration_monce,mapping_encry_expiration_day)       # 날짜 계산을 위해 연,월,일 정보를 합하여 datetime 데이터로 변형함.
        alignmenter_encry_expiration = dt.datetime(alignmenter_encry_expiration_year,alignmenter_encry_expiration_monce,alignmenter_encry_expiration_day)
        period_VPN_encry_expiration = dt.datetime(period_VPN_encry_expiration_year,period_VPN_encry_expiration_monce,period_VPN_encry_expiration_day)

        mapping_encry_service_period = mapping_encry_expiration - self.today            # [만기일 - 현재일 = 서비스 기간] 식을 만들어 줌.
        alignmenter_encry_service_period = alignmenter_encry_expiration - self.today
        period_VPN_encry_service_period = period_VPN_encry_expiration - self.today

        self.mapping_encry_service_period_status.setText(str(int(mapping_encry_service_period.days)+1))    # 서비스 기간 데이터들 서비스기간 label에 출력
        self.alignmenter_encry_service_period_status.setText(str(int(alignmenter_encry_service_period.days)+1))
        self.period_VPN_encry_service_period_status.setText(str(int(period_VPN_encry_service_period.days)+1))

QApplication.setStyle("fusion")
app = QApplication(sys.argv)
main_dialog = MainDialog()
main_dialog.show()

sys.exit(app.exec_())