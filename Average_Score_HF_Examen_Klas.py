import requests
from bs4 import BeautifulSoup
import re
import school_creds

loginurl = 'https://leerlingenhf.trinitascollege.nl/Login?passAction=login&path=/'
site = 'https://leerlingenhf.trinitascollege.nl/Portaal/Persoonlijke_info/Examendossier'

logininfo = {
    'wu_loginname': school_creds.username,
    'wu_password': school_creds.password 
}

def main():
    global grades_lst
    grades_lst = grades() # cijfers achterhalen
    tekortpunten = tekort_compensatie_punten()[0] # tekortpunten optellen
    compensatiepunten = tekort_compensatie_punten()[1] # compensatie punten optellen
    gemiddelde = sum(grades_lst) / len(grades_lst) # average of all my grades
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
            if number == 3 or number == 4 or number == 5 or number == 7: # skipping these numbers because these are parts of the 'combi cijfer'
                continue
            else:
                grade = soup.select(f'tr:nth-child({number}) td:nth-child(3) span a span')
                grade = grade[0].text # Instead of [<span>8</span>] if will say 8
                grades_lst.append(grade)
        grades_lst = [float(string) for string in grades_lst] # float will make the numbers and not strings so that I can use sum()
        return grades_lst
    
def tekort_compensatie_punten():
    tekortpunten = 0
    compensatiepunten = 0
    for number in grades_lst:
        onvoldoende = 6 - round(number)  
        if onvoldoende > 0:
            tekortpunten += onvoldoende 
        elif onvoldoende < 0:
            compensatiepunten -= onvoldoende
    return [tekortpunten, compensatiepunten]
            
if __name__ == '__main__':
     main()



    
    
    
    