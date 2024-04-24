import strawberry
from typing import List, Optional
from maxmind_db_manager import maxmind_db  # Import the global reader

@strawberry.type
class IP_Metadata:
    # City
    ip: Optional[str] = None
    continent: Optional[str] = None
    continent_code: Optional[str] = None
    country: Optional[str] = None # where the ip is located
    country_code: Optional[str] = None
    registered_country: Optional[str] = None # where the ip is registered
    registered_country_code: Optional[str] = None
    city: Optional[str] = None
    accuracy_radius: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    timezone: Optional[str] = None
    # Connection Type
    connection_type: Optional[str] = None
    # Domain
    domain: Optional[str] = None
    # ISP
    asn: Optional[int] = None
    asn_org: Optional[str] = None
    isp: Optional[str] = None
    isp_org: Optional[str] = None


@strawberry.type
class Maxmind_DB_INFO:
    binary_format_major_version: Optional[int] = None
    binary_format_minor_version: Optional[int] = None
    node_count: Optional[int] = None
    record_size: Optional[int] = None
    description: Optional[str] = None
    build_epoch: Optional[int] = None

@strawberry.type
class Query:
    @strawberry.field
    def enrich_ip(self, ip: str) -> IP_Metadata:
        ip_metadata = IP_Metadata()
        ip_metadata.ip = ip

        # City
        if maxmind_db.city_db:
            city_ip = maxmind_db.city_db.get(ip)
            ip_metadata.continent = city_ip.get('continent', {}).get('names', {}).get('en', 'Unknown') if maxmind_db.city_db else 'Unknown'
            ip_metadata.continent_code = city_ip.get('continent', {}).get('code', 'Unknown') if maxmind_db.city_db else 'Unknown'
            ip_metadata.country = city_ip.get('country', {}).get('names', {}).get('en', 'Unknown') if maxmind_db.city_db else 'Unknown'
            ip_metadata.country_code = city_ip.get('country', {}).get('iso_code', 'Unknown') if maxmind_db.city_db else 'Unknown'
            ip_metadata.registered_country = city_ip.get('registered_country', {}).get('names', {}).get('en', 'Unknown') if maxmind_db.city_db else 'Unknown'
            ip_metadata.registered_country_code = city_ip.get('registered_country', {}).get('iso_code', 'Unknown') if maxmind_db.city_db else 'Unknown'
            ip_metadata.city = city_ip.get('city', {}).get('names', {}).get('en', 'Unknown') if maxmind_db.city_db else 'Unknown'
            ip_metadata.accuracy_radius = city_ip.get('location', {}).get('accuracy_radius', -1) if maxmind_db.city_db else -1
            ip_metadata.latitude = city_ip.get('location', {}).get('latitude', -1) if maxmind_db.city_db else -1
            ip_metadata.longitude = city_ip.get('location', {}).get('longitude', -1) if maxmind_db.city_db else -1
            ip_metadata.timezone = city_ip.get('location', {}).get('time_zone', 'Unknown') if maxmind_db.city_db else 'Unknown'
            
        # Connection Type
        if maxmind_db.connection_type_db:
            ip_metadata.connection_type = maxmind_db.connection_type_db.get(ip).get('connection_type', 'Unknown') if maxmind_db.connection_type_db.get(ip) else 'Unknown'

        # Domain
        if maxmind_db.domain_db:
            ip_metadata.domain = maxmind_db.domain_db.get(ip).get('domain', 'Unknown') if maxmind_db.domain_db.get(ip) else 'Unknown'

        # ISP
        if maxmind_db.isp_db:
            isp_ip = maxmind_db.isp_db.get(ip)
            ip_metadata.asn = isp_ip.get('autonomous_system_number', -1) if maxmind_db.isp_db.get(ip) else -1
            ip_metadata.asn_org = isp_ip.get('autonomous_system_organization', 'Unknown') if maxmind_db.isp_db.get(ip) else 'Unknown'
            ip_metadata.isp = isp_ip.get('isp', 'Unknown') if maxmind_db.isp_db.get(ip) else 'Unknown'
            ip_metadata.isp_org = isp_ip.get('organization', 'Unknown') if maxmind_db.isp_db.get(ip) else 'Unknown'

        return ip_metadata
    
    @strawberry.field
    def enrich_ips(self, ips: List[str]) -> List[IP_Metadata]:
        return [Query.enrich_ip(self, ip) for ip in ips]

    @strawberry.field
    def metadata(self) -> List[Maxmind_DB_INFO]:
        db_info_list = []
        db_list = [maxmind_db.city_db, maxmind_db.connection_type_db, maxmind_db.domain_db, maxmind_db.isp_db]
        for db in db_list:
            if db is None: # Skip if db is not loaded
                continue
            reader = db.metadata()
            db_info = Maxmind_DB_INFO()
            db_info.binary_format_major_version = reader.binary_format_major_version
            db_info.binary_format_minor_version = reader.binary_format_minor_version
            db_info.node_count = reader.node_count
            db_info.record_size = reader.record_size
            db_info.description = reader.description['en']
            db_info.build_epoch = reader.build_epoch
            db_info_list.append(db_info)
        
        return db_info_list

schema = strawberry.Schema(query=Query)
