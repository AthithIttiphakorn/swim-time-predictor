#Working!

import http.client
athleteID = 4470524


def html():
    

    #Establish HTTPS connection
    conn = http.client.HTTPSConnection("www.swimrankings.net")

    #send GET request
    conn.request("GET", f"/index.php?page=athleteDetail&athleteId={athleteID}&styleId=13")

    #get response
    response = conn.getresponse()
    print(f"status code: {response.status}")
    print(f"Reason {response.reason}")
    body1 = response.read().decode()

    return body1, conn, athleteID

_, conn, _ = html()

#print(body)
conn.close()
