"""MoscowPrices: Flask site and the original CatBoost model from Spring_2026."""
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd
from catboost import CatBoostRegressor
from flask import Flask, jsonify, redirect, render_template, request

ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "catboost_model.cbm"
app = Flask(__name__)
metro_coefs = pd.read_csv(ROOT / "metro_coefs.csv")
station_prices = dict(zip(metro_coefs["Metro station"], metro_coefs["Metro_coef"]))
stations = sorted(station_prices)


@lru_cache(maxsize=1)
def load_model():
    model = CatBoostRegressor()
    model.load_model(str(MODEL_PATH))
    return model


@app.get("/")
def home():
    return render_template("moscow.html")


@app.get("/moscow.html")
def legacy_home():
    return redirect("/")


@app.get("/metro_map")
@app.get("/metro_map.html")
def metro_map():
    return render_template("metro_map.html")


@app.get("/stations")
def station_list():
    return jsonify(stations)


@app.get("/health")
def health():
    ready = MODEL_PATH.is_file()
    return jsonify(service="moscow-prices", model_ready=ready), 200 if ready else 503


@app.post("/predict")
def predict():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="Передайте параметры квартиры в формате JSON."), 400
    values = {}
    limits = {"area": (10, 300), "rooms": (1, 10), "floor": (1, 50), "minutes": (0, 60)}
    for name, (minimum, maximum) in limits.items():
        value = data.get(name)
        try:
            if isinstance(value, bool):
                raise ValueError
            value = float(value)
        except (ValueError, TypeError):
            return jsonify(error=f"Некорректное значение поля {name}."), 400
        if not np.isfinite(value) or not minimum <= value <= maximum:
            return jsonify(error=f"Поле {name}: допустимо от {minimum} до {maximum}."), 400
        if name != "area" and value != int(value):
            return jsonify(error=f"Поле {name} должно быть целым числом."), 400
        values[name] = value

    station = data.get("metro")
    if not isinstance(station, str) or station.strip() not in station_prices:
        return jsonify(error="Выберите станцию из списка."), 400
    if not MODEL_PATH.is_file():
        return jsonify(error="Модель пока недоступна. Попробуйте позже."), 503
    features = pd.DataFrame({
        "Area": [values["area"]],
        "Number of rooms": [values["rooms"]],
        "Metro_coef": [station_prices[station.strip()]],
        "Minutes to metro": [values["minutes"]],
        "Floor": [values["floor"]],
    })
    prediction = float(np.expm1(load_model().predict(features)[0]))
    if not np.isfinite(prediction) or prediction <= 0:
        return jsonify(error="Не удалось рассчитать стоимость для этих параметров."), 422
    return jsonify(prediction=prediction)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
