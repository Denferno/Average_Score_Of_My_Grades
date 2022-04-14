import requests
from bs4 import BeautifulSoup
import school_creds

loginurl = 'https://leerlingenhf.trinitascollege.nl/Login?passAction=login&path=/'
site = 'https://leerlingenhf.trinitascollege.nl/Portaal/Persoonlijke_info/Examendossier'

# Als je dit ook wilt gebruiken:
# Ga naar het bestand school_creds.py en vul daar je leerlingnummer en wachtwoord in
logininfo = {
    'wu_loginname': school_creds.username,
    'wu_password' : school_creds.password 
}


def main():
    global grades_lst
    grades_lst = grades()  # cijfers achterhalen
    tekort_en_compensatie = tekort_compensatie_punten()  # tekortpunten optellen
    tekortpunten = tekort_en_compensatie[0]  # de eerste is de tekortpunten
    compensatiepunten = tekort_en_compensatie[-1]  # de laatste zijn de compensatiepunten 
    gemiddelde = sum(grades_lst) / len(grades_lst)  # gemiddelde van al mijn cijfers
    print(f'Je staat een {gemiddelde} gemiddeld')
    print(f'Je hebt {tekortpunten} tekortpunten')
    print(f'Je hebt {compensatiepunten} compensatiepunten')
    input('Druk op ENTER to exit')
 
    
def grades():
    grades_lst = []
    with requests.session() as s:
        s.post(loginurl, data=logininfo)
        response = s.get(site)
        soup = BeautifulSoup(response.content, 'html.parser')
        for number in range(1, 13): 
            # Deze skippen, omdat dit hoort bij het combi cijfer
            if number == 3 or number == 4 or number == 5 or number == 7:  
                continue
            else:
                grade = soup.select(f'tr:nth-child({number}) td:nth-child(3) span a span')
                grade = grade[0].text  # In plaats van [<span>8</span>] zegt het 8 
                grades_lst.append(grade)
        # float zal het getallen maken en geen strings, zodat ik sum() kan gebruiken
        grades_lst = [float(string) for string in grades_lst]          
        return grades_lst
 
    
def tekort_compensatie_punten():
    tekort_lst = []
    compensatie_lst = []
    for cijfer in grades_lst:
        tekortpunten = 0
        compensatie = 0
        # int rond het altijd naar beneden af, dus bijv 5.4 + 0.5 wordt 5.9 wat dan een 5 wordt
        # door int, maar een 5.5 wordt een 6 en int(6) blijft nog steeds een
        cijfer = int(cijfer + 0.5) 
        print(cijfer)
        if cijfer < 6:
            tekort_lst.append(6 - cijfer)# checken hoeveel tekortpunten
        elif cijfer > 6:
            compensatie_lst.append(cijfer - 6)  # checken hoeveel compensatie punten
    return [sum(tekort_lst), sum(compensatie_lst)]

if __name__ == '__main__':
     main()
