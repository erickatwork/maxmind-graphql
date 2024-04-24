import maxminddb
import sys
import os

class MaxMindDBManager:
    def __init__(self, script_directory):
        self.script_directory = script_directory

        # dbs
        city_file_path = os.path.join(script_directory, './mmdb/GeoIP2-City.mmdb')
        connection_type_file_path = os.path.join(script_directory, './mmdb/GeoIP2-Connection-Type.mmdb')
        domain_file_path = os.path.join(script_directory, './mmdb/GeoIP2-Domain.mmdb')
        isp_file_path = os.path.join(script_directory, './mmdb/GeoIP2-ISP.mmdb')

        # Initialize database variables
        self.city_db = self.load_database(city_file_path)
        self.connection_type_db = self.load_database(connection_type_file_path)
        self.domain_db = self.load_database(domain_file_path)
        self.isp_db = self.load_database(isp_file_path)

        # Try using free dbs if premium dbs are not found
        if not self.city_db:
            lite_city_path = os.path.join(script_directory, './mmdb/GeoLite2-City.mmdb')
            self.city_db = self.load_database(lite_city_path)
        if not self.isp_db:
            lite_asn_path = os.path.join(script_directory, './mmdb/GeoLite2-ASN.mmdb')
            self.isp_db = self.load_database(lite_asn_path)

    def load_database(self, file_path):
        # Only attempt to load if a path is provided
        if os.path.exists(file_path):
            return maxminddb.open_database(file_path)
        return None

# Create a global instance of the DB manager
script_directory = os.path.dirname(os.path.abspath(__file__))
maxmind_db = MaxMindDBManager(script_directory)


# For local testing
if __name__ == "__main__":
    ip = '1.1.1.1'

    response = maxmind_db.city_db.get(ip)
    print ("CITY")
    print (response)

    response = maxmind_db.connection_type_db.get(ip)
    print ("CONNECTION TYPE")
    print (response)

    response = maxmind_db.domain_db.get(ip)
    print ("DOMAIN")
    print (response)

    response = maxmind_db.isp_db.get(ip)
    print ("ISP")
    print (response)

