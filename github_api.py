import requests

class GitHubAPI:
    def __init__(self):
        self.base_url = "https://api.github.com/search/repositories"

    def isci_po_githubu(self, kljucna_beseda, stevilo_zadetkov=10):
        params = {"q": kljucna_beseda, "sort": "stars", "order": "desc", "per_page": stevilo_zadetkov}
        response = requests.get(self.base_url, params=params)

        if response.status_code == 200:
            podatki = response.json()
            zadetki = podatki.get("items", [])
            if zadetki:
                return zadetki
            else:
                return []
        else:
            return []

    def prikazi_zadetke(self, zadetki):
        if zadetki:
            print("Zadetki najdeni na GitHubu:")
            for i, zadetek in enumerate(zadetki, start=1):
                print(f"{i}. Ime projekta: {zadetek['name']}")
                print(f"   Lastnik: {zadetek['owner']['login']}")
                print(f"   Zvezdice: {zadetek['stargazers_count']}")
                print(f"   Opis: {zadetek['description']}")
                print(f"   URL: {zadetek['html_url']}")
                print()
        else:
            print("Ni zadetkov za iskano ključno besedo.")

    def pridobi_najnovejse_prispevke(self, lastnik, ime_projekta, stevilo_prispevkov=5):
        # Pridobi seznam najnovejših prispevkov v projektu
        url = f"https://api.github.com/repos/{lastnik}/{ime_projekta}/commits?per_page={stevilo_prispevkov}"
        response = requests.get(url)

        if response.status_code == 200:
            latest_commits = response.json()
            return latest_commits
        else:
            print(f"Napaka pri pridobivanju najnovejših prispevkov: {response.status_code}")
            return []

    def pridobi_prispevajoce(self, lastnik, ime_projekta):
        # Dodana metoda za pridobivanje števila prispevajočih
        url = f"https://api.github.com/repos/{lastnik}/{ime_projekta}/contributors"
        response = requests.get(url)
        if response.status_code == 200:
            contributors = response.json()
            return len(contributors)
        else:
            print(f"Napaka pri pridobivanju prispevajočih: {response.status_code}")
            return 0