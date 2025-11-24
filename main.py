import sys
import webbrowser
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QMessageBox, QFrame)
from PyQt5.QtCore import Qt
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

class DistanceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        # Initialize Nominatim geocoder with a user_agent
        self.geolocator = Nominatim(user_agent="distance_app_v1")
        self.start_coords = None
        self.end_coords = None

    def initUI(self):
        self.setWindowTitle('OpenStreetMap 거리 계산기')
        self.setGeometry(300, 300, 500, 400)

        layout = QVBoxLayout()

        # Start Location Section
        start_layout = QHBoxLayout()
        self.start_input = QLineEdit()
        self.start_input.setPlaceholderText("출발지 입력 (예: 서울역)")
        self.start_search_btn = QPushButton("검색")
        self.start_search_btn.clicked.connect(lambda: self.search_location('start'))
        start_layout.addWidget(QLabel("출발지:"))
        start_layout.addWidget(self.start_input)
        start_layout.addWidget(self.start_search_btn)
        layout.addLayout(start_layout)
        
        self.start_label = QLabel("선택되지 않음")
        self.start_label.setStyleSheet("color: gray; font-size: 10pt;")
        layout.addWidget(self.start_label)

        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)

        # End Location Section
        end_layout = QHBoxLayout()
        self.end_input = QLineEdit()
        self.end_input.setPlaceholderText("도착지 입력 (예: 부산역)")
        self.end_search_btn = QPushButton("검색")
        self.end_search_btn.clicked.connect(lambda: self.search_location('end'))
        end_layout.addWidget(QLabel("도착지:"))
        end_layout.addWidget(self.end_input)
        end_layout.addWidget(self.end_search_btn)
        layout.addLayout(end_layout)

        self.end_label = QLabel("선택되지 않음")
        self.end_label.setStyleSheet("color: gray; font-size: 10pt;")
        layout.addWidget(self.end_label)

        # Calculate Button
        self.calc_btn = QPushButton("거리 계산")
        self.calc_btn.clicked.connect(self.calculate_distance)
        self.calc_btn.setStyleSheet("font-weight: bold; font-size: 12pt; margin-top: 20px;")
        layout.addWidget(self.calc_btn)

        # Result Section
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-size: 14pt; color: blue; margin-top: 10px;")
        layout.addWidget(self.result_label)

        # Map Link
        self.map_link = QLabel('<a href="#">지도에서 보기</a>')
        self.map_link.setAlignment(Qt.AlignCenter)
        self.map_link.setOpenExternalLinks(False)
        self.map_link.linkActivated.connect(self.open_map)
        self.map_link.hide() # Hide initially
        layout.addWidget(self.map_link)

        self.setLayout(layout)

    def search_location(self, loc_type):
        if loc_type == 'start':
            query = self.start_input.text()
        else:
            query = self.end_input.text()

        if not query:
            QMessageBox.warning(self, "입력 오류", "장소 이름을 입력해주세요.")
            return

        try:
            location = self.geolocator.geocode(query)
            if location:
                address = location.address
                coords = (location.latitude, location.longitude)
                
                if loc_type == 'start':
                    self.start_coords = coords
                    self.start_label.setText(f"찾음: {address}")
                    self.start_label.setStyleSheet("color: green; font-size: 10pt;")
                else:
                    self.end_coords = coords
                    self.end_label.setText(f"찾음: {address}")
                    self.end_label.setStyleSheet("color: green; font-size: 10pt;")
            else:
                QMessageBox.information(self, "찾을 수 없음", "위치를 찾을 수 없습니다. 다른 이름으로 시도해주세요.")
                if loc_type == 'start':
                    self.start_coords = None
                    self.start_label.setText("찾을 수 없음")
                    self.start_label.setStyleSheet("color: red; font-size: 10pt;")
                else:
                    self.end_coords = None
                    self.end_label.setText("찾을 수 없음")
                    self.end_label.setStyleSheet("color: red; font-size: 10pt;")
        except Exception as e:
            QMessageBox.critical(self, "오류", f"오류가 발생했습니다: {str(e)}")

    def calculate_distance(self):
        if self.start_coords and self.end_coords:
            dist = geodesic(self.start_coords, self.end_coords).kilometers
            self.result_label.setText(f"총 거리: {dist:.2f} km")
            self.map_link.show()
        else:
            QMessageBox.warning(self, "정보 부족", "출발지와 도착지를 모두 검색하고 선택해주세요.")

    def open_map(self):
        if self.start_coords and self.end_coords:
            # OSM routing URL format
            # https://www.openstreetmap.org/directions?engine=graphhopper_car&route={start_lat}%2C{start_lon}%3B{end_lat}%2C{end_lon}
            url = f"https://www.openstreetmap.org/directions?engine=graphhopper_car&route={self.start_coords[0]}%2C{self.start_coords[1]}%3B{self.end_coords[0]}%2C{self.end_coords[1]}"
            webbrowser.open(url)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DistanceApp()
    ex.show()
    sys.exit(app.exec_())
