__author__ = "Jonathan Braun"
__version__ = "1.0"
__maintainer__ = "Jonathan Braun"
__email__ = "jonathan.braun@eduvaud.ch"
__status__ = "Prototype"
__date__ = "February 2023"

#-----------------------------------------------------
# Importing libraries and modules
#-----------------------------------------------------
import datetime                                                             # Library for date and time related stuff
import math                                                                 # Library for math stuff
import csv                                                                  # Library for csv handling stuff
import smtplib

from sensirion_i2c_driver import I2cConnection                              # Sensor driver
from sensirion_i2c_sht.sht4x import Sht4xI2cDevice                          # Sensor driver
from sensirion_i2c_driver.linux_i2c_transceiver import LinuxI2cTransceiver  # Sensor driver

#-----------------------------------------------------
# Declaring the sensor object
#-----------------------------------------------------
sht40 = Sht4xI2cDevice(I2cConnection(LinuxI2cTransceiver('/dev/i2c-2')))

#-----------------------------------------------------
# Declaring functions
#-----------------------------------------------------
def read_sensor():
    try:
        t, rh = sht40.single_shot_measurement()
        # Watch out! t and rh are variable that contain not only the values but also the units.
        # You can print the values with the units (print(t)) or you can also recover only the value
        # by specifying which one: t.degrees_celsius or rh.percent_rh
    except Exception as ex:
        print("Error while recovering sensor values:", ex)
        return None, None
    else:
        return t, rh

def calculate_dew_point(temp, humidity):
    beta = 17.62
    _lambda = 243.12
    const = math.log(humidity / 100) + ((beta * temp) / (_lambda + temp))
    dewpoint = (_lambda * const) / (beta - const)
    return dewpoint

def csv_write_row(filename, date, time, temp, humidity, dewpoint):
    data = [date, time, temp, humidity, dewpoint]
    try:
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)
    except Exception as ex:
        return 0, ex
    else:
        return 1

def send_email(receiver, subject, message):
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login("ETML.ES.EMSY@gmail.com", "cely neve caly akjz")
        sender = "ETML.ES.EMSY@gmail.com"

        headers = {
            'Content-Type': 'text/html; charset=utf-8',
            'Content-Disposition': 'inline',
            'Content-Transfer-Encoding': '8bit',
            'From': sender,
            'To': receiver,
            'Date': datetime.datetime.now().strftime('%a, %d %b %Y  %H:%M:%S %Z'),
            'X-Mailer': 'python',
            'Subject': subject
        }
        # create the message
        msg = ''
        for key, value in headers.items():
            msg += "%s: %s\n" % (key, value)

        # add contents
        msg += "\n%s\n" % (message)

        try:
            server.sendmail(headers['From'], headers['To'], msg.encode("utf8"))
            server.quit()
            print("Email sent successfully!")
        except Exception as ex:
            print("Something went wrong...", ex)

#-----------------------------------------------------
# Main script
#-----------------------------------------------------
if __name__ == "__main__":  # Runs only if called as a script but not if imported
    print("Hello and welcome to EMSY")

    temperature, humidity = read_sensor()
    if temperature is not None and humidity is not None:
        dewpoint = calculate_dew_point(temperature.degrees_celsius, humidity.percent_rh)

        now = datetime.datetime.now()
        date_str = now.strftime("%d.%m.%Y")
        time_str = now.strftime("%H:%M")

        temp = temperature.degrees_celsius
        humidity = humidity.percent_rh

        csv_write_row('/home/debian/TempLog.csv', date_str, time_str, temp, humidity, dewpoint)

        temp_limit = 28.0
        if temp > temp_limit:
            subject = "Attention, temperature excessive !"
            message = f"Bonjour, la temperature exterieure a depasse la limite de {temp_limit}°C."
            send_email("jeremie.jeanelie@eduvaud.ch", subject, message)
    else:
        print("Failed to read sensor data")