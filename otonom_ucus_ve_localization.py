from dronekit import connect, VehicleMode, LocationGlobalRelative
from collections.abc import MutableMapping
from gmplot import gmplot
import webbrowser
import time


def create_map_with_markers(coord1, coord2, apikey=None):
    gmap = gmplot.GoogleMapPlotter(0, 0, 2, apikey=apikey)
    gmap.marker(coord1[0], coord1[1], title='Fatih:)', color='orange')
    gmap.marker(coord2[0], coord2[1], title='İrfan:)', color='blue')
    gmap.draw("ATA-UAV.html")
    webbrowser.open("ATA-UAV.html")

def autonomous_flight_with_markers(coord1, coord2, connection_string, target_altitude, apikey=None):
    iha = connect(connection_string, wait_ready=True, timeout=100)

    # Google Maps üzerinde işaretlenen yerleri göster
    create_map_with_markers(coord1, coord2, apikey=apikey)

    i = 5
    while i > 0:
        print("Uçuş başlıyor:", i)
        i = i - 1
        time.sleep(1)

    # Arm ve yükselme fonksiyonları buraya eklenir
    while iha.is_armable == False:
        print("Arm için gerekli şartlar sağlanamadı.")
        time.sleep(1)
    print("İHA şu anda arm edilebilir.")

    iha.mode = VehicleMode("GUIDED")
    while iha.mode == 'GUIDED':
        print('Guided moduna geçiş yapılıyor')
        time.sleep(1.5)

    print("Guided moduna geçiş yapıldı")
    iha.armed = True
    while iha.armed is False:
        print("Arm için bekleniyor")
        time.sleep(1)

    print("Drone Armed")
    print("Drone Take OFF")

    iha.simple_takeoff(target_altitude)
    while iha.location.global_relative_frame.alt <= target_altitude * 0.94:
        print("Şu anki yükseklik{}".format(iha.location.global_relative_frame.alt))
        time.sleep(0.5)
    print("Takeoff gerçekleşti")

    # Belirli koordinatlara hareket etme kodları buraya eklenir
    print("10 Saniye Sonra 1. Koordinata Hareket Edecek ...")
    point1 = LocationGlobalRelative(coord1[0], coord1[1], target_altitude)
    iha.simple_goto(point1, airspeed=1)
    time.sleep(30)

    print("30 Saniye içinde Nokta 2'ye Hareket Edecek...")
    point2 = LocationGlobalRelative(coord2[0], coord2[1], target_altitude)
    iha.simple_goto(point2, airspeed=1)
    time.sleep(30)

    # Diğer hareket noktalarını ve kodlarını buraya ekleyebilirsiniz.

    print("Airspeed 1'e sabitlendi")
    iha.airspeed = 1

    # İniş kodları buraya eklenir
    print("30 Saniye içinde İniş Yapacak ")
    iha.mode = VehicleMode("LAND")
    time.sleep(30)

    print("Drone İniş Yapıyor")
    print("Drone Disarmed")
    iha.close()

if __name__ == "__main__":
    coordinate1 = (-35.36311264, 149.16516789)  # Örnek koordinatlar (New York)
    coordinate2 = (-35.36308038, 149.16527996)  # Örnek koordinatlar (Los Angeles)
    connection_str = "192.168.48.81:14550"
    target_altitude = 5
    google_maps_api_key = "AIzaSyBv1Mz-hd6Fo1V9OJBv-YDFuiU1ayoKZrg"

    autonomous_flight_with_markers(coordinate1, coordinate2, connection_str, target_altitude, apikey=google_maps_api_key)
