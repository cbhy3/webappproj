import qrcode
from io import BytesIO
from Order import Order
import random
import shelve
import crcmod
import datetime
import qrcode
from PIL import Image



point_of_initiation = '12'
proxy_type = '0'
proxy_value = '+6598980039'
editable = '0'
amount = '0.01'
expiry = (datetime.datetime.now() + datetime.timedelta(minutes=10, seconds=30)).strftime('%Y%m%d')  # one day later, YYYMMDD
bill_number = '0'

'''
Function to translate QR information dictionary payload to string of characters 
Works for any layers of nested objects (for this case we only have one nested layer ID 26)
'''


def get_info_string(info):
    final_string = ''  # Empty string to store the generated output
    for key, value in info.items():  # Loop through the outer dictionary
        if type(value) == dict:  # If there is a nested dictionary
            temp_string_length, temp_string = get_info_string(
                value)  # call this function recusively to get the nested info
            # Adds the ID, length and value of the nested object
            final_string += key
            final_string += temp_string_length
            final_string += temp_string
        else:  # Normal value, adds the 3 fields: ID, length, value
            final_string += key
            final_string += str(len(value)).zfill(2)
            final_string += value
    return str(len(final_string)).zfill(2), final_string  # Returns the length of the current string and its value


def generatePayNowQR(amount, bill_number , point_of_initiation = point_of_initiation,
                     proxy_type = proxy_type,
                     proxy_value = proxy_value,
                     editable = editable,
                     expiry = expiry,

                     ):
    '''
    Nested dictionary that follows the structure of the data object
    dictionary key = data object id,
    dictionary value = data object value
    Application can also insert new key-value pairs corrosponding to its ID-value in whichever nested layer
    as long as the first and last root ID are 00 and 63 respectively. Order doesnt matter for the rest.
    '''
    info = {"00": "01",
            "01": str(point_of_initiation),
            "26": {"00": "SG.PAYNOW",
                   "01": str(proxy_type),
                   "02": str(proxy_value),
                   "03": str(editable),
                   "04": str(expiry)
                   },
            "52": "0000",
            "53": "702",
            "54": str(amount),
            "58": "SG",
            "59": "NA",
            "60": "Singapore",
            "62": {"01": str(bill_number)}
            }
    payload = get_info_string(info)[1]  # gets the final string, length is not needed
    payload += '6304'  # append ID 63 and length 4 (generated result will always be of length 4)
    crc_value = crc16_ccitt(payload)  # calculate CRC checksum
    crc_value = ('{:04X}'.format(crc_value))  # convert into 4 digit uppercase hex
    payload += crc_value  # add the CRC checksum result

    # Creating an instance of qrcode
    qr = qrcode.QRCode(
        version=1,  # the size of QR code matrix.
        box_size=5,  # how many pixels is each box of the QR code
        border=4,  # how thick is the border
        error_correction=qrcode.constants.ERROR_CORRECT_H, )  # able to damage/cover the QR Code up to a certain percentage. H - 30%
    qr.add_data(payload)
    qr.make(fit=True)  # QR code to fit the entire dimension even when the input data could fit into fewer boxes
    img = BytesIO()
    qr.make_image(fill_color=(144, 19, 123), back_color='white').save(img, format = "PNG")
    img.seek(0)
    return (img, bill_number)




def crc16_ccitt(data):
    crc = 0xFFFF  # initial value
    msb = crc >> 8
    lsb = crc & 255
    for c in data:
        x = ord(c) ^ msb
        x ^= (x >> 4)
        msb = (lsb ^ (x >> 3) ^ (x << 4)) & 255
        lsb = (x ^ (x << 5)) & 255
    return (msb << 8) + lsb




