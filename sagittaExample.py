__author__ = 'afox'

import logins
from webservices import Sagitta

# create the Sagitta object by passing in login creds. see logins.py
s = Sagitta(**logins.sagitta)

response = s.call('rolodexStartsWith', 'smith')
print(response)

"""
(startsWithInfoMap){
   TotalHits = 1
   TotalReturned = 1
   startsWithArray =
      (ArrayOfStartsWithArray){
         startsWithArray[] =
            (startsWithArray){
               ID = 234550
               ClientCd = "SMITHJOHN"
               ClientName = "JOHN SMITH"
               Addr1 = "221 B BAKER ST."
               City = "Memphis"
               StateProvCd = "TN"
               PostalCode = "37204"
               Producer1Cd = "PJW"
               Servicer1Cd = "ASD"
               Archived = None
               ContactMethod = "555 555-5555"
               Note = None
               SIC1Cd = None
               SourceCd = None
            },
      }
 }
"""