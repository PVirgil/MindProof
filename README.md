# 🧠 MindProof

**MindProof** is a blockchain system designed to register, timestamp, and verify **original ideas, concepts, and intellectual claims**. Whether you're a researcher, innovator, creative, or AI, MindProof offers an immutable ledger for proving authorship, documenting originality, and establishing idea ownership.

Deployed with **Flask on Vercel**, MindProof combines proof-of-work validation with a REST API and a live blockchain explorer to ensure transparency and permanence for intellectual property assertions.

---

## 🚀 Features

- ✅ Immutable recording of authorship and creative claims
- 🧾 Proof-of-work secured intellectual registry
- 🔍 Web-based blockchain explorer (HTML rendered)
- 🔗 RESTful API for submitting and mining claims
- 🗃️ JSON-based portable chain ledger

---

## 📁 Project Structure

```
/
├── mindproof_app.py          # Flask blockchain app
├── mindproof_chain.json      # Persistent ledger
├── requirements.txt          # Python dependencies
└── vercel.json               # Vercel deployment config
```

---

## 🔗 API Endpoints

| Method | Route      | Function                            |
|--------|------------|-------------------------------------|
| GET    | `/`        | HTML Blockchain Explorer            |
| GET    | `/chain`   | Return full chain as JSON           |
| GET    | `/mine`    | Mine the next claim block           |
| POST   | `/submit`  | Submit a new intellectual claim     |

### Example: `POST /submit`

```json
{
  "author": "Ada Lovelace",
  "claim_title": "Analytical Engine Framework",
  "description": "A method for symbolic computation using punched cards.",
  "categories": ["computing", "mathematics", "early AI"],
  "doc_hash": "e8b7be43e3...",
  "reference_links": ["https://archives.org/lovelace-paper"]
}
```

---

## 🔍 Use Cases

- Academic idea timestamping  
- Protecting invention claims pre-patent  
- Tracking original content from creators or AI  
- Verifying concept originality in science and tech  
- Collaborative innovation trust logs  

---

> MindProof is where **thought becomes trust**. Lock in your originality, protect your ideas, and prove your authorship forever.
