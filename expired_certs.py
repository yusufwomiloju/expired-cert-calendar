import pprint
from datetime import datetime, timedelta
from ibmsecurity.appliance.isamappliance import ISAMAppliance
from ibmsecurity.user.applianceuser import ApplianceUser
from ibmsecurity.isam.base.ssl_certificates import certificate_databases, signer_certificate, personal_certificate
from ics import Calendar, Event, DisplayAlarm

# Function to pretty print JSON data
def p(jdata):
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(jdata)

# Function to create an Event
def create_event(kdb_id, cert_type, cert, reminderInDays):
    a = DisplayAlarm(trigger=timedelta(days=-int(reminderInDays)))

    e = Event(alarms=[a])
    e.name = cert['id'] 
    e.begin = datetime.fromtimestamp(int(cert['notafter_epoch'])).strftime('%Y-%m-%d %H:%M:%S')

    e.description = ("Key Database: " + kdb_id + "\n\n" +
                     "Type: " + cert_type + "\n" + 
                     "Subject: " + cert['subject'] + "\n" + 
                     "Issuer: " + cert['issuer'])
    e.make_all_day()

    return e

if __name__ == "__main__":
    """
    This test program should not execute when imported, which would otherwise
    cause problems when generating the documentation.
    """

    hostname = "winagent.ibm.com"
    reminderInDays = 14

    # Create a user credential for ISAM appliance
    u = ApplianceUser(username="admin", password="admin")
    # Create an ISAM appliance with above credential
    isam_server = ISAMAppliance(hostname, user=u, lmi_port=443)

    c = Calendar()

    # Get all the certificate databases
    jdata = certificate_databases.get_all(isamAppliance=isam_server)

    kdbs = jdata.get("data")  
    for kdb in kdbs:
        # certificate database id
        kdb_id = kdb['id']
        print("kdb id: ", kdb_id)
        
        # Signer Certificates 
        jdata = signer_certificate.get_all(isamAppliance=isam_server, kdb_id = kdb_id)
        #print(jdata)

        signer_certs = jdata.get("data")  # list of Signer Certs
        for cert in signer_certs:
            #print(cert)

            e = create_event(kdb_id, "Signer", cert, reminderInDays)
            c.events.add(e)
                
        # Personal Certificates 
        jdata = personal_certificate.get_all(isamAppliance=isam_server, kdb_id = kdb_id)
        #print(jdata)

        personal_certs = jdata.get("data")  # list of Personal Certs
        for cert in personal_certs:
            #print(cert)

            e = create_event(kdb_id, "Personal", cert, reminderInDays)
            c.events.add(e)        

    with open(hostname + '.ics', 'w') as f:
        f.write(str(c))