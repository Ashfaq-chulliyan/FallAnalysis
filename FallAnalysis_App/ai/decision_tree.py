from sklearn.tree import DecisionTreeClassifier
from FallAnalysis_App.models import resident_detail, Incident
import joblib, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "fall_risk_model.pkl")

LABELS = ["Low Risk", "Medium Risk", "High Risk"]


# ---------- TRAIN MODEL ----------
def train_model():
    X, y = [], []

    residents = resident_detail.objects.all()

    for r in residents:
        incidents = Incident.objects.filter(Resident=r)

        incident_count = incidents.count()
        serious_injury = incidents.filter(
            Incident_type__in=["HI", "FI"]
        ).exists()
        risky_location = incidents.filter(
            Incident_location__in=["BR", "ST"]
        ).exists()

        X.append([
            r.Resident_Age,
            incident_count,
            int(serious_injury),
            int(risky_location)
        ])

        # LABEL LOGIC
        if r.Resident_Age >= 75 and incident_count >= 2:
            y.append(2)
        elif serious_injury or risky_location:
            y.append(2)
        elif r.Resident_Age >= 60 and incident_count >= 1:
            y.append(1)
        else:
            y.append(0)

    if not X:
        return None

    model = DecisionTreeClassifier(
        max_depth=4,           # prevents overfitting
        min_samples_leaf=2,
        random_state=42
    )
    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)
    return model


# ---------- LOAD MODEL ----------
_model = None

def load_model():
    global _model
    if _model:
        return _model

    if os.path.exists(MODEL_PATH):
        _model = joblib.load(MODEL_PATH)
    else:
        _model = train_model()

    return _model


# ---------- PREDICT RISK ----------
def predict_resident_risk(resident_id):
    model = load_model()
    if not model:
        return {
            "risk": "Low Risk",
            "confidence": 0
        }

    r = resident_detail.objects.get(id=resident_id)
    incidents = Incident.objects.filter(Resident=r)

    incident_count = incidents.count()
    serious_injury = incidents.filter(
        Incident_type__in=["HI", "FI"]
    ).exists()
    risky_location = incidents.filter(
        Incident_location__in=["BR", "ST"]
    ).exists()

    features = [[
        r.Resident_Age,
        incident_count,
        int(serious_injury),
        int(risky_location)
    ]]

    prediction = model.predict(features)[0]
    confidence = model.predict_proba(features).max() * 100

    return {
        "risk": LABELS[prediction],
        "confidence": round(confidence, 2),
        "features": {
            "age": r.Resident_Age,
            "incidents": incident_count,
            "serious_injury": serious_injury,
            "risky_location": risky_location
        }
    }
