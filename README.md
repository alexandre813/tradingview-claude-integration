# TradingView-Claude Integration

Une intégration complète entre **TradingView** et **Claude AI** pour analyser automatiquement les signaux de trading et générer des recommandations intelligentes.

## 🎯 Fonctionnalités

✅ **Webhooks TradingView** - Reçois les alertes en temps réel  
✅ **Analyse Claude** - Génère des analyses complètes avec IA  
✅ **Conversation persistante** - Garde l'historique pour du contexte  
✅ **Analyse technique** - Prix, volume, support/résistance  
✅ **Recommandations** - Points d'entrée/sortie et risque/récompense  
✅ **REST API** - Endpoints pour analyses manuelles  

## 📋 Prérequis

- Python 3.8+
- Compte Claude (pour l'API key)
- Compte TradingView (pour les webhooks)
- Un serveur ou VPS pour héberger

## 🚀 Installation

### 1. Clone le repo
```bash
git clone https://github.com/alexandre813/tradingview-claude-integration.git
cd tradingview-claude-integration
```

### 2. Installe les dépendances
```bash
pip install -r requirements.txt
```

### 3. Configure les variables d'environnement
```bash
cp .env.example .env
```

Édite `.env` et ajoute :
- `CLAUDE_API_KEY` : Ta clé API Claude
- `TRADINGVIEW_WEBHOOK_TOKEN` : Un token sécurisé pour les webhooks

### 4. Lance l'application
```bash
python main.py
```

L'app tourne sur `http://localhost:5000`

## 📡 Utilisation

### Option 1 : Webhooks TradingView

1. Dans TradingView, crée une alerte avec webhook :
```
URL: http://your-server.com:5000/webhook/tradingview?token=YOUR_TOKEN
```

2. Formate le message JSON :
```json
{
  "ticker": "BTCUSD",
  "close": 45000,
  "change_percent": 2.5,
  "volume": 1000000,
  "alert_message": "Signal d'achat confirmé",
  "resistance": 46000,
  "support": 44000
}
```

### Option 2 : API manuelle

```bash
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "EURUSD",
    "price": 1.0950,
    "change_percent": 0.5,
    "volume": 500000,
    "signal": "Breakout haussier",
    "resistance": 1.1000,
    "support": 1.0900
  }'
```

### Option 3 : Test de santé
```bash
curl http://localhost:5000/health
```

### Option 4 : Réinitialiser la conversation
```bash
curl -X POST http://localhost:5000/reset
```

## 📊 Exemple de réponse Claude

```
Analyse Technique :
- Le prix a franchi la résistance à 46000
- Volume en hausse confirme la tendance haussière
- MACD positif et RSI > 70

Sentiment : HAUSSIER 📈

Points d'entrée : 45500 - 45800
Points de sortie : 46200 - 46500
Stop Loss : 45200

Risque/Récompense : 1:2.5 (Excellent)
```

## 🔧 Structure du projet

```
tradingview-claude-integration/
├── main.py              # Application Flask principale
├── config.py            # Configuration
├── requirements.txt     # Dépendances Python
├── .env                 # Variables d'environnement
└── README.md            # Ce fichier
```

## 🌐 Déploiement

### Sur Heroku
```bash
heroku create your-app-name
git push heroku main
```

### Sur un VPS (Ubuntu)
```bash
# Installe Python et dépendances
sudo apt-get update
sudo apt-get install python3-pip python3-venv

# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Lance avec Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

### Avec Docker
```bash
docker build -t tradingview-claude .
docker run -p 5000:5000 --env-file .env tradingview-claude
```

## 🔐 Sécurité

- ⚠️ Ne mets JAMAIS tes clés API dans le code
- Utilise des variables d'environnement
- Protège ton webhook avec un token fort
- Utilise HTTPS en production

## 📝 API Endpoints

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/webhook/tradingview` | Reçoit les alertes TradingView |
| POST | `/analyze` | Analyse manuelle |
| GET | `/health` | Vérification de santé |
| POST | `/reset` | Réinitialise l'historique |

## 🐛 Troubleshooting

**Erreur : "Unauthorized"**
- Vérifie que le token dans l'URL correspond à `TRADINGVIEW_WEBHOOK_TOKEN`

**Erreur : "CLAUDE_API_KEY not found"**
- Assure-toi que `.env` existe et contient la clé

**L'app ne démarre pas**
- Vérifie : `pip install -r requirements.txt`
- Check le port 5000 n'est pas utilisé

## 📚 Documentation utile

- [Anthropic Claude API Docs](https://docs.anthropic.com)
- [Flask Documentation](https://flask.palletsprojects.com)
- [TradingView Webhooks](https://www.tradingview.com/pine_script_docs/#webhooks)

## 💡 Idées futures

- [ ] Dashboard web pour visualiser l'historique
- [ ] Support de plusieurs paires simultanément
- [ ] Machine learning pour améliorer les analyses
- [ ] Notifications Telegram/Discord
- [ ] Backtesting des signaux
- [ ] Gestion de portefeuille

## 📞 Support

Des questions ? Crée une issue sur GitHub !

## 📄 License

MIT

---

**Créé par** : Alexandre813  
**Dernière mise à jour** : 2026-09-14
