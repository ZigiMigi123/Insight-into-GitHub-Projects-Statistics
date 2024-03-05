from github_api import GitHubAPI
import pandas as pd

class Projekt:
    def __init__(self, name=None, stars=None, commits=None, contributors=None):
        self.name = name
        self.stars = stars
        self.commits = commits
        self.contributors = contributors

    def to_dict(self):
        # vsi stolpci ki bodo vkljuceni v Excel tabeli:
        return {'name':         self.name,
                'stars':        self.stars if self.stars else '/',
                'commits':      self.commits if self.commits else '/',
                'contributors': self.contributors if self.contributors else '/',
                }
class GitHubStatistika:
    def __init__(self):
        self.uporabnik = None
        self.api = GitHubAPI()
        self.projekti = []

    def pozdravi_uporabnika(self):
        print("Pozdravljeni v programu za pridobivanje statistike iz platforme GitHub.")
        self.uporabnik = input("Da se bolj spoznamo, vas lahko vprašam kako vam je ime? (Če nam ne želite izdati vašega imena lahko nadaljujete z izvajanjem programa z pritiskom tipke ENTER!): ")

        if self.uporabnik:
            print(f"Pozdravljeni, {self.uporabnik}!")
        else:
            print("Pozdravljeni, naključni uporabnik!")

    def izberi_in_isci_projekt(self):
        while True:
            kljucna_beseda = input("Prosim, da vnesete ključno besedo za iskanje na GitHubu: ")
            if kljucna_beseda == "exit":
                print("Izhod iz programa.")
                return

            # Dodaj funkcionalnost za določanje števila zadetkov
            stevilo_zadetkov = input("Vnesite želeno število zadetkov (privzeto 10): ")
            if not stevilo_zadetkov:
                stevilo_zadetkov = 10
            else:
                try:
                    stevilo_zadetkov = int(stevilo_zadetkov)
                except ValueError:
                    print("Neveljaven vnos. Uporabljeno bo privzeto število zadetkov (10).")
                    stevilo_zadetkov = 10
            zadetki = self.api.isci_po_githubu(kljucna_beseda, stevilo_zadetkov)

            if not zadetki:
                print("Ni zadetkov. Poskusite znova z drugo ključno besedo.")
                continue
            self.api.prikazi_zadetke(zadetki)

            # Uporabnik izbere projekt za analizo
            while True:
                izbira_projekta = ""
                if self.projekti:
                    print("~~~")
                    print(f"Analiziranih projektov: {len(self.projekti)}")
                    print("~~~")
                izbira_projekta = input("Vnesite številko projekta, ki ga želite analizirati (ali pritisnite ENTER za izhod): ")

                # uporabnik ni vnesel nic, pritisnil je ENTER za izhod
                if (izbira_projekta) == "":
                    print("Izhod iz programa.")
                    return
                try:
                    izbira_projekta = int(izbira_projekta)
                    if 1 <= izbira_projekta <= len(zadetki):
                        izbrani_projekt = zadetki[izbira_projekta - 1]
                        print(f"Izbrali ste projekt številka {izbira_projekta}, z naslovom: {izbrani_projekt['full_name']}")
                        self.analiziraj_projekt(izbrani_projekt)
                        print(f"Projekt analiziran...")
                        vnos = None

                        while vnos not in ['1', '2']:
                            print("~~~")
                            print("1. Nadaljuj analizo")
                            print("2. Izpisi analizirane podatke v Excel datoteko")
                            print("~~~")
                            vnos = input("Potrdi izbiro:")

                            if vnos == '2':
                                ime_datoteke = input("Vnesite ime izhodne Excel datoteke: ")
                                self.zapis_v_excel(ime_datoteke)
                                print("Izhod iz programa.")
                                return
                        break  # Izhod iz zanke izbire projekta
                    else:
                        print("Neveljavna izbira. Prosimo, poskusite znova.")

                except ValueError as e:
                    print("Neveljaven vnos. Prosimo, vnesite številko projekta.")
                    print(e)

    def analiziraj_projekt(self, izbrani_projekt):
        ime_izbranega_projekta = izbrani_projekt['full_name'].replace('/', '_')
        projekt = Projekt(ime_izbranega_projekta)
        self.projekti.append(projekt)

        while True:
            print("Kaj bi želeli analizirati v tem projektu?")
            print("1. Število zvezdic")
            print("2. Število prispevajočih")
            print("3. Seznam najnovejših prispevkov")
            print("4. Izhod")
            izbira_analize = input("Vnesite številko izbire: ")

            if izbira_analize == '1':
                # Tukaj lahko dodam funkcionalnost za analizo števila zvezdic
                print(izbrani_projekt['stargazers_count'])
                projekt.stars = izbrani_projekt['stargazers_count']
            elif izbira_analize == '2':
                # Tukaj lahko dodam funkcionalnost za analizo števila prispevajočih
                contributors = self.api.pridobi_prispevajoce(izbrani_projekt['owner']['login'], izbrani_projekt['name'])
                projekt.contributors = contributors
            elif izbira_analize == '3':
                # Tukaj lahko dodam funkcionalnost za analizo najnovejših prispevkov
                latest_commits = self.api.pridobi_najnovejse_prispevke(izbrani_projekt['owner']['login'],
                                                                       izbrani_projekt['name'])
                # for commit in latest_commits:
                    # rezultati.append(f"- {commit['commit']['author']['name']}: {commit['commit']['message']}")
                projekt.commits = len(latest_commits)
            elif izbira_analize == '4':
                print("Izhod iz analize.")
                return
            else:
                print("Neveljavna izbira. Prosimo, poskusite znova.")

    def zapis_v_excel(self, ime_datoteke):
        podatki = []
        for projekt in self.projekti:
            podatki.append(projekt.to_dict())
        df = pd.DataFrame(podatki)

        # ce hocemo preimovat stolpce s poljubnimi naslovi:
        nova_imena = {'name': 'ime',
                      'commits': 'spremembe',
                      'contributors': 'kontributorji',
                      'stars': 'zvezdice'}
        df.rename(index=str, columns=nova_imena)
        print(df)
        df.to_excel(f"{ime_datoteke}.xlsx", index=False)
        print(f"Analizirani podatki so shranjeni v Excel datoteko: {ime_datoteke}")