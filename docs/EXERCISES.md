# OptionPrisma - Ejercicios Prácticos 🎯

## 📚 Tabla de Contenidos
1. [Ejercicios Básicos (Comenzar aquí)](#basicos)
2. [Ejercicios Intermedios](#intermedios)
3. [Ejercicios Avanzados](#avanzados)

**Tarea:** Modifica `app/main.py` para agregar logging cuando se crea una simulación.

```python
import logging

logger = logging.getLogger(__name__)

@app.post("/simulations", ...)
async def create_simulation(request: OptionPricingRequest):
    logger.info(f"New simulation request: {request.option_type} "
                f"S={request.spot_price} K={request.strike_price}")
    
    # ... código existente ...
    
    logger.info(f"Simulation {simulation_id} completed: "
                f"MC=${pricing_result['price']:.2f} "
                f"BS=${bs_price:.2f}")
```

**Verifica:** Los logs deben aparecer en la consola cuando crees una simulación.

---

### Ejercicio 10: Test Personalizado

**Tarea:** Crea un nuevo test en `tests/test_monte_carlo.py`:

```python
def test_itm_call_has_higher_price_than_atm():
    """In-the-money call should be more expensive than at-the-money."""
    # ATM
    atm_result = price_european_option(
        spot_price=100,
        strike_price=100,
        time_to_maturity=1.0,
        volatility=0.2,
        risk_free_rate=0.05,
        option_type="call",
        num_simulations=50_000,
        random_seed=42,
    )
    
    # ITM
    itm_result = price_european_option(
        spot_price=100,
        strike_price=90,  # Strike más bajo
        time_to_maturity=1.0,
        volatility=0.2,
        risk_free_rate=0.05,
        option_type="call",
        num_simulations=50_000,
        random_seed=42,
    )
    
    # ITM debe ser más cara
    assert itm_result["price"] > atm_result["price"]
```

**Ejecuta:** `pytest tests/test_monte_carlo.py::test_itm_call_has_higher_price_than_atm -v`

---

## 🔴 Ejercicios Avanzados {#avanzados}

### Ejercicio 11: Nuevo Endpoint - Compare Options

**Tarea:** Agrega un nuevo endpoint que compare call vs put.

```python
@app.post("/compare")
async def compare_options(request: OptionPricingRequest):
    """Compare call and put prices for the same parameters."""
    
    # Calcular call
    call_result = price_european_option(
        spot_price=request.spot_price,
        strike_price=request.strike_price,
        time_to_maturity=request.time_to_maturity,
        volatility=request.volatility,
        risk_free_rate=request.risk_free_rate,
        option_type="call",
        num_simulations=request.num_simulations,
    )
    
    # Calcular put
    put_result = price_european_option(
        spot_price=request.spot_price,
        strike_price=request.strike_price,
        time_to_maturity=request.time_to_maturity,
        volatility=request.volatility,
        risk_free_rate=request.risk_free_rate,
        option_type="put",
        num_simulations=request.num_simulations,
    )
    
    return {
        "call_price": call_result["price"],
        "put_price": put_result["price"],
        "put_call_parity_check": {
            "call_minus_put": call_result["price"] - put_result["price"],
            "spot_minus_pv_strike": request.spot_price - request.strike_price * np.exp(-request.risk_free_rate * request.time_to_maturity),
            "difference": abs((call_result["price"] - put_result["price"]) - (request.spot_price - request.strike_price * np.exp(-request.risk_free_rate * request.time_to_maturity)))
        }
    }
```

**Test:** Verifica que el endpoint funciona en http://localhost:8000/docs

---

### Ejercicio 12: Cache con Dictionary

**Tarea:** Implementa un caché simple para evitar recalcular simulaciones idénticas.

```python
# En app/main.py
from functools import lru_cache
import hashlib
import json

# Caché en memoria
simulation_cache = {}

def create_cache_key(request: OptionPricingRequest) -> str:
    """Create a unique cache key from request parameters."""
    params = request.model_dump()
    params_str = json.dumps(params, sort_keys=True)
    return hashlib.md5(params_str.encode()).hexdigest()

@app.post("/simulations", ...)
async def create_simulation(request: OptionPricingRequest):
    # Check cache first
    cache_key = create_cache_key(request)
    if cache_key in simulation_cache:
        logger.info(f"Cache hit for {cache_key[:8]}...")
        return simulation_cache[cache_key]
    
    # ... código existente (cálculos) ...
    
    # Store in cache
    simulation_cache[cache_key] = response
    
    return response
```

**Test:** Haz dos requests idénticos y verifica que el segundo es instantáneo.

---

### Ejercicio 13: Validación Personalizada

**Tarea:** Agrega una validación que rechace opciones con riesgo/recompensa irreal.

En `app/models.py`:

```python
from pydantic import field_validator, model_validator

class OptionPricingRequest(BaseModel):
    # ... campos existentes ...
    
    @model_validator(mode='after')
    def validate_realistic_scenario(self):
        """Reject unrealistic option scenarios."""
        # Si la opción está muy OTM y tiene poco tiempo, rechazar
        moneyness = self.spot_price / self.strike_price
        
        if self.option_type == "call":
            # Call muy OTM con poco tiempo
            if moneyness < 0.8 and self.time_to_maturity < 0.1:
                raise ValueError(
                    "Deep OTM call with short maturity is likely worthless. "
                    "Consider increasing time to maturity or adjusting strike."
                )
        else:  # put
            # Put muy OTM con poco tiempo
            if moneyness > 1.2 and self.time_to_maturity < 0.1:
                raise ValueError(
                    "Deep OTM put with short maturity is likely worthless. "
                    "Consider increasing time to maturity or adjusting strike."
                )
        
        return self
```

**Test:** Intenta crear una simulación con S=100, K=150, T=0.05, type="call". Debería ser rechazada.

---

### Ejercicio 14: Stress Testing

**Tarea:** Crea un test que verifique que el sistema maneja cargas altas.

```python
# En tests/test_performance.py
import concurrent.futures
import time

def test_concurrent_load():
    """Test API under concurrent load."""
    from fastapi.testclient import TestClient
    from app.main import app
    
    client = TestClient(app)
    
    payload = {
        "spot_price": 100,
        "strike_price": 105,
        "time_to_maturity": 1.0,
        "volatility": 0.2,
        "risk_free_rate": 0.05,
        "option_type": "call",
        "num_simulations": 10000,  # Pequeño para velocidad
    }
    
    def make_request():
        response = client.post("/simulations", json=payload)
        return response.status_code
    
    # Simular 50 requests concurrentes
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request) for _ in range(50)]
        results = [f.result() for f in futures]
    
    duration = time.time() - start
    
    # Todas deben ser exitosas
    assert all(status == 201 for status in results)
    
    # No debería tomar más de 10 segundos
    assert duration < 10.0
    
    print(f"\n50 concurrent requests completed in {duration:.2f}s")
    print(f"Average: {duration/50:.3f}s per request")
```

**Ejecuta:** `pytest tests/test_performance.py::test_concurrent_load -v -s`

---

### Ejercicio 15: Endpoint de Analytics

**Tarea:** Crea un endpoint que devuelva estadísticas de todas las simulaciones.

```python
@app.get("/analytics")
async def get_analytics():
    """Get analytics from all simulations."""
    results = await get_all_simulation_results()
    
    if not results:
        return {"message": "No simulations yet"}
    
    # Extraer precios
    mc_prices = [r.option_price for r in results]
    bs_prices = [r.black_scholes_price for r in results if r.black_scholes_price]
    
    # Calcular diferencias MC vs BS
    differences = [
        abs(r.option_price - r.black_scholes_price) 
        for r in results 
        if r.black_scholes_price
    ]
    
    return {
        "total_simulations": len(results),
        "monte_carlo": {
            "mean_price": np.mean(mc_prices),
            "median_price": np.median(mc_prices),
            "min_price": min(mc_prices),
            "max_price": max(mc_prices),
        },
        "black_scholes": {
            "mean_price": np.mean(bs_prices) if bs_prices else None,
        },
        "mc_vs_bs": {
            "mean_difference": np.mean(differences) if differences else None,
            "max_difference": max(differences) if differences else None,
        },
        "option_types": {
            "calls": sum(1 for r in results if r.inputs.get("option_type") == "call"),
            "puts": sum(1 for r in results if r.inputs.get("option_type") == "put"),
        }
    }
```

**Test:** Crea varias simulaciones y luego llama a `GET /analytics`.

---

## 💼 Desafíos de Interview {#interview-challenges}

### Challenge 1: Explain in 2 Minutes

**Sin mirar tus notas**, grábate explicando:
1. ¿Qué es una opción call?
2. ¿Cómo funciona Monte Carlo?
3. ¿Qué es Black-Scholes?

**Criterio de éxito:** Claro, conciso, sin "eeeh" o "mmm".

---

### Challenge 2: Live Coding

**Escenario:** El entrevistador dice "Muéstrame cómo agregarías un nuevo parámetro 'dividend_yield' al modelo."

**Debes:**
1. Modificar `OptionPricingRequest` en `models.py`
2. Actualizar `price_european_option` en `monte_carlo.py` para usar:
   ```python
   drift = (risk_free_rate - dividend_yield - 0.5 * volatility**2) * time_to_maturity
   ```
3. Agregar un test simple

**Tiempo límite:** 15 minutos

---

### Challenge 3: Debugging

**Escenario:** Un usuario reporta que las opciones PUT siempre dan precio 0.

**Tu tarea:** Identifica el bug en este código:

```python
# CÓDIGO CON BUG
def price_european_option(...):
    # ...
    if option_type == "call":
        payoffs = np.maximum(terminal_prices - strike_price, 0)
    if option_type == "put":  # ← ¿Ves el problema?
        payoffs = np.maximum(strike_price - terminal_prices, 0)
```

**Pregunta:** ¿Cuál es el bug? ¿Cómo lo arreglas?

---

### Challenge 4: Architecture Question

**Pregunta del entrevistador:**
> "¿Por qué separaste `monte_carlo.py` de `main.py`? ¿No sería más simple tener todo en un solo archivo?"

**Tu respuesta debe incluir:**
- Separation of concerns
- Testability
- Reusability
- Mantenibilidad

**Practica tu respuesta en voz alta.**

---

### Challenge 5: Optimization

**Escenario:** Las simulaciones con 1M paths son muy lentas.

**Propón 3 soluciones:**
1. Una solución rápida (fácil de implementar)
2. Una solución intermedia (mejor performance)
3. Una solución ideal (máximo performance)

**Pistas:**
- Multiprocessing
- NumPy optimizations
- Caching
- Algoritmos alternativos

---

## ✅ Soluciones {#soluciones}

### Ejercicio 1: Payoff
```
a) S_T = $120, K = $100 → Payoff = max(120-100, 0) = $20
b) S_T = $95,  K = $100 → Payoff = max(95-100, 0) = $0
c) S_T = $100, K = $100 → Payoff = max(100-100, 0) = $0
```

### Ejercicio 4: Standard Error
**Respuesta:** Simulación B (100,000) tendrá menor error porque:
```
SE = σ / √N

N = 10,000  → SE = σ / 100
N = 100,000 → SE = σ / 316.2

Más simulaciones = menor error estándar
```

### Ejercicio 5: Precio de Opciones
**Orden de precio (mayor a menor):**
1. ITM (K=$90): ~$13
2. ATM (K=$100): ~$10
3. OTM (K=$110): ~$6

**Razón:** Opciones ITM tienen valor intrínseco inmediato.

### Ejercicio 6: Put-Call Parity
```
Ejemplo con S=100, K=100, T=1, r=0.05:

Call ≈ $10.45
Put ≈ $5.57

C - P = 10.45 - 5.57 = 4.88
S - K*e^(-rT) = 100 - 100*e^(-0.05) = 100 - 95.12 = 4.88

¡Coinciden! ✅
```

### Challenge 3: Debugging
**Bug:** Se usa `if` en lugar de `elif`, causando que put sobreescriba call.

**Solución:**
```python
if option_type == "call":
    payoffs = np.maximum(terminal_prices - strike_price, 0)
elif option_type == "put":  # ← Cambiar a elif
    payoffs = np.maximum(strike_price - terminal_prices, 0)
```

### Challenge 5: Optimization
```
Solución 1 (Rápida):
- Reducir num_simulations a 100K por defecto
- Agregar endpoint para simulaciones "express"

Solución 2 (Intermedia):
- Implementar multiprocessing con Pool
- Dividir simulaciones entre cores CPU

Solución 3 (Ideal):
- Usar Numba JIT compilation
- Implementar en C++/Cython
- Usar GPU con CuPy
```

---

## 🎯 Plan de Práctica Recomendado

### Semana 1:
- Día 1-2: Ejercicios básicos (1-4)
- Día 3-4: Ejercicios intermedios (5-7)
- Día 5-6: Ejercicios intermedios (8-10)
- Día 7: Revisión y consolidación

### Semana 2:
- Día 1-2: Ejercicios avanzados (11-12)
- Día 3-4: Ejercicios avanzados (13-15)
- Día 5-6: Interview challenges (1-3)
- Día 7: Interview challenges (4-5) + Mock interview

---

**¡Buena suerte con la práctica!** 🚀

Recuerda: La mejor forma de aprender es construyendo y experimentando.
No tengas miedo de romper cosas, ¡así se aprende!