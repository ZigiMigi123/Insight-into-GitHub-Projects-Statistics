from github_statistika import GitHubStatistika
from spanje import spanje

if __name__ == "__main__":
    aplikacija = GitHubStatistika()
    print("Nalaganje...")
    aplikacija.pozdravi_uporabnika()
    aplikacija.izberi_in_isci_projekt()
    # print(aplikacija.zbrani_podatki)