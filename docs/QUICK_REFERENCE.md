# OptionPrisma - Quick Reference Guide 🚀
# OptionPrisma - Quick Reference Guide
## 📋 Comandos Esenciales

## Comandos Esenciales
# Activar entorno virtual
source venv/bin/activate

# Ejecutar servidor (desarrollo)
fastapi dev app/main.py

# Ejecutar servidor (alternativo)
uvicorn app.main:app --reload

# Ejecutar tests
pytest -v

# Tests con coverage
pytest --cov=app

# Crear archivo JSON inicial
echo '[]' > data/results.json
```

---


### Option Pricing Formula (Monte Carlo)
```
1. Simular N precios futuros: S_T = S_0 * exp((r - 0.5σ²)T + σ√T*Z)
2. Calcular payoffs: max(S_T - K, 0) para call
3. Descontar: payoffs * e^(-rT)
4. Promediar: mean(discounted_payoffs)
```

### Black-Scholes (Fórmula exacta)
```
Call: S*N(d1) - K*e^(-rT)*N(d2)
Put:  K*e^(-rT)*N(-d2) - S*N(-d1)

d1 = [ln(S/K) + (r + σ²/2)T] / (σ√T)
d2 = d1 - σ√T
```

### The Greeks (Quick)
```
Delta (Δ):  ∂C/∂S    → Cambio por $1 en precio
Gamma (Γ):  ∂²C/∂S²  → Curvatura del precio
Vega (ν):   ∂C/∂σ    → Cambio por 1% volatilidad
Theta (Θ):  ∂C/∂t    → Time decay (pérdida diaria)
Rho (ρ):    ∂C/∂r    → Sensibilidad a tasas
```

---


```
app/
├── config.py          → Configuración (paths, constantes)
├── models.py          → Pydantic (validación de datos)
├── monte_carlo.py     → 🎲 Simulación estocástica
├── black_scholes.py   → 📐 Fórmula analítica + Greeks
├── persistence.py     → 💾 CRUD en JSON (async)
└── main.py            → 🌐 API endpoints (FastAPI)

tests/
├── test_monte_carlo.py  → ✅ Unit tests (lógica)
├── test_persistence.py  → ✅ Tests de CRUD
└── test_api.py          → ✅ Integration tests (endpoints)
```

---


```
Client
  │
  ├── POST /simulations
  │   {spot_price: 100, strike_price: 105, ...}
  ▼
FastAPI (main.py)
  │
  ├── 1. Pydantic validation
  ├── 2. await validate_inputs_async()
  ├── 3. await fetch_risk_free_rate_async()
  ├── 4. price_european_option()  ← Monte Carlo
  ├── 5. black_scholes_price()    ← Analytical
  ├── 6. calculate_greeks()       ← Sensitivities
  ├── 7. await save_simulation_result()
  │
  └── Response
      {
        simulation_id: "sim_xxx",
        option_price: 10.45,
        black_scholes_price: 10.48,
        greeks: {...},
        ...
      }
```

---


```
┌─────────────────────────────┐
│   ¿Es I/O operation?        │
│  (file, network, DB)        │
└───────┬─────────────────────┘
        │
    ┌───┴───┐
   YES     NO
    │       │
    ▼       ▼
async def   def
    │       │
use await   pure
            computation
```

**Examples:**
```python
# ✅ Async (I/O)
async def save_to_file():
    async with aiofiles.open(...) as f:
        await f.write(data)

# ✅ Sync (CPU)
def calculate_option_price():
    return np.mean(payoffs)

# ✅ Mix (call sync from async)
async def endpoint():
    await validate()     # I/O
    result = compute()   # CPU
    await save(result)   # I/O
```

---


```python
# Unit test (Monte Carlo logic)
def test_call_option_pricing():
    result = price_european_option(
        spot_price=100,
        strike_price=100,
        volatility=0.2,
        # ...
    )
    assert 9.0 < result["price"] < 12.0

# Integration test (API endpoint)
def test_create_simulation(client):
    response = client.post("/simulations", json={...})
    assert response.status_code == 201
    assert "simulation_id" in response.json()
```

---


### Issue 1: "Module not found"
```bash
# Solution: Activate venv
source venv/bin/activate
```

### Issue 2: "results.json not found"
```bash
# Solution: Create data directory and file
mkdir -p data
echo '[]' > data/results.json
```

### Issue 3: "Port already in use"
```bash
# Solution: Change port
fastapi dev app/main.py --port 8001
```

### Issue 4: Tests failing
```bash
# Solution: Check temp_results_file fixture is working
pytest tests/test_persistence.py -v -s
```

---


```bash
# Health Check
GET http://localhost:8000/
Response: {"status": "healthy", "timestamp": "...", "version": "1.0.0"}

# Create Simulation
POST http://localhost:8000/simulations
Body: {
  "spot_price": 100,
  "strike_price": 105,
  "time_to_maturity": 1.0,
  "volatility": 0.25,
  "risk_free_rate": 0.05,
  "option_type": "call"
}
Response 201: {
  "simulation_id": "sim_xxx",
  "option_price": 10.45,
  "std_error": 0.03,
  "black_scholes_price": 10.48,
  "greeks": {...},
  ...
}

# Get All Simulations
GET http://localhost:8000/simulations
Response 200: [{...}, {...}, ...]

# Get One Simulation
GET http://localhost:8000/simulations/sim_xxx
Response 200: {...} or 404

# Delete Simulation
DELETE http://localhost:8000/simulations/sim_xxx
Response 204: (no body) or 404
```

---


### "What's interesting about this project?"

**Option 1: Technical**
> "I built an async API that combines financial mathematics with modern Python. The interesting part was balancing CPU-intensive Monte Carlo simulations with async I/O. I use async/await for all I/O operations while keeping numerical computation synchronous, which allows handling 100+ concurrent requests efficiently."

**Option 2: Finance**
> "I implemented two different option pricing methods: Monte Carlo simulation and Black-Scholes analytical solution. This demonstrates both stochastic methods and closed-form solutions in quantitative finance. I also calculate all the Greeks for risk management."

**Option 3: Architecture**
> "I followed clean architecture principles with separation of concerns. The pricing logic is completely independent from the API layer, making it easy to test and reuse. I can swap JSON storage for PostgreSQL without touching any business logic."

### "What would you add next?"

> "Three things: (1) Redis caching for repeated calculations, (2) WebSocket support for real-time price streaming, (3) Historical volatility calculation from market data APIs."

---


### Geometric Brownian Motion
```
S_T = S_0 * exp((r - 0.5σ²)T + σ√T*Z)
```

### Standard Error
```
SE = σ_payoffs / √N
```

### Put-Call Parity
```
C - P = S - K*e^(-rT)
```

### Delta (Call)
```
Δ_call = N(d1)
```

---


```bash
# 1. Start coding session
cd ~/projects/optionprisma
source venv/bin/activate
code .

# 2. Make changes in VS Code

# 3. Run server (auto-reload enabled)
fastapi dev app/main.py

# 4. Test in another terminal
curl http://localhost:8000/
# or open http://localhost:8000/docs

# 5. Run tests
pytest -v

# 6. Commit changes
git add .
git commit -m "Add feature X"
git push
```

---


### Priority 1 (Must Read):
1. FastAPI docs: https://fastapi.tiangolo.com
2. Options basics: Investopedia "Options" section
3. NumPy for Finance: Chapter 1-3 of "Python for Finance"

### Priority 2 (Deep Dive):
4. Black-Scholes: Hull's "Options, Futures, and Other Derivatives"
5. Monte Carlo: Glasserman's "Monte Carlo Methods in Financial Engineering"
6. Async Python: Real Python's async tutorial

---


Before presenting this project:

- [ ] Can explain Monte Carlo simulation in 2 minutes
- [ ] Can explain Black-Scholes in 2 minutes

Reference it whenever you need a quick reminder.