# Discriminations dans les publicités sur les plateformes

## Installation

```
sudo apt update && sudo apt install ffmpeg cmake tesseract-ocr tesseract-ocr-fra
pip install -r requirements.txt
pip install --user --no-deps -e .
export KEY=<tiktok-api-key>
export SECRET=<tiktok-secret-key>
```

## Tâches

- [x] Déterminer les plateformes d'intérêt:
  - Tiktok
  - Meta (Facebook + Instagram)
- [x] Regarder ce que les CGU exigent sur les discriminations sur les publicités (d'emploi en particulier)

Stratégie d'échantillonage:
- [ ] Quelles professions ?
- [x] Comment on sélectionne les publicités ? Mots-clés, annonceurs ?

Collecte des données:
- [x] API
- [x] Dump Meta
- [x] Scraping

Traitement des données:
- [x] Récupération données de reach
- [x] Récupération données de ciblage
- [x] Classification: H/F dans la publicité, profession

## Stratégies d'échantillonnage

### Professions

Comment récupérer les professions ? Slides du commissariat général à la stratégie et à la prospective. Rapport sur comment lutter contre les stéréotypes fille-garçon.

### Récupération des publicités

1. Par annonceur
2. Par mots-clés

## Développement

Lien test de vidéo Tiktok: https://library.tiktok.com/api/v1/cdn/1740492773/video/aHR0cHM6Ly92NzcudGlrdG9rY2RuLmNvbS9lNTQ2Y2ExYWM4YWNmNDdlOWZlZTFkZjhmYzgwZGFiMi82N2JlMjQ3My92aWRlby90b3MvYWxpc2cvdG9zLWFsaXNnLXZlLTAwNTFjMDAxLXNnL29ZQXdER2NQZ0laQVViZVJHNGZlQ0xFSG9HVzh3eGc3cVhsaktBLw==/796a014b-93db-4144-94f7-f9700f1e4474?a=475769&bti=PDU2NmYwMy86&ch=0&cr=0&dr=1&cd=0%7C0%7C0%7C0&cv=1&br=1822&bt=911&cs=0&ds=1&ft=.NpOcInz7ThywZ4OXq8Zmo&mime_type=video_mp4&qs=0&rc=OGY0ZWdpaTM3ZmgzZTRlM0BpM3Q2M3g5cm1yeDMzODYzNEBjNmI1NmNfNS4xYC9iX2BeYSNrZmlyMmQ0ZTRgLS1kMC1zcw%3D%3D&vvpl=1&l=2025022514125250EC4F069228EBD5B790&btag=e00088000&cc=13
